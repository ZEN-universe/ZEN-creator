import importlib
from pathlib import Path

from pydantic import Field

from ._base import Subscriptable
from .data import DataConfig
from .element import ElementConfig, ElementTypeList
from .energy_system import (
    EnergySystemConfig,
    ParameterInterpolationConfig,
    UnitsConfig,
)
from .system import SystemConfig


class Config(Subscriptable):
    """Default configuration for ZEN-creator."""

    name: str = ""
    source_path: str | None = None
    output_folder: str | None = None
    elements: ElementConfig = Field(default_factory=ElementConfig)
    system: SystemConfig = Field(default_factory=SystemConfig)
    energy_system: EnergySystemConfig = Field(default_factory=EnergySystemConfig)
    data: DataConfig = Field(default_factory=DataConfig)

    @classmethod
    def load_from_yaml(cls, path: str | Path) -> "Config":
        if not isinstance(path, (str, Path)):
            raise TypeError(f"Expected path of type `str` or `Path`, got {type(path)}")

        config_path = Path(path)

        if not config_path.exists():
            raise FileNotFoundError(
                f"Could not find the configuration file {config_path}."
            )

        yaml = importlib.import_module("yaml")
        with open(config_path, "r", encoding="utf-8") as f:
            user_dict = yaml.safe_load(f) or {}

        config = cls.model_validate(user_dict)
        config.validate_config()

        return config

    @classmethod
    def load_from_existing_model(cls, existing_model_path: str | Path) -> "Config":
        if not isinstance(existing_model_path, (str, Path)):
            raise TypeError(
                f"Expected path of type `str` or `Path`, "
                f"got {type(existing_model_path)}"
            )

        model_path = Path(existing_model_path)

        if not model_path.exists():
            raise FileNotFoundError(
                f"Could not find the configuration file {model_path}."
            )

        config = cls()
        config.name = model_path.name
        config.system = SystemConfig.load_from_existing_model(model_path)
        config.elements.insert = ElementTypeList.load_from_existing_model(model_path)
        config.energy_system.units = UnitsConfig.load_from_existing_model(model_path)
        config.energy_system.parameters_interpolation_off = (
            ParameterInterpolationConfig.load_from_existing_model(model_path)
        )

        config.validate_config()

        return config

    def validate_config(self) -> None:
        if not self.name:
            raise ValueError(
                "The attribute `name` is missing from the configuration file"
            )
        if not self.system.set_nodes:
            raise ValueError(
                "The attribute `system.set_nodes` is missing form the "
                "configuration file."
            )
        if not self.system.reference_year:
            raise ValueError(
                "The attribute `system.reference_year` is missing form the "
                "configuration file."
            )
        if not self.system.optimized_years:
            raise ValueError(
                "The attribute `system.set_optimized_years` is missing form the "
                "configuration file."
            )
        if not self.system.interval_between_years:
            raise ValueError(
                "The attribute `system.interval_between_years` is missing form the "
                "configuration file."
            )
