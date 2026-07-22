"""Tests for the open_business_plan pydantic models."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from open_business_plan import (
    BusinessPlan,
    load_business_plan_file,
    parse_business_plan,
)

EXAMPLE = Path(__file__).resolve().parents[3] / "examples" / "example-business-plan.json"


def test_load_example_file_returns_typed_object() -> None:
    plan = load_business_plan_file(EXAMPLE)
    assert isinstance(plan, BusinessPlan)
    assert plan.name == "Cedar & Stone Coffee"
    assert plan.organization[0].first_name == "Ana"
    assert plan.date_started.year == 2024
    assert plan.plan.naics_categories[0].code == "311920"
    # Nested objects are real typed models, not dicts.
    assert plan.plan.financial_plan is not None
    assert plan.plan.financial_plan.startup_costs[0].amount == 45000


def test_parse_from_dict_and_json_string_agree() -> None:
    raw = EXAMPLE.read_text(encoding="utf-8")
    from_str = parse_business_plan(raw)
    from_dict = parse_business_plan(json.loads(raw))
    assert from_str == from_dict


def test_roundtrip_preserves_document() -> None:
    original = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    plan = parse_business_plan(original)
    dumped = plan.model_dump(mode="json", exclude_none=True)
    assert dumped == original


def test_missing_required_field_raises() -> None:
    with pytest.raises(ValidationError):
        parse_business_plan({"name": "Incomplete"})


def test_additional_property_on_closed_object_raises() -> None:
    data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    data["plan"]["surprise"] = "not allowed"
    with pytest.raises(ValidationError):
        parse_business_plan(data)


def test_naics_code_pattern_enforced() -> None:
    data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    data["plan"]["naics_categories"][0]["code"] = "not-a-code"
    with pytest.raises(ValidationError):
        parse_business_plan(data)


def test_empty_organization_rejected() -> None:
    data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    data["organization"] = []
    with pytest.raises(ValidationError):
        parse_business_plan(data)
