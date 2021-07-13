.. image:: https://raw.githubusercontent.com/biotite-dev/ammolite/master/doc/static/assets/ammolite_logo_s.png
  :alt: Ammolite logo
  :align: center

Ammolite - From Biotite to PyMOL and back again
====================================================

This package enables the transfer of structure related objects
from `Biotite <https://www.biotite-python.org/>`_
to `PyMOL <https://pymol.org/>`_ for visualization,
via PyMOL's Python API:

- Import ``AtomArray`` and ``AtomArrayStack`` objects into *PyMOL* -
  without intermediate structure files.
- Convert *PyMOL* objects into ``AtomArray`` and ``AtomArrayStack`` instances.
- Use *Biotite*'s boolean masks for atom selection in *PyMOL*.
- Display images rendered with *PyMOL* in *Jupyter* notebooks.

Have a look at `this example <https://ammolite.biotite-python.org/examples/gallery/heme_complex.html>`_:

|

.. image:: https://raw.githubusercontent.com/biotite-dev/ammolite/master/doc/demo/demo.gif
    :alt: ammolite demo

|

*PyMOL is a trademark of Schrodinger, LLC.*
