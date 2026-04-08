from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Generic, Optional, TypeVar, Union

import pandas as pd

from zen_creator.utils.singleton_registry_meta import SingletonRegistryMeta

# return type of data property
T = TypeVar("T", bound=Union[pd.DataFrame, Dict[str, pd.DataFrame]])


class Dataset(ABC, Generic[T], metaclass=SingletonRegistryMeta):
    """
    Abstract base class for datasets.

    Subclasses must implement internal abstract hooks to provide
    author, title, publication, publication_year, url, and data.
    """

    name: str

    def __init__(self, source_path: str | Path | None):
        """Initialize a Dataset instance.

        Args:
            source_path (str | Path | None): Path to the source data directory.
        """
        print(f"Loading dataset `{self.name}`...")
        self.source_path: Path | None = (
            Path(source_path) if source_path is not None else None
        )

        # Internal storage for validated properties
        self._title: str
        self._author: str
        self._publication: str
        self._publication_year: int
        self._url: str
        self._doi: Optional[str] = None
        self._path: Path | None
        self._data: Any

        # Initialize required fields using abstract hooks
        self.title = self._set_title()
        self.author = self._set_author()
        self.publication = self._set_publication()
        self.publication_year = self._set_publication_year()
        self.url = self._set_url()
        self.path = self._set_path()
        self.data = self._set_data()

    def __init_subclass__(cls, **kwargs):
        """Initialize subclass and ensure name attribute is defined.

        Args:
            **kwargs: Additional keyword arguments.

        Raises:
            Exception: If the subclass does not define a 'name' attribute.
        """
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "name"):
            raise Exception(
                f"Subclass {cls.__name__} should define a class variable " "" "'name'."
            )

    @property
    def title(self) -> str:
        """The title of the dataset.

        Returns:
            str: The dataset title.
        """
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(
                "title must be `str`, " f"got '{type(value).__name__}' instead."
            )
        self._title = value

    @property
    def author(self) -> str:
        """The author of the dataset.

        Returns:
            str: The dataset author.
        """
        return self._author

    @author.setter
    def author(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(
                "author must be `str`, " f"got '{type(value).__name__}' instead."
            )
        self._author = value

    @property
    def publication(self) -> str:
        """The publication where the dataset was published.

        Returns:
            str: The publication name.
        """
        return self._publication

    @publication.setter
    def publication(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(
                "publication must be `str`, " f"got '{type(value).__name__}' instead."
            )
        self._publication = value

    @property
    def publication_year(self) -> int:
        """The year the dataset was published.

        Returns:
            int: The publication year.
        """
        return self._publication_year

    @publication_year.setter
    def publication_year(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(
                "publication_year must be `int`, "
                f"got '{type(value).__name__}' instead."
            )
        self._publication_year = value

    @property
    def url(self) -> str:
        """The URL where the dataset can be accessed.

        Returns:
            str: The dataset URL.
        """
        return self._url

    @url.setter
    def url(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(
                "url must be `str`, " f"got '{type(value).__name__}' instead."
            )
        self._url = value

    @property
    def doi(self) -> Optional[str]:
        """The DOI (Digital Object Identifier) for the dataset.

        Returns:
            Optional[str]: The DOI if available, None otherwise.
        """
        return self._doi

    @doi.setter
    def doi(self, value: str) -> None:
        if value is not None and not isinstance(value, str):
            raise TypeError(
                "doi must be `str` or `None`, " f"got '{type(value).__name__}' instead."
            )
        self._doi = value

    @property
    def path(self) -> Path:
        """The file path to the dataset.

        Returns:
            Path: The path to the dataset file.

        Raises:
            ValueError: If the path has not been set or does not exist.
        """
        if self._path is None:
            raise ValueError("Path has not yet been set or does not exist")
        return self._path

    @path.setter
    def path(self, value: Path | None) -> None:
        if value is None:
            self._path = None
            return
        if not isinstance(value, Path):
            raise TypeError(
                "path must be of type `Path`" f"got '{type(value).__name__}' instead."
            )
        if not value.exists():
            raise ValueError(f"Provided path '{value}' does not exist.")
        self._path = value

    @property
    def data(self) -> T:
        """The dataset data.

        Returns:
            T: The dataset as a DataFrame or dict of DataFrames.
        """
        return self._data

    @data.setter
    def data(self, value: T) -> None:
        # runtime type check
        if isinstance(value, pd.DataFrame):
            self._data = value
        elif isinstance(value, dict):
            if not all(
                isinstance(k, str) and isinstance(v, pd.DataFrame)
                for k, v in value.items()
            ):
                raise TypeError("data must be dict[str, DataFrame]")
            self._data = value
        else:
            raise TypeError(
                f"data must be pd.DataFrame or dict[str, DataFrame], got {type(value)}"
            )

    @property
    def metadata(self) -> dict[str, object]:
        """Metadata dictionary for the dataset.

        Returns:
            dict[str, object]: Dictionary containing dataset metadata.
        """
        return {
            "name": self.name,
            "title": self.title,
            "author": self.author,
            "publication": self.publication,
            "publication_year": self.publication_year,
            "url": self.url,
            "doi": self.doi,
        }

    # ---------------- Abstract hooks ------------------

    @abstractmethod
    def _set_title(self) -> str:
        """Return the title for this dataset."""

    @abstractmethod
    def _set_author(self) -> str:
        """Return the author string for this dataset."""

    @abstractmethod
    def _set_publication(self) -> str:
        """Return the publication for this dataset."""

    @abstractmethod
    def _set_publication_year(self) -> int:
        """Return the publication year for this dataset."""

    @abstractmethod
    def _set_url(self) -> str:
        """Return the URL for this dataset."""

    @abstractmethod
    def _set_path(self) -> Path | None:
        """Return the file path to the dataset."""

    @abstractmethod
    def _set_data(self) -> T:
        """Return the dataset as a DataFrame or dict of DataFrames."""
