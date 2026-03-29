"""Unit tests for TemplateConversionTechnology lifecycle methods.

The template conversion technology can be tested directly with the real
``TemplateDataset`` implementation because it is self-contained and does not
depend on external source files in this template setup.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from zen_creator.elements.conversion_technologies.aa_template import (
    TemplateConversionTechnology,
)
from zen_creator.model import Model


@pytest.fixture
def model(tmp_path: Path) -> Model:
    """Create a minimal model object that is sufficient for element tests.

    The element ``write()`` path resolution requires ``output_folder`` and
    ``name`` to be defined, while the template's optional ``_set_max_load``
    uses ``source_path``.
    """
    model = Model()
    model.name = "template_conversion_technology_test_model"
    model.output_folder = tmp_path / "outputs"
    model.source_path = tmp_path
    return model


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
    assert technology.max_load.source["name"] == "template_dataset"


def test_template_conversion_technology_write(
    model: Model,
):
    """Write persists ``attributes.json`` with values created by build()."""
    technology = TemplateConversionTechnology(model=model)
    technology.build()
    technology.write()

    attributes_path = technology.output_path / "attributes.json"

    assert attributes_path.exists()

    attributes = json.loads(attributes_path.read_text())
    assert attributes["lifetime"]["default_value"] == 25.0
    assert attributes["max_load"]["default_value"] == 100.0
    assert attributes["max_load"]["unit"] == "MW"
    assert attributes["conversion_factor"] == [
        {"electricity": {"default_value": 1, "unit": "GWh/GWh"}}
    ]

if __name__ == "__main__":
    pytest.main([__file__])