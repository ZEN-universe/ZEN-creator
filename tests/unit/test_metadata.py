"""Unit tests for MetaData."""

from __future__ import annotations

import pytest

from zen_creator.datasets.datasets.metadata import MetaData


def _metadata(url: str | None = None, doi: str | None = None) -> MetaData:
    return MetaData(
        name="x",
        title="T",
        author=["A"],
        publication="P",
        publication_year=2020,
        url=url,
        doi=doi,
    )


@pytest.mark.parametrize(
    "url, doi", [("https://example.org", None), (None, "10.1016/j.x.2020.1")]
)
def test_url_or_doi_suffices(url: str | None, doi: str | None) -> None:
    _metadata(url=url, doi=doi)


@pytest.mark.parametrize("url", [None, ""])
def test_url_or_doi_is_required(url: str | None) -> None:
    """A source without url and doi cannot be traced and is rejected."""
    with pytest.raises(ValueError, match="needs a url or a doi"):
        _metadata(url=url)
