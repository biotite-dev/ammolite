Common issues
=============

As *PyMOL* is a quite complex software with a lot of its functionality written
in *C++*, sometimes unexpected results or crashes may occur under certain
circumstances.
This page should provide help in such and similar cases.


Interactive PyMOL crashes when launched after usage of Matplotlib
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Interactive *PyMOL* will crash, if it is launched after a *Matplotlib* figure
is created. This does not happen in the object-oriented library mode of
*PyMOL*.
Presumably the reason is a conflict in the *OpenGL* contexts.

Example code that leads to crash:

.. code-block:: python

  import matplotlib.pyplot as plt
  import ammolite

  figure = plt.figure()
  ammolite.launch_interactive_pymol()


'cmd.png()' command crashes in pytest function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*PyTest* executes the test functions via ``exec()``, which might lead to the
crash.
Up to now the only way to prevent this, is not to test the ``png()`` command
in pytest.


Launching PyMOL for the first time raises DuplicatePyMOLException
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For example the code snippet

.. code-block:: python

  from ammolite import cmd, launch_pymol
  
  launch_pymol()

raises

.. code-block:: python

  ammolite.DuplicatePyMOLException: A PyMOL instance is already running

The reason:

If ``from ammolite import pymol`` or ``from ammolite import cmd``
is called, *PyMOL* is already launched upon import in order to make
the ``pymol`` or ``cmd`` attribute available.
Subsequent calls of :func:`launch_pymol()` or
:func:`launch_interactive_pymol()` would start a second *PyMOL* session,
which is forbidden.

To circumvent this problem do not import ``pymol`` or ``cmd`` from
``ammolite``, but access these attributes via ``ammolite.pymol`` or
``ammolite.cmd`` at the required places in your code.