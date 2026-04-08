"""Unit tests for TemplateEnergySystem lifecycle methods."""

from __future__ import annotations

from pathlib import Path

import pytest

from zen_creator.elements.energy_systems.aa_template import TemplateEnergySystem
from zen_creator.model import Model
from zen_creator.utils.compare_trees import compare_files


def test_template_energy_system_construction(
    model: Model,
):
    """Construction sets class name and default energy-system attributes."""
    energy_system = TemplateEnergySystem(model=model)

    assert energy_system.name == "template_energy_system"
    assert energy_system.price_carbon_emissions.default_value == 0
    assert energy_system.discount_rate.default_value == 0.05
    assert energy_system.set_nodes.default_value is None
    assert energy_system.set_edges.default_value is None


def test_template_energy_system_build(
    model: Model,
):
    """Build populates required set_nodes and set_edges template attributes."""
    energy_system = TemplateEnergySystem(model=model)

    energy_system.build()

    assert energy_system.set_nodes.default_value is None
    assert energy_system.set_edges.default_value is None


def test_template_energy_system_write(
    model: Model,
):
    """Write persists ``attributes.json`` and matches the reference output file."""
    energy_system = TemplateEnergySystem(model=model)
    energy_system.build()
    energy_system.write()

    attributes_path = energy_system.output_path / "attributes.json"
    reference_path = (
        Path(__file__).parent
        / "fixtures"
        / "template_energy_system"
        / "attributes_energy_system.json"
    )

    differences = compare_files(reference_path, attributes_path)
    assert differences == [], "\n".join(differences)


if __name__ == "__main__":
    pytest.main([__file__])
