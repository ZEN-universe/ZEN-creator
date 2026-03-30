"""Unit tests for TemplateConversionTechnology lifecycle methods.

The template conversion technology can be tested directly with the real
``TemplateDataset`` implementation because it is self-contained and does not
depend on external source files in this template setup.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from zen_creator.elements.conversion_technologies.aa_template import (
    TemplateConversionTechnology,
)
from zen_creator.model import Model
from zen_creator.utils.compare_trees import compare_files


def test_template_conversion_technology_construction(
    model: Model,
):
    """Construction sets class name and mandatory carrier defaults."""
    technology = TemplateConversionTechnology(model=model)

    assert technology.name == "template_conversion_technology"
    assert technology.reference_carrier.default_value == ["heat"]
    assert technology.input_carrier.default_value == ["electricity"]
    assert technology.output_carrier.default_value == ["heat"]


def test_template_conversion_technology_build(
    model: Model,
):
    """Build populates required template attributes and optional max_load."""
    technology = TemplateConversionTechnology(model=model)

    technology.build()

    assert technology.lifetime.default_value == 25
    assert technology.lifetime.source == "assumption"
    assert technology.conversion_factor.default_value == [
        {"electricity": {"default_value": 1, "unit": "GWh/GWh"}}
    ]
    assert technology.max_load.default_value == 100
    assert technology.max_load.unit == "MW"
    assert isinstance(technology.max_load.source, dict)
    assert technology.max_load.source["name"] == "template_dataset"


def test_template_conversion_technology_write(
    model: Model,
):
    """Write persists ``attributes.json`` and matches the reference output file."""
    technology = TemplateConversionTechnology(model=model)
    technology.build()
    technology.write()

    attributes_path = technology.output_path / "attributes.json"
    reference_path = (
        Path(__file__).parent
        / "fixtures"
        / "template_conversion_technology"
        / "attributes_conversion_technology.json"
    )

    differences = compare_files(reference_path, attributes_path)
    assert differences == [], "\n".join(differences)


if __name__ == "__main__":
    pytest.main([__file__])
