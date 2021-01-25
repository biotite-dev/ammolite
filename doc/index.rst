.. image:: /static/assets/ammolite_logo.svg
  :height: 200px
  :align: center

|

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


.. toctree::
   :maxdepth: 1
   :hidden:
   
   install
   usage
   apidoc
   examples/gallery/index
   issues
