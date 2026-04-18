.. _contributing.contributing:

########################
Contribution Guide
########################

Thank you for your interest in contributing to ZEN-creator! 🎉  
Community contributions are highly appreciated and help improve the project.

Before submitting changes, please read the following guidelines.  
There are several ways to contribute:

* :ref:`Reporting bugs or suggesting new features <contributing.issues>`
* :ref:`Modifying the code <contributing.code>`
* :ref:`Improving docstrings and comments <contributing.coding_rules>`
* :ref:`Writing tests <contributing.tests>`


.. _contributing.issues:

Reporting Bugs or Suggesting Features
=====================================

If you discover a bug, have a feature request, or want to suggest an improvement,
please create an issue in the 
`GitHub repository <https://github.com/ZEN-universe/ZEN-creator/issues>`_.

When creating an issue, please follow these guidelines:

* Use a **short and descriptive title**
* Provide enough detail to clearly describe the issue or feature
* For bugs, include a **minimal working example** that reproduces the problem
* Select the appropriate **issue type** (e.g., bug, enhancement, documentation)


.. _contributing.code:

Editing Code in ZEN-creator
===========================

GitHub Workflow
---------------

All contributions follow the **fork-and-pull request workflow**.

1. Fork the repository to your personal GitHub account.
2. Clone your fork locally.
3. Create a new branch for your changes:

.. code:: shell

    git checkout -b <feature_name>

4. Implement your changes.
5. Run formatting, linting, type checking, and tests locally.
6. Submit a **Pull Request (PR)** from your fork to the upstream repository.

.. note::
  
   Contributors **must not create branches directly on the upstream repository**.
   All development should take place in personal forks.


.. _contributing.coding_rules:

Coding Standards
----------------

ZEN-creator follows the `PEP 8 <https://peps.python.org/pep-0008/>`_ 
Python style guide with a few project-specific conventions.

**General naming rules:**

* Classes: PascalCase (first letter capitalized)
* Functions and methods: lowercase_with_underscores
* Variables: lowercase_with_underscores
* Files: lowercase_with_underscores
* Folders: lowercase_with_underscores

**Documentation:**

* All classes must include a clear docstring
* Public methods should include *Google-style docstrings*
* Keep docstrings and comments aligned with the style in this guide

**Comments:**

* Place comments above the code they describe
* Use comments to explain *why*, not *what*

**Files:**

* Each file should include a short header describing its purpose.

**Project-specific deviation from PEP-8:**

* Maximum line length: 88 characters


.. _contributing.format:

Code Formatting
---------------

All Python code must be formatted using *Black* before submitting a pull 
request.

To format the code, run the following command in the repository root:

.. code:: shell

    black .

Pull requests that do not follow the formatting rules may not be merged.


.. _contributing.lint:

Linting
-------

All code must pass linting checks using *Ruff*.

Run the following command in the repository root:

.. code:: shell

    ruff check .

Please resolve all reported issues before submitting a pull request.

Some issues can be fixed automatically:

.. code:: shell

    ruff check . --fix


.. _contributing.type_checking:

Type Checking
-------------

All code must pass type checking using *Mypy*.

Run the following command in the repository root:

.. code:: shell

    mypy .

Please resolve all reported issues before submitting a pull request.

.. _contributing.tests:

Testing
-------

All contributions should include tests when behavior changes.

Run the test suite from the repository root:

.. code:: shell

    pytest

If you add or modify logic, add or update the corresponding unit tests.

.. _contributing.branch_protections:

Branch Protection Rules
-----------------------

The **main branch** of ZEN-creator is protected to ensure code quality and 
stability.

The following rules apply:

1. **All changes must be submitted via pull request**

   Direct pushes to the main branch are not allowed.

2. **Pull requests must be up to date**

   If your branch is outdated, update it by merging or rebasing with 
   the latest version of the main branch.

3. **All tests must pass**

    GitHub Actions automatically runs the ZEN-creator test suite.
    All tests must pass before the pull request can be merged.

4. **Code quality checks must pass**

   The **Black** formatter and **Ruff** linter must not report any issues.


.. _contributing.merge:

Merging Pull Requests (Administrators Only)
-------------------------------------------

Pull requests can only be merged by ZEN-creator administrators.

According to the :ref:`branch protection rules <contributing.branch_protections>`,
a pull request can only be merged if:

* All automated tests pass
* Code quality checks pass
* The pull request is up to date with the main branch
