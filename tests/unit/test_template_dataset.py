"""Unit tests for TemplateDataset construction."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from zen_creator.datasets.datasets import TemplateDataset


def test_template_dataset_construction(tmp_path: Path) -> None:
    """Construction populates path, metadata, and in-memory data."""
    dataset = TemplateDataset(source_path=tmp_path)

    assert dataset.name == "template_dataset"
    assert dataset.source_path == tmp_path
    assert (
        dataset.metadata.title
        == "Technology lifetimes and availability data for energy system modeling"
    )
    assert dataset.metadata.author == "Reliability and Risk Engineering Lab"
    assert dataset.metadata.publication == "Journal of Reliability and Risk Engineering"
    assert dataset.metadata.publication_year == 2026
    assert dataset.metadata.url == "https://example.com/dataset.csv"
    assert dataset.path == Path(".")

    assert isinstance(dataset.data, pd.DataFrame)
    assert list(dataset.data.columns) == ["max_load", "availability_import"]
    assert "template_conversion_technology" in dataset.data.index


def test_template_dataset_metadata_construction(tmp_path: Path) -> None:
    """Construction exposes metadata with expected template values."""
    dataset = TemplateDataset(source_path=tmp_path)

    assert dataset.metadata.to_dict() == {
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
