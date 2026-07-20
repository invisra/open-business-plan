# Schema Reference

This document describes every field defined by [`business_plan.schema.json`](../business_plan.schema.json). It complements the schema's own `description` keywords — read this for the "why" and cross-field context, read the schema for the authoritative types and constraints.

The schema targets [JSON Schema 2020-12](https://json-schema.org/draft/2020-12/schema). Reusable object shapes live under `$defs` and are referenced with `$ref` (e.g. `Member`, `NamedDescription`) so the same structure isn't redefined for every list that needs it.

Every object in the schema sets `additionalProperties: false`. Typos in field names (e.g. `role` vs. `roles`) will fail validation loudly instead of being silently dropped.

## Root object

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | integer (≥ 1) | | An internal identifier for the business, e.g. a database primary key. |
| `name` | string | ✓ | The common/trading name. |
| `filed_name` | string | ✓ | The legal name on file with the relevant registrar. |
| `tagline` | string | ✓ | |
| `logo_link` | string (`uri`) | | Must be a full URI, e.g. `https://example.com/logo.png`. |
| `domain` | string (`hostname`) | ✓ | Just the hostname, e.g. `example.com` — not a full URL. |
| `organization` | array of [`Member`](#member) | ✓ | At least one member is required. |
| `date_started` | [`Date`](#date) | ✓ | |
| `plan` | [`Plan`](#plan) | ✓ | The business plan itself; see below. |

## `Member`

Used in `organization`.

| Field | Type | Required |
|---|---|---|
| `first_name` | string | ✓ |
| `last_name` | string | ✓ |
| `role` | string | ✓ |
| `email` | string (`email`) | |

## `Date`

Used for `date_started`. Only `year` is required so businesses that don't track an exact founding day can still populate the field.

| Field | Type | Required |
|---|---|---|
| `year` | integer | ✓ |
| `month` | integer (1–12) | |
| `day` | integer (1–31) | |

## `Plan`

The core of the document. All sub-sections except `marketing_plan` and `operations_plan` are required, on the assumption that a plan without a mission, vision, executive summary, core values, or industry classification isn't yet a usable plan — but the objects themselves have no required *fields*, so start with an empty `{}` and fill in as you go.

| Field | Type | Required |
|---|---|---|
| `mission_statement` | string | ✓ |
| `vision_statement` | string | ✓ |
| `executive_summary` | [`ExecutiveSummary`](#executivesummary) | ✓ |
| `market_analysis` | [`MarketAnalysis`](#marketanalysis) | |
| `marketing_plan` | [`MarketingPlan`](#marketingplan) | |
| `financial_plan` | [`FinancialPlan`](#financialplan) | |
| `operations_plan` | [`OperationsPlan`](#operationsplan) | |
| `core_values` | array of [`NamedDescription`](#nameddescription) | ✓ |
| `naics_categories` | array of [`NaicsCategory`](#naicscategory) | ✓ |

### `ExecutiveSummary`

| Field | Type | Required |
|---|---|---|
| `overview` | string | ✓ |
| `objectives` | array of [`NamedDescription`](#nameddescription) | |

### `MarketAnalysis`

| Field | Type |
|---|---|
| `target_market` | string |
| `industry_trends` | array of string |
| `competitors` | array of [`Competitor`](#competitor) |
| `customer_demographics` | array of string |
| `swot_analysis` | [`SwotAnalysis`](#swotanalysis) |

### `Competitor`

| Field | Type | Required |
|---|---|---|
| `name` | string | ✓ |
| `strengths` | array of string | |
| `weaknesses` | array of string | |

### `SwotAnalysis`

`strengths`, `weaknesses`, `opportunities`, `threats` — each an array of strings. All optional.

### `MarketingPlan`

| Field | Type |
|---|---|
| `unique_value_proposition` | string |
| `pricing_strategy` | string |
| `promotion_channels` | array of string |
| `sales_strategy` | string |
| `branding_strategy` | string |

### `FinancialPlan`

| Field | Type | Notes |
|---|---|---|
| `startup_costs` | array of [`LineItem`](#lineitem) | One-time launch costs. |
| `funding_sources` | array of [`LineItem`](#lineitem) | Where the money comes from (savings, loans, investors...). |
| `revenue_streams` | array of string | Descriptive, not quantified — pair with `revenue_projections` for numbers. |
| `revenue_projections` | array of [`YearlyProjection`](#yearlyprojection) | |
| `expense_projections` | array of [`YearlyProjection`](#yearlyprojection) | |
| `break_even_point` | string | Free text; the schema doesn't prescribe a break-even calculation model. |

All monetary `amount` fields are unitless numbers (`minimum: 0`) — the schema does not currently model currency. If you need multi-currency support, see [Possible future improvements](#possible-future-improvements) below.

### `OperationsPlan`

| Field | Type |
|---|---|
| `location` | string |
| `facilities` | string |
| `equipment` | array of string |
| `suppliers` | array of [`NamedDescription`](#nameddescription) |
| `staffing_plan` | array of [`StaffingRole`](#staffingrole) |
| `workflow` | string |

### `NamedDescription`

A generic `{ name, description }` pair, reused for `core_values`, `executive_summary.objectives`, and `operations_plan.suppliers`.

| Field | Type | Required |
|---|---|---|
| `name` | string | ✓ |
| `description` | string | ✓ |

### `LineItem`

| Field | Type | Required |
|---|---|---|
| `name` | string | ✓ |
| `amount` | number (≥ 0) | ✓ |
| `description` | string | |

### `YearlyProjection`

| Field | Type | Required |
|---|---|---|
| `year` | integer | ✓ |
| `amount` | number (≥ 0) | ✓ |

### `StaffingRole`

| Field | Type | Required |
|---|---|---|
| `role` | string | ✓ |
| `count` | integer (≥ 0) | ✓ |
| `description` | string | |

### `NaicsCategory`

One entry per [NAICS](https://www.census.gov/naics/) code that describes a service or product line of the business.

| Field | Type | Required | Notes |
|---|---|---|---|
| `code` | string | ✓ | Must match `^[0-9]{2,6}$` — NAICS codes are 2 to 6 digits. |
| `description` | string | ✓ | |

## Possible future improvements

Ideas that are intentionally out of scope for now, but worth considering if the schema grows:

- **Currency**: `LineItem` and `YearlyProjection` amounts are unitless. A `currency` field (ISO 4217 code) or a shared `Money { amount, currency }` type would make multi-currency plans unambiguous.
- **`date_started` as ISO 8601**: the `{ year, month, day }` object works but a plain `"date"`-format string is more interoperable with other tools. Kept as an object for now for parity with the original design and to allow a year-only date.
- **Versioning**: as the schema evolves, published plans may want a `schema_version` field to pin the version they were authored against.
