from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Generic, TypeVar, Union

import pandas as pd

from zen_creator.utils.singleton_registry_meta import SingletonRegistryMeta

from .metadata import MetaData

# setup logger
logger = logging.getLogger(__name__)

# return type of data property
T = TypeVar("T", bound=Union[pd.DataFrame, Dict[str, pd.DataFrame]])


class Dataset(ABC, Generic[T], metaclass=SingletonRegistryMeta):
    """
    Abstract base class for datasets.

    Subclasses must implement internal abstract hooks to provide
    metadata, path, and data.
    """

    name: str

    def __init__(self, source_path: str | Path | None):
        """Initialize a Dataset instance.

        Args:
            source_path (str | Path | None): Path to the source data directory.
        """
        logger.info(f"Loading dataset `{self.name}`...")
        self.source_path: Path | None = (
            Path(source_path) if source_path is not None else None
        )

        # Internal storage for validated properties
        self._metadata: MetaData
        self._path: Path | None
        self._data: Any

        # Initialize required fields using abstract hooks
        self.metadata = self._set_metadata()
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
    def metadata(self) -> MetaData:
        """Citation metadata for the dataset.

        Returns:
            MetaData: Citation metadata object.
        """
        return self._metadata

    @metadata.setter
    def metadata(self, value: MetaData) -> None:
        if not isinstance(value, MetaData):
            raise TypeError(
                "metadata must be of type `MetaData`, "
                f"got '{type(value).__name__}' instead."
            )
        self._metadata = value

    # ---------------- Abstract hooks ------------------

    @abstractmethod
    def _set_metadata(self) -> MetaData:
        """Return citation metadata for this dataset."""

    @abstractmethod
    def _set_path(self) -> Path | None:
        """Return the file path to the dataset."""

    @abstractmethod
    def _set_data(self) -> T:
        """Return the dataset as a DataFrame or dict of DataFrames."""
