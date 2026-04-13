"""Unit tests for TemplateTransportTechnology lifecycle methods.

The template transport technology can be tested directly with the real
``TemplateDataset`` implementation because it is self-contained and does not
depend on external source files in this template setup.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from zen_creator.datasets.datasets.metadata import MetaData
from zen_creator.elements.transport_technologies.aa_template import (
    TemplateTransportTechnology,
)
from zen_creator.model import Model
from zen_creator.utils.compare_trees import compare_files


def test_template_transport_technology_construction(
    model: Model,
):
    """Construction sets class name and mandatory carrier defaults."""
    technology = TemplateTransportTechnology(model=model)

    assert technology.name == "template_transport_technology"
    assert technology.reference_carrier.default_value == []


def test_template_transport_technology_build(
    model: Model,
):
    """Build populates required template attributes and optional max_load."""
    technology = TemplateTransportTechnology(model=model)

    technology.build()

    assert technology.lifetime.default_value == 25
    assert len(technology.lifetime.sources) == 1
    assert technology.lifetime.sources[0].description == "Description of assumption."
    assert technology.max_load.default_value == 200
    assert technology.max_load.unit == "MW"
    assert len(technology.max_load.sources) == 1
    assert isinstance(technology.max_load.sources[0].metadata, MetaData)
    assert technology.max_load.sources[0].metadata.name == "template_dataset"


def test_template_transport_technology_write(
    model: Model,
):
    """Write persists ``attributes.json`` and matches the reference output file."""
    technology = TemplateTransportTechnology(model=model)
    technology.build()
    technology.write()

    attributes_path = technology.output_path / "attributes.json"
    reference_path = (
        Path(__file__).parent
        / "fixtures"
        / "template_transport_technology"
        / "attributes_transport_technology.json"
    )

    differences = compare_files(reference_path, attributes_path)
    assert differences == [], "\n".join(differences)


if __name__ == "__main__":
    pytest.main([__file__])
