"""Unit tests for the Sector mechanism: required_sectors and AND-membership."""

from __future__ import annotations

import pytest

from zen_creator.elements.carriers.aa_template import TemplateCarrier
from zen_creator.elements.conversion_technologies.aa_template import (
    TemplateConversionTechnology,
)
from zen_creator.elements.storage_technologies.aa_template import (
    TemplateStorageTechnology,
)
from zen_creator.model import Model
from zen_creator.sectors import Sector
from zen_creator.utils.config.element import ElementTypeList


class _RootSector(Sector):
    """Owns an element required by ``_DependentSector``."""

    name = "test_root"
    required_sectors: list[str] = []

    def __init__(self) -> None:
        super().__init__()
        self.elements = [TemplateCarrier]


class _DependentSector(Sector):
    """Requires ``test_root``; owns an element solely."""

    name = "test_dependent"
    required_sectors = ["test_root"]

    def __init__(self) -> None:
        super().__init__()
        self.elements = [TemplateStorageTechnology]


class _SharedSectorA(Sector):
    """Shares ``TemplateConversionTechnology`` with ``_SharedSectorB``."""

    name = "test_shared_a"
    required_sectors: list[str] = []

    def __init__(self) -> None:
        super().__init__()
        self.elements = [TemplateConversionTechnology]


class _SharedSectorB(Sector):
    """Shares ``TemplateConversionTechnology`` with ``_SharedSectorA``."""

    name = "test_shared_b"
    required_sectors: list[str] = []

    def __init__(self) -> None:
        super().__init__()
        self.elements = [TemplateConversionTechnology]


def test_initialize_sectors_raises_on_missing_required_sector(model: Model) -> None:
    """Selecting a sector without its required sector raises ValueError."""
    with pytest.raises(ValueError, match="test_root"):
        model._initialize_sectors(["test_dependent"])


def test_initialize_sectors_succeeds_when_required_sector_included(
    model: Model,
) -> None:
    """Selecting a sector together with its required sector succeeds."""
    model._initialize_sectors(["test_root", "test_dependent"])

    assert TemplateCarrier.name in model.elements
    assert TemplateStorageTechnology.name in model.elements


def test_and_membership_waits_for_all_owning_sectors(model: Model) -> None:
    """An element declared by two sectors is added only once both are active."""
    model.add_sector_by_name("test_shared_a")
    assert TemplateConversionTechnology.name not in model.elements

    model.add_sector_by_name("test_shared_b")
    assert TemplateConversionTechnology.name in model.elements


def test_and_membership_is_order_independent(model: Model) -> None:
    """Activating the owning sectors in a different order gives the same result."""
    model.add_sector_by_name("test_shared_b")
    assert TemplateConversionTechnology.name not in model.elements

    model.add_sector_by_name("test_shared_a")
    assert TemplateConversionTechnology.name in model.elements


def test_remove_sector_by_name(model: Model) -> None:
    """Removing a sector removes the elements it declares."""
    model.add_sector_by_name("test_root")
    assert TemplateCarrier.name in model.elements

    model.remove_sector_by_name("test_root")
    assert TemplateCarrier.name not in model.elements


def test_exclude_set_sectors_removes_previously_inserted_elements(
    model: Model,
) -> None:
    """`_initialize_technologies_and_carriers` removes excluded sectors."""
    insert = ElementTypeList(set_sectors=["test_root"])

    model._initialize_sectors(insert.set_sectors)
    assert TemplateCarrier.name in model.elements

    model._initialize_technologies_and_carriers(insert, ["test_root"], [])
    assert TemplateCarrier.name not in model.elements


if __name__ == "__main__":
    pytest.main([__file__])
