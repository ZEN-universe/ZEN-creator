"""Unit tests for citing only the datasets read while an attribute is built."""

from __future__ import annotations

import functools
from functools import cached_property
from pathlib import Path

import pandas as pd
import pytest

from zen_creator import (
    Dataset,
    DatasetCollection,
    MetaData,
    SourceInformation,
    instance_cache,
)
from zen_creator.datasets.usage import track_usage


def _metadata(name: str) -> MetaData:
    return MetaData(
        name=name,
        title=name,
        author=["author"],
        publication="publication",
        publication_year=2026,
        url=f"https://example.com/{name}",
    )


class _DatasetA(Dataset[pd.Series]):
    name = "usage_dataset_a"

    def _set_metadata(self) -> MetaData:
        return _metadata(self.name)

    def _set_path(self) -> Path | None:
        return None

    def _set_data(self) -> pd.Series:
        return pd.Series([1.0, 2.0])


class _DatasetB(_DatasetA):
    name = "usage_dataset_b"


class _Collection(DatasetCollection):
    name = "usage_collection"

    def _get_data(self) -> dict[str, Dataset]:
        return {"a": _DatasetA(None), "b": _DatasetB(None)}

    @cached_property
    def total_a(self) -> float:
        return float(self.data["a"].data.sum())

    @instance_cache
    def scaled_b(self, factor: float) -> float:
        return float(self.data["b"].data.sum()) * factor

    def source(self) -> SourceInformation:
        return SourceInformation(description="description", metadata=self.metadata)


def _cited(source: SourceInformation) -> set[str]:
    cited = source.cited_metadata
    return set(cited) if isinstance(cited, dict) else set()


def test_only_datasets_read_are_cited() -> None:
    collection = _Collection()
    with track_usage():
        collection.data["a"]
        source = collection.source()
    assert _cited(source) == {"a"}


def test_no_dataset_read_writes_only_the_description() -> None:
    collection = _Collection()
    with track_usage():
        source = collection.source()
    assert source.cited_metadata is None
    assert source.to_str() == "description"


def test_iterating_does_not_record_but_mark_used_does() -> None:
    collection = _Collection()
    with track_usage():
        list(collection.data.items())
        collection.mark_used("b")
        source = collection.source()
    assert _cited(source) == {"b"}


def test_outside_a_build_and_single_metadata_are_cited_in_full() -> None:
    collection = _Collection()
    assert _cited(collection.source()) == {"a", "b"}
    metadata = collection.metadata["a"]
    with track_usage():
        source = SourceInformation(description="description", metadata=metadata)
    assert source.cited_metadata is metadata


def test_cached_property_records_its_datasets_on_every_call() -> None:
    collection = _Collection()
    with track_usage():
        first = collection.total_a
    with track_usage():
        assert collection.total_a == first
        source = collection.source()
    assert _cited(source) == {"a"}


def test_instance_cache_records_its_datasets_on_every_call() -> None:
    collection = _Collection()
    with track_usage():
        collection.scaled_b(2.0)
    with track_usage():
        assert collection.scaled_b(2.0) == 6.0
        source = collection.source()
    assert _cited(source) == {"b"}


def test_functools_cache_on_a_collection_is_rejected() -> None:
    with pytest.raises(TypeError, match="instance_cache"):

        class _Cached(_Collection):
            name = "usage_collection_cached"

            @functools.cache  # noqa: B019, rejected on purpose
            def value(self) -> float:
                return 1.0
