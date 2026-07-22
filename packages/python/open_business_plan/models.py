"""Pydantic models for the open-business-plan JSON Schema.

Each model mirrors ``business_plan.schema.json`` one-to-one. Field names match
the JSON keys (snake_case) exactly, so JSON documents map onto these models
with no field aliasing.

Objects whose schema sets ``additionalProperties: false`` subclass
``_ClosedModel`` (``extra="forbid"``), so unexpected keys raise a
``ValidationError`` — mirroring the schema. The top-level ``BusinessPlan`` does
not forbid extra properties, matching the schema's root object.

Note: JSON Schema string *formats* (``email``, ``uri``, ``hostname``) are not
re-checked here; those fields are plain ``str``. Use the JSON Schema validator
(the TypeScript package, or any 2020-12 validator) when full format validation
is required.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class _ClosedModel(BaseModel):
    """Base for objects that set ``additionalProperties: false`` in the schema."""

    model_config = ConfigDict(extra="forbid")


class Member(_ClosedModel):
    """A key member of the business. Schema ``$defs.member``."""

    first_name: str
    last_name: str
    role: str
    email: Optional[str] = None


class BusinessDate(_ClosedModel):
    """A partial calendar date. Schema ``$defs.date`` (title ``Date``)."""

    year: int
    month: Optional[int] = Field(default=None, ge=1, le=12)
    day: Optional[int] = Field(default=None, ge=1, le=31)


class NamedDescription(_ClosedModel):
    """A name + description pair. Schema ``$defs.namedDescription``."""

    name: str
    description: str


class Competitor(_ClosedModel):
    """A known competitor. Schema ``$defs.competitor``."""

    name: str
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None


class SwotAnalysis(_ClosedModel):
    """A SWOT analysis. Schema ``$defs.swotAnalysis``."""

    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None
    opportunities: Optional[List[str]] = None
    threats: Optional[List[str]] = None


class LineItem(_ClosedModel):
    """A named financial line item. Schema ``$defs.lineItem``."""

    name: str
    amount: float = Field(ge=0)
    description: Optional[str] = None


class YearlyProjection(_ClosedModel):
    """A projected amount for a year. Schema ``$defs.yearlyProjection``."""

    year: int
    amount: float = Field(ge=0)


class StaffingRole(_ClosedModel):
    """A role the business needs to staff. Schema ``$defs.staffingRole``."""

    role: str
    count: int = Field(ge=0)
    description: Optional[str] = None


class NaicsCategory(_ClosedModel):
    """A NAICS category. Schema ``$defs.naicsCategory``."""

    code: str = Field(pattern=r"^[0-9]{2,6}$")
    description: str


class ExecutiveSummary(_ClosedModel):
    """Schema ``plan.executive_summary``."""

    overview: str
    objectives: Optional[List[NamedDescription]] = None


class MarketAnalysis(_ClosedModel):
    """Schema ``plan.market_analysis``."""

    target_market: Optional[str] = None
    industry_trends: Optional[List[str]] = None
    competitors: Optional[List[Competitor]] = None
    customer_demographics: Optional[List[str]] = None
    swot_analysis: Optional[SwotAnalysis] = None


class MarketingPlan(_ClosedModel):
    """Schema ``plan.marketing_plan``."""

    unique_value_proposition: Optional[str] = None
    pricing_strategy: Optional[str] = None
    promotion_channels: Optional[List[str]] = None
    sales_strategy: Optional[str] = None
    branding_strategy: Optional[str] = None


class FinancialPlan(_ClosedModel):
    """Schema ``plan.financial_plan``."""

    startup_costs: Optional[List[LineItem]] = None
    funding_sources: Optional[List[LineItem]] = None
    revenue_streams: Optional[List[str]] = None
    revenue_projections: Optional[List[YearlyProjection]] = None
    expense_projections: Optional[List[YearlyProjection]] = None
    break_even_point: Optional[str] = None


class OperationsPlan(_ClosedModel):
    """Schema ``plan.operations_plan``."""

    location: Optional[str] = None
    facilities: Optional[str] = None
    equipment: Optional[List[str]] = None
    suppliers: Optional[List[NamedDescription]] = None
    staffing_plan: Optional[List[StaffingRole]] = None
    workflow: Optional[str] = None


class Plan(_ClosedModel):
    """The business plan body. Schema ``plan``."""

    mission_statement: str
    vision_statement: str
    executive_summary: ExecutiveSummary
    market_analysis: Optional[MarketAnalysis] = None
    marketing_plan: Optional[MarketingPlan] = None
    financial_plan: Optional[FinancialPlan] = None
    operations_plan: Optional[OperationsPlan] = None
    core_values: List[NamedDescription]
    naics_categories: List[NaicsCategory]


class BusinessPlan(BaseModel):
    """The top-level business plan document. Schema root ``BusinessPlan``.

    The root object does not set ``additionalProperties: false`` in the schema,
    so this model does not forbid extra keys.
    """

    id: Optional[int] = Field(default=None, ge=1)
    name: str
    filed_name: str
    tagline: str
    logo_link: Optional[str] = None
    domain: str
    organization: List[Member] = Field(min_length=1)
    date_started: BusinessDate
    plan: Plan
