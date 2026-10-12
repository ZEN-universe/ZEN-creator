.. _scenarios.scenarios:

#########
Scenarios
#########

ZEN-garden can solve several variations of one dataset in a scenario analysis.
The variations are declared in ``scenarios.yaml``. ZEN-creator collects all
scenario entries of a model in ``model.scenarios``
(:class:`~zen_creator.utils.scenario.ScenarioRegistry`) and writes
``scenarios.yaml`` together with the data files that the scenarios reference.
As soon as a scenario is defined, ``conduct_scenario_analysis`` is enabled in
the system file.

Scenario entries are defined in three places, depending on what they vary.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - What varies
     - Where it is defined
     - How
   * - One attribute of one element
     - In the element, where the attribute is set
     - ``Attribute.set_data(scenarios=...)``
   * - System, analysis or solver settings
     - In the configuration file, or in the project's global scenarios
     - ``scenarios:`` block, or ``model.scenarios.add()``
   * - One attribute of all elements of a set
     - In the project's global scenarios
     - ``model.scenarios.add_set()``


Scenarios of an attribute
=========================

A :class:`~zen_creator.Scenario` describes the variation of one attribute in
one scenario. It is attached where the attribute is set, so the variation
stays next to the data it varies:

.. code-block:: python

   from zen_creator import AssumptionInformation, Scenario

   def _set_discount_rate(self) -> Attribute:
       return self.discount_rate.set_data(
           default_value=0.05,
           unit="1",
           source=AssumptionInformation(description="The discount rate is 0.05."),
           scenarios=[
               Scenario("low_discount_rate", default_value=0.02),
               Scenario("discount_rate", default_op=[0.5, 1.5]),
           ],
       )

A scenario sets at least one of:

- ``default_value`` (with an optional ``unit``): replaces the default value.
  Written to ``attributes_<suffix>.yaml``.
- ``df`` or ``yearly_variations_df``: replaces the data. Written to
  ``<attribute>_<suffix>.csv`` or ``<attribute>_yearly_variation_<suffix>.csv``.
- ``default_op`` or ``file_op``: factor applied to the default value or to the
  data. A list of factors creates one sub-scenario per factor, named with
  ``fmt`` (by default ``<attribute>_{}``).

The ``suffix`` of the files defaults to the scenario name. The values of a
scenario are validated with the same rules as the values of the attribute.
The same scenario name can be used by several attributes and elements; their
entries are combined into one scenario.


Scenarios of settings
=====================

Overrides of system, analysis and solver settings can be declared in the
configuration file:

.. code-block:: yaml

   scenarios:
     coarse:
       system:
         aggregated_time_steps_per_year: 24
     resolution:
       system:
         aggregated_time_steps_per_year:
           values: [24, 96, 192]
           fmt: "tsa_{}"

or in code:

.. code-block:: python

   from zen_creator import ValueList

   model.scenarios.add("coarse", system={"aggregated_time_steps_per_year": 24})
   model.scenarios.add(
       "resolution",
       system={"aggregated_time_steps_per_year": ValueList([24, 96, 192], fmt="tsa_{}")},
   )

A :class:`~zen_creator.ValueList` (or a mapping with ``values`` and ``fmt``) is
expanded by ZEN-garden into one sub-scenario per value. A system override
must keep the type of the configured value; a mismatch raises an error.


Scenarios of a set
==================

``model.scenarios.add_set()`` adds an entry that applies to all elements of a
set (``set_technologies``, ``set_conversion_technologies``,
``set_storage_technologies``, ``set_transport_technologies``,
``set_retrofitting_technologies`` or ``set_carriers``):

.. code-block:: python

   model.scenarios.add_set(
       name="slow_diffusion",
       set_label="set_technologies",
       param="max_diffusion_rate",
       default_op=0.5,
       exclude=["photovoltaics"],
   )

Set entries only accept operators and names of files, since the registry does
not write data into the folders of the elements.


Global scenario definitions
===========================

A project collects its setting and set scenarios in one function, which is run
after the model is built:

.. code-block:: python

   def define_global_scenarios(model: Model) -> None:
       """Register the system, analysis, solver, and set-wide scenarios."""
       if model.settings.scenario.sensitivity_no_diffusion_rate:
           model.scenarios.add_set(
               name="no_diffusion_rate",
               set_label="set_technologies",
               param="max_diffusion_rate",
               default_op=0.0,
           )

   model.build()
   model.apply_global_scenarios(define_global_scenarios)
   model.write()

Inside ``apply_global_scenarios``, scenarios of single attributes are
rejected. They belong in the element that sets the attribute.


Validation
==========

Before writing, ``model.validate()`` checks that every scenario refers to an
element of the model, a set, or a settings block. Defining the same parameter
twice in one scenario raises an error when it is registered.
