from __future__ import annotations
from typing import Dict, Optional
from zen_creator.datasets.dataset import Dataset
from zen_creator.utils.default_config import Config
from zen_creator.datasets.combined_datasets.dataset_collection import DatasetCollection
import os
import pandas as pd


class UserMetricsDatasetCollection(DatasetCollection):
    """
    Concrete dataset collection providing user-related metrics.
    """

    def __init__(self, config: Optional[Config] = None):
        # Initialize subclass-specific attributes FIRST
        self.source = "internal_db"

        # Call base initializer (this sets name, config, and calls _get_data)
        super().__init__(
            name="user_metrics",
            config=config,
        )

    def _get_data(self) -> Dict[str, Dataset]:
        """
        Build and return the datasets in this collection.
        """

        # Example data (replace with real loading logic)
        user_counts = [10, 20, 30]
        active_users = [7, 15, 22]

        return {
            "user_counts": Dataset(
                data=user_counts,
                metadata={
                    "description": "Total registered users per month",
                    "source": self.source,
                },
            ),
            "active_users": Dataset(
                data=active_users,
                metadata={
                    "description": "Active users per month",
                    "source": self.source,
                },
            ),
        }
