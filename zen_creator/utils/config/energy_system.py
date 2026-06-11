import json
from pathlib import Path
from typing import Dict, List

from pydantic import Field

from ._base import Subscriptable


class ParameterInterpolationConfig(Subscriptable):
    """Config for controlling which parameters get interpolated."""

    parameter_name: list[str] = Field(default_factory=list)

    @classmethod
    def load_from_existing_model(cls, existing_model_path: Path):
        if not isinstance(existing_model_path, (str, Path)):
            raise TypeError(
                f"Expected path of type `str` or `Path`, "
                f"got {type(existing_model_path)}"
            )

        file_path_interp = (
            Path(existing_model_path)
            / "energy_system"
            / "parameters_interpolation_off.json"
        )

        if file_path_interp.exists():
            with open(file_path_interp, "r") as f:
                user_dict = json.load(f)
            return cls.model_validate(user_dict)

        return cls()


class UnitDefinition(Subscriptable):
    dimension: str
    aliases: List[str] = Field(default_factory=list)


class UnitsConfig(Subscriptable):
    base_units: List[str] = Field(default_factory=list)
    definitions: Dict[str, UnitDefinition] = Field(default_factory=dict)

    @classmethod
    def load_from_existing_model(cls, existing_model_path: Path):
        if not isinstance(existing_model_path, (str, Path)):
            raise TypeError(
                f"Expected path of type `str` or `Path`, "
                f"got {type(existing_model_path)}"
            )

        model_path = Path(existing_model_path)

        units_config = cls()
        units_config._base_units_from_existing_model(model_path)
        units_config._unit_definitions_from_existing_model(model_path)

        return units_config

    def _base_units_from_existing_model(self, existing_model_path: Path) -> None:
        base_unit_path = existing_model_path / "energy_system" / "base_units.json"

        if not base_unit_path.exists():
            raise FileNotFoundError(
                f"Could not find the configuration file {base_unit_path}."
            )

        with open(base_unit_path, "r") as f:
            user_dict = json.load(f)

        self.base_units = user_dict["unit"]

    def _unit_definitions_from_existing_model(self, existing_model_path: Path) -> None:
        unit_definition_path = (
            existing_model_path / "energy_system" / "unit_definitions.txt"
        )

        if not unit_definition_path.exists():
            raise FileNotFoundError(
                f"Could not find the configuration file {unit_definition_path}."
            )

        with open(unit_definition_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        unit_definitions = {}
        for line in lines:
            parts = [p.strip() for p in line.split("=")]
            canonical = parts[0]
            dimension = parts[1].strip("[]")
            aliases = parts[2:]
            unit_definitions[canonical] = UnitDefinition(
                dimension=dimension, aliases=aliases
            )

        self.definitions = unit_definitions

    def get_base_units(self) -> Dict[str, list]:
        return {"unit": self.base_units}

    def get_unit_definitions(self) -> str:
        txt = []
        for unit, definition in self.definitions.items():
            aliases_str = " = ".join(definition.aliases)
            line = f"{unit} = [{definition.dimension}] = {aliases_str}"
            txt.append(line)

        return "\n".join(txt)


class EnergySystemConfig(Subscriptable):
    """Config for data that goes into the EnergySystem folder."""

    units: UnitsConfig = Field(default_factory=UnitsConfig)
    parameters_interpolation_off: ParameterInterpolationConfig = Field(
        default_factory=ParameterInterpolationConfig
    )
