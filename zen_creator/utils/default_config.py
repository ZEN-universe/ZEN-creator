import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from pydantic import BaseModel, ConfigDict, Field


class Subscriptable(BaseModel):
    """
    Allows dictionary-like access to class attributes.

    This class allows dictionary-like access to class attributes, such as
    ``obj["key"]`` instead of ``obj.key``. Similarly, attribute values can
    be changed in a dictionary like fashion ``obj["key"] = new_value``. Lastly,
    attribute names and values can be called using the methods ``.keys()``,
    ``.values()``, and ``.items()`` like in a normal dictionary.

    Inherits from:
        :class:`BaseModel` - Class from the Pydantic package which provides
        advanced features in input data handling and validation.

    """

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    def __getitem__(self, __name: str) -> Any:
        return getattr(self, __name)

    def __setitem__(self, __name: str, __value: Any) -> None:
        setattr(self, __name, __value)

    def keys(self) -> Any:
        return self.model_dump().keys()

    def items(self) -> Any:
        return self.model_dump().items()

    def values(self) -> Any:
        return self.model_dump().values()


# ----- Element Configurations ---------------


class ElementTypeList(Subscriptable):
    """
    Config for list of elements by type.
    """

    energy_system: str = ""
    set_sectors: list[str] = Field(default_factory=list)
    set_conversion_technologies: list[str] = Field(default_factory=list)
    set_storage_technologies: list[str] = Field(default_factory=list)
    set_transport_technologies: list[str] = Field(default_factory=list)
    set_retrofitting_technologies: list[str] = Field(default_factory=list)
    set_carriers: list[str] = Field(default_factory=list)

    @classmethod
    def load_from_existing_model(
        cls, existing_model_path: Path | str
    ) -> "ElementTypeList":
        """
        Construct an ElementTypeList from an already‑built model directory.

        Reads `system.json` to populate the element lists and walks the
        technology sub‑directories in `set_technologies` to infer the
        list of carriers.
        """
        model_path = Path(existing_model_path)
        if not model_path.exists():
            raise FileNotFoundError(f"{model_path} does not exist")

        system_path = model_path / "system.json"
        if not system_path.is_file():
            raise FileNotFoundError(f"could not find {system_path}")

        system_dict = json.loads(system_path.read_text())

        et = cls()
        # copy any known lists from the system file
        for field in (
            "set_conversion_technologies",
            "set_storage_technologies",
            "set_transport_technologies",
            "set_retrofitting_technologies",
        ):
            setattr(et, field, system_dict.get(field, []))

        et.set_carriers = cls._infer_carriers(model_path, et)
        return et

    @staticmethod
    def _infer_carriers(model_path: Path, et: "ElementTypeList") -> list[str]:
        carriers: set[str] = set()

        # mapping of attr name → relative subfolder; only conversion
        # and retrofit technologies have input/output carriers
        tech_map = {
            "set_conversion_technologies": ("set_conversion_technologies", True),
            "set_retrofitting_technologies": (
                "set_conversion_technologies/set_retrofitting_technologies",
                True,
            ),
            "set_storage_technologies": ("set_storage_technologies", False),
            "set_transport_technologies": ("set_transport_technologies", False),
        }

        for attr, (subfolder, has_io) in tech_map.items():
            for tech in getattr(et, attr):
                attr_file = (
                    model_path
                    / "set_technologies"
                    / subfolder
                    / tech
                    / "attributes.json"
                )
                if not attr_file.is_file():
                    raise FileNotFoundError(
                        f"attributes for {tech!r} not found at {attr_file}"
                    )
                data = json.loads(attr_file.read_text())

                carriers |= set(
                    data.get("reference_carrier", {}).get("default_value", [])
                )
                if has_io:
                    carriers |= set(
                        data.get("input_carrier", {}).get("default_value", [])
                    )
                    carriers |= set(
                        data.get("output_carrier", {}).get("default_value", [])
                    )

        return sorted(carriers)


