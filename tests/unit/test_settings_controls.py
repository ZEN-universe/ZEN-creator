"""Unit tests for the settings 'controls' protocol.

A SettingsCategory may control one or more ZEN-garden config values via its
``controls`` mapping, so the value has a single place it is defined: the
settings field, not the config file.
"""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar, Iterator

import pytest

from zen_creator.utils.config import Config
from zen_creator.utils.settings import Settings, SettingsCategory


@pytest.fixture(autouse=True)
def reset_settings_registry() -> Iterator[None]:
    """Reset the SettingsCategory registry for test isolation."""
    SettingsCategory.clear_registry()
    yield
    SettingsCategory.clear_registry()


@pytest.fixture
def time_category():
    """Register a category that controls two plain system fields."""

    class TimeSettings(SettingsCategory):
        name: ClassVar[str] = "time"
        controls: ClassVar[dict[str, str]] = {
            "reference_year": "system.reference_year",
            "interval_between_years": "system.interval_between_years",
        }

        reference_year: int = 2022
        interval_between_years: int = 2

    return TimeSettings


@pytest.fixture
def derived_time_category():
    """Register a category that derives a config value in an override."""

    class TimeSettings(SettingsCategory):
        name: ClassVar[str] = "time"
        controls: ClassVar[dict[str, str]] = {
            "reference_year": "system.reference_year",
        }

        reference_year: int = 2022
        last_year: int = 2030

        def apply(self, config) -> None:
            super().apply(config)
            config.system.optimized_years = self.last_year - self.reference_year + 1

    return TimeSettings


def test_apply_writes_controlled_fields_into_config(time_category) -> None:
    """A category's controlled fields land on the config it is applied to."""
    settings = Settings()
    config = Config()

    settings.apply(config)

    assert config.system.reference_year == 2022
    assert config.system.interval_between_years == 2


def test_apply_uses_overridden_settings(time_category) -> None:
    """A settings override is what gets written, not the class default."""
    settings = Settings.model_validate({"time": {"reference_year": 2026}})
    config = Config()

    settings.apply(config)

    assert config.system.reference_year == 2026


def test_derived_control_runs_its_override(derived_time_category) -> None:
    """A category that overrides apply() can compute a config value."""
    settings = Settings.model_validate({"time": {"last_year": 2032}})
    config = Config()

    settings.apply(config)

    assert config.system.reference_year == 2022
    assert config.system.optimized_years == 11


def test_two_categories_controlling_the_same_path_raise() -> None:
    """A second category controlling an already-controlled path is rejected."""

    class FirstSettings(SettingsCategory):
        name: ClassVar[str] = "first"
        controls: ClassVar[dict[str, str]] = {"a": "system.reference_year"}

        a: int = 2022

    class SecondSettings(SettingsCategory):
        name: ClassVar[str] = "second"
        controls: ClassVar[dict[str, str]] = {"b": "system.reference_year"}

        b: int = 2023

    with pytest.raises(ValueError, match="is controlled by both"):
        Settings.controlled_paths()


def test_config_yaml_rejects_a_controlled_path(tmp_path: Path, time_category) -> None:
    """A config file may not restate a value a settings category controls."""
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "system:\n  set_nodes: [CH]\n  reference_year: 2022\n", encoding="utf-8"
    )

    with pytest.raises(ValueError, match="controlled by the settings field 'time"):
        Config.load_from_yaml(config_path)


def test_config_yaml_allows_uncontrolled_system_fields(
    tmp_path: Path, time_category
) -> None:
    """A config file may still set fields no category controls."""
    config_path = tmp_path / "config.yaml"
    config_path.write_text("system:\n  set_nodes: [CH]\n", encoding="utf-8")

    config = Config.load_from_yaml(config_path)

    assert config.system.set_nodes == ["CH"]


def test_settings_rejects_unknown_category() -> None:
    """An unregistered top-level settings category raises."""
    with pytest.raises(ValueError, match="Unknown settings categories"):
        Settings.model_validate({"bogus_category": {"x": 1}})


def test_model_from_config_applies_settings(tmp_path: Path, time_category) -> None:
    """Model.from_config projects settings into config automatically."""
    from zen_creator.model import Model

    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "system:\n  set_nodes: [CH]\n" "settings:\n  time:\n    reference_year: 2030\n",
        encoding="utf-8",
    )

    model = Model.from_config(config_path)

    assert model.config.system.reference_year == 2030


def test_apply_does_not_overwrite_an_already_set_field(time_category) -> None:
    """A value already set on the config (e.g. read from an existing model)
    wins over the settings default, since it comes from a more specific
    source."""
    settings = Settings()
    config = Config()
    config.system.reference_year = 1999  # simulates a value read from a dataset

    settings.apply(config)

    assert config.system.reference_year == 1999
    # a field the existing model left unconfigured is still filled in
    assert config.system.interval_between_years == 2
