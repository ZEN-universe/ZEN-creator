.. _settings_and_models.settings_and_models:

############################
Settings and Model Variants
############################

A project built on ZEN-creator (for example ZEN-europe) usually generates
several datasets from the same code: with other nodes, another time horizon,
fewer sectors or alternative data sources. ZEN-creator supports this with two
concepts:

- **Settings**: typed, project-defined options that the element and dataset
  classes read while the model is built.
- **Models files**: named variants of a dataset, each a sparse patch of the
  settings.


Settings
========

ZEN-creator defines no settings itself. A project defines them as subclasses
of :class:`~zen_creator.utils.settings.SettingsCategory`, one class per
category:

.. code-block:: python

   from typing import ClassVar

   from zen_creator.utils.settings import SettingsCategory


   class EmissionsSettings(SettingsCategory):
       """Emissions and carbon-budget settings."""

       name: ClassVar[str] = "emissions"

       use_carbon_budget: bool = True
       temperature_increase: float = 1.5

Every category that has been imported is registered and becomes available as
``model.settings.<name>``, for example
``model.settings.emissions.temperature_increase``. Elements and datasets read
the settings through ``self.settings`` or ``element.settings``.

Settings are set in the ``settings:`` block of the configuration file. Only
fields that differ from their default need to be listed:

.. code-block:: yaml

   settings:
     emissions:
       temperature_increase: 2.0

The block is validated when it is loaded. Unknown categories, unknown fields
and values of the wrong type raise an error.

Settings that control the configuration
---------------------------------------

Some values of the ZEN-garden configuration follow from a setting, for
example the nodes of the model. To keep a single place for such a value, a
category declares it in ``controls``, mapping the field to the dotted path in
the :class:`~zen_creator.Config`:

.. code-block:: python

   class RegionSettings(SettingsCategory):
       name: ClassVar[str] = "region"
       controls: ClassVar[dict[str, str]] = {"set_nodes": "system.set_nodes"}

       set_nodes: list[str] = Field(default_factory=lambda: ["AT", "CH", "DE"])

``Model.from_config`` writes the controlled fields into the configuration
before the model is created. A configuration file that sets a controlled path
itself (here ``system.set_nodes``) is rejected with an error that names the
setting to use instead. Two categories cannot control the same path.

A category that derives a configuration value from several fields overrides
``apply(config)`` and calls ``super().apply(config)`` for its plain copies:

.. code-block:: python

   class TimeSettings(SettingsCategory):
       name: ClassVar[str] = "time"
       controls: ClassVar[dict[str, str]] = {
           "reference_year": "system.reference_year",
       }

       reference_year: int = 2022
       last_year: int = 2050

       def apply(self, config: Config) -> None:
           """Write the horizon into the system config."""
           super().apply(config)
           config.system.optimized_years = self.last_year - self.reference_year + 1

Controlled paths can also point to the element selection
(``elements.insert.set_sectors``, ``elements.exclude_elements``, ...), so that
the structure of the model becomes a setting as well.

A controlled value that has already been set explicitly on the configuration,
for example by ``Config.load_from_existing_model``, is kept.


Models files
============

A models file declares named variants of a dataset. Each variant only lists
the settings that differ:

.. code-block:: yaml

   defaults:                     # optional, applied to every model
     settings:
       time: {last_year: 2050}

   models:
     base: {}
     late_start:
       settings:
         time: {reference_year: 2026}
     no_chemicals:
       extends: base             # optional
       settings:
         structure: {remove_sectors: [methanol]}

The file is read with :class:`~zen_creator.utils.settings.ModelSet`:

.. code-block:: python

   from zen_creator import Model
   from zen_creator.utils.settings import ModelSet, Settings

   model_set = ModelSet.load_from_yaml("models.yaml")

   for name in model_set.names:
       settings = Settings.load_from_yaml(
           "config.yaml", patch=model_set.settings_patch(name)
       )
       model = Model.from_config("config.yaml", settings=settings)
       model.name = name
       model.output_folder = "./data"
       model.build()
       model.write()

The patch of a variant is built from its ``defaults``, then the settings of the
models it extends (furthest ancestor first), then its own settings. The patch
is merged into the ``settings:`` block of the configuration file. Nested
mappings are merged; lists and all other values are replaced, so a patch
always states a list in full.

The models file is validated when it is loaded: a variant may only declare
``extends`` and ``settings``, and ``extends`` must name a declared model
without cycles. A variant cannot patch the ``system`` or ``analysis`` blocks
directly. A value that needs to vary between variants is therefore defined as
a setting, if needed with ``controls``.

Each variant is a separate dataset. A variation that ZEN-garden should solve
within one dataset is a scenario instead (see :ref:`scenarios.scenarios`).
