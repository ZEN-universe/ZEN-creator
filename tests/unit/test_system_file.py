"""Unit tests for reading a model's system file."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from zen_creator.utils.config import SystemConfig
from zen_creator.utils.config.system import find_system_file

SYSTEM = {"set_nodes": ["CH", "DE"], "reference_year": 2023}


def test_reads_system_yaml(tmp_path: Path) -> None:
    """A system.yaml is read into the config."""
    (tmp_path / "system.yaml").write_text(yaml.safe_dump(SYSTEM), encoding="utf-8")

    system = SystemConfig.load_from_existing_model(tmp_path)

    assert system.set_nodes == ["CH", "DE"]
    assert system.reference_year == 2023


def test_reads_legacy_system_json(tmp_path: Path) -> None:
    """A model that still carries the deprecated system.json is read."""
    (tmp_path / "system.json").write_text(json.dumps(SYSTEM), encoding="utf-8")

    system = SystemConfig.load_from_existing_model(tmp_path)

    assert system.set_nodes == ["CH", "DE"]
    assert system.reference_year == 2023


def test_prefers_yaml_over_json(tmp_path: Path) -> None:
    """With both formats present, the yaml file is used."""
    (tmp_path / "system.yaml").write_text(yaml.safe_dump(SYSTEM), encoding="utf-8")
    (tmp_path / "system.json").write_text(
        json.dumps({"reference_year": 1999}), encoding="utf-8"
    )

    assert find_system_file(tmp_path).name == "system.yaml"


def test_raises_without_a_system_file(tmp_path: Path) -> None:
    """A model without any system file is reported as such."""
    with pytest.raises(FileNotFoundError, match="Could not find a system file"):
        SystemConfig.load_from_existing_model(tmp_path)


def test_only_configured_settings_are_marked_as_set(tmp_path: Path) -> None:
    """Settings absent from the file stay unset, so they are not written back."""
    (tmp_path / "system.yaml").write_text(yaml.safe_dump(SYSTEM), encoding="utf-8")

    system = SystemConfig.load_from_existing_model(tmp_path)

    assert system.model_fields_set == {"set_nodes", "reference_year"}
