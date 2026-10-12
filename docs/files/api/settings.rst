.. _api.settings:

Settings
========

Overview
--------

``Settings`` holds the project-defined settings categories of a model.
``SettingsCategory`` is the base class of a category. ``ModelSet`` reads a
models file that declares variants of a dataset as patches of the settings.

Use Cases
---------

- Define typed options that elements and datasets read during the build.
- Control values of the ZEN-garden configuration from a single setting.
- Generate several datasets from one configuration file and one models file.

See :ref:`settings_and_models.settings_and_models` for a guide.

.. rubric:: Summary

.. autosummary::
   :nosignatures:

   zen_creator.utils.settings.Settings
   zen_creator.utils.settings.SettingsCategory
   zen_creator.utils.settings.ModelSet
   zen_creator.utils.settings.deep_merge

.. rubric:: Member Reference

.. autoclass:: zen_creator.utils.settings.Settings
   :members: load_from_yaml, controlled_paths, apply
   :show-inheritance:
   :no-index:

.. autoclass:: zen_creator.utils.settings.SettingsCategory
   :members: apply, controlled_paths
   :show-inheritance:
   :no-index:

.. autoclass:: zen_creator.utils.settings.ModelSet
   :members: load_from_yaml, settings_patch, names
   :show-inheritance:
   :no-index:

.. autofunction:: zen_creator.utils.settings.deep_merge
   :no-index:
