"""Unit tests for the model variants declared in a models file."""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar, Iterator

import pytest

from zen_creator.utils.settings import (
    ModelSet,
    Settings,
    SettingsCategory,
    deep_merge,
)

MODELS_YAML = """
defaults:
  settings:
    cache: {overwrite_dea: false}

models:
  base:
    settings:
      time: {reference_year: 2022}
  late_start:
    extends: base
    settings:
      time: {reference_year: 2026}
  no_chemicals:
    extends: late_start
    settings:
      structure: {remove_sectors: [methanol]}
  plain: {}
"""


@pytest.fixture
def models_file(tmp_path: Path) -> Path:
    """A models file covering defaults, extends chains and an empty model."""
    path = tmp_path / "models.yaml"
    path.write_text(MODELS_YAML, encoding="utf-8")
    return path


# ---------- deep_merge ----------


def test_deep_merge_merges_nested_mappings() -> None:
    """Nested mappings are merged rather than replaced."""
    merged = deep_merge(
        {"time": {"reference_year": 2022, "last_year": 2050}},
        {"time": {"reference_year": 2026}},
    )

    assert merged == {"time": {"reference_year": 2026, "last_year": 2050}}


def test_deep_merge_replaces_lists() -> None:
    """A list states the value in full instead of extending the old one."""
    merged = deep_merge(
        {"structure": {"remove_sectors": ["cement", "steel"]}},
        {"structure": {"remove_sectors": ["methanol"]}},
    )

    assert merged == {"structure": {"remove_sectors": ["methanol"]}}


def test_deep_merge_leaves_the_inputs_alone() -> None:
    """Merging does not mutate either input."""
    base = {"time": {"reference_year": 2022}}
    patch = {"time": {"last_year": 2040}}

    deep_merge(base, patch)

    assert base == {"time": {"reference_year": 2022}}
    assert patch == {"time": {"last_year": 2040}}


# ---------- reading a models file ----------


def test_declared_models_are_listed_in_file_order(models_file: Path) -> None:
    """The declared names are available in the order the file declares them."""
    model_set = ModelSet.load_from_yaml(models_file)

    assert model_set.names == ["base", "late_start", "no_chemicals", "plain"]
    assert len(model_set) == 4
    assert "late_start" in model_set


def test_defaults_apply_to_every_model(models_file: Path) -> None:
    """A model without its own settings still receives the defaults."""
    model_set = ModelSet.load_from_yaml(models_file)

    assert model_set.settings_patch("plain") == {"cache": {"overwrite_dea": False}}


def test_a_model_patch_overrides_the_defaults(models_file: Path) -> None:
    """The model's own settings win over the defaults."""
    model_set = ModelSet.load_from_yaml(models_file)

    patch = model_set.settings_patch("base")

    assert patch["time"] == {"reference_year": 2022}
    assert patch["cache"] == {"overwrite_dea": False}


def test_extends_applies_the_ancestor_first(models_file: Path) -> None:
    """A model overrides what the model it extends set."""
    model_set = ModelSet.load_from_yaml(models_file)

    assert model_set.settings_patch("late_start")["time"] == {"reference_year": 2026}


def test_extends_follows_the_whole_chain(models_file: Path) -> None:
    """An extends chain is applied from the furthest ancestor down."""
    model_set = ModelSet.load_from_yaml(models_file)

    patch = model_set.settings_patch("no_chemicals")

    assert patch["time"] == {"reference_year": 2026}
    assert patch["structure"] == {"remove_sectors": ["methanol"]}
    assert patch["cache"] == {"overwrite_dea": False}


def test_unknown_model_is_reported_with_the_declared_names(
    models_file: Path,
) -> None:
    """Asking for a model that is not declared names the ones that are."""
    model_set = ModelSet.load_from_yaml(models_file)

    with pytest.raises(ValueError, match="Unknown model 'bogus'"):
        model_set.settings_patch("bogus")


# ---------- rejected models files ----------


def test_missing_file_is_reported(tmp_path: Path) -> None:
    """A models file that does not exist is reported as such."""
    with pytest.raises(FileNotFoundError, match="Could not find the models file"):
        ModelSet.load_from_yaml(tmp_path / "models.yaml")


def test_file_without_models_is_rejected(tmp_path: Path) -> None:
    """A models file has to declare at least one model."""
    path = tmp_path / "models.yaml"
    path.write_text("defaults:\n  settings: {}\n", encoding="utf-8")

    with pytest.raises(ValueError, match="declares no models"):
        ModelSet.load_from_yaml(path)


def test_unknown_top_level_key_is_rejected(tmp_path: Path) -> None:
    """Only 'defaults' and 'models' may be declared."""
    path = tmp_path / "models.yaml"
    path.write_text("system:\n  set_nodes: [CH]\nmodels:\n  base: {}\n", "utf-8")

    with pytest.raises(ValueError, match=r"declares \['system'\]"):
        ModelSet.load_from_yaml(path)


def test_a_model_may_only_patch_settings(tmp_path: Path) -> None:
    """A model may not reach past the settings into the config."""
    path = tmp_path / "models.yaml"
    path.write_text(
        "models:\n  base:\n    system: {reference_year: 2030}\n", encoding="utf-8"
    )

    with pytest.raises(ValueError, match="may only patch the settings"):
        ModelSet.load_from_yaml(path)


def test_extending_an_unknown_model_is_rejected(tmp_path: Path) -> None:
    """An extends typo is caught when the file is read."""
    path = tmp_path / "models.yaml"
    path.write_text("models:\n  base: {}\n  other:\n    extends: bse\n", "utf-8")

    with pytest.raises(ValueError, match="extends the unknown model 'bse'"):
        ModelSet.load_from_yaml(path)


def test_a_cyclic_extends_chain_is_rejected(tmp_path: Path) -> None:
    """Two models extending each other are reported instead of hanging."""
    path = tmp_path / "models.yaml"
    path.write_text(
        "models:\n  a:\n    extends: b\n  b:\n    extends: a\n", encoding="utf-8"
    )
    model_set = ModelSet.load_from_yaml(path)

    with pytest.raises(ValueError, match="is cyclic"):
        model_set.settings_patch("a")


# ---------- the patch reaching the settings ----------


@pytest.fixture(autouse=True)
def reset_settings_registry() -> Iterator[None]:
    """Reset the SettingsCategory registry for test isolation."""
    SettingsCategory.clear_registry()
    yield
    SettingsCategory.clear_registry()


def test_a_patch_overrides_the_config_files_settings(tmp_path: Path) -> None:
    """A model's patch wins over the `settings:` block of the config file."""

    class TimeSettings(SettingsCategory):
        name: ClassVar[str] = "time"

        reference_year: int = 2022
        last_year: int = 2050

    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "settings:\n  time:\n    reference_year: 2024\n    last_year: 2045\n",
        encoding="utf-8",
    )

    settings = Settings.load_from_yaml(
        config_path, patch={"time": {"reference_year": 2030}}
    )

    assert settings.time.reference_year == 2030
    # a field the patch leaves alone keeps the config file's value
    assert settings.time.last_year == 2045


def test_a_patch_is_validated(tmp_path: Path) -> None:
    """A patch with an unknown field fails like any other settings input."""

    class TimeSettings(SettingsCategory):
        name: ClassVar[str] = "time"

        reference_year: int = 2022

    config_path = tmp_path / "config.yaml"
    config_path.write_text("settings: {}\n", encoding="utf-8")

    with pytest.raises(Exception, match="bogus_field"):
        Settings.load_from_yaml(config_path, patch={"time": {"bogus_field": 1}})
