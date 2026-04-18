.. _installation.installation:

############
Installation
############

.. note::
    This section is written for ZEN-creator users who want to install and use the
    package as a ready-to-run tool. If you want to modify the code or contribute
    changes, see the :ref:`installation guide for developers <dev_install.dev_install>`
    for instructions on how to work with the repository as a developer.

ZEN-creator is written in Python and is available as a package. You can install
the package via `pip <https://pypi.org/project/zen-creator/>`_ in a terminal or
command prompt.

We recommend working from a conda environment for the installation. If you have
not installed Anaconda, you can download it from the
`Anaconda website <https://docs.anaconda.com/anaconda/install/>`_.
For the general installer and beginner documentation of Python, please visit
`Python.org <https://www.python.org/about/gettingstarted/>`_.
You can check if you have Anaconda installed by running the following command in
a terminal (MacOS)/command prompt (Windows)

.. code:: shell

    conda --version

You can quickly create an environment with the command below. Here,
"zen-creator-env" is the name of the newly created environment:

.. code:: shell

    conda create -n zen-creator-env python==3.13
 
Activate the environment with the following command

.. code:: shell

    conda activate zen-creator-env

Now you can install the zen-creator package with the following command

.. code:: shell

        pip install zen-creator

To test whether the installation was successful, type:

.. code:: shell

    conda list
    
into the command prompt. This will print a list of all installed packages. You 
should see ``zen_creator`` in the list.


.. warning::
    ZEN-creator currently only supports Python versions 3.11 through 3.13.

.. warning::
    The directory in which you install Anaconda should not contain any blank 
    spaces in its file path. Otherwise, the installation of ZEN-creator might
    fail.

.. _installation.activate:

Activate Conda environment
==========================

After installing ZEN-creator, you need to activate the ZEN-creator environment 
each time you open a new terminal. To activate the environment, type

.. code:: shell

    conda activate zen-creator-env  

into the terminal in which you would like to run ZEN-creator. At any time, you 
can deactivate the environment by typing: 

.. code:: shell

    conda deactivate

