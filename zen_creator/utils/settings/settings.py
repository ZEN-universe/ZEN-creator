from __future__ import annotations

import importlib
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pydantic import ConfigDict, model_validator

from zen_creator.utils.config._base import Subscriptable

from .category import SettingsCategory

if TYPE_CHECKING:
    from zen_creator.utils.config import Config


def deep_merge(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    """Merge patch into base, returning a new dict.

    Nested mappings are merged recursively. Any other value, a list
    included, replaces the value in base rather than extending it, so a
    patch always states the value it wants in full.
    """
    merged = dict(base)
    for key, value in patch.items():
        current = merged.get(key)
        if isinstance(value, dict) and isinstance(current, dict):
            merged[key] = deep_merge(current, value)
        else:
            merged[key] = value
    return merged


class Settings(Subscriptable):
    """Root settings container.

    Empty by default: concrete settings categories are registered by
    downstream projects as ``SettingsCategory`` subclasses (e.g.
    ZEN-europe's ``TimeSettings``, with ``name = "time_settings"``), and
    become queryable by name, e.g. ``model.settings.time_settings.<field>``.
    """

    model_config = ConfigDict(extra="allow", validate_assignment=True)

    if TYPE_CHECKING:
        # Categories are registered downstream and stored as pydantic extra
        # fields, which pydantic only exposes through a runtime __getattr__.
        # Declaring it for type checkers makes `settings.<category>` typed Any.
        def __getattr__(self, name: str) -> Any: ...

    @model_validator(mode="before")
    @classmethod
    def populate_and_validate_categories(cls, data: Any) -> Any:
        """Validate each registered category against its user-provided data.

        Every ``SettingsCategory`` subclass that has been imported (and
        therefore registered) is included in the result, using its own
        defaults unless the user provided an override for that category.

        Raises:
            ValueError: If data names a category that is not registered.
        """
        if not isinstance(data, dict):
            data = {}

        populated: dict[str, Any] = {}
        for name, category_cls in SettingsCategory.get_registry().items():
            if category_cls is SettingsCategory:
                continue
            populated[name] = category_cls.model_validate(data.get(name) or {})

        unknown = set(data) - set(populated)
        if unknown:
            raise ValueError(
                f"Unknown settings categories: {sorted(unknown)}. Registered "
                f"categories: {sorted(populated)}."
            )

        return populated

    @classmethod
    def load_from_yaml(
        cls, path: str | Path, patch: dict[str, Any] | None = None
    ) -> "Settings":
        """Load the `settings:` block of a config file.

        Args:
            path: The config file to read.
            patch: Overrides to deep-merge into the block before it is
                validated, as a model of a models file declares them.
        """
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

        raw = user_dict.get("settings") or {}
        if patch:
            raw = deep_merge(raw, patch)

        return cls.model_validate(raw)

    @classmethod
    def controlled_paths(cls) -> dict[str, str]:
        """Map every controlled config path to the settings field controlling it.

        Raises:
            ValueError: If two categories control the same config path.
        """
        controlled: dict[str, str] = {}
        for category_cls in SettingsCategory.get_registry().values():
            if category_cls is SettingsCategory:
                continue
            for path, owner in category_cls.controlled_paths().items():
                if path in controlled:
                    raise ValueError(
                        f"Config path '{path}' is controlled by both "
                        f"'{controlled[path]}' and '{owner}'."
                    )
                controlled[path] = owner
        return controlled

    def apply(self, config: "Config") -> None:
        """Write every registered category's controlled fields into config.

        Called after settings are loaded/patched and before the config is
        used to build a model, so a settings field is the single place each
        controlled config value is set.

        Raises:
            ValueError: If two categories control the same config path.
        """
        self.controlled_paths()  # raise on a collision before writing anything

        for name, category_cls in SettingsCategory.get_registry().items():
            if category_cls is SettingsCategory:
                continue
            getattr(self, name).apply(config)
