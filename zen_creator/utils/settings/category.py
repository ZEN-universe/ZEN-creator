from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Any, ClassVar

from zen_creator.utils.config._base import Subscriptable
from zen_creator.utils.registry import Registry

if TYPE_CHECKING:
    from zen_creator.utils.config import Config


def _set_dotted(target: Any, path: str, value: Any) -> None:
    """Set a dotted attribute path on target, e.g. 'system.reference_year'.

    A leaf that was already explicitly set on its parent (e.g. loaded from an
    existing model's system file) is left as it is: settings fill in what a
    more specific source left unconfigured, they do not overwrite it.
    """
    *parents, leaf = path.split(".")
    obj = target
    for part in parents:
        obj = getattr(obj, part)
    if leaf in getattr(obj, "model_fields_set", ()):
        return
    setattr(obj, leaf, value)


class SettingsCategory(
    ABC, Subscriptable, Registry["SettingsCategory"], is_base_registry=True
):
    """Base class for a named, type-checked group of settings.

    ZEN-creator defines no concrete settings categories itself. Downstream
    projects (e.g. ZEN-europe) define concrete subclasses with a unique
    ``name`` (e.g. ``"time_settings"``) and their own typed fields. Every
    registered subclass becomes queryable on ``Settings`` as
    ``model.settings.<name>``.

    A category may also *control* one or more ZEN-garden config values, so
    that value has a single place it is defined: the settings field, not the
    config file. ``controls`` maps a field of this category to the dotted
    path it writes on the ``Config`` (e.g.
    ``{"reference_year": "system.reference_year"}``). ``Config.load_from_yaml``
    rejects a config file that also sets a controlled path.

    A category that derives a config value rather than copying it (e.g.
    computing ``optimized_years`` from ``last_year``) overrides ``apply``,
    calling ``super().apply(config)`` first for any plain copies it also
    controls.

    A controlled path that was already explicitly set on the config (e.g.
    ``Config.load_from_existing_model`` reading it from a dataset's own
    system file) is left as it is: settings fill in what a more specific
    source left unconfigured, they do not overwrite it.
    """

    name: ClassVar[str] = "generic_settings_category"
    controls: ClassVar[dict[str, str]] = {}

    def apply(self, config: "Config") -> None:
        """Write this category's controlled fields into the given config."""
        for field, path in self.controls.items():
            _set_dotted(config, path, getattr(self, field))

    @classmethod
    def controlled_paths(cls) -> dict[str, str]:
        """Map this category's controlled config paths to their owner.

        The owner is reported as ``<category name>.<field>``, e.g.
        ``"time.reference_year"``.
        """
        return {path: f"{cls.name}.{field}" for field, path in cls.controls.items()}
