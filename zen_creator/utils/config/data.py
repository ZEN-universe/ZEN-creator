from abc import ABC
from typing import Any, Dict, Type

from pydantic import BaseModel, ConfigDict, Field, model_validator

from zen_creator.utils.registry import Registry

from ._base import Subscriptable


class DatasetConfig(ABC, Subscriptable, Registry["DatasetConfig"], is_base_registry=True):
    name: str = "generic_dataset_config"
    type: str
    model_config = ConfigDict(extra="forbid")


class DatasetCollectionConfig(ABC, Subscriptable, Registry["DatasetCollectionConfig"], is_base_registry=True):
    name: str = "generic_dataset_collection_config"
    type: str
    model_config = ConfigDict(extra="forbid")


class TechnologyConfig(ABC, Subscriptable, Registry["TechnologyConfig"], is_base_registry=True):
    name: str = "generic_technology_config"
    type: str
    model_config = ConfigDict(extra="forbid")


class CarrierConfig(ABC, Subscriptable, Registry["CarrierConfig"], is_base_registry=True):
    name: str = "generic_carrier_config"
    type: str
    model_config = ConfigDict(extra="forbid")


class ConversionTechnologyConfig(ABC, Subscriptable, Registry["ConversionTechnologyConfig"], is_base_registry=True):
    name: str = "generic_conversion_tech_config"
    type: str
    model_config = ConfigDict(extra="forbid")


class StorageTechnologyConfig(ABC, Subscriptable, Registry["StorageTechnologyConfig"], is_base_registry=True):
    name: str = "generic_storage_tech_config"
    type: str
    model_config = ConfigDict(extra="forbid")


class TransportTechnologyConfig(ABC, Subscriptable, Registry["TransportTechnologyConfig"], is_base_registry=True):
    name: str = "generic_transport_tech_config"
    type: str
    model_config = ConfigDict(extra="forbid")


class DataConfig(Subscriptable):
    """Config container for data operations."""

    model_config = ConfigDict(extra="forbid")

    dataset: Dict[str, DatasetConfig] = Field(default_factory=dict)
    dataset_collection: Dict[str, DatasetCollectionConfig] = Field(default_factory=dict)
    technology: Dict[str, TechnologyConfig] = Field(default_factory=dict)
    carrier: Dict[str, CarrierConfig] = Field(default_factory=dict)
    conversion_technology: Dict[str, ConversionTechnologyConfig] = Field(default_factory=dict)
    storage_technology: Dict[str, StorageTechnologyConfig] = Field(default_factory=dict)
    transport_technology: Dict[str, TransportTechnologyConfig] = Field(default_factory=dict)

    @classmethod
    def _process_registry_field(
        cls,
        user_input_dict: Dict[str, Any],
        base_config_cls: Type[Any],
    ) -> Dict[str, Any]:
        discovered_defaults = {
            name: {"type": cls_type.__name__}
            for name, cls_type in base_config_cls.get_registry().items()
            if cls_type != base_config_cls and hasattr(cls_type, "name")
        }

        merged_payload = {**discovered_defaults, **user_input_dict}

        registered_classes = {
            c.__name__: c
            for c in base_config_cls.get_registry().values()
            if c != base_config_cls and issubclass(c, BaseModel)
        }

        validated_payload: Dict[str, Any] = {}
        for name, value in merged_payload.items():
            if isinstance(value, dict):
                value_type = value.get("type")
                target_cls = registered_classes.get(value_type)
                if target_cls is not None:
                    validated_payload[name] = target_cls.model_validate(value)
                    continue

            validated_payload[name] = value

        return validated_payload

    @model_validator(mode="before")
    @classmethod
    def populate_and_validate_registries(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            data = {}

        registry_mappings = {
            "dataset": DatasetConfig,
            "dataset_collection": DatasetCollectionConfig,
            "technology": TechnologyConfig,
            "carrier": CarrierConfig,
            "conversion_technology": ConversionTechnologyConfig,
            "storage_technology": StorageTechnologyConfig,
            "transport_technology": TransportTechnologyConfig,
        }

        for key, base_cls in registry_mappings.items():
            user_data_block = data.get(key) or {}
            data[key] = cls._process_registry_field(user_data_block, base_cls)

        return data
