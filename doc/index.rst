.. include:: logo.rst

Ammolite - From Biotite to PyMOL and back again
===============================================

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
  :target: _images/demo.gif

|

.. contents::
   :depth: 2

|
|
|


Installation
------------

Conda installation
^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

|

Usage
-----

.. currentmodule:: ammolite


Launching PyMOL
^^^^^^^^^^^^^^^

Library mode
""""""""""""

The recommended way to invoke *PyMOL* in a Python script depends on whether a
GUI should be displayed.
If no GUI is required, we recommend launching a *PyMOL* session in library
mode.

.. code-block:: python

  import ammolite

  ammolite.launch_pymol()

Usually launching *PyMOL* manually via :func:`launch_pymol()` is not even
necessary:
When *Ammolite* requires a *PyMOL* session, e.g. for creating a *PyMOL* object
or invoking a command, and none is already running, *PyMOL* is automatically
started in library mode.

GUI mode
""""""""

When the *PyMOL* GUI is necessary, the *PyMOL* library mode is not
available.
Instead *PyMOL* can be launched in interactive (GUI) mode:

.. code-block:: python

  import ammolite

  ammolite.launch_interactive_pymol("-qixkF", "-W", "400", "-H", "400")

:func:`launch_interactive_pymol()` starts *PyMOL* using the given command
line options, reinitializes it and sets necessary parameters.

After that, the usual *PyMOL* commands and the other functions from
*Ammolite* are available.

Note that the *PyMOL* window will stay open after the end of the script.
This can lead to issues when using interactive Python (e.g. *IPython*):
The *PyMOL* window could not be closed by normal means and a forced
termination might be necessary.
This can be solved by using *PyMOL*'s integrated command line for executing
Python.

Launching PyMOL directly
""""""""""""""""""""""""

.. note::
  
  This is not the recommended way to use *Ammolite*.
  Usage is at your own risk. 

You can also *PyMOL* directly using the *PyMOL* Python API, that
:func:`launch_pymol()` and :func:`launch_interactive_pymol()` use internally.
In this case, it is important to call :func:`setup_parameters()` for setting
parameters that are necessary for *Ammolite* to interact properly with *PyMOL*.
Furthermore, the ``pymol_instance`` parameter must be set the first time
a :class:`PyMOLObject` is created to inform *Ammolite* about the *PyMOL*
session.

.. code-block:: python

  from pymol2 import PyMOL
  import ammolite

  pymol_app = PyMOL()
  pymol_app.start()
  ammolite.setup_parameters(pymol_instance=pymol_app)
  cmd = pymol_app.cmd
  
  pymol_object = ammolite.PyMOLObject.from_structure(
      atom_array, pymol_instance=pymol_app
  )

|

Transferring structures from Biotite to PyMOL and vice versa
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A *Biotite* :class:`AtomArray` or :class:`AtomArrayStack` can be converted into
a *PyMOL* object via :meth:`PyMOLObject.from_structure()`.
This static method returns a :class:`PyMOLObject` - a wrapper around a
*PyMOL* object (alias *PyMOL* model).
This wrapper becomes invalid when atoms are added to or are deleted from the
wrapped *PyMOL* object or if the underlying *PyMOL* object does not exist
anymore.

Conversely, :meth:`PyMOLObject.to_structure()` converts a :class:`PyMOLObject`
object back into an :class:`AtomArray` or :class:`AtomArrayStack`.

.. code-block:: python

  # From Biotite to PyMOL...
  pymol_object = ammolite.PyMOLObject.from_structure(atom_array)
  # ...and back again
  second_atom_array = pymol_object.to_structure()

If you need to convert a *PyMOL* object, that was created or loaded within
*PyMOL* you can create a :class:`PyMOLObject` via its constructor.

.. code-block:: python

  pymol_object = PyMOLObject("Name_of_the_object")
  atom_array = pymol_object.to_structure()

Internally, :meth:`PyMOLObject.from_structure()` calls
:func:`convert_to_chempy_model`, that converts the :class:`AtomArray` into a
*PyMOL* :class:`chempy.models.Indexed` model at first.
Then the model is added to the *PyMOL* session using the :func:`load_model`
command.
:meth:`to_structure()` obtains the model via the :func:`get_model()` command
and converts it into an :class:`AtomArray` via :func:`convert_to_atom_array`.

|

Atom selections
^^^^^^^^^^^^^^^

*PyMOL* uses selection expressions (strings) to select atoms for its commands.
On the other side, *Biotite* uses boolean masks from *NumPy*.
These boolean masks can be converted into selection expressions via the
:meth:`PyMOLObject.where()` method.

.. code-block:: python

  pymol_object = ammolite.PyMOLObject.from_structure(atom_array)
  ca_selection = pymol_object.where(atom_array.atom_name == "CA")

|

Invoking commands
^^^^^^^^^^^^^^^^^

*PyMOL* commands can be called as usual:
The current *PyMOL* session is obtained via ``ammolite.pymol`` and commands
can be invoked using ``ammolite.cmd``.

.. code-block:: python
  
  ammolite.cmd.set("sphere_scale", 1.5)

But additionally, boolean masks can be used instead of *PyMOL*'s selection
expressions via the :meth:`PyMOLObject.where()` method.

.. code-block:: python
  
  pymol_object = ammolite.PyMOLObject.from_structure(atom_array)
  # Instead of this...
  ammolite.cmd.show_as("sticks", "resi 42")
  # ...this can also be used
  ammolite.cmd.show_as("sticks", pymol_object.where(atom_array.res_id == 42))

To add syntactic sugar, common commands are available as :class:`PyMOLObject`
methods.
These methods accept boolean masks directly, without the need to call
:meth:`PyMOLObject.where()`.

.. code-block:: python

  pymol_object = ammolite.PyMOLObject.from_structure(atom_array)
  pymol_object.show_as("sticks", atom_array.res_id == 42)

When no selection is given, these methods are applied all atoms from the
respective *PyMOL* object.

The following commands are supported as instance methods:

- :meth:`PyMOLObject.alter()`
- :meth:`PyMOLObject.cartoon()`
- :meth:`PyMOLObject.center()`
- :meth:`PyMOLObject.clip()`
- :meth:`PyMOLObject.color()`
- :meth:`PyMOLObject.desaturate()`
- :meth:`PyMOLObject.disable()`
- :meth:`PyMOLObject.distance()`
- :meth:`PyMOLObject.dss()`
- :meth:`PyMOLObject.enable()`
- :meth:`PyMOLObject.hide()`
- :meth:`PyMOLObject.indicate()`
- :meth:`PyMOLObject.label()`
- :meth:`PyMOLObject.orient()`
- :meth:`PyMOLObject.origin()`
- :meth:`PyMOLObject.select()`
- :meth:`PyMOLObject.set()`
- :meth:`PyMOLObject.set_bond()`
- :meth:`PyMOLObject.show()`
- :meth:`PyMOLObject.show_as()`
- :meth:`PyMOLObject.smooth()`
- :meth:`PyMOLObject.unset()`
- :meth:`PyMOLObject.unset_bond()`
- :meth:`PyMOLObject.zoom()`

|

Jupyter notebook support
^^^^^^^^^^^^^^^^^^^^^^^^

*Jupyter* notebooks can directly display images rendered by *PyMOL* via
:func:`show()` (not to be confused with :meth:`PyMOLObject.show()`).

|

Examples
--------

`A few examples are provided as Jupyter notebooks. <https://github.com/biotite-dev/ammolite/tree/master/doc/examples>`_

|

API Reference
-------------

.. toctree::
  :maxdepth: 2

  startup
  model
  convert
  display
