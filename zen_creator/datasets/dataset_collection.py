from __future__ import annotations

from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    pass
from abc import ABC, abstractmethod
from pathlib import Path

from zen_creator.datasets.dataset import Dataset
from zen_creator.utils.singleton_registry_meta import SingletonRegistryMeta


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
        self._data: Dict[str, Dataset] = {}

        # Initialize required fields using abstract hooks
        self.data = self._get_data()

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
    def data(self) -> Dict[str, Dataset]:
        """
        Dictionary of datasets.

        Each key is the dataset name and each value is the dataset object.
        """
        return self._data

    # ------------ setters -----------------------------
    @data.setter
    def data(self, value: Dict[str, Dataset]):
        """Set the data dictionary and validate its contents.

        Args:
            value (Dict[str, Dataset]): Dictionary of dataset names to Dataset objects.

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
            if not isinstance(v, Dataset):
                raise TypeError(
                    "Data must be a dictionary of with "
                    "values of type `Dataset`, got "
                    f"'{type(v).__name__}' instead."
                )
        self._data = value

    # ----------- metadata -----------------------------
    @property
    def metadata(self) -> Dict[str, dict]:
        """Metadata for all datasets in the collection.

        Returns:
            Dict[str, dict]: Dictionary mapping dataset names to their metadata.
        """
        metadata = {}
        for name, dataset in self.data.items():
            metadata[name] = dataset.metadata
        return metadata

    # ---------------- Abstract hooks ------------------

    @abstractmethod
    def _get_data(self) -> Dict[str, Dataset]:
        """Return the data for this dataset collection."""
