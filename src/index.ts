import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";
import path from "node:path";
import type { Ajv2020 as Ajv2020Type, Options as Ajv2020Options, ErrorObject } from "ajv/dist/2020.js";
import type { FormatsPlugin } from "ajv-formats";

// ajv and ajv-formats ship CJS builds whose *default* export type doesn't
// line up with real Node ESM/CJS interop under NodeNext (their declaration
// files use `export default`, but TS models a CJS default import as the
// entire `module.exports` value, so it resolves to a non-constructable
// namespace type). Named types (the `Ajv2020` class, `FormatsPlugin`
// interface) are unaffected, so we import those for typing and load the
// actual runtime values via `require`.
const require = createRequire(import.meta.url);
const Ajv2020: typeof Ajv2020Type = require("ajv/dist/2020.js").Ajv2020;
const addFormats: FormatsPlugin = require("ajv-formats");

export interface ValidationResult {
  valid: boolean;
  errors: ErrorObject[];
}

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SCHEMA_PATH = path.join(__dirname, "..", "business_plan.schema.json");

let cachedSchema: object | undefined;

/** Loads and parses business_plan.schema.json from the package root. */
export function loadSchema(): object {
  if (!cachedSchema) {
    const raw = readFileSync(SCHEMA_PATH, "utf-8");
    cachedSchema = JSON.parse(raw) as object;
  }
  return cachedSchema as object;
}

function createAjv(): Ajv2020Type {
  const options: Ajv2020Options = { allErrors: true, strict: true };
  const ajv = new Ajv2020(options);
  addFormats(ajv);
  return ajv;
}

/**
 * Validates a business plan object (already parsed from JSON) against the
 * open-business-plan JSON Schema.
 */
export function validateBusinessPlan(data: unknown): ValidationResult {
  const ajv = createAjv();
  const validateFn = ajv.compile(loadSchema());
  const valid = validateFn(data);
  return { valid, errors: validateFn.errors ?? [] };
}

/** Reads a JSON file from disk and validates it against the schema. */
export function validateBusinessPlanFile(filePath: string): ValidationResult {
  const raw = readFileSync(filePath, "utf-8");
  const data = JSON.parse(raw);
  return validateBusinessPlan(data);
}

/** Formats Ajv errors into human-readable strings, e.g. "plan.mission_statement: is required". */
export function formatErrors(errors: ErrorObject[]): string[] {
  return errors.map((err) => {
    const location = err.instancePath.replace(/^\//, "").replace(/\//g, ".") || "(root)";
    return `${location}: ${err.message}`;
  });
}