class ElementConfig(Subscriptable):
    """
    Config for element settings.
    """

    # list of elements to include
    insert: ElementTypeList = Field(default_factory=ElementTypeList)
    # list of elements to exclude
    exclude: ElementTypeList = Field(default_factory=ElementTypeList)


# -------- System.json configurations ------------------


class SystemConfig(Subscriptable):
    """
    Config for settings in system.json.

    This includes all configurations located in the `system.json` file.
    If `None`, the configuration gets skipped when writing the system
    file. This means that ZEN-garden will simply use its default value.
    """

    set_nodes: list[str] = []
    set_transport_technologies_loss_exponential: Optional[list[str]] = None
    use_existing_capacities: Optional[bool] = None
    allow_investment: Optional[bool] = None
    double_capex_transport: Optional[bool] = None
    unaggregated_time_steps_per_year: Optional[int] = None
    conduct_time_series_aggregation: Optional[bool] = None
    aggregated_time_steps_per_year: Optional[int] = None
    reference_year: Optional[int] = None
    total_hours_per_year: Optional[int] = None
    optimized_years: Optional[int] = None
    interval_between_years: Optional[int] = None
    use_rolling_horizon: Optional[bool] = None
    years_in_rolling_horizon: Optional[int] = None
    years_in_decision_horizon: Optional[int] = None
    conduct_scenario_analysis: Optional[bool] = None
    run_default_scenario: Optional[bool] = None
    clean_sub_scenarios: Optional[bool] = None
    storage_periodicity: Optional[bool] = None
    multiyear_periodicity: Optional[bool] = None
    exclude_parameters_from_TSA: Optional[bool] = None
    knowledge_depreciation_rate: Optional[float] = None
    storage_charge_discharge_binary: Optional[bool] = None

    @classmethod
    def load_from_existing_model(cls, existing_model_path: Path):

        if not isinstance(existing_model_path, (str, Path)):
            raise TypeError(
                f"Expected path of type `str` or `Path`, "
                f"got {type(existing_model_path)}"
            )

        system_path = Path(existing_model_path) / "system.json"

        if not system_path.exists():
            raise FileNotFoundError(
                f"Could not find the configuration file {system_path}."
            )

        with open(system_path, "r") as f:
            # Load the JSON data into a dictionary
            user_dict = json.load(f)

        # Validate and create the Config object
        system_config = cls().model_validate(user_dict, extra="allow")

        return system_config


# ------- Dataset configurations ----------------------------


class ENSOEAPIConfig(Subscriptable):
    api_key: Optional[str] = None


class DatasetConfig(Subscriptable):
    ensoe_api: ENSOEAPIConfig = Field(default_factory=ENSOEAPIConfig)


class DatasetCollectionConfig(Subscriptable):
    setting: bool = True


class DataConfig(Subscriptable):
    """
    Config for data and datasets.
    """

    datasets: DatasetConfig = Field(default_factory=DatasetConfig)
    dataset_collections: DatasetCollectionConfig = Field(
        default_factory=DatasetCollectionConfig
    )


# ----- Energy System Configurations ------------------


class ParameterInterpolationConfig(Subscriptable):
    """
    Config for controlling which parameters get interpolated.
    """

    parameter_name: list[str] = Field(default_factory=list)

    @classmethod
    def load_from_existing_model(cls, existing_model_path: Path):
        """
        Constructor based on data from an existing model.
        """

        if not isinstance(existing_model_path, (str, Path)):
            raise TypeError(
                f"Expected path of type `str` or `Path`, "
                f"got {type(existing_model_path)}"
            )

        # make type path
        file_path_interp = (
            Path(existing_model_path)
            / "energy_system"
            / "parameters_interpolation_off.json"
        )

        if file_path_interp.exists():
            # Load the data from json
            with open(file_path_interp, "r") as f:
                user_dict = json.load(f)
            return cls.model_validate(user_dict)

        else:
            # construct as empty
            return cls()


class UnitDefinition(Subscriptable):
    dimension: str
    aliases: List[str] = Field(default_factory=list)


