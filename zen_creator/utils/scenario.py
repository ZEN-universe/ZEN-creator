"""Scenario analysis definitions for ZEN-garden models.

This module provides the building blocks of the scenario analysis: the
per-attribute variation (:class:`Scenario`), the marker for list-valued
settings (:class:`ValueList`), and the model-wide :class:`ScenarioRegistry` that
collects all entries and serializes them to ``scenarios.yaml``.
"""

from __future__ import annotations

import logging
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Generator, Union

import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from zen_creator.model import Model

logger = logging.getLogger(__name__)

DataFrame = Union[pd.DataFrame, pd.Series]
DefaultValue = Union[float, list, None]

# element sets that a scenario entry can address instead of a single element
SET_LABELS = frozenset(
    {
        "set_technologies",
        "set_conversion_technologies",
        "set_storage_technologies",
        "set_transport_technologies",
        "set_retrofitting_technologies",
        "set_carriers",
    }
)

# top-level keys of scenarios.yaml that hold configuration overrides
SETTING_BLOCKS = ("system", "analysis", "solver")

# key of the energy system in scenarios.yaml
ENERGY_SYSTEM_KEY = "EnergySystem"


@dataclass
class ValueList:
    """List of values for a system, analysis, or solver setting.

    Marks a list as a set of values to run one after another, as opposed to a
    setting whose value is itself a list.

    Attributes:
        values: The values to iterate over.
        fmt: Format string for the sub-scenario name, must contain '{}'.
    """

    values: list
    fmt: str | None = None


@dataclass(eq=False)
class Scenario:
    """Variation of a single attribute in one scenario.

    The entry type determines the entry in scenarios.yaml: a default value is
    written to an ``attributes_<suffix>.yaml``, a data frame to a
    ``<param>_<suffix>.csv``, and the operators (``default_op`` and ``file_op``) 
    are written as factors that ZEN-garden applies to the unmodified values. 
    A list-valued operator is expanded by ZEN-garden into one sub-scenario per entry.

    Attributes:
        name: The name of the scenario this variation belongs to.
        default_value: Default value replacing the one in attributes.yaml.
        unit: Unit of the default value, defaults to the unit of the attribute.
        df: Time-series data replacing the one of the attribute.
        yearly_variations_df: Yearly variations replacing the ones of the
            attribute.
        default_op: Factor applied to the default value.
        file_op: Factor applied to the time-series data.
        suffix: Suffix of the generated files, defaults to the scenario name.
        fmt: Format string for the sub-scenario name of a list-valued operator,
            must contain '{}'.
    """

    name: str
    default_value: DefaultValue = field(default=None, kw_only=True)
    unit: str | None = field(default=None, kw_only=True)
    df: DataFrame | None = field(default=None, kw_only=True)
    yearly_variations_df: DataFrame | None = field(default=None, kw_only=True)
    default_op: float | list | None = field(default=None, kw_only=True)
    file_op: float | list | None = field(default=None, kw_only=True)
    suffix: str | None = field(default=None, kw_only=True)
    fmt: str | None = field(default=None, kw_only=True)

    def __post_init__(self) -> None:
        """Validate the value types and fall back to the scenario name as suffix."""
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("A scenario needs a non-empty name.")

        entry_types = (
            self.default_value,
            self.df,
            self.yearly_variations_df,
            self.default_op,
            self.file_op,
        )
        if all(entry is None for entry in entry_types):
            raise ValueError(
                f"Scenario '{self.name}' does not change anything. Set one of "
                "'default_value', 'df', 'yearly_variations_df', 'default_op', or "
                "'file_op'."
            )

        if self.unit is not None and self.default_value is None:
            raise ValueError(
                f"Scenario '{self.name}' sets a unit without a 'default_value'."
            )

        if self.fmt is not None and "{}" not in self.fmt:
            raise ValueError(
                f"The format '{self.fmt}' of scenario '{self.name}' must contain "
                "the placeholder '{}'."
            )

        if self.suffix is None:
            self.suffix = self.name

    def entries(self, param: str) -> dict[str, dict]:
        """Build the scenarios.yaml entries of this variation.

        Yearly variations are a parameter of their own in ZEN-garden, so they
        are returned under a separate key.

        Args:
            param: Name of the attribute this variation belongs to.

        Returns:
            dict: Mapping of parameter name to its scenarios.yaml entry.
        """
        result = {}

        entry = build_entry(
            param,
            default=(
                f"attributes_{self.suffix}" if self.default_value is not None else None
            ),
            file=f"{param}_{self.suffix}" if self.df is not None else None,
            default_op=self.default_op,
            file_op=self.file_op,
            fmt=self.fmt,
        )
        if entry:
            result[param] = entry

        if self.yearly_variations_df is not None:
            variations_param = f"{param}_yearly_variation"
            result[variations_param] = {"file": f"{variations_param}_{self.suffix}"}

        return result

    def data_files(self, param: str) -> dict[str, DataFrame]:
        """Return the data files of this variation.

        Args:
            param: Name of the attribute this variation belongs to.

        Returns:
            dict: Mapping of file name, without extension, to its data.
        """
        files = {}
        if self.df is not None:
            files[f"{param}_{self.suffix}"] = self.df
        if self.yearly_variations_df is not None:
            files[f"{param}_yearly_variation_{self.suffix}"] = self.yearly_variations_df

        return files


