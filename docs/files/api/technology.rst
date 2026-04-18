Technology
==========

Overview
--------

``Technology`` is the common base for technology-type elements in the model.

Use Cases
---------

- Implement shared behavior across all technology subclasses.
- Extend with project-specific technology logic and attributes.

Examples
--------

.. code-block:: python

   from zen_creator import Technology

   # Typically extended in project-specific implementations.
   class MyTechnology(Technology):
       pass

.. rubric:: Summary

.. autosummary::
   :nosignatures:

   zen_creator.Technology.__init__

.. rubric:: Constructors

.. automethod:: zen_creator.Technology.__init__

.. rubric:: Member Reference

.. autoclass:: zen_creator.Technology
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: __init__
   :no-index: