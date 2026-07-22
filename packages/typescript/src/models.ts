/**
 * TypeScript object model for the open-business-plan JSON Schema.
 *
 * These interfaces mirror `business_plan.schema.json` one-to-one. Field names
 * are kept identical to the JSON keys (snake_case) so a validated document can
 * be used directly as a typed object with no key remapping — see
 * `parseBusinessPlan` in `index.ts`.
 *
 * Optionality here matches the schema's `required` arrays: a property is
 * optional (`?`) exactly when the schema does not require it.
 */

/** The top-level business plan document. Schema title: `BusinessPlan`. */
export interface BusinessPlan {
  /** Unique identifier of the business (>= 1). */
  id?: number;
  /** The common name of the business. */
  name: string;
  /** The registered/legal name of the business. */
  filed_name: string;
  /** The tagline of the business. */
  tagline: string;
  /** A link to the logo of the business (uri). */
  logo_link?: string;
  /** The web domain of the business (hostname). */
  domain: string;
  /** The key members of the business (at least one). */
  organization: Member[];
  /** The date the business started. */
  date_started: BusinessDate;
  /** The business plan itself. */
  plan: Plan;
}

/** A key member of the business. Schema title: `Member`. */
export interface Member {
  first_name: string;
  last_name: string;
  role: string;
  /** Email address (email format). */
  email?: string;
}

/**
 * A partial calendar date. Schema title: `Date`; renamed here to avoid
 * clashing with the built-in `Date` type.
 */
export interface BusinessDate {
  year: number;
  /** Month of year, 1-12. */
  month?: number;
  /** Day of month, 1-31. */
  day?: number;
}

/** A short name + description pair. Schema title: `NamedDescription`. */
export interface NamedDescription {
  name: string;
  description: string;
}

/** The business plan body. Schema title: `Plan`. */
export interface Plan {
  mission_statement: string;
  vision_statement: string;
  executive_summary: ExecutiveSummary;
  market_analysis?: MarketAnalysis;
  marketing_plan?: MarketingPlan;
  financial_plan?: FinancialPlan;
  operations_plan?: OperationsPlan;
  core_values: NamedDescription[];
  naics_categories: NaicsCategory[];
}

/** Schema title: `ExecutiveSummary`. */
export interface ExecutiveSummary {
  overview: string;
  objectives?: NamedDescription[];
}

/** Schema title: `MarketAnalysis`. */
export interface MarketAnalysis {
  target_market?: string;
  industry_trends?: string[];
  competitors?: Competitor[];
  customer_demographics?: string[];
  swot_analysis?: SwotAnalysis;
}

/** A known competitor of the business. Schema title: `Competitor`. */
export interface Competitor {
  name: string;
  strengths?: string[];
  weaknesses?: string[];
}

/** A SWOT analysis. Schema title: `SwotAnalysis`. */
export interface SwotAnalysis {
  strengths?: string[];
  weaknesses?: string[];
  opportunities?: string[];
  threats?: string[];
}

/** Schema title: `MarketingPlan`. */
export interface MarketingPlan {
  unique_value_proposition?: string;
  pricing_strategy?: string;
  promotion_channels?: string[];
  sales_strategy?: string;
  branding_strategy?: string;
}

/** Schema title: `FinancialPlan`. */
export interface FinancialPlan {
  startup_costs?: LineItem[];
  funding_sources?: LineItem[];
  revenue_streams?: string[];
  revenue_projections?: YearlyProjection[];
  expense_projections?: YearlyProjection[];
  break_even_point?: string;
}

/** A named financial line item. Schema title: `LineItem`. */
export interface LineItem {
  name: string;
  /** Amount in the business's base currency (>= 0). */
  amount: number;
  description?: string;
}

/** A projected amount for a given year. Schema title: `YearlyProjection`. */
export interface YearlyProjection {
  year: number;
  /** Projected amount in the business's base currency (>= 0). */
  amount: number;
}

/** Schema title: `OperationsPlan`. */
export interface OperationsPlan {
  location?: string;
  facilities?: string;
  equipment?: string[];
  suppliers?: NamedDescription[];
  staffing_plan?: StaffingRole[];
  workflow?: string;
}

/** A role the business needs to staff. Schema title: `StaffingRole`. */
export interface StaffingRole {
  role: string;
  /** Number of people needed in the role (>= 0). */
  count: number;
  description?: string;
}

/** A NAICS category for a business service. Schema title: `NaicsCategory`. */
export interface NaicsCategory {
  /** A NAICS code, 2-6 digits. */
  code: string;
  description: string;
}
