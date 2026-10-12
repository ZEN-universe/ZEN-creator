import importlib
from pathlib import Path
from typing import Any

from pydantic import Field, PrivateAttr

from ._base import Subscriptable
from .analysis import AnalysisConfig
from .data import DataConfig
from .element import ElementConfig, ElementTypeList
from .energy_system import (
    EnergySystemConfig,
    ParameterInterpolationConfig,
    UnitsConfig,
)
from .solver import SolverConfig
from .system import SystemConfig


def _reject_controlled_paths(user_dict: dict[str, Any]) -> None:
    """Raise if the config file sets a path that a settings category controls.

    Settings is imported locally: the settings package already depends on
    ``zen_creator.utils.config._base``, and importing it at module level here
    would create a needless dependency between the two packages.
    """
    from zen_creator.utils.settings import Settings

    for path, owner in Settings.controlled_paths().items():
        node: Any = user_dict
        for part in path.split("."):
            if not isinstance(node, dict) or part not in node:
                break
            node = node[part]
        else:
            raise ValueError(
                f"'{path}' is set in the configuration file, but it is "
                f"controlled by the settings field '{owner}'. Remove it "
                "from the configuration file and set it via settings "
                "instead."
            )


class Config(Subscriptable):
    """Default configuration for ZEN-creator.

    The ``analysis``, ``solver`` and ``plugins`` blocks are written to
    ZEN-garden's config file, ``system`` to the dataset's system file, and
    ``energy_system`` to the dataset's energy_system folder. The name and the
    output folder of a model are set on the Model.
    """

    # the file this config was loaded from, used to keep the written
    # ZEN-garden config from overwriting it
    _loaded_from: Path | None = PrivateAttr(default=None)

    source_path: str | None = None
    analysis: AnalysisConfig = Field(default_factory=AnalysisConfig)
    solver: SolverConfig = Field(default_factory=SolverConfig)
    system: SystemConfig = Field(default_factory=SystemConfig)
    plugins: dict[str, Any] = Field(default_factory=dict)
    elements: ElementConfig = Field(default_factory=ElementConfig)
    energy_system: EnergySystemConfig = Field(default_factory=EnergySystemConfig)
    data: DataConfig = Field(default_factory=DataConfig)
    scenarios: dict[str, dict[str, dict[str, Any]]] = {}

    @property
    def loaded_from(self) -> Path | None:
        """The file this config was loaded from, if any."""
        return self._loaded_from

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

        # `settings:` is validated separately by Settings.load_from_yaml();
        # Config itself has extra="forbid", so this key must be stripped.
        user_dict.pop("settings", None)

        _reject_controlled_paths(user_dict)

        config = cls.model_validate(user_dict)
        config._loaded_from = config_path.resolve()

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
        config.system = SystemConfig.load_from_existing_model(model_path)
        config.elements.insert = ElementTypeList.load_from_existing_model(model_path)
        config.energy_system.units = UnitsConfig.load_from_existing_model(model_path)
        config.energy_system.parameters_interpolation_off = (
            ParameterInterpolationConfig.load_from_existing_model(model_path)
        )

        return config