def build_entry(
    param: str,
    default: str | None = None,
    file: str | None = None,
    default_op: float | list | None = None,
    file_op: float | list | None = None,
    fmt: str | None = None,
) -> dict[str, Any]:
    """Assemble the scenarios.yaml entry of a single parameter.

    Args:
        param: Name of the parameter.
        default: Name of the attributes file, without extension.
        file: Name of the csv file, without extension.
        default_op: Factor applied to the default value.
        file_op: Factor applied to the time-series data.
        fmt: Format string for the sub-scenario name of a list-valued operator.

    Returns:
        dict: The entry of the parameter, empty if nothing is set.

    Raises:
        ValueError: If an operator is not numeric or a format is ambiguous.
    """
    if fmt is not None and "{}" not in fmt:
        raise ValueError(
            f"The format '{fmt}' of parameter '{param}' must contain the "
            "placeholder '{}'."
        )

    operators = {"default_op": default_op, "file_op": file_op}
    expanded = [key for key, value in operators.items() if isinstance(value, list)]

    if fmt is not None and len(expanded) > 1:
        raise ValueError(
            f"Parameter '{param}' expands both operators {expanded}, so the format "
            f"'{fmt}' is ambiguous. Use separate scenarios."
        )

    entry: dict[str, Any] = {}
    if default is not None:
        entry["default"] = default
    if file is not None:
        entry["file"] = file

    for key, value in operators.items():
        if value is None:
            continue
        _validate_operator(param, key, value)
        entry[key] = value
        if isinstance(value, list):
            if fmt is not None:
                entry[f"{key}_fmt"] = fmt
            elif len(expanded) > 1:
                entry[f"{key}_fmt"] = f"{param}_{key}_{{}}"
            else:
                entry[f"{key}_fmt"] = f"{param}_{{}}"

    return entry


def _validate_operator(param: str, key: str, value: float | list) -> None:
    """Check that an operator is numeric or a non-empty list of numbers.

    Args:
        param: Name of the parameter.
        key: Name of the operator, 'default_op' or 'file_op'.
        value: The operator value to check.

    Raises:
        ValueError: If the value is not numeric or an empty list.
    """
    values = value if isinstance(value, list) else [value]

    if not values:
        raise ValueError(f"The operator '{key}' of parameter '{param}' is empty.")

    for entry in values:
        if isinstance(entry, bool) or not isinstance(
            entry, (int, float, np.integer, np.floating)
        ):
            raise ValueError(
                f"The operator '{key}' of parameter '{param}' must be numeric. "
                f"Got type {type(entry).__name__}."
            )


