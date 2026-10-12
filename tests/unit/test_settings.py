"""Unit tests for the generic Settings/SettingsCategory mechanism.

ZEN-creator itself defines no concrete settings categories -- downstream
projects (e.g. ZEN-europe) register SettingsCategory subclasses. These
tests register a small dummy category to exercise the mechanism.
"""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar, Iterator, Type

import pytest
from pydantic import ValidationError

from zen_creator.utils.config import Config
from zen_creator.utils.settings import Settings, SettingsCategory


@pytest.fixture(autouse=True)
def reset_settings_registry() -> Iterator[None]:
    """Reset the SettingsCategory registry for test isolation."""
    SettingsCategory.clear_registry()
    yield
    SettingsCategory.clear_registry()


@pytest.fixture
def dummy_category() -> Type[SettingsCategory]:
    """Register a small settings category for use in tests."""

    class DummyTimeSettings(SettingsCategory):
        name: ClassVar[str] = "time_settings"

        years_in_rolling_horizon: int = 2
        reference_year: int = 2022

    return DummyTimeSettings


def test_settings_empty_by_default():
    """With no registered categories, Settings has no attributes."""
    assert Settings().model_dump() == {}


def test_settings_uses_category_defaults(dummy_category):
    """A registered category is populated with its own defaults."""
    settings = Settings()

    assert settings.time_settings.years_in_rolling_horizon == 2
    assert settings.time_settings.reference_year == 2022


def test_settings_override_from_dict(dummy_category):
    """User-provided values override the category's defaults."""
    settings = Settings.model_validate(
        {"time_settings": {"years_in_rolling_horizon": 5}}
    )

    assert settings.time_settings.years_in_rolling_horizon == 5
    assert settings.time_settings.reference_year == 2022


def test_settings_rejects_wrong_type(dummy_category):
    """Wrong-typed values raise a ValidationError."""
    with pytest.raises(ValidationError):
        Settings.model_validate({"time_settings": {"years_in_rolling_horizon": "five"}})


def test_settings_rejects_unknown_field(dummy_category):
    """Unknown fields on a category raise (extra='forbid' from Subscriptable)."""
    with pytest.raises(ValidationError):
        Settings.model_validate({"time_settings": {"bogus_field": 1}})


def test_load_from_yaml_defaults(tmp_path: Path, dummy_category):
    """A yaml file with no settings: block yields all-default categories."""
    config_path = tmp_path / "config.yaml"
    config_path.write_text("system:\n  set_nodes: [CH]\n")

    settings = Settings.load_from_yaml(config_path)

    assert settings.time_settings.years_in_rolling_horizon == 2


def test_load_from_yaml_override(tmp_path: Path, dummy_category):
    """A settings: block in yaml overrides specific nested values."""
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "system:\n"
        "  set_nodes: [CH]\n"
        "settings:\n"
        "  time_settings:\n"
        "    years_in_rolling_horizon: 7\n"
    )

    settings = Settings.load_from_yaml(config_path)

    assert settings.time_settings.years_in_rolling_horizon == 7
    assert settings.time_settings.reference_year == 2022


def test_config_tolerates_sibling_settings_key(tmp_path: Path):
    """Config.load_from_yaml ignores an unrelated top-level settings: key."""
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "system:\n"
        "  set_nodes: [CH]\n"
        "  reference_year: 2022\n"
        "  optimized_years: 1\n"
        "  interval_between_years: 1\n"
        "settings:\n"
        "  time_settings:\n"
        "    years_in_rolling_horizon: 7\n"
    )

    config = Config.load_from_yaml(config_path)

    assert config.system.set_nodes == ["CH"]


if __name__ == "__main__":
    pytest.main([__file__])
