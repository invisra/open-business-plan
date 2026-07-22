# open-business-plan

An open source [JSON Schema](https://json-schema.org/) that defines a business plan, plus TypeScript and Python packages that parse and validate documents against it.

The schema covers a business's identity (name, org chart, NAICS codes) and its plan (mission/vision, executive summary, market analysis, marketing plan, financial plan, operations plan, core values). See [`docs/schema-reference.md`](docs/schema-reference.md) for a field-by-field reference, and [`examples/example-business-plan.json`](examples/example-business-plan.json) for a complete example document.

## Repo layout

```
business_plan.schema.json           the schema itself (JSON Schema 2020-12) — canonical source
docs/schema-reference.md            field-by-field documentation
examples/example-business-plan.json a full example document
scripts/sync-schema.mjs             copies the schema into the TypeScript package at build time
packages/
  typescript/                       @invisra/open-business-plan — types, parser, validator (Ajv)
    src/models.ts                   TypeScript interfaces mirroring the schema
    src/index.ts                    parseBusinessPlan(), validateBusinessPlan(), …
    src/cli.ts                      command-line entry point
  python/                           open-business-plan (PyPI) — pydantic v2 models
    open_business_plan/models.py    pydantic models mirroring the schema
    open_business_plan/__init__.py  parse_business_plan(), load_business_plan_file()
```

The root of the repo is a private npm workspace that ties the TypeScript package together; the Python package is installed separately with `pip`.

## Using the schema directly

`business_plan.schema.json` is a standalone file — you don't need either package to use it. Point any JSON Schema 2020-12–compatible validator at it, e.g.:

```jsonc
// in your business-plan.json
{
  "$schema": "https://github.com/invisra/open-business-plan/blob/main/business_plan.schema.json",
  "name": "...",
  ...
}
```

## TypeScript package — [`@invisra/open-business-plan`](packages/typescript)

Parse JSON into a typed `BusinessPlan` object (validates first, throws on invalid input):

```ts
import { parseBusinessPlanFile, type BusinessPlan } from "@invisra/open-business-plan";

const plan: BusinessPlan = parseBusinessPlanFile("business-plan.json");
console.log(plan.name, plan.plan.mission_statement);
```

It also exports `validateBusinessPlan` / `validateBusinessPlanFile` (non-throwing, returning Ajv errors) and a `validate-business-plan` CLI. See the [package README](packages/typescript/README.md).

## Python package — [`open-business-plan`](packages/python)

Pydantic v2 models that turn JSON into typed objects:

```python
from open_business_plan import load_business_plan_file

plan = load_business_plan_file("business-plan.json")
print(plan.name, plan.plan.mission_statement)
```

Invalid documents raise `pydantic.ValidationError`. A `parse-business-plan` CLI is included. See the [package README](packages/python/README.md).

## Development

```sh
# TypeScript package (from the repo root)
npm install
npm run build          # syncs the schema into the package, then compiles
npm test               # runs the TypeScript tests

# Python package
npm run test:python    # or: cd packages/python && pip install -e ".[test]" && pytest
```

## Contributing

`business_plan.schema.json` is the single source of truth; keep the TypeScript interfaces (`packages/typescript/src/models.ts`) and the pydantic models (`packages/python/open_business_plan/models.py`) in sync with it. Schema changes should reuse `$defs` across sections where the shape repeats (e.g. `NamedDescription` for anything that's just a name + description), and every object should keep `additionalProperties: false` so typos fail loudly. If you add or change a field, update `docs/schema-reference.md`, the example document, and both packages' models in the same change.

## License

[Apache-2.0](LICENSE)
