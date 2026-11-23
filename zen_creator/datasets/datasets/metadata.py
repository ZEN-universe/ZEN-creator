from __future__ import annotations

from typing import Any, Dict, Optional, Union

from pydantic import ConfigDict, PrivateAttr, field_validator, model_validator
from typing_extensions import TypeAliasType

from zen_creator.utils.config import Subscriptable

from ..usage import Usage, active_usage


class MetaData(Subscriptable):
    """Citation metadata for a dataset.

    A pydantic BaseModel that stores bibliographic information for dataset sources.
    Enforces strict type validation to prevent runtime type errors.

    Attributes:
        name: Unique identifier for the dataset.
        title: Full title of the dataset or publication.
        author: List of authors or organizations responsible for publishing.
        publication: Name of the journal, conference, or publication venue.
        publication_year: Year the dataset or publication was released.
        url: Web URL pointing to the dataset or publication. A url or a doi
            is required.
        doi: Digital Object Identifier (DOI) for persistent citation.
    """

    model_config = ConfigDict(strict=True)

    name: str
    title: str
    author: list[str]
    publication: str
    publication_year: int
    url: Optional[str] = None
    doi: Optional[str] = None
    note: Optional[str] = None

    @model_validator(mode="after")
    def _require_url_or_doi(self) -> MetaData:
        """Every source must be traceable, by a URL or a DOI."""
        if not (self.url or self.doi):
            raise ValueError(f"MetaData '{self.name}' needs a url or a doi.")
        return self

    def to_dict(self) -> dict[str, object]:
        """Serialize metadata to a dictionary.

        Converts the MetaData instance to a dictionary representation, maintaining
        compatibility with legacy code that expects dict-based metadata.

        Returns:
            dict[str, object]: Dictionary with all metadata fields and their values.
        """
        return self.model_dump()

    def to_str(self) -> str:
        """Generate a formatted citation string in APA-style format.

        Produces a human-readable citation combining author, year, title, publication,
        and a persistent identifier (DOI preferred over URL).

        Returns:
            str: Formatted citation string. Example: Smith, J. (2024). Energy
                Dataset. Nature Energy. https://doi.org/10.1234/example
        """
        authors_str = ", ".join(self.author)
        citation = (
            f"{authors_str} ({self.publication_year}). {self.title}. "
            f"{self.publication}."
        )
        if self.doi:
            citation += f" https://doi.org/{self.doi}"
        elif self.url:
            citation += f" {self.url}"
        if self.note:
            citation += f". Note: {self.note}"
        return citation


# A dataset's metadata is either a single citation (an atomic Dataset) or a
# dictionary mapping source names to further metadata (a DatasetCollection),
# which may itself contain nested DatasetCollections, hence the recursion.
# TypeAliasType (rather than a plain Union alias) is required so pydantic can
# recognize the self-reference and avoid infinite schema expansion. The value is
# a single string so mypy can resolve the self-reference too.
MetadataTree = TypeAliasType("MetadataTree", "Union[MetaData, Dict[str, MetadataTree]]")