class UnitsConfig(Subscriptable):
    base_units: List[str] = Field(default_factory=list)
    definitions: Dict[str, UnitDefinition] = Field(default_factory=dict)

    @classmethod
    def load_from_existing_model(cls, existing_model_path: Path):
        """
        Constructor based on data from an existing model.
        """

        if not isinstance(existing_model_path, (str, Path)):
            raise TypeError(
                f"Expected path of type `str` or `Path`, "
                f"got {type(existing_model_path)}"
            )

        # make path
        model_path = Path(existing_model_path)

        # construct units config
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
            # Load the JSON data into a dictionary
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
            # Load the JSON data into a dictionary
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
        """
        Create dictionary for the `base_units.json` file.
        """
        return {"unit": self.base_units}

    def get_unit_definitions(self) -> str:
        """
        Create text for the `unit_definitions.txt` file.
        """
        txt = []
        for unit, definition in self.definitions.items():
            # Format the unit definition
            aliases_str = " = ".join(definition.aliases)
            line = f"{unit} = [{definition.dimension}] = {aliases_str}"
            txt.append(line)

        return "\n".join(txt)


class EnergySystemConfig(Subscriptable):
    """
    Config for data that goes into the EnergySystem folder.
    """

    units: UnitsConfig = Field(default_factory=UnitsConfig)
    parameters_interpolation_off: ParameterInterpolationConfig = Field(
        default_factory=ParameterInterpolationConfig
    )


# -------- Main Config ----------------------------------------


class Config(Subscriptable):
    """
    Default configuration for ZEN-creator.
    """

    name: str = ""
    source_path: str | None = None
    output_folder: str | None = None
    elements: ElementConfig = Field(default_factory=ElementConfig)
    system: SystemConfig = Field(default_factory=SystemConfig)
    energy_system: EnergySystemConfig = Field(default_factory=EnergySystemConfig)
    data: DataConfig = Field(default_factory=DataConfig)

    @classmethod
    def load_from_yaml(cls, path: str | Path) -> "Config":
        """Load a configuration from a YAML file.

        Args:
            path (str | Path): Path to the YAML configuration file.

        Returns:
            Config: The loaded configuration object.

        Raises:
            TypeError: If path is not a string or Path.
            FileNotFoundError: If the configuration file does not exist.
        """
        if not isinstance(path, (str, Path)):
            raise TypeError(f"Expected path of type `str` or `Path`, got {type(path)}")

        config_path = Path(path)

        if not config_path.exists():
            raise FileNotFoundError(
                f"Could not find the configuration file {config_path}."
            )

        with open(config_path, "r") as f:
            user_dict = yaml.safe_load(f) or {}

        # create config from file
        config = cls.model_validate(user_dict)

        # check requirements
        config.validate_config()

        return config

    @classmethod
    def load_from_existing_model(cls, existing_model_path: str | Path) -> "Config":
        """Load a configuration from an existing model.

        Args:
            path (str | Path): Path to the existing model.

        Returns:
            Config: The loaded configuration object.

        Raises:
            TypeError: If path is not a string or Path.
        """
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
        # config.output_folder = str(model_path.parent)
        config.system = SystemConfig.load_from_existing_model(model_path)
        config.elements.insert = ElementTypeList.load_from_existing_model(model_path)
        config.energy_system.units = UnitsConfig.load_from_existing_model(model_path)
        config.energy_system.parameters_interpolation_off = (
            ParameterInterpolationConfig.load_from_existing_model(model_path)
        )

        # check requirements
        config.validate_config()

        return config

    def validate_config(self) -> None:
        """
        Validate the configurations loaded from the config.

        Raises:
            ValueError: If one of the required config inputs does not exist.
                The required inputs are `name`, `source_path`,
                `system.set_nodes`, `system.reference_year`,
                `system.optimized_years`, and `system.interval_between_years`.
        """
        if not self.name:
            raise ValueError(
                "The attribute `name` is missing from the configuration file"
            )
        # if not self.source_path:
        #     raise ValueError(
        #         "The attribute `source_path` is missing form the configuration file."
        #         "The source path is the path where the raw data is located."
        #     )
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
