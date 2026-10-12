from __future__ import annotations

from typing import Dict, Optional, Union

from pydantic import ConfigDict, field_validator
from typing_extensions import TypeAliasType

from zen_creator.utils.config import Subscriptable


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
        url: Optional web URL pointing to the dataset or publication.
        doi: Optional Digital Object Identifier (DOI) for persistent citation.
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

    def to_str(self) -> str:
        """Generate a formatted string with description and associated citations.

        Produces a human-readable text block combining the source description with
        properly formatted citations. Handles both single-source and multi-source
        (including nested) scenarios automatically.

        Returns:
            str: Multi-line string with description, followed by citations. For
                multi-source, each citation is prefixed with its source name in
                brackets, indented by its nesting depth.
        """
        lines = [self.description, ""]

        if isinstance(self.metadata, dict):
            lines.append("**Citations**")
            lines.append("")
            lines.extend(self._format_metadata_tree(self.metadata))
        else:
            lines.append("**Citation**")
            lines.append("")
            lines.append(self.metadata.to_str())

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

    def to_str(self) -> str:
        """Generate a formatted string with description.

        Produces a human-readable text block combining the source description.

        Returns:
            str: Multi-line string with description
        """
        lines = [self.description]

        return "\n".join(lines)