class SourceInformation(Subscriptable):
    """Information about the source of a dataset attribute.

    Combines a descriptive explanation of an attribute's origin with associated
    citation metadata. Supports both single-source (single MetaData) and multi-source
    (dict of MetaData, arbitrarily nested for DatasetCollections composed of other
    DatasetCollections) configurations for flexibility in citation requirements.

    A dictionary, the metadata of a dataset collection, is cited only with the
    datasets that were read while the attribute was built, see
    ``cited_metadata``.

    Attributes:
        description: Narrative explanation of the attribute's source, collection
            method, or data processing applied.
        metadata: Citation metadata, either as a single MetaData object or as a
            (possibly nested) dictionary mapping source names to MetaData objects
            for multi-source attributes.
    """

    model_config = ConfigDict(strict=True)

    description: str
    metadata: MetadataTree

    # the datasets read for the attribute being built when this source was created
    _usage: Optional[Usage] = PrivateAttr(default=None)

    def model_post_init(self, context: Any, /) -> None:
        """Keep the record of the datasets read for the attribute being built."""
        self._usage = active_usage()

    @property
    def cited_metadata(self) -> Optional[MetadataTree]:
        """The metadata cited in ``sources.md``.

        A dictionary keeps only the datasets read while the attribute was built,
        and is None if none was read. A single MetaData, and a source created
        outside an attribute build, where nothing was recorded, are cited in full.
        """
        if self._usage is None or not isinstance(self.metadata, dict):
            return self.metadata
        return _select_read(self.metadata, self._usage)

    @field_validator("metadata")
    @classmethod
    def _validate_metadata(cls, value: MetadataTree):
        """Reject empty metadata dictionaries, at any nesting level."""
        if isinstance(value, dict):
            if not value:
                raise ValueError(
                    "SourceInformation.metadata cannot be an empty dictionary. "
                    "Provide MetaData entries."
                )
            for sub_value in value.values():
                cls._validate_metadata(sub_value)
        return value

    def to_str(self, references: Optional[References] = None) -> str:
        """Generate a formatted string with description and associated citations.

        Produces a human-readable text block combining the source description with
        properly formatted citations. Handles both single-source and multi-source
        (including nested) scenarios automatically.

        Args:
            references: The reference list of the page. If given, the citations
                are listed there and only cited here by their author-year labels.

        Returns:
            str: Multi-line string with description, followed by citations. For
                multi-source, each citation is prefixed with its source name in
                brackets, indented by its nesting depth.
        """
        metadata = self.cited_metadata
        if metadata is None:
            return self.description

        if references is not None:
            labels = sorted(set(references.cite(metadata)))
            heading = "**Citations**" if len(labels) > 1 else "**Citation**"
            return f"{self.description}\n\n{heading}: [{'; '.join(labels)}]"

        lines = [self.description, ""]

        if isinstance(metadata, dict):
            lines.append("**Citations**")
            lines.append("")
            lines.extend(self._format_metadata_tree(metadata))
        else:
            lines.append("**Citation**")
            lines.append("")
            lines.append(metadata.to_str())

        return "\n".join(lines)

    @staticmethod
    def _format_metadata_tree(
        tree: dict[str, MetadataTree], depth: int = 0
    ) -> list[str]:
        """Recursively render a (possibly nested) metadata dictionary as
        indented bullet lines."""
        indent = "  " * depth
        lines: list[str] = []
        for name, value in tree.items():
            if isinstance(value, dict):
                lines.append(f"{indent}- **{name}**:")
                lines.extend(SourceInformation._format_metadata_tree(value, depth + 1))
            else:
                lines.append(f"{indent}- **{name}**: {value.to_str()}")
        return lines


class References:
    """The reference list of a page, e.g. the ``sources.md`` of an element: every
    citation is listed once and cited by its author-year label, e.g.
    "Burandt et al. 2018". Equal labels of different citations get a suffix,
    "2021a", "2021b", in the order they are first cited, so a page is rendered
    after all its citations are added."""

    def __init__(self) -> None:
        # citation string -> (dataset name, metadata), in order of first citation
        self._entries: dict[str, tuple[str, MetaData]] = {}

    def cite(self, metadata: MetadataTree, name: Optional[str] = None) -> list[str]:
        """Add the citations of a (possibly nested) metadata tree and return their
        labels. The dataset name of a citation is its key in the tree, or the name
        in its metadata."""
        if isinstance(metadata, dict):
            return [n for key, value in metadata.items() for n in self.cite(value, key)]
        citation = metadata.to_str()
        self._entries.setdefault(citation, (name or metadata.name, metadata))
        return [self.label(citation)]

    def label(self, citation: str) -> str:
        """The author-year label of a citation, with a suffix if it is shared."""
        label = _author_year(self._entries[citation][1])
        shared = [c for c, (_, m) in self._entries.items() if _author_year(m) == label]
        if len(shared) > 1:
            label += "abcdefghijklmnopqrstuvwxyz"[shared.index(citation)]
        return label

    def to_str(self) -> str:
        """The reference list, sorted by label, with the dataset name each
        citation belongs to."""
        lines = sorted(
            (self.label(citation), name, citation)
            for citation, (name, _) in self._entries.items()
        )
        return "\n".join(
            f"- **{label}** ({name}): {citation}" for label, name, citation in lines
        )

    def __bool__(self) -> bool:
        return bool(self._entries)


