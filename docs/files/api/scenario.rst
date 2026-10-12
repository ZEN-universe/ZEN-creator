.. _api.scenario:

Scenario
========

Overview
--------

``Scenario`` describes the variation of one attribute in one scenario.
``ValueList`` marks a list of values of a system, analysis or solver setting to be
run one after another. ``ScenarioRegistry`` (``model.scenarios``) collects all
entries of a model and writes ``scenarios.yaml``.

Use Cases
---------

- Vary an attribute of an element via ``Attribute.set_data(scenarios=...)``.
- Vary ZEN-garden settings via ``model.scenarios.add()``.
- Vary an attribute of all elements of a set via ``model.scenarios.add_set()``.

See :ref:`scenarios.scenarios` for a guide.

.. rubric:: Summary

.. autosummary::
   :nosignatures:

   zen_creator.Scenario
   zen_creator.ValueList
   zen_creator.utils.scenario.ScenarioRegistry

.. rubric:: Member Reference

.. autoclass:: zen_creator.Scenario
   :show-inheritance:
   :no-index:

.. autoclass:: zen_creator.ValueList
   :show-inheritance:
   :no-index:

.. autoclass:: zen_creator.utils.scenario.ScenarioRegistry
   :members: add, add_set, global_scope, validate, to_dict, names
   :show-inheritance:
   :no-index:
