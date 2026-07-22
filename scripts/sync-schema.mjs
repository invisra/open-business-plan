// Copies the canonical business_plan.schema.json from the repo root into the
// TypeScript package so it ships inside the published npm tarball. The copies
// are generated artifacts (git-ignored); the root file is the single source of
// truth. Run via `npm run sync:schema` (also invoked automatically by the
// TypeScript package's `prebuild`).
import { copyFileSync, mkdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const repoRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const source = path.join(repoRoot, "business_plan.schema.json");

const targets = [
  path.join(repoRoot, "packages", "typescript", "business_plan.schema.json"),
];

for (const target of targets) {
  mkdirSync(path.dirname(target), { recursive: true });
  copyFileSync(source, target);
  console.log(`synced schema -> ${path.relative(repoRoot, target)}`);
}