# words marking an author as an organization rather than a person
_ORGANIZATION_WORDS = {
    "Academy", "Agency", "Association", "Bank", "Centre", "Center", "Commission",
    "Council", "Department", "Economics", "Europe", "European", "Federal", "Group",
    "Institute", "International", "Laboratory", "Ministry", "Monitor", "National",
    "Network", "Observatory", "Office", "Organisation", "Organization", "Research",
    "Statistical", "Statistics", "Union", "University", "World",
    "and", "for", "of", "the",
}  # fmt: skip
# lower-case parts of a surname, e.g. "De Felice", "van der Berg"
_NAME_PARTICLES = {
    "da",
    "de",
    "del",
    "den",
    "der",
    "di",
    "du",
    "la",
    "le",
    "van",
    "von",
}


def _short_author(author: str) -> str:
    """The surname of a person, or the short name of an organization: its
    abbreviation in parentheses, e.g. "JRC", or its name."""
    author = author.removesuffix("et al.").strip()
    if "(" in author:
        name, abbreviation = author.split("(", 1)
        return min(name.strip(" ,"), abbreviation.split(")")[0].strip(), key=len)
    if "," in author:
        # "Rehfeldt, Matthias" or "European Commission, Joint Research Centre"
        return author.split(",", 1)[0].strip()
    words = author.split()
    is_organization = len(words) == 1 or any(
        word in _ORGANIZATION_WORDS
        or (len(word) > 1 and word.isalpha() and word.isupper())  # "LCP Delta"
        for word in words
    )
    if is_organization:
        return author
    start = len(words) - 1
    while start > 1 and words[start - 1].lower() in _NAME_PARTICLES:
        start -= 1
    return " ".join(words[start:])


def _author_year(metadata: MetaData) -> str:
    """The author-year label of a citation, e.g. "Burandt et al. 2018"."""
    if not metadata.author:
        return f"{metadata.name} {metadata.publication_year}"
    names = [_short_author(author) for author in metadata.author]
    if len(names) > 2 or metadata.author[-1].strip().endswith("et al."):
        authors = f"{names[0]} et al."
    else:
        authors = " and ".join(names)
    return f"{authors} {metadata.publication_year}"


def _select_read(
    tree: dict[str, MetadataTree], usage: Usage
) -> Optional[dict[str, MetadataTree]]:
    """The part of a metadata dictionary whose datasets are in `usage`, None if
    there is none."""
    selected: dict[str, MetadataTree] = {}
    for name, value in tree.items():
        kept = (
            _select_read(value, usage)
            if isinstance(value, dict)
            else (value if id(value) in usage else None)
        )
        if kept is not None:
            selected[name] = kept
    return selected or None


class AssumptionInformation(Subscriptable):
    """Information about the assumptions used in a dataset attribute.

    Combines a descriptive explanation of an attribute's assumptions.
    An assumption is not a source of data, but rather a choice made
    in the modeling process that affects the attribute's value.
    Assumptions do not have associated citation metadata,
    but they may have a description of the rationale behind the assumption.

    Attributes:
        description: Narrative explanation of the attribute's assumptions, collection
            method, or data processing applied.
    """

    model_config = ConfigDict(strict=True)

    description: str
    metadata: Optional[MetadataTree] = None

    def to_str(self, references: Optional[References] = None) -> str:
        """Generate a formatted string with description.

        Produces a human-readable text block combining the source description.

        Args:
            references: Unused, assumptions have no citations.

        Returns:
            str: Multi-line string with description
        """
        lines = [self.description]

        return "\n".join(lines)
