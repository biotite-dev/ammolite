.. image:: https://raw.githubusercontent.com/biotite-dev/bioview/master/doc/static/assets/bioview_logo_s.png
  :alt: Bioview logo
  :align: center

Bioview - From Biotite to PyMOL and back again
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

Have a look at the `example Jupyter notebook <https://github.com/biotite-dev/bioview/blob/master/doc/examples/cytochrome.ipynb>`_.

|

.. image:: https://raw.githubusercontent.com/biotite-dev/bioview/master/doc/demo/demo.gif
    :alt: bioview demo

|

*PyMOL is a trademark of Schrodinger, LLC.*
