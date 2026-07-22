#!/usr/bin/env node
import { validateBusinessPlanFile, formatErrors } from "./index.js";

function main(): void {
  const [, , ...files] = process.argv;

  if (files.length === 0) {
    console.error("Usage: validate-business-plan <file.json> [file2.json ...]");
    process.exit(2);
  }

  let allValid = true;

  for (const file of files) {
    try {
      const result = validateBusinessPlanFile(file);
      if (result.valid) {
        console.log(`✔ ${file} is a valid business plan`);
      } else {
        allValid = false;
        console.log(`✘ ${file} is invalid:`);
        for (const line of formatErrors(result.errors)) {
          console.log(`  - ${line}`);
        }
      }
    } catch (err) {
      allValid = false;
      const message = err instanceof Error ? err.message : String(err);
      console.log(`✘ ${file} could not be read/parsed: ${message}`);
    }
  }

  process.exit(allValid ? 0 : 1);
}

main();
