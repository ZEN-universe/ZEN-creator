"""Helpers for reading data files that may be YAML or (deprecated) JSON.

Used wherever ZEN-creator reads attributes, base units, or similar mapping
files from an existing model directory, since that directory may still carry
the deprecated JSON format.
"""

import json
import warnings
from pathlib import Path
from typing import Any

import yaml

# extensions searched, in order of preference
_SUPPORTED_EXTENSIONS = ("yaml", "yml", "json")


def find_data_file(directory: Path, stem: str) -> Path | None:
    """Return the yaml/yml/json file named ``stem`` in ``directory``.

    Yaml is preferred over the deprecated json format. Returns None if none
    of the supported files exist.
    """
    for extension in _SUPPORTED_EXTENSIONS:
        candidate = directory / f"{stem}.{extension}"
        if candidate.exists():
            return candidate

    return None


def read_data_file(file_path: Path) -> Any:
    """Read a yaml or (deprecated) json data file."""
    with open(file_path, "r", encoding="utf-8") as f:
        if file_path.suffix.lower() in (".yaml", ".yml"):
            return yaml.safe_load(f)

        warnings.warn(
            f"Loading JSON from '{file_path}' is deprecated. Convert the file "
            "to YAML.",
            DeprecationWarning,
            stacklevel=2,
        )
        return json.load(f)
