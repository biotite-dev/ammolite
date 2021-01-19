Installation
============

Conda installation
------------------

The simplest and recommended way to install *Ammolite* along with open-source
*PyMOL* is via the *Conda* package manager:

.. code-block:: console

  $ conda install -c conda-forge ammolite

If you prefer the proprietary version of *PyMOL*, you can install *PyMOL* via
*Conda* and *Ammolite* via *pip*.

.. code-block:: console

  $ conda install -c schrodinger pymol-bundle
  $ pip install ammolite


PyMOL installation from pymol.org
---------------------------------

Otherwise, if you have downloaded the *PyMOL* binary from
`<https://pymol.org/>`_, add the install location the ``$PYTHONPATH`` path
variable:

.. code-block:: console

  $ export PATH="/path/to/pymol/lib/python3.7/site-packages:$PATH"

or add the path directly in your Python script.

.. code-block:: python

  import sys
  sys.path.insert(0, "/path/to/pymol/lib/python3.x/site-packages")


Note that this only works, if the Python version of your *PyMOL* installation
matches the version of your Python interpreter.

The correct installation of *PyMOL* can be checked by opening your Python
interpreter in interactive mode and typing

.. code-block:: python

  import pymol
  pymol.finish_launching(["pymol", "-qk"])

If no error shows up, the installation is correct.