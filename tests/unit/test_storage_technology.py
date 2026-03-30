"""Unit tests for TemplateStorageTechnology lifecycle methods.

The template storage technology can be tested directly with the real
``TemplateDataset`` implementation because it is self-contained and does not
depend on external source files in this template setup.
"""

from __future__ import annotations

import json

import pytest

from zen_creator.elements.storage_technologies.aa_template import (
    TemplateStorageTechnology,
)
from zen_creator.model import Model


def test_template_storage_technology_construction(
    model: Model,
):
    """Construction sets class name and mandatory carrier defaults."""
    technology = TemplateStorageTechnology(model=model)

    assert technology.name == "template_storage_technology"
    assert technology.reference_carrier.default_value == ["heat"]


def test_template_storage_technology_build(
    model: Model,
):
    """Build populates required template attributes and optional max_load."""
    technology = TemplateStorageTechnology(model=model)

    technology.build()

    assert technology.lifetime.default_value == 25
    assert technology.lifetime.source == "assumption"
    assert technology.max_load.default_value == 150
    assert technology.max_load.unit == "MW"
    assert isinstance(technology.max_load.source, dict)
    assert technology.max_load.source["name"] == "template_dataset"


def test_template_storage_technology_write(
    model: Model,
):
    """Write persists ``attributes.json`` with values created by build()."""
    technology = TemplateStorageTechnology(model=model)
    technology.build()
    technology.write()

    attributes_path = technology.output_path / "attributes.json"

    assert attributes_path.exists()

    attributes = json.loads(attributes_path.read_text())
    assert attributes["lifetime"]["default_value"] == 25.0
    assert attributes["max_load"]["default_value"] == 150.0
    assert attributes["max_load"]["unit"] == "MW"


if __name__ == "__main__":
    pytest.main([__file__])
