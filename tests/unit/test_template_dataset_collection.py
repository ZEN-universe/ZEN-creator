"""Unit tests for TemplateDatasetCollection construction."""

from __future__ import annotations

from pathlib import Path

from zen_creator.datasets.dataset_collections.aa_Template import (
    TemplateDatasetCollection,
)
from zen_creator.datasets.datasets import TemplateDataset


def test_template_dataset_collection_construction(tmp_path: Path) -> None:
    """Construction populates source path and dataset mapping."""
    dataset_collection = TemplateDatasetCollection(source_path=tmp_path)

    assert dataset_collection.name == "template_dataset_collection"
    assert dataset_collection.source_path == tmp_path
    assert set(dataset_collection.data.keys()) == {"template_dataset"}
    assert isinstance(dataset_collection.data["template_dataset"], TemplateDataset)


def test_template_dataset_collection_metadata_construction(tmp_path: Path) -> None:
    """Construction exposes metadata with expected template values."""
    dataset_collection = TemplateDatasetCollection(source_path=tmp_path)

    assert dataset_collection.metadata == {
        "template_dataset": {
            "name": "template_dataset",
            "title": (
                "Technology lifetimes and availability data for energy "
                "system modeling"
            ),
            "author": "Reliability and Risk Engineering Lab",
            "publication": "Journal of Reliability and Risk Engineering",
            "publication_year": 2026,
            "url": "https://example.com/dataset.csv",
            "doi": None,
        }
    }
