# open-business-plan

An open source [JSON Schema](https://json-schema.org/) that defines a business plan, plus a TypeScript validator for checking documents against it.

The schema covers a business's identity (name, org chart, NAICS codes) and its plan (mission/vision, executive summary, market analysis, marketing plan, financial plan, operations plan, core values). See [`docs/schema-reference.md`](docs/schema-reference.md) for a field-by-field reference, and [`examples/example-business-plan.json`](examples/example-business-plan.json) for a complete example document.

## Repo layout

```
business_plan.schema.json        the schema itself (JSON Schema 2020-12)
docs/schema-reference.md         field-by-field documentation
examples/example-business-plan.json   a full example document
src/                             TypeScript validator source
  index.ts                       validateBusinessPlan(), validateBusinessPlanFile()
  cli.ts                         command-line entry point
```

## Using the schema directly

`business_plan.schema.json` is a standalone file — you don't need Node or this repo's validator to use it. Point any JSON Schema 2020-12–compatible validator at it, e.g.:

```jsonc
// in your business-plan.json
{
  "$schema": "https://github.com/Invisra/open-business-plan/blob/main/business_plan.schema.json",
  "name": "...",
  ...
}
```

## Using the TypeScript validator

### Install

```sh
npm install
npm run build
```

### CLI

```sh
node dist/cli.js path/to/your-business-plan.json
```

Prints `✔` and exits `0` if the file is valid, or `✘` with a list of validation errors and exits `1` otherwise. Multiple files can be passed at once.

```sh
$ node dist/cli.js examples/example-business-plan.json
✔ examples/example-business-plan.json is a valid business plan
```

### Programmatic use

```ts
import { validateBusinessPlan, validateBusinessPlanFile, formatErrors } from "./dist/index.js";
// or, without a build step: import from "./src/index.ts" using tsx/ts-node

const result = validateBusinessPlanFile("business-plan.json");
if (!result.valid) {
  console.error(formatErrors(result.errors).join("\n"));
}
```

`validateBusinessPlan(data)` validates an already-parsed object; `validateBusinessPlanFile(path)` reads and parses a JSON file first. Both return `{ valid: boolean, errors: ErrorObject[] }` (the `errors` array is [Ajv](https://ajv.js.org/)'s native error format).

### Try it against the example

```sh
npm run test
```

Builds the project and runs the CLI against `examples/example-business-plan.json`.

## Contributing

Schema changes should keep `$defs` reused across sections where the shape repeats (e.g. `NamedDescription` for anything that's just a name + description), and every object should keep `additionalProperties: false` so typos fail loudly. If you add or change a field, update `docs/schema-reference.md` and the example document in the same change.

## License

[Apache-2.0](LICENSE)
