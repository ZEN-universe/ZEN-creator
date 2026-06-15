from abc import ABC
from typing import Any, Dict, Type

from pydantic import ConfigDict, Field, model_validator

from zen_creator.utils.registry import Registry

from ._base import Subscriptable


class DatasetConfig(
    ABC, Subscriptable, Registry["DatasetConfig"], is_base_registry=True
):
    name: str = "generic_dataset_config"
    model_config = ConfigDict(extra="forbid")


class DatasetCollectionConfig(
    ABC, Subscriptable, Registry["DatasetCollectionConfig"], is_base_registry=True
):
    name: str = "generic_dataset_collection_config"
    model_config = ConfigDict(extra="forbid")


class TechnologyConfig(
    ABC, Subscriptable, Registry["TechnologyConfig"], is_base_registry=True
):
    name: str = "generic_technology_config"
    model_config = ConfigDict(extra="forbid")


class CarrierConfig(
    ABC, Subscriptable, Registry["CarrierConfig"], is_base_registry=True
):
    name: str = "generic_carrier_config"
    model_config = ConfigDict(extra="forbid")


class ConversionTechnologyConfig(
    ABC, Subscriptable, Registry["ConversionTechnologyConfig"], is_base_registry=True
):
    name: str = "generic_conversion_tech_config"
    model_config = ConfigDict(extra="forbid")


class StorageTechnologyConfig(
    ABC, Subscriptable, Registry["StorageTechnologyConfig"], is_base_registry=True
):
    name: str = "generic_storage_tech_config"
    model_config = ConfigDict(extra="forbid")


class TransportTechnologyConfig(
    ABC, Subscriptable, Registry["TransportTechnologyConfig"], is_base_registry=True
):
    name: str = "generic_transport_tech_config"
    model_config = ConfigDict(extra="forbid")


class DataConfig(Subscriptable):
    """Config container for data operations."""

    model_config = ConfigDict(extra="forbid", validate_default=True)

    dataset: Dict[str, DatasetConfig] = Field(default_factory=dict)
    dataset_collection: Dict[str, DatasetCollectionConfig] = Field(default_factory=dict)
    technology: Dict[str, TechnologyConfig] = Field(default_factory=dict)
    carrier: Dict[str, CarrierConfig] = Field(default_factory=dict)
    conversion_technology: Dict[str, ConversionTechnologyConfig] = Field(
        default_factory=dict
    )
    storage_technology: Dict[str, StorageTechnologyConfig] = Field(default_factory=dict)
    transport_technology: Dict[str, TransportTechnologyConfig] = Field(
        default_factory=dict
    )

    @classmethod
    def _process_registry_field(
        cls,
        user_input_dict: Dict[str, Any],
        base_config_cls: Type[Any],
    ) -> Dict[str, Any]:
        """Helper method to process a registry field in the config.

        This method takes the user input for a specific registry (e.g. datasets,
        technologies, etc.) and merges it with the discovered defaults from the
        registry. It then validates each user-provided configuration against the
        appropriate class from the registry, ensuring that all entries are valid and
        that all registered subclasses are included in the final config, even if the
        user did not specify them.

        Args:
            user_input_dict: The dictionary of user-provided configurations for a
                specific registry.
            base_config_cls: The base configuration class for the registry (e.g.
                DatasetConfig, TechnologyConfig, etc.), which is used to access the
                registry and validate the user input.

        Returns:
            A dictionary containing the merged and validated configurations for the
            registry, including both user-provided entries and defaults for any
            registered subclasses that were not specified by the user.
        """

        # make sure all registered subclasses are included in the
        # config, even if the user did not specify them
        discovered_defaults: Dict[str, Any] = {
            name: {}
            for name, cls_type in base_config_cls.get_registry().items()
            if cls_type != base_config_cls and issubclass(cls_type, base_config_cls)
        }

        merged_payload = {**discovered_defaults, **user_input_dict}

        # validate each entry with the appropriate class
        validated_payload: Dict[str, Any] = {}
        for name, value in merged_payload.items():
            if isinstance(value, dict):
                target_cls = base_config_cls.get_by_name(name)
                if target_cls is not None:
                    validated_payload[name] = target_cls.model_validate(value)
                    continue
                else:
                    raise ValueError(
                        f"Invalid configuration entry '{name}' for registry of type "
                        f"{base_config_cls.__name__}. No matching class found in the "
                        f"registry."
                    )
            validated_payload[name] = value

        return validated_payload

    @model_validator(mode="before")
    @classmethod
    def populate_and_validate_registries(cls, data: Any) -> Any:
        """Validate and populate fields in the data config.

        This validator ensures that all registered subclasses of the various
        config types (e.g. DatasetConfig, TechnologyConfig, etc.) are included
        in the config, even if the user did not specify them. It also
        validates any user-provided configurations against the appropriate
        classes from the registry.
        """
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
