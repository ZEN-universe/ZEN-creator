compare_trees
=============

Overview
--------

``compare_trees`` compares two directory trees and reports differences.

Use Cases
---------

- Validate generated model outputs against a baseline input tree.
- Inspect structural and file-content changes between two model versions.

Examples
--------

.. code-block:: python

   from pathlib import Path
   from zen_creator import compare_trees

   compare_trees(Path("./baseline"), Path("./candidate"))

.. rubric:: API Reference

.. autofunction:: zen_creator.compare_trees
   :no-index: