# Contributing

Use focused pull requests. `business_plan.schema.json` is the single source of truth; keep the TypeScript interfaces (`packages/typescript/src/models.ts`) and the pydantic models (`packages/python/open_business_plan/models.py`) in sync with it, and update `docs/schema-reference.md` and `examples/example-business-plan.json` in the same change. Keep every schema object `additionalProperties: false` so typos fail loudly, and reuse `$defs` where a shape repeats.

## Local setup

```sh
npm install
python -m venv .venv && source .venv/bin/activate
python -m pip install -e "packages/python[test]" ruff mypy
```

## Running tests

```sh
npm test            # TypeScript package (build + tests)
npm run test:python # Python package (pytest)
```

## Linting and type checking

```sh
npm run lint:ts     # eslint, prettier --check
npm run lint:python # ruff check, ruff format --check, mypy
npm run lint        # both
```

`npm run format` applies Prettier to TypeScript/JavaScript sources; `ruff format packages/python` does the equivalent for Python.

## Before opening a PR

Run `npm run lint`, `npm test`, and `npm run test:python`. If you change `business_plan.schema.json`, update both packages' models, the docs reference, and the example document together.
