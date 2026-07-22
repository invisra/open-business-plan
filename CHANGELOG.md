# Changelog

## Unreleased

- Add TypeScript (`@invisra/open-business-plan`) and Python (`open-business-plan`, pydantic v2) packages that parse a business-plan JSON document into typed, validated objects.
- Restructure the repository into a `packages/{typescript,python}` layout matching printspec, with the canonical `business_plan.schema.json` at the root synced into the TypeScript package at build time.
- Add `llms.txt`, community health files (`CONTRIBUTING`, `SECURITY`, `CODE_OF_CONDUCT`), issue/PR templates, linting (eslint/prettier, ruff/mypy), and a single-job CI workflow.
