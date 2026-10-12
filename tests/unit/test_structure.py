"""Unit tests for model_structure."""

from __future__ import annotations

import pytest

from zen_creator.elements.conversion_technologies.aa_template import (
    TemplateConversionTechnology,
)
from zen_creator.elements.storage_technologies.aa_template import (
    TemplateStorageTechnology,
)
from zen_creator.model import Model
from zen_creator.sectors import Sector
from zen_creator.utils.structure import carrier_flows, model_structure


class _HeatPump(TemplateConversionTechnology):
    name = "test_structure_heat_pump"


class _HeatStorage(TemplateStorageTechnology):
    name = "test_structure_heat_storage"


class _StructureSector(Sector):
    """Heat supply for the structure test."""

    name = "test_structure"
    required_sectors: list[str] = []

    def __init__(self) -> None:
        super().__init__()
        self.elements = [_HeatPump, _HeatStorage]


def test_model_structure(model: Model) -> None:
    """Sectors, technologies and carriers are linked through their carriers."""
    model.add_sector_by_name("test_structure")
    model.add_element_by_name("heat", generic="carrier")

    structure = model_structure(model)

    conversion = _HeatPump.name
    storage = _HeatStorage.name
    assert structure["sectors"]["test_structure"] == {
        "description": "Heat supply for the structure test.",
        "required_sectors": [],
        "elements": [conversion, storage],
    }
    assert structure["technologies"][conversion] == {
        "type": "conversion_technology",
        "sectors": ["test_structure"],
        "reference_carrier": ["heat"],
        "input_carrier": ["electricity"],
        "output_carrier": ["heat"],
    }
    assert structure["technologies"][storage]["type"] == "storage_technology"
    assert structure["carrier_flows"] == [("electricity", "heat")]
    assert structure["carriers"] == {
        "heat": {
            "sectors": [],
            "produced_by": [conversion],
            "consumed_by": [],
            "stored_by": [storage],
            "transported_by": [],
        }
    }


def test_carrier_flows() -> None:
    """Each input carrier of a conversion technology flows to each output carrier."""
    technologies = {
        "turbine": {
            "input_carrier": ["natural_gas"],
            "output_carrier": ["electricity"],
        },
        "electrolysis": {
            "input_carrier": ["electricity"],
            "output_carrier": ["hydrogen", "heat"],
        },
        "fuel_cell": {"input_carrier": ["hydrogen"], "output_carrier": ["electricity"]},
        "grid": {"input_carrier": ["heat"], "output_carrier": ["heat"]},
        "battery": {"reference_carrier": ["electricity"]},
    }

    assert carrier_flows(technologies) == [
        ("electricity", "heat"),
        ("electricity", "hydrogen"),
        ("hydrogen", "electricity"),
        ("natural_gas", "electricity"),
    ]


if __name__ == "__main__":
    pytest.main([__file__])
