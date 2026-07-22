# @invisra/open-business-plan (TypeScript)

TypeScript types, an object parser, and a JSON Schema validator for the
[open-business-plan](https://github.com/invisra/open-business-plan) schema.
ESM-only.

## Install

```sh
npm install @invisra/open-business-plan
```

## Usage

Parse JSON into a typed object (validates first, throws on invalid input):

```ts
import {
  parseBusinessPlan,
  parseBusinessPlanFile,
  BusinessPlanValidationError,
  type BusinessPlan,
} from "@invisra/open-business-plan";

const plan: BusinessPlan = parseBusinessPlanFile("business-plan.json");
console.log(plan.name, plan.plan.mission_statement);

try {
  parseBusinessPlan({ name: "Incomplete" });
} catch (err) {
  if (err instanceof BusinessPlanValidationError) {
    console.error(err.errors); // raw Ajv errors
  }
}
```

Or validate without throwing:

```ts
import { validateBusinessPlan, formatErrors } from "@invisra/open-business-plan";

const result = validateBusinessPlan(data);
if (!result.valid) console.error(formatErrors(result.errors).join("\n"));
```

The exported interfaces (`BusinessPlan`, `Plan`, `Member`, `FinancialPlan`, …)
mirror the JSON Schema key-for-key, so a validated document is usable directly
as a typed object with no field remapping.

## CLI

```sh
npx validate-business-plan business-plan.json [more.json ...]
```

Exits `0` if every file is valid, `1` otherwise.

## License

[Apache-2.0](../../LICENSE)