class ScenarioRegistry:
    """Collects the scenario entries of a model and writes scenarios.yaml.

    Entries come from three places: the variations attached to an attribute via
    ``Attribute.set_data``, the configuration overrides added with :meth:`add`,
    and the set-wide entries added with :meth:`add_set`.

    Attributes:
        model: The model this registry belongs to.
    """

    def __init__(self, model: Model):
        """Initialize an empty registry.

        Args:
            model: The model this registry belongs to.
        """
        self.model: Model = model
        self._scenarios: dict[str, dict[str, dict]] = {}
        self._global_scope = False

    @contextmanager
    def global_scope(self) -> Generator[None, None, None]:
        """Restrict registrations to settings overrides and set-wide entries.

        Entered while a project's global scenario definitions run (see
        :meth:`Model.apply_global_scenarios`), so that element-level scenarios
        stay defined next to the attribute they modify instead of being
        duplicated here. :meth:`register_scenario`, the only entry point for
        element-level scenarios, raises for as long as this is active.
        """
        self._global_scope = True
        try:
            yield
        finally:
            self._global_scope = False

    def __bool__(self) -> bool:
        """Whether any scenario has been defined."""
        return bool(self._scenarios)

    def __len__(self) -> int:
        """Number of defined scenarios."""
        return len(self._scenarios)

    @property
    def names(self) -> list[str]:
        """Names of all defined scenarios."""
        return sorted(self._scenarios)

    def register_scenario(
        self, element_key: str, param: str, scenario: Scenario
    ) -> None:
        """Add the entries of an attribute variation.

        Args:
            element_key: Key of the element in scenarios.yaml.
            param: Name of the attribute.
            scenario: The variation to add.

        Raises:
            ValueError: If called while :meth:`global_scope` is active, since
                element-level scenarios must be defined where the attribute
                itself is set, not in a project's global scenario definitions.
        """
        if self._global_scope:
            raise ValueError(
                f"Cannot register the element-level scenario '{scenario.name}' "
                f"for '{element_key}' from the global scenario definitions. "
                f"Define it where '{param}' itself is set, e.g. via "
                f"'{element_key}.{param}.set_data(scenarios=...)'."
            )

        for scenario_param, entry in scenario.entries(param).items():
            self._register(scenario.name, element_key, scenario_param, entry)

    def add(
        self,
        name: str,
        system: dict | None = None,
        analysis: dict | None = None,
        solver: dict | None = None,
    ) -> None:
        """Add configuration overrides to a scenario.

        The values are written to scenarios.yaml as they are. A :class:`ValueList`
        value, or a dict with a 'values' key, is expanded by ZEN-garden into one
        sub-scenario per entry.

        Args:
            name: Name of the scenario.
            system: Overrides of settings in system.yaml.
            analysis: Overrides of the analysis settings.
            solver: Overrides of solver settings.

        Examples:
            >>> model.scenarios.add("coarse", system={"optimized_years": 3})
            >>> model.scenarios.add(
            ...     "value_list", system={"optimized_years": ValueList([2, 4, 6])}
            ... )
        """
        blocks = {"system": system, "analysis": analysis, "solver": solver}

        for block, settings in blocks.items():
            if not settings:
                continue
            for key, value in settings.items():
                if block == "system":
                    self._validate_system_setting(name, key, value)
                self._register(name, block, key, _setting_entry(key, value))

    def add_set(
        self,
        name: str,
        set_label: str,
        param: str,
        default: str | None = None,
        file: str | None = None,
        default_op: float | list | None = None,
        file_op: float | list | None = None,
        fmt: str | None = None,
        exclude: list[str] | tuple[str, ...] = (),
    ) -> None:
        """Add an entry that applies to every element of a set.

        Only names of files and operators are accepted, since the registry
        cannot write data into the folder of each element. The referenced files
        must therefore be written by the elements themselves.

        Args:
            name: Name of the scenario.
            set_label: The set to address, e.g. 'set_technologies'.
            param: Name of the parameter.
            default: Name of the attributes file, without extension.
            file: Name of the csv file, without extension.
            default_op: Factor applied to the default value.
            file_op: Factor applied to the time-series data.
            fmt: Format string for the sub-scenario name of a list-valued
                operator.
            exclude: Elements of the set to leave unchanged.

        Raises:
            ValueError: If the set label is unknown or nothing is set.

        Examples:
            >>> model.scenarios.add_set(
            ...     "slow_diffusion", "set_technologies", "max_diffusion_rate",
            ...     default_op=0.5,
            ... )
        """
        if set_label not in SET_LABELS:
            raise ValueError(
                f"Unknown set '{set_label}'. Expected one of "
                f"{', '.join(sorted(SET_LABELS))}."
            )

        entry = build_entry(
            param,
            default=default,
            file=file,
            default_op=default_op,
            file_op=file_op,
            fmt=fmt,
        )
        if not entry:
            raise ValueError(
                f"The entry for '{param}' of '{set_label}' in scenario '{name}' "
                "does not change anything."
            )
        if exclude:
            entry["exclude"] = list(exclude)

        self._register(name, set_label, param, entry)

    def _register(
        self, name: str, element_key: str, param: str, entry: dict
    ) -> None:
        """Store a single entry, rejecting duplicates.

        Args:
            name: Name of the scenario.
            element_key: Key of the element, set, or setting block.
            param: Name of the parameter or setting.
            entry: The entry to store.

        Raises:
            ValueError: If the parameter is already set in this scenario.
        """
        element_entry = self._scenarios.setdefault(name, {}).setdefault(element_key, {})

        if param in element_entry:
            raise ValueError(
                f"Parameter '{param}' of '{element_key}' is already defined in "
                f"scenario '{name}'."
            )

        element_entry[param] = entry

    def _validate_system_setting(self, name: str, key: str, value: Any) -> None:
        """Check a system override against the system configuration.

        ZEN-garden requires the setting to exist and to keep its type, so a
        mismatch is rejected here rather than at runtime.

        Args:
            name: Name of the scenario.
            key: Name of the setting.
            value: The new value, or a ValueList of new values.

        Raises:
            ValueError: If the new value has another type than the current one.
        """
        system = self.model.config.system

        if key not in system.keys():
            logger.warning(
                f"Scenario '{name}' overrides the system setting '{key}', which is "
                "not set in the configuration. Make sure ZEN-garden knows it."
            )
            return

        current = system[key]
        if current is None:
            return

        value_list = _as_value_list(value)
        values = value_list.values if value_list is not None else [value]
        for entry in values:
            if type(entry) is not type(current):
                raise ValueError(
                    f"Scenario '{name}' sets the system setting '{key}' to {entry} "
                    f"of type {type(entry).__name__}, but it is of type "
                    f"{type(current).__name__}."
                )

    def validate(self) -> None:
        """Check that all scenario entries refer to elements of the model.

        Raises:
            ValueError: If an entry refers to an unknown element.
        """
        known = (
            set(self.model.elements)
            | set(SET_LABELS)
            | set(SETTING_BLOCKS)
            | {ENERGY_SYSTEM_KEY}
        )

        for name, scenario in self._scenarios.items():
            unknown = set(scenario) - known
            if unknown:
                raise ValueError(
                    f"Scenario '{name}' refers to {sorted(unknown)}, which are not "
                    "part of the model."
                )

    def to_dict(self) -> dict:
        """Convert the registry to the content of scenarios.yaml.

        Returns:
            dict: Mapping of scenario name to its entries.
        """
        return {name: self._scenarios[name] for name in sorted(self._scenarios)}


