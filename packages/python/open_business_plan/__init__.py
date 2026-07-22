"""open-business-plan: pydantic models for the business-plan JSON Schema.

Parse a business plan (from a dict, a JSON string, or a file) into a typed
:class:`BusinessPlan` object::

    from open_business_plan import parse_business_plan, load_business_plan_file

    plan = load_business_plan_file("business-plan.json")
    print(plan.name, plan.plan.mission_statement)

Invalid input raises :class:`pydantic.ValidationError`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Union

from pydantic import ValidationError

from .models import (
    BusinessDate,
    BusinessPlan,
    Competitor,
    ExecutiveSummary,
    FinancialPlan,
    LineItem,
    MarketAnalysis,
    MarketingPlan,
    Member,
    NaicsCategory,
    NamedDescription,
    OperationsPlan,
    Plan,
    StaffingRole,
    SwotAnalysis,
    YearlyProjection,
)

__all__ = [
    "BusinessPlan",
    "BusinessDate",
    "Competitor",
    "ExecutiveSummary",
    "FinancialPlan",
    "LineItem",
    "MarketAnalysis",
    "MarketingPlan",
    "Member",
    "NaicsCategory",
    "NamedDescription",
    "OperationsPlan",
    "Plan",
    "StaffingRole",
    "SwotAnalysis",
    "YearlyProjection",
    "ValidationError",
    "parse_business_plan",
    "load_business_plan_file",
]

__version__ = "1.0.0"


def parse_business_plan(data: Union[dict[str, Any], str, bytes]) -> BusinessPlan:
    """Parse and validate a business plan into a :class:`BusinessPlan`.

    ``data`` may be an already-parsed mapping, or a JSON ``str``/``bytes``.
    Raises :class:`pydantic.ValidationError` if the document is invalid.
    """
    if isinstance(data, (str, bytes)):
        return BusinessPlan.model_validate_json(data)
    return BusinessPlan.model_validate(data)


def load_business_plan_file(path: Union[str, Path]) -> BusinessPlan:
    """Read a JSON file from disk and parse it into a :class:`BusinessPlan`."""
    raw = Path(path).read_text(encoding="utf-8")
    return parse_business_plan(raw)
