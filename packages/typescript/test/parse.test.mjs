import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  parseBusinessPlan,
  parseBusinessPlanFile,
  validateBusinessPlan,
  BusinessPlanValidationError,
} from "../dist/index.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const EXAMPLE = path.join(
  __dirname,
  "..",
  "..",
  "..",
  "examples",
  "example-business-plan.json",
);

test("parseBusinessPlanFile returns a typed object for the example", () => {
  const plan = parseBusinessPlanFile(EXAMPLE);
  assert.equal(plan.name, "Cedar & Stone Coffee");
  assert.equal(plan.organization[0].first_name, "Ana");
  assert.equal(plan.plan.executive_summary.overview.length > 0, true);
  assert.equal(plan.plan.naics_categories[0].code, "311920");
});

test("parseBusinessPlan throws BusinessPlanValidationError on invalid input", () => {
  assert.throws(
    () => parseBusinessPlan({ name: "Missing required fields" }),
    (err) => {
      assert.ok(err instanceof BusinessPlanValidationError);
      assert.ok(err.errors.length > 0);
      return true;
    },
  );
});

test("validateBusinessPlan reports valid for the example document", () => {
  const plan = parseBusinessPlanFile(EXAMPLE);
  const result = validateBusinessPlan(plan);
  assert.equal(result.valid, true);
  assert.equal(result.errors.length, 0);
});
