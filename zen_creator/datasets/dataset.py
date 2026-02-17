from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict, Union
import pandas as pd
from zen_creator.utils.singleton_registry_meta import SingletonRegistryMeta

class Dataset(ABC, metaclass=SingletonRegistryMeta):
    """
    Abstract base class for datasets.

    Subclasses must implement internal abstract hooks to provide
    author, publication_year, url, and data.
    """
    name: str

    def __init__(self, source_path: str | Path | None):
        
        print(f"Loading dataset `{self.name}`...")
        self.source_path: Path | None = (
            Path(source_path) if source_path is not None else None
        )

        # Internal storage for validated properties
        self._author: str
        self._publication_year: int
        self._url: str
        self._doi: Optional[str] = None
        self._path: Path | None
        self._data: Union[pd.DataFrame, Dict[str, pd.DataFrame]]

        # Initialize required fields using abstract hooks
        self.author = self._get_author()
        self.publication_year = self._get_publication_year()
        self.url = self._get_url()
        self.path = self._get_path()
        self.data = self._get_data()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, 'name'):
            raise Exception(
                f"Subclass {cls.__name__} should define a class variable """
                "'name'."
            )


    # ------- properties ----------------------------
    @property
    def author(self) -> str:
        return self._author
    
    @author.setter
    def author(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("author must be `str`, "
                f"got '{type(value).__name__}' instead.")
        self._author = value

    @property
    def publication_year(self) -> int:
        return self._publication_year

    @publication_year.setter
    def publication_year(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("publication_year must be `int`, "
                f"got '{type(value).__name__}' instead.")
        self._publication_year = value

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("url must be `str`, "
                f"got '{type(value).__name__}' instead.")
        self._url = value

    @property
    def doi(self) -> Optional[str]:
        return self._doi

    @doi.setter
    def doi(self, value: str) -> None:
        if value is not None and not isinstance(value, str):
            raise TypeError("doi must be `str` or `None`, "
                f"got '{type(value).__name__}' instead.")
        self._doi = value

    @property
    def path(self) -> Path | None:
        return self._path
    
    @path.setter
    def path(self, value: str) -> None:
        if value is None:
            self._path = None
            return  
        if not isinstance(value, Path):
            raise TypeError("path must be of type `Path`"
                f"got '{type(value).__name__}' instead.")
        if not value.exists():
            raise ValueError(f"Provided path '{value}' does not exist.")
        self._path = value

    @property
    def data(self) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
        return self._data

    @data.setter
    def data(self, value: pd.DataFrame | dict[str, pd.DataFrame]) -> None:
        if isinstance(value, pd.DataFrame):
            self._data = value
        elif isinstance(value, dict):
            if not all(isinstance(k, str) and isinstance(v, pd.DataFrame)
                       for k, v in value.items()):
                raise TypeError("data must be `dict[str, DataFrame]`")
            self._data = value
        else:
            raise TypeError("data must be `DataFrame` or "
                "`dict[str, DataFrame]`")      

   
    # --------- metadata ---------------------------
    @property
    def metadata(self) -> dict[str, object]:
        return {
            "name": self.name,
            "author": self.author,
            "publication_year": self.publication_year,
            "url": self.url,
            "doi": self.doi,
        }
    
    # ---------------- Abstract hooks ------------------

    @abstractmethod
    def _get_author(self) -> str:
        """Return the author string for this dataset."""

    @abstractmethod
    def _get_publication_year(self) -> int:
        """Return the publication year for this dataset."""

    @abstractmethod
    def _get_url(self) -> str:
        """Return the URL for this dataset."""

    @abstractmethod
    def _get_path(self) -> Path | None:
        """Return the file path to the dataset"""

    @abstractmethod
    def _get_data(self) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
        """Return the dataset as a DataFrame or dict of DataFrames."""
        
    # # ----- Methods to get data -----
    # def create_time_interval(self):
    #     """ this method sets a year and then creates the time interval for which the data is extracted
    #      ToDo: maybe move to model??
    #     """
    #     # set year for which data is extracted
    #     self.data_general_year = self.model.config.time_settings.data_general_year
    #     self.data_timeseries_year = self.model.config.time_settings.data_timeseries_year
    #     self.time_start = pd.Timestamp(year=self.data_general_year, month=1, day=1, hour=0, tz='Europe/Brussels')
    #     self.time_end = pd.Timestamp(year=self.data_general_year + 1, month=1, day=1, hour=0, tz='Europe/Brussels')
    #     self.time_start_ts = pd.Timestamp(year=self.data_timeseries_year, month=1, day=1, hour=0, tz='Europe/Brussels')
    #     self.time_end_ts = pd.Timestamp(year=self.data_timeseries_year + 1, month=1, day=1, hour=0, tz='Europe/Brussels')
    #     self.time_start_history = pd.Timestamp(year=1900, month=1, day=1, hour=0, tz='Europe/Brussels')
    #     self.time_end_history = pd.Timestamp.today()
    #     self.time_range = pd.date_range(self.time_start, self.time_end, freq="h")[:-1]
    #     self.time_range_ts = pd.date_range(self.time_start_ts, self.time_end_ts, freq="h")[:-1]