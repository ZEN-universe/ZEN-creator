from __future__ import annotations

from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    pass
from abc import ABC, abstractmethod
from collections.abc import Mapping
from pathlib import Path

from zen_creator.utils.singleton_registry_meta import SingletonRegistryMeta

from ..datasets.dataset import Dataset
from ..datasets.metadata import MetadataTree


class DatasetCollection(ABC, metaclass=SingletonRegistryMeta):
    """Combined dataset for various data."""

    name: str

    def __init__(self, source_path: Path | str | None = None):
        """Initialize a DatasetCollection instance.

        Args:
            source_path (Path | str | None): Path to the source data directory.
        """
        self.source_path: Path | None = (
            Path(source_path) if source_path is not None else None
        )

        # Internal storage for validated properties
        self._data: Dict[str, Dataset | DatasetCollection] = {}

        # Initialize required fields using abstract hooks
        self.data = dict(self._get_data())

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

    # ------------ properties --------------------------
    @property
    def data(self) -> Dict[str, Dataset | DatasetCollection]:
        """
        Dictionary of datasets.

        Each key is the dataset name and each value is the dataset object.
        """
        return self._data

    # ------------ setters -----------------------------
    @data.setter
    def data(self, value: Dict[str, Dataset | DatasetCollection]):
        """Set the data dictionary and validate its contents.

        Args:
            value: Dictionary of dataset names to Dataset or DatasetCollection
                objects.

        Raises:
            TypeError: If value is not a dict or contains invalid types.
        """
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected an instance of 'dict', got "
                f"'{type(value).__name__}' instead."
            )
        for k, v in value.items():
            if not isinstance(k, str):
                raise TypeError(
                    "Data must be a dictionary of with keys "
                    f"of type `str`, got '{type(k).__name__}' instead."
                )
            if not isinstance(v, Dataset) and not isinstance(v, DatasetCollection):
                raise TypeError(
                    "Data must be a dictionary of with "
                    "values of type `Dataset` or `DatasetCollection`, got "
                    f"'{type(v).__name__}' instead."
                )
        self._data = value

    # ----------- metadata -----------------------------
    @property
    def metadata(self) -> Dict[str, MetadataTree]:
        """Metadata for all datasets in the collection.

        Each value is either a single MetaData object (for an atomic Dataset)
        or a nested dictionary of the same shape (for a DatasetCollection
        composed of other DatasetCollections).

        Returns:
            Dict[str, MetadataTree]: Dictionary mapping dataset names to metadata.
        """
        metadata: Dict[str, MetadataTree] = {}
        for name, dataset in self.data.items():
            metadata[name] = dataset.metadata
        return metadata

    # ---------------- Abstract hooks ------------------

    @abstractmethod
    def _get_data(self) -> Mapping[str, Dataset | DatasetCollection]:
        """Return the data for this dataset collection."""
