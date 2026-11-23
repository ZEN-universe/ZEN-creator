"""Unit tests for the reference list of sources.md."""

from __future__ import annotations

import pytest

from zen_creator import MetaData, SourceInformation
from zen_creator.datasets.datasets.metadata import (
    AssumptionInformation,
    References,
    _author_year,
)


def _metadata(name: str, author: list[str], year: int = 2026) -> MetaData:
    return MetaData(
        name=name,
        title=name,
        author=author,
        publication="publication",
        publication_year=year,
    )


@pytest.mark.parametrize(
    "author, label",
    [
        (["Thorsten Burandt", "Konstantin Löffler", "Karlo Hainsch"], "Burandt et al."),
        (["Diego Hangartner", "Andreas Hurni"], "Hangartner and Hurni"),
        (["Matteo De Felice"], "De Felice"),
        (["A.D. Korberg", "S. Brynolf"], "Korberg and Brynolf"),
        (["Rehfeldt, Matthias", "Fleiter, Tobias"], "Rehfeldt and Fleiter"),
        (["Friedlingstein, P. et al."], "Friedlingstein et al."),
        (["Bundesamt für Energie (BFE)"], "BFE"),
        (["ECRA (European Cement Research Academy)"], "ECRA"),
        (["European Commission, Joint Research Centre"], "European Commission"),
        (["Danish Energy Agency"], "Danish Energy Agency"),
        (["Eurostat"], "Eurostat"),
        (["ENTSO-E", "ENTSOG"], "ENTSO-E and ENTSOG"),
        (["LCP Delta", "Energy Storage Europe Association"], "LCP Delta and "
         "Energy Storage Europe Association"),
    ],
)  # fmt: skip
def test_author_year_label(author: list[str], label: str) -> None:
    """Persons are cited by surname, organizations by abbreviation or name."""
    assert _author_year(_metadata("x", author)) == f"{label} 2026"


def test_citations_are_listed_once_and_cited_by_label() -> None:
    """A citation shared by several sources is listed once; equal labels of
    different citations get a suffix; nested collections are flattened."""
    a = _metadata("a", ["Anna Smith"])
    b = _metadata("b", ["Ben Jones"], 2020)
    c = _metadata("c", ["Carl Smith"])  # same label as a
    references = References()
    sources: list[SourceInformation | AssumptionInformation] = [
        SourceInformation(description="first", metadata={"a": a, "b": b}),
        SourceInformation(description="second", metadata={"a": a, "x": {"c": c}}),
        SourceInformation(description="third", metadata=c),
        AssumptionInformation(description="assumed"),
    ]
    for source in sources:  # add all citations first, as a page does
        source.to_str(references)

    assert [source.to_str(references) for source in sources] == [
        "first\n\n**Citations**: [Jones 2020; Smith 2026a]",
        "second\n\n**Citations**: [Smith 2026a; Smith 2026b]",
        "third\n\n**Citation**: [Smith 2026b]",
        "assumed",
    ]
    assert references.to_str().splitlines() == [
        "- **Jones 2020** (b): Ben Jones (2020). b. publication.",
        "- **Smith 2026a** (a): Anna Smith (2026). a. publication.",
        "- **Smith 2026b** (c): Carl Smith (2026). c. publication.",
    ]


def test_without_references_citations_stay_inline() -> None:
    """Without a reference list, e.g. printing a single attribute's sources, the
    citations are written out in full."""
    source = SourceInformation(description="single", metadata=_metadata("a", ["A"]))
    assert source.to_str() == "single\n\n**Citation**\n\nA (2026). a. publication."
