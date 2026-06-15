Carrier
=======

Overview
--------

``Carrier`` represents energy carriers used across technologies and system
components in a model.

Use Cases
---------

- Define or customize carrier behavior in a project-specific subclass.
- Store carrier-related attributes used by technologies and validation logic.

Examples
--------

The code below shows an example of how to implement a subclass of the
``Carrier`` abstract class. Please read the docstrings
carefully as they contain detailed information on required methods and
syntax.

.. literalinclude:: ../../../zen_creator/elements/carriers/aa_template.py
   :language: python

.. rubric:: Summary

.. autosummary::
   :nosignatures:

   zen_creator.Carrier.__init__

.. rubric:: Constructors

.. automethod:: zen_creator.Carrier.__init__

.. rubric:: Member Reference

.. autoclass:: zen_creator.Carrier
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __init__
   :no-index: