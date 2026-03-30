"""Unit tests for TemplateCarrier lifecycle methods."""

from __future__ import annotations

from pathlib import Path

import pytest

from zen_creator.elements.carriers.aa_template import TemplateCarrier
from zen_creator.model import Model
from zen_creator.utils.compare_trees import compare_files


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
    """Write persists ``attributes.json`` and matches the reference output file."""
    carrier = TemplateCarrier(model=model)
    carrier.build()
    carrier.write()

    attributes_path = carrier.output_path / "attributes.json"
    reference_path = (
        Path(__file__).parent
        / "fixtures"
        / "template_carrier"
        / "attributes_carrier.json"
    )

    differences = compare_files(reference_path, attributes_path)
    assert differences == [], "\n".join(differences)


if __name__ == "__main__":
    pytest.main([__file__])
