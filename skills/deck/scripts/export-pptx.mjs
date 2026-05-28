#!/usr/bin/env node

import { rm } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import PptxGenJS from 'pptxgenjs';
import { discoverSlides, renderSlides, DEFAULT_SCALE_FACTOR } from './lib/render.mjs';

function parseArgs() {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.error('Usage: node export-pptx.mjs <presentation-dir> [output-filename] [--scale N]');
    console.error('Example: node export-pptx.mjs ./presentation deck --scale 3');
    process.exit(1);
  }

  let scaleFactor = DEFAULT_SCALE_FACTOR;
  const scaleIdx = args.indexOf('--scale');
  if (scaleIdx !== -1) {
    scaleFactor = parseInt(args[scaleIdx + 1]) || DEFAULT_SCALE_FACTOR;
    args.splice(scaleIdx, 2);
  }

  const presentationDir = resolve(args[0]);
  const outputName = args[1] || 'deck';
  return { presentationDir, outputName, scaleFactor };
}

async function buildPptx(imagePaths, outputPath, title) {
  const pptx = new PptxGenJS();

  // Standard 16:9 widescreen layout (10" x 5.625")
  pptx.defineLayout({ name: 'CUSTOM_16_9', width: 10, height: 5.625 });
  pptx.layout = 'CUSTOM_16_9';
  pptx.title = title;

  for (const imagePath of imagePaths) {
    const slide = pptx.addSlide();
    slide.addImage({
      path: imagePath,
      x: 0,
      y: 0,
      w: '100%',
      h: '100%',
    });
  }

  await pptx.writeFile({ fileName: outputPath });
}

async function cleanup(tempDir) {
  try {
    await rm(tempDir, { recursive: true, force: true });
  } catch {
    // best-effort cleanup
  }
}

async function main() {
  const { presentationDir, outputName, scaleFactor } = parseArgs();
  const tempDir = join(presentationDir, '.export-temp');
  const outputFile = join(presentationDir, `${outputName}.pptx`);

  console.log('Exporting presentation to PPTX...');
  console.log(`  Source: ${presentationDir}`);
  console.log(`  Output: ${outputFile}`);
  console.log(`  Scale:  ${scaleFactor}x`);

  try {
    console.log('\n[1/3] Discovering slides...');
    const slidePaths = await discoverSlides(presentationDir);
    console.log(`  Found ${slidePaths.length} slides`);

    console.log('\n[2/3] Rendering slides to images...');
    const { imagePaths } = await renderSlides(slidePaths, tempDir, {
      scaleFactor,
      onProgress: console.log,
    });

    console.log('\n[3/3] Building PPTX file...');
    await buildPptx(imagePaths, outputFile, outputName);

    console.log(`\nDone! PPTX saved to: ${outputFile}`);
  } catch (error) {
    console.error(`\nExport failed: ${error.message}`);
    process.exit(1);
  } finally {
    await cleanup(tempDir);
  }
}

main();
