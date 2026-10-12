"""Unit tests for writing the config.yaml that ZEN-garden is run with."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from zen_creator.elements import GenericEnergySystem
from zen_creator.model import Model
from zen_creator.utils.config import Config, SystemConfig


@pytest.fixture
def model(tmp_path: Path) -> Model:
    """A minimal writable model."""
    model = Model()
    model.name = "dataset"
    model.output_folder = tmp_path / "outputs"
    model.energy_system = GenericEnergySystem(model=model)
    model.config.system.set_nodes = ["CH"]
    return model


def test_config_is_written_next_to_the_dataset(model: Model) -> None:
    """The file sits in the output folder, not inside the dataset."""
    model.write()

    assert (model.output_folder / "config.yaml").is_file()
    assert not (model.output_path / "config.yaml").exists()


def test_config_points_at_the_dataset(model: Model) -> None:
    """The analysis block names the dataset that was written."""
    model.write()

    written = yaml.safe_load((model.output_folder / "config.yaml").read_text())

    assert written["analysis"]["dataset"] == "dataset"


def test_only_configured_settings_are_written(model: Model) -> None:
    """Settings left at their defaults are omitted, so ZEN-garden defaults them."""
    model.config.solver.name = "gurobi"
    model.write()

    written = yaml.safe_load((model.output_folder / "config.yaml").read_text())

    assert written["solver"] == {"name": "gurobi"}
    assert set(written["analysis"]) == {"dataset"}


def test_writing_twice_keeps_one_config(model: Model) -> None:
    """A second model written to the same folder replaces the config."""
    model.write()
    model.name = "other_dataset"
    model.write()

    written = yaml.safe_load((model.output_folder / "config.yaml").read_text())

    assert written["analysis"]["dataset"] == "other_dataset"
    assert sorted(p.name for p in model.output_folder.iterdir()) == [
        "config.yaml",
        "dataset",
        "other_dataset",
    ]


def test_refuses_to_overwrite_the_loaded_config(tmp_path: Path) -> None:
    """The written config never replaces the config it was loaded from."""
    config_path = tmp_path / "outputs" / "config.yaml"
    config_path.parent.mkdir(parents=True)
    config_path.write_text("system:\n  set_nodes: [CH]\n", encoding="utf-8")

    model = Model.from_config(config_path)
    model.name = "dataset"
    model.output_folder = tmp_path / "outputs"
    model.energy_system = GenericEnergySystem(model=model)

    with pytest.raises(ValueError, match="would overwrite the configuration file"):
        model.write()

    assert config_path.read_text(encoding="utf-8") == "system:\n  set_nodes: [CH]\n"


def test_no_guard_without_a_loaded_file(tmp_path: Path) -> None:
    """A config built in code has no source file to protect."""
    config = Config(system=SystemConfig(set_nodes=["CH"]))

    assert config.loaded_from is None
