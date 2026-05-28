// Shared rendering library for the deck skill.
//
// Owns all Puppeteer/headless-browser logic so both the PPTX exporter
// (export-pptx.mjs) and the visual-QA screenshotter (screenshot.mjs) use one
// renderer with no duplication.

import { readdir, mkdir, access } from 'node:fs/promises';
import { join, basename } from 'node:path';
import puppeteer from 'puppeteer';

export const SLIDE_WIDTH = 1280;
export const SLIDE_HEIGHT = 720;

// Crisp output for the PPTX deliverable (PowerPoint upscales on big screens).
export const DEFAULT_SCALE_FACTOR = 3;
// Slides are authored at exactly 1280x720; QA screenshots only need to be
// legible for visual inspection, so 1x keeps PNGs small and fast to read.
export const QA_SCALE_FACTOR = 1;

/**
 * Find slide HTML files in <presentationDir>/slides, sorted numerically.
 * @returns {Promise<string[]>} absolute paths to slideN.html
 */
export async function discoverSlides(presentationDir) {
  const slidesDir = join(presentationDir, 'slides');

  try {
    await access(slidesDir);
  } catch {
    throw new Error(`Slides directory not found: ${slidesDir}`);
  }

  const files = await readdir(slidesDir);
  const slideFiles = files
    .filter(f => /^slide\d+\.html$/i.test(f))
    .sort((a, b) => {
      const numA = parseInt(a.match(/\d+/)[0]);
      const numB = parseInt(b.match(/\d+/)[0]);
      return numA - numB;
    });

  if (slideFiles.length === 0) {
    throw new Error(`No slide HTML files found in ${slidesDir}`);
  }

  return slideFiles.map(f => join(slidesDir, f));
}

/** Numeric suffix of a slideN.html path (e.g. ".../slide7.html" -> 7). */
export function slideNumberOf(slidePath) {
  return parseInt(basename(slidePath).match(/\d+/)[0], 10);
}

/**
 * Keep only the slide paths whose number is in `numbers` (used for cheap
 * re-checks of just the slides that were edited).
 */
export function filterSlidesByNumbers(allSlidePaths, numbers) {
  const want = new Set(numbers);
  return allSlidePaths.filter(p => want.has(slideNumberOf(p)));
}

/**
 * Measure overflow on the current page. Runs in the browser context.
 *
 * Two complementary checks:
 *  - scrollHeight/scrollWidth vs clientHeight/clientWidth — reliable even under
 *    `overflow:hidden`, since scroll size still reflects clipped flow content.
 *  - per-descendant getBoundingClientRect vs the slide rect — catches absolutely
 *    positioned children that escape the canvas without growing scroll size.
 *
 * @returns {Promise<{overflowY,overflowX,scrollH,clientH,scrollW,clientW,offendingSelectors:string[]}>}
 */
async function probeOverflow(page) {
  return page.evaluate(() => {
    const TOL = 2; // sub-pixel rounding tolerance
    const slide = document.querySelector('.slide') || document.body;
    const r = slide.getBoundingClientRect();

    const scrollH = slide.scrollHeight;
    const clientH = slide.clientHeight;
    const scrollW = slide.scrollWidth;
    const clientW = slide.clientWidth;
    const overflowY = scrollH - clientH > TOL;
    const overflowX = scrollW - clientW > TOL;

    const offendingSelectors = [];
    for (const el of slide.querySelectorAll('*')) {
      const b = el.getBoundingClientRect();
      if (b.width === 0 || b.height === 0) continue;
      const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) === 0) continue;

      const crosses =
        b.right > r.right + TOL ||
        b.bottom > r.bottom + TOL ||
        b.left < r.left - TOL ||
        b.top < r.top - TOL;
      if (!crosses) continue;

      // Decorative shapes (no text, gradient background) are meant to bleed
      // off-canvas in cover/closing patterns — don't flag them.
      const hasText = (el.textContent || '').trim().length > 0;
      if (!hasText && /gradient/.test(cs.backgroundImage)) continue;

      let id;
      if (el.id) {
        id = `#${el.id}`;
      } else if (typeof el.className === 'string' && el.className.trim()) {
        id = `${el.tagName.toLowerCase()}.${el.className.trim().split(/\s+/).join('.')}`;
      } else {
        id = el.tagName.toLowerCase();
      }
      if (!offendingSelectors.includes(id)) offendingSelectors.push(id);
    }

    return {
      overflowY,
      overflowX,
      scrollH,
      clientH,
      scrollW,
      clientW,
      offendingSelectors: offendingSelectors.slice(0, 12), // cap noise
    };
  });
}

/**
 * Render each slide HTML to a PNG via a headless browser.
 *
 * @param {string[]} slidePaths absolute paths to slideN.html (already ordered/filtered)
 * @param {string}   outDir     directory to write PNGs into (created if missing)
 * @param {object}   [options]
 * @param {number}   [options.scaleFactor=DEFAULT_SCALE_FACTOR] deviceScaleFactor
 * @param {boolean}  [options.detectOverflow=false] run the overflow probe per slide
 * @param {(msg:string)=>void} [options.onProgress] progress logger (default no-op)
 * @param {(slidePath:string,index:number)=>string} [options.nameFor] output PNG basename
 * @returns {Promise<{imagePaths:string[], reports:object[]}>}
 */
export async function renderSlides(slidePaths, outDir, options = {}) {
  const {
    scaleFactor = DEFAULT_SCALE_FACTOR,
    detectOverflow = false,
    onProgress = () => {},
    nameFor = (_p, i) => `slide${i + 1}.png`,
  } = options;

  await mkdir(outDir, { recursive: true });

  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  const imagePaths = [];
  const reports = [];

  try {
    const page = await browser.newPage();
    await page.setViewport({
      width: SLIDE_WIDTH,
      height: SLIDE_HEIGHT,
      deviceScaleFactor: scaleFactor,
    });

    for (let i = 0; i < slidePaths.length; i++) {
      const slidePath = slidePaths[i];
      const imageFile = join(outDir, nameFor(slidePath, i));

      onProgress(`  Rendering slide ${i + 1}/${slidePaths.length}: ${basename(slidePath)}`);

      await page.goto(`file://${slidePath}`, {
        waitUntil: 'networkidle0',
        timeout: 30000,
      });

      // Wait for CSS animations to complete (slides use up to ~2s animations with staggered delays)
      await new Promise(r => setTimeout(r, 2500));

      if (detectOverflow) {
        reports.push({ slidePath, slide: slideNumberOf(slidePath), ...(await probeOverflow(page)) });
      }

      // Target the .slide element directly for a precise capture
      const slideElement = await page.$('.slide');
      if (slideElement) {
        await slideElement.screenshot({ path: imageFile, type: 'png' });
      } else {
        // Fallback: clip the viewport area
        await page.screenshot({
          path: imageFile,
          type: 'png',
          clip: { x: 0, y: 0, width: SLIDE_WIDTH, height: SLIDE_HEIGHT },
        });
      }

      imagePaths.push(imageFile);
    }
  } finally {
    await browser.close();
  }

  return { imagePaths, reports };
}
