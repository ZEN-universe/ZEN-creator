from __future__ import annotations

from typing import Optional

from pydantic import ConfigDict, field_validator

from zen_creator.utils.default_config import Subscriptable


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
        return citation


class SourceInformation(Subscriptable):
    """Information about the source of a dataset attribute.

    Combines a descriptive explanation of an attribute's origin with associated
    citation metadata. Supports both single-source (single MetaData) and multi-source
    (dict of MetaData) configurations for flexibility in citation requirements.

    Attributes:
        description: Narrative explanation of the attribute's source, collection
            method, or data processing applied.
        metadata: Citation metadata, either as a single MetaData object or as a
            dictionary mapping source names to MetaData objects for multi-source
            attributes.
    """

    model_config = ConfigDict(strict=True)

    description: str
    metadata: MetaData | dict[str, MetaData]

    @field_validator("metadata")
    @classmethod
    def _validate_metadata(cls, value: MetaData | dict[str, MetaData]):
        """Reject empty metadata dictionaries."""
        if isinstance(value, dict) and not value:
            raise ValueError(
                "SourceInformation.metadata cannot be an empty dictionary. "
                "Provide MetaData entries."
            )
        return value

    def to_str(self) -> str:
        """Generate a formatted string with description and associated citations.

        Produces a human-readable text block combining the source description with
        properly formatted citations. Handles both single-source and multi-source
        scenarios automatically.

        Returns:
            str: Multi-line string with description, followed by citations. For
                multi-source, each citation is prefixed with its source name in
                brackets.
        """
        lines = [self.description, ""]

        if isinstance(self.metadata, dict):
            lines.append("**Citations**")
            lines.append("")
            for name, metadata in self.metadata.items():
                lines.append(f"- **{name}**: {metadata.to_str()}")
        else:
            lines.append("**Citation**")
            lines.append("")
            lines.append(self.metadata.to_str())

        return "\n".join(lines)
