from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

from .settings import deep_merge

# the only keys a models file and a model may declare
FILE_KEYS = ("defaults", "models")
MODEL_KEYS = ("extends", "settings")


class ModelSet:
    """The model variants declared in a models file.

    A models file declares named variants of one dataset, each a sparse
    patch of the settings::

        defaults:                     # optional, applied to every model
          settings:
            cache: {overwrite_dea: false}

        models:
          base: {}
          late_start:
            settings:
              time: {reference_year: 2026}
          no_chemicals:
            extends: base             # optional
            settings:
              structure: {remove_sectors: [methanol]}

    A model may only patch settings, so that a settings field stays the
    single place a value is defined. The patch of a model is its defaults,
    then the models it extends, then its own settings, deep-merged in that
    order, with a list replacing rather than extending the list it
    overrides.

    Each model becomes its own dataset, unlike a ZEN-garden scenario, which
    varies a value within one dataset. A variant belongs here when it
    changes what the dataset contains.
    """

    def __init__(
        self,
        path: Path,
        defaults: dict[str, Any],
        models: dict[str, dict[str, Any]],
    ) -> None:
        self.path = path
        self._defaults = defaults
        self._models = models

    @property
    def names(self) -> list[str]:
        """The declared model names, in the order the file declares them."""
        return list(self._models)

    def __len__(self) -> int:
        return len(self._models)

    def __contains__(self, name: str) -> bool:
        return name in self._models

    @classmethod
    def load_from_yaml(cls, path: str | Path) -> "ModelSet":
        """Read and validate a models file.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file declares no models, or a model declares
                something other than 'extends' and 'settings', or extends a
                model that is not declared.
        """
        models_path = Path(path)

        if not models_path.exists():
            raise FileNotFoundError(f"Could not find the models file {models_path}.")

        yaml = importlib.import_module("yaml")
        with open(models_path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}

        cls._reject_unknown_keys(raw, FILE_KEYS, f"{models_path}")

        defaults = raw.get("defaults") or {}
        cls._reject_unknown_keys(
            defaults, ("settings",), f"the 'defaults' of {models_path}"
        )

        declared = raw.get("models") or {}
        if not declared:
            raise ValueError(f"{models_path} declares no models.")

        models: dict[str, dict[str, Any]] = {}
        for name, entry in declared.items():
            entry = entry or {}
            if not isinstance(entry, dict):
                raise ValueError(
                    f"Model '{name}' in {models_path} must be a mapping, got "
                    f"{type(entry).__name__}."
                )
            cls._reject_unknown_keys(
                entry,
                MODEL_KEYS,
                f"model '{name}' in {models_path}",
                "a model may only patch the settings",
            )
            models[name] = entry

        for name, entry in models.items():
            extends = entry.get("extends")
            if extends is not None and extends not in models:
                raise ValueError(
                    f"Model '{name}' in {models_path} extends the unknown "
                    f"model '{extends}'. Declared models: "
                    f"{', '.join(models)}."
                )

        return cls(models_path, defaults.get("settings") or {}, models)

    @staticmethod
    def _reject_unknown_keys(
        data: dict[str, Any],
        allowed: tuple[str, ...],
        where: str,
        because: str = "",
    ) -> None:
        """Raise if data declares a key that is not allowed."""
        unknown = set(data) - set(allowed)
        if unknown:
            reason = f", since {because}" if because else ""
            raise ValueError(
                f"{where} declares {sorted(unknown)}. Only "
                f"{', '.join(repr(key) for key in allowed)} can be set{reason}."
            )

    def settings_patch(self, name: str) -> dict[str, Any]:
        """The settings overrides that define the given model.

        Raises:
            ValueError: If the model is not declared, or its 'extends' chain
                is cyclic.
        """
        if name not in self._models:
            raise ValueError(
                f"Unknown model '{name}' in {self.path}. Declared models: "
                f"{', '.join(self.names)}."
            )

        patch = dict(self._defaults)
        for ancestor in self._lineage(name):
            patch = deep_merge(patch, self._models[ancestor].get("settings") or {})

        return patch

    def _lineage(self, name: str) -> list[str]:
        """The models to apply for the given model, furthest ancestor first."""
        lineage: list[str] = []
        seen: set[str] = set()

        current: str | None = name
        while current is not None:
            if current in seen:
                raise ValueError(
                    f"The 'extends' chain of model '{current}' in {self.path} "
                    "is cyclic."
                )
            seen.add(current)
            lineage.append(current)
            current = self._models[current].get("extends")

        lineage.reverse()
        return lineage
