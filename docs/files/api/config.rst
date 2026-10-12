.. _api.config:

Config
======

Overview
--------

``Config`` stores the model configuration used to initialize model structure,
input paths, and selected element sets.

A configuration file has the following blocks:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Block
     - Content
   * - ``source_path``
     - Folder with the raw data.
   * - ``system``
     - ZEN-garden system settings, written to ``system.yaml``.
   * - ``analysis``, ``solver``, ``plugins``
     - ZEN-garden settings, written to ``config.yaml`` in the output folder.
   * - ``elements``
     - Energy system, sectors and elements to insert, and sectors and
       elements to exclude.
   * - ``energy_system``
     - Units and interpolation settings, written to the ``energy_system``
       folder.
   * - ``data``
     - Registered dataset, collection, technology and carrier configurations.
   * - ``scenarios``
     - Scenarios of system, analysis and solver settings (see
       :ref:`scenarios.scenarios`).
   * - ``settings``
     - Project-defined settings, loaded into ``Settings`` rather than
       ``Config`` (see :ref:`settings_and_models.settings_and_models`).

A value that is controlled by a settings category must not be set in the
configuration file; it is written by the settings instead.

Use Cases
---------

- Load model settings from YAML files.
- Pass validated configuration objects into ``Model.from_config``.

Examples
--------

The code below shows an example of a full ``config.yaml`` file. This file is
used to configure ZEN-creator and is required for it to run.

.. literalinclude:: ../generated/default_config_example.yaml
   :language: yaml

.. rubric:: Summary

.. autosummary::
   :nosignatures:

   zen_creator.Config.__init__

.. rubric:: Constructors

.. automethod:: zen_creator.Config.__init__

.. rubric:: Member Reference

.. autoclass:: zen_creator.Config
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __init__
   :no-index: