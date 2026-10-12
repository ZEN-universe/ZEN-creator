.. _design.design:

###########################
Design Ideas
###########################

ZEN-creator generates input data for
`ZEN-garden <https://zen-garden.readthedocs.io/en/latest/>`_ from Python code.
A project (for example ZEN-europe) implements the abstract classes of
ZEN-creator: one class per technology and carrier, one class per data source,
and a set of typed settings that control which dataset is generated.

This page describes the ideas behind this structure and why it differs from a
workflow manager such as Snakemake or from a collection of scripts that write
the input files by hand.


Core ideas
==========

Every carrier and technology is a Python class. Every attribute of an element
(for example ``capex_specific_conversion`` of ``photovoltaics``) has exactly
one method, ``_set_<attribute>()``, that decides where its value comes from.
Reading an element file therefore answers the question "where does this number
come from?" without searching through scripts or intermediate files.

One class per data source
-------------------------

Each publication, database or API is wrapped in its own ``Dataset`` class.
The dataset reads the raw files, cleans them and exposes
``get_<attribute>()`` methods that return ready-to-use attributes. Whenever an
attribute combines several sources, a ``DatasetCollection`` does the
combination. The element only calls the dataset or collection and never
processes raw data itself.

Provenance travels with the value
---------------------------------

An attribute can only be set together with a ``SourceInformation`` (data from
a cited source) or an ``AssumptionInformation`` (a modeling choice). Each
processing step appends its own entry. When the dataset is written, these
entries end up in a ``sources.md`` file next to the ``attributes.yaml`` of
each element, with full citations of every dataset involved.

Dependencies are resolved on demand
-----------------------------------

An attribute may read the value of another attribute, also of another element
(for example a retrofitting technology reading the lifetime of the technology it
retrofits). ZEN-creator builds the requested attribute first if it has not
been built yet, and detects cycles. There is no dependency graph to declare
by hand.

Datasets are loaded once
------------------------

Datasets and dataset collections are singletons: the first call constructs
and loads them, every later call returns the same object. A large source is
therefore read once per run, no matter how many elements use it.

Typed settings, one place per value
-----------------------------------

All choices that change the generated dataset are settings: typed fields
grouped in categories that the project defines. A misspelled setting or a
value of the wrong type is rejected before any data is read. A setting that
determines a ZEN-garden value (for example a region setting determining
``system.set_nodes``) is the only place where that value can be set.

Model variants are sparse patches
---------------------------------

A models file declares named variants of the dataset. Each variant only lists
the settings that differ from the defaults, and variants can extend each
other. All variants are generated from the same code.

Validation before writing
-------------------------

Attribute values, units and data frame indices are checked when they are set.
Before writing, the model checks that every carrier used by a technology
exists and that every scenario refers to an element of the model. A dataset
that violates these rules is not written.


Comparison with other approaches
================================

.. list-table::
   :header-rows: 1
   :widths: 22 26 26 26

   * -
     - Manual scripts
     - Snakemake
     - ZEN-creator
   * - Unit of work
     - Script that writes one or several files
     - Rule that turns input files into output files
     - Method that sets one attribute of one element
   * - Dependencies
     - Implicit, by execution order
     - Declared per rule through file names
     - Resolved automatically when an attribute reads another
   * - Intermediate results
     - Files, often untracked
     - Files on disk
     - Python objects in memory
   * - Provenance
     - Comments, if any
     - Rule and script names
     - Mandatory source or assumption entry per attribute, written to
       ``sources.md``
   * - Output structure
     - Written by hand, easy to break
     - Written by each rule
     - Written by ZEN-creator from the element classes, always a valid
       ZEN-garden input folder
   * - Validation
     - None or ad hoc
     - File existence
     - Types, units, indices, carrier consistency, scenario references
   * - Variants
     - Copies of scripts or folders
     - Config files and wildcards
     - Typed settings and sparse variants in a models file
   * - Scope of a change
     - Hard to predict
     - Rule level
     - One element or one dataset class

Advantages of this structure:

- **Readability.** The element file is a map of the data sources of that
  element. The dataset file contains everything about one source.
- **Collaboration.** Contributors work on separate files (one element, one
  source), which keeps changes small and reviews focused.
- **Reuse.** A dataset written once (for example inflation rates or a
  technology cost database) is available to every element and every project.
- **Consistency.** The output always follows the ZEN-garden input format,
  including units, file names and folder layout.
- **Traceability.** Every value in the dataset can be traced to a source or an
  explicit assumption.

Trade-offs:

- A workflow manager rebuilds only the outputs whose inputs changed.
  ZEN-creator rebuilds the full dataset in every run. Projects can cache
  expensive downloads, but the processing itself is repeated.
- The structure relies on conventions (naming, folder layout, one source per
  dataset), which each project documents for its contributors.