def _setting_entry(key: str, value: Any) -> Any:
    """Convert a setting override to its scenarios.yaml representation.

    Args:
        key: Name of the setting.
        value: The new value, a ValueList, or a dict with 'values' and 'fmt' keys.

    Returns:
        The value itself, or the expansion entry of a value_list.
    """
    value_list = _as_value_list(value)
    if value_list is None:
        return value

    if not value_list.values:
        raise ValueError(f"The value_list of setting '{key}' is empty.")
    if value_list.fmt is not None and "{}" not in value_list.fmt:
        raise ValueError(
            f"The format '{value_list.fmt}' of setting '{key}' must contain the "
            "placeholder '{}'."
        )

    return {
        "value": list(value_list.values),
        "value_fmt": value_list.fmt or f"{key}_{{}}",
    }


def _as_value_list(value: Any) -> ValueList | None:
    """Return the value_list a value describes, if any.

    Args:
        value: A ValueList, a dict with 'values' and optionally 'fmt', or any other
            value.

    Returns:
        ValueList | None: The value_list, or None if the value is not one.
    """
    if isinstance(value, ValueList):
        return value
    if not isinstance(value, dict):
        return None
    if "values" in value and set(value) <= {"values", "fmt"}:
        return ValueList(values=value["values"], fmt=value.get("fmt"))

    return None
