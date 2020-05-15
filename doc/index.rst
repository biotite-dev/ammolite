.. image:: static/assets/bioview_logo.svg
  :height: 200px
  :align: center

|

Bioview - From Biotite to PyMOL and back again
====================================================

This package enables the transfer of structure related objects
from `Biotite <https://www.biotite-python.org/>`_
to `PyMOL <https://pymol.org/>`_ for visualization,
via *PyMOL*'s Python API:

- Import :class:`AtomArray` and :class:`AtomArrayStack` objects into *PyMOL* -
  without intermediate structure files.
- Convert *PyMOL* objects into :class:`AtomArray` and :class:`AtomArrayStack`
  instances.
- Use *Biotite*'s boolean masks for atom selection in *PyMOL*.
- Display images rendered with *PyMOL* in *Jupyter* notebooks.

|

.. image:: demo/demo.gif

|

.. contents::
   :depth: 2

|
|
|


Installation
------------

*Bioview* can be installed via *pip*:

.. code-block:: console

  $ pip install bioview

However, *PyMOL* (at least version 2.0) must also be installed and needs to be
importable by your Python interpreter:

Installation via Conda
^^^^^^^^^^^^^^^^^^^^^^

The simplest and recommended way to install *PyMOL* in combination with
*Bioview* is via the *Conda* package manager.
Either install the proprietary version with

.. code-block:: console

  $ conda install -c schrodinger pymol

or the free and open-source variant with

  $ conda install -c tpeulen pymol-open-source

Note that the open-source build is maintained by an individual, so it might
contain bugs or could not work at all for your system.

Installation from pymol.org
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Otherwise, if you have downloaded the *PyMOL* binary from
`<https://pymol.org/>`_, add the install location the `$PYTHONPATH` path
variable:

.. code-block:: console

  $ TODO

Note that this only works, if the Python version of your *PyMOL* installation
matches the version of your Python interpreter.

The correct installation of *PyMOL* can be checked by opening your Python
interpreter in interactive mode and typing

.. code-block:: python

  import pymol
  pymol.finish_launching(["pymol", "-qk"])

If no error shows up, the installation is correct.


Usage
-----

.. currentmodule:: bioview

Launching PyMOL
^^^^^^^^^^^^^^^

The recommended way to invoke *PyMOL* in a Python script depends on whether a
GUI should be displayed.
If no GUI is required, we recommend using object-oriented *PyMOL*.

.. code-block:: python

  from pymol2 import PyMOL
  from bioview import setup_parameters

  pymol_app = PyMOL()
  pymol_app.start()
  setup_parameters(pymol_instance=pymol_app)
  cmd = pymol_app.cmd
  
  # The molecule visualization stuff goes here

  pymol_app.stop()

The line with ``pymol_app.start()`` is essential here:
Without this statement the following commands to *PyMOL* might lead to
crashes.
:func:`setup_parameters()` sets *PyMOL* parameters that are necessary for
*Bioview* to interact properly with *PyMOL*.

.. autofunction:: setup_parameters

For further demonstrations, on how to use object-oriented *PyMOL* with
interactive Python in combination with *Bioview*, have a look at
the `example Jupyter notebooks <https://github.com/biotite-dev/bioview/tree/master/doc/examples>`_.

|

When the *PyMOL* GUI is necessary, the object-oriented *PyMOL* API is not
available.
Instead *PyMOL* can be launched in the following way:

.. code-block:: python

  from pymol import cmd
  from bioview import launch_pymol

  launch_pymol("-qixkF", "-W", "400", "-H", "400")

  # The molecule visualization stuff goes here

:func:`launch_pymol()` starts *PyMOL* using the given command line options,
reinitializes it and sets necessary parameters.

.. autofunction:: launch_pymol

After that, the usual *PyMOL* commandos and the other functions from
*Bioview* are available.

Note that the *PyMOL* window will stay open after the end of the script.
This can lead to issues when using interactive Python (e.g. *IPython*):
The *PyMOL* window could not be closed by normal means and a forced
termination might be necessary.
This can be solved by using *PyMOL*'s integrated command line for executing
Python.

Transfer objects from Biotite to PyMOL and vice versa
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After *PyMOL* initialization, a *Biotite* :class:`AtomArray` or
:class:`AtomArrayStack` can be converted to *PyMOL* objects via
:func:`to_pymol()`.
Conversely, :func:`to_biotite()` converts a *PyMOL* object into an
:class:`AtomArray` or :class:`AtomArrayStack`.

.. autofunction:: to_pymol

.. autofunction:: to_biotite

Internally, :func:`to_pymol()` converts the :class:`AtomArray` is into a
*PyMOL* :class:`chempy.models.Indexed` model at first.
Then the model is added to the *PyMOL* session using the
:func:`load_model` command.
:func:`to_pymol()` obtains the model via the :func:`get_model()` command
and converts it into an :class:`AtomArray`.
These two internal conversion functions are also available:

.. autofunction:: convert_to_chempy_model

.. autofunction:: convert_to_atom_array

Atom selections
^^^^^^^^^^^^^^^

*PyMOL* uses selection strings to select atoms for its command.
On the other side, *Biotite* uses boolean masks from *NumPy*.
These boolean masks can be converted into selection strings via the
:func:`select()` function.

.. autofunction:: select

Jupyter notebook support
^^^^^^^^^^^^^^^^^^^^^^^^

*Jupyter* notebooks can directly display images rendered by *PyMOL* via
:func:`show()`.

.. autofunction:: show


Examples
--------

`A few examples are provided as Jupyter notebooks. <https://github.com/biotite-dev/bioview/tree/master/doc/examples>`_