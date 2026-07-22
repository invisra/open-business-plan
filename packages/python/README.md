# open-business-plan (Python)

Pydantic v2 models that parse and validate the [open-business-plan](https://github.com/invisra/open-business-plan)
JSON Schema, turning a business-plan JSON document into typed Python objects.

## Install

```sh
pip install open-business-plan
```

## Usage

```python
from open_business_plan import parse_business_plan, load_business_plan_file

# From a file
plan = load_business_plan_file("business-plan.json")

# From an already-parsed dict, or a JSON string / bytes
plan = parse_business_plan({"name": "...", "filed_name": "...", ...})

print(plan.name)
print(plan.plan.mission_statement)
for member in plan.organization:
    print(member.first_name, member.role)
```

`plan` is a fully typed `BusinessPlan` model; every nested section
(`plan.financial_plan`, `plan.market_analysis.swot_analysis`, …) is a typed
model too, with IDE autocompletion and static type checking.

Invalid documents raise `pydantic.ValidationError`:

```python
from open_business_plan import parse_business_plan, ValidationError

try:
    parse_business_plan({"name": "Incomplete"})
except ValidationError as err:
    print(err)
```

## CLI

A small command-line checker is installed as `parse-business-plan` (also
runnable as `python -m open_business_plan`):

```sh
parse-business-plan business-plan.json
```

Exits `0` if every file parses, `1` otherwise.

## Notes

Field names match the JSON keys exactly (snake_case), so no aliasing is needed.
Objects that set `additionalProperties: false` in the schema reject unknown
keys. JSON Schema string *formats* (`email`, `uri`, `hostname`) are not
re-validated by these models — use the JSON Schema validator (the
[`@invisra/open-business-plan`](../typescript) TypeScript package or any
2020-12 validator) when full format validation is needed.

## License

[Apache-2.0](../../LICENSE)
