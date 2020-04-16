.. image:: static/assets/biotite2pymol_logo.svg
  :width: 300px
  :align: center

|

biotite2pymol - From Biotite to PyMOL and back again
====================================================

This package enables the transfer of structure related objects
from `Biotite <https://www.biotite-python.org/>`_
to `PyMOL <https://pymol.org/>`_ for visualization,
via PyMOL's Python API:

- Import :class:`AtomArray` and :class:`AtomArrayStack` objects into *PyMOL* -
  without intermediate structure files.
- Convert *PyMOL* objects into :class:`AtomArray` and :class:`AtomArrayStack`
  instances.
- Use *Biotite*'s boolean masks for atom selection in *PyMOL*.

|

.. image:: demo/demo.gif

|
|
|


Installation
------------

*biotite2pymol* can be installed via *pip*:

.. code-block:: console

  $ pip install biotite

However, PyMOL (at least version 2.0) must also be installed and needs to be
importable by your Python interpreter:

Installation via Conda
^^^^^^^^^^^^^^^^^^^^^^

The simplest and recommended way to install PyMOL in combination with
*biotite2pymol* is via the *Conda* package manager.
Either install the proprietary version with

.. code-block:: console

  $ conda install -c schrodinger pymol

or the free and open-source variant with

  $ conda install -c tpeulen pymol-open-source

Note that the open-source build is maintained by an individual, so it might
contain bugs or could not work at all for your system.

Installation from pymol.org
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Otherwise, if you have downloaded the PyMOL binary from
`<https://pymol.org/>`_, add the install location the `$PYTHONPATH` path
variable:

.. code-block:: console

  $ TODO

Note that this only works, if the Python version of your PyMOL2 installation
matches the version of your Python interpreter.

The correct installation of PyMOL can be checked by opening your Python
interpreter in interactive mode and typing

.. code-block:: python

  import pymol
  pymol.finish_launching(["pymol", "-qk"])

If no error shows up, the installation is correct.


Usage
-----


API Reference
-------------

