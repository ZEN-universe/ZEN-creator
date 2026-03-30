"""Unit tests for TemplateCarrier lifecycle methods."""

from __future__ import annotations

import json

import pytest

from zen_creator.elements.carriers.aa_template import TemplateCarrier
from zen_creator.model import Model


def test_template_carrier_construction(
    model: Model,
):
    """Construction sets class name and default carrier attributes."""
    carrier = TemplateCarrier(model=model)

    assert carrier.name == "template_carrier"
    assert carrier.demand.default_value == 0.0
    assert carrier.price_shed_demand.default_value == float("inf")


def test_template_carrier_build(
    model: Model,
):
    """Build keeps or overrides template attributes through _set_* methods."""
    carrier = TemplateCarrier(model=model)

    carrier.build()

    assert carrier.demand.default_value == 0.0
    assert carrier.demand.unit == "MW"
    assert carrier.price_shed_demand.default_value == float("inf")


def test_template_carrier_write(
    model: Model,
):
    """Write persists ``attributes.json`` with values available after build()."""
    carrier = TemplateCarrier(model=model)
    carrier.build()
    carrier.write()

    attributes_path = carrier.output_path / "attributes.json"

    assert attributes_path.exists()

    attributes = json.loads(attributes_path.read_text())
    assert attributes["demand"]["default_value"] == 0.0
    assert attributes["demand"]["unit"] == "MW"
    assert attributes["price_shed_demand"]["default_value"] == "inf"
    assert attributes["price_shed_demand"]["unit"] == "Euro/MWh"


if __name__ == "__main__":
    pytest.main([__file__])
