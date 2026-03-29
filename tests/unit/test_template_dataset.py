"""Unit tests for TemplateDataset construction."""

from __future__ import annotations

from pathlib import Path
from typing import Iterator

import pandas as pd
import pytest

from zen_creator.datasets.datasets import TemplateDataset
from zen_creator.utils.singleton_registry_meta import SingletonRegistryMeta


@pytest.fixture(autouse=True)
def reset_singleton_registries() -> Iterator[None]:
    """Reset singleton registries for test isolation."""
    SingletonRegistryMeta._registries.clear()
    yield
    SingletonRegistryMeta._registries.clear()


def test_template_dataset_construction(tmp_path: Path) -> None:
    """Construction populates path, metadata, and in-memory data."""
    dataset = TemplateDataset(source_path=tmp_path)

    assert dataset.name == "template_dataset"
    assert dataset.source_path == tmp_path
    assert (
        dataset.title
        == "Technology lifetimes and availability data for energy system modeling"
    )
    assert dataset.author == "Reliability and Risk Engineering Lab"
    assert dataset.publication == "Journal of Reliability and Risk Engineering"
    assert dataset.publication_year == 2026
    assert dataset.url == "https://example.com/dataset.csv"
    assert dataset.path == Path(".")

    assert isinstance(dataset.data, pd.DataFrame)
    assert list(dataset.data.columns) == ["max_load", "availability_import"]
    assert "template_conversion_technology" in dataset.data.index


def test_template_dataset_metadata_construction(tmp_path: Path) -> None:
    """Construction exposes metadata with expected template values."""
    dataset = TemplateDataset(source_path=tmp_path)

    assert dataset.metadata == {
        "name": "template_dataset",
        "title": (
            "Technology lifetimes and availability data for energy " "system modeling"
        ),
        "author": "Reliability and Risk Engineering Lab",
        "publication": "Journal of Reliability and Risk Engineering",
        "publication_year": 2026,
        "url": "https://example.com/dataset.csv",
        "doi": None,
    }
