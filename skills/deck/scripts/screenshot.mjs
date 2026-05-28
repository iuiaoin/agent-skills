#!/usr/bin/env node

// Screenshot generated slides for visual QA, optionally emitting an overflow
// report. Used by the deck skill's visual-QA-and-autofix step (and `--qa` mode).
// Shares its renderer with export-pptx.mjs via ./lib/render.mjs.

import { writeFile } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import {
  discoverSlides,
  filterSlidesByNumbers,
  renderSlides,
  slideNumberOf,
  QA_SCALE_FACTOR,
} from './lib/render.mjs';

function parseArgs() {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.error('Usage: node screenshot.mjs <presentation-dir> [--slides 1,4,7] [--scale N] [--out <dir>] [--report]');
    console.error('Example: node screenshot.mjs ./presentation --report');
    console.error('Example: node screenshot.mjs ./presentation --slides 3,5 --report');
    process.exit(1);
  }

  let scaleFactor = QA_SCALE_FACTOR;
  const scaleIdx = args.indexOf('--scale');
  if (scaleIdx !== -1) {
    scaleFactor = parseInt(args[scaleIdx + 1]) || QA_SCALE_FACTOR;
    args.splice(scaleIdx, 2);
  }

  let slidesFilter = null;
  const slidesIdx = args.indexOf('--slides');
  if (slidesIdx !== -1) {
    slidesFilter = (args[slidesIdx + 1] || '')
      .split(',')
      .map(n => parseInt(n.trim(), 10))
      .filter(n => Number.isInteger(n));
    args.splice(slidesIdx, 2);
  }

  let outDir = null;
  const outIdx = args.indexOf('--out');
  if (outIdx !== -1) {
    outDir = resolve(args[outIdx + 1]);
    args.splice(outIdx, 2);
  }

  let report = false;
  const reportIdx = args.indexOf('--report');
  if (reportIdx !== -1) {
    report = true;
    args.splice(reportIdx, 1);
  }

  const presentationDir = resolve(args[0]);
  return { presentationDir, slidesFilter, scaleFactor, outDir, report };
}

async function main() {
  const { presentationDir, slidesFilter, scaleFactor, outDir, report } = parseArgs();
  const out = outDir || join(presentationDir, '.screenshots');

  console.log('Screenshotting slides for QA...');
  console.log(`  Source: ${presentationDir}`);
  console.log(`  Output: ${out}`);
  console.log(`  Scale:  ${scaleFactor}x`);

  try {
    const allSlides = await discoverSlides(presentationDir);
    const targets = slidesFilter ? filterSlidesByNumbers(allSlides, slidesFilter) : allSlides;

    if (targets.length === 0) {
      throw new Error(`No slides matched --slides ${slidesFilter?.join(',')}`);
    }

    console.log(`  Slides: ${targets.length}${slidesFilter ? ` (subset: ${slidesFilter.join(',')})` : ''}\n`);

    const { imagePaths, reports } = await renderSlides(targets, out, {
      scaleFactor,
      detectOverflow: report,
      onProgress: console.log,
      // Name PNGs by the slide's own number so a subset render still maps
      // slideN.png -> slides/slideN.html.
      nameFor: p => `slide${slideNumberOf(p)}.png`,
    });

    if (report) {
      const slides = reports.map(r => ({
        slide: r.slide,
        file: `slide${r.slide}.png`,
        overflowY: r.overflowY,
        overflowX: r.overflowX,
        offendingSelectors: r.offendingSelectors,
        scrollH: r.scrollH,
        clientH: r.clientH,
        scrollW: r.scrollW,
        clientW: r.clientW,
      }));
      const flagged = slides.filter(s => s.overflowY || s.overflowX || s.offendingSelectors.length > 0);
      const reportPath = join(out, 'overflow-report.json');
      await writeFile(
        reportPath,
        JSON.stringify({ generatedAt: new Date().toISOString(), scale: scaleFactor, slides, flagged }, null, 2),
      );
      console.log(`\nReport: ${reportPath}`);
      console.log(flagged.length ? `  Flagged ${flagged.length} slide(s): ${flagged.map(s => s.slide).join(', ')}` : '  No overflow detected.');
    }

    console.log(`\nDone! ${imagePaths.length} screenshot(s) written to ${out}`);
  } catch (error) {
    console.error(`\nScreenshot failed: ${error.message}`);
    process.exit(1);
  }
}

main();
