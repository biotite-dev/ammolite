__name__ = "ammolite"
__author__ = "Patrick Kunzmann"
__all__ = ["draw_cgo", "get_cylinder_cgo", "get_cone_cgo", "get_sphere_cgo"]

import itertools
import numpy as np
from .startup import get_and_set_pymol_instance


_object_counter = 0


def draw_cgo(cgo_list, name=None, pymol_instance=None):
    """
    Draw geometric shapes using *Compiled Graphics Objects* (CGOs).

    Each CGO is represented by a list of floats, which can be obtained
    via the ``get_xxx_cgo()`` functions.

    Parameters
    ----------
    cgo_list : list of list of float
        The CGOs to draw.
        It is recommended to use a ``get_xxx_cgo()`` function to obtain
        the elements for this list, if possible.
        Otherwise, shapes may be drawn incorrectly or omitted entirely,
        if a CGO is incorrectly formatted.
    name : str, optional
        The name of the newly created CGO object.
        If omitted, a unique name is generated.
    pymol_instance : module or SingletonPyMOL or PyMOL, optional
        If *PyMOL* is used in library mode, the :class:`PyMOL`
        or :class:`SingletonPyMOL` object is given here.
        If otherwise *PyMOL* is used in GUI mode, the :mod:`pymol`
        module is given.
        By default the currently used *PyMOL* instance
        (``ammolite.pymol``) is used.
        If no *PyMOL* instance is currently running,
        *PyMOL* is started in library mode.
    """
    global _object_counter
    if name is None:
        name = f"ammolite_cgo_{_object_counter}"
        _object_counter += 1
    pymol_instance = get_and_set_pymol_instance(pymol_instance)
    pymol_instance.cmd.load_cgo(list(itertools.chain(*cgo_list)), name)


def get_cylinder_cgo(start, end, radius, start_color, end_color):
    """
    Get the CGO for a cylinder.

    Parameters
    ----------
    start, end : array-like, shape=(3,)
        The start and end position of the cylinder.
    radius : float
        The radius of the cylinder
    start_color, end_color : array-like, shape=(3,)
        The color at the start and end of the cylinder given as RGB
        values in the range *(0, 1)*.
    """
    CYLINDER = 9.0
    _expect_length(start, "start", 3)
    _expect_length(end, "end", 3)
    _expect_length(start_color, "start_color", 3)
    _expect_length(end_color, "end_color", 3)
    _check_color(start_color)
    _check_color(end_color)
    return [
        CYLINDER, *start, *end, radius, *start_color, *end_color
    ]

def get_cone_cgo(start, end, start_radius, end_radius,
                  start_color, end_color, start_cap, end_cap):
    """
    Get the CGO for a cone.

    Parameters
    ----------
    start, end : array-like, shape=(3,)
        The start and end position of the cone.
    start_radius, end_radius : float
        The radius of the cone at the start and end.
    start_color, end_color : array-like, shape=(3,)
        The color at the start and end of the cone given as RGB
        values in the range *(0, 1)*.
    start_cap, end_cap : bool
        If true, a cap is drawn at the start or end of the cone.
        Otherwise the cone is displayed as *open*.
    """
    CONE = 27.0
    _expect_length(start, "start", 3)
    _expect_length(end, "end", 3)
    _expect_length(start_color, "start_color", 3)
    _expect_length(end_color, "end_color", 3)
    _check_color(start_color)
    _check_color(end_color)
    return [
        CONE, *start, *end, start_radius, end_radius, *start_color, *end_color,
        float(start_cap), float(end_cap)
    ]

def get_sphere_cgo(pos, radius, color):
    """
    Get the CGO for a sphere.

    Parameters
    ----------
    pos : array-like, shape=(3,)
        The position of the sphere.
    radius : float
        The radius of the sphere.
    color : array-like, shape=(3,)
        The color of the sphere given as RGB values in the range
        *(0, 1)*.
    """
    COLOR = 6.0
    SPHERE = 7.0
    _expect_length(pos, "pos", 3)
    _expect_length(color, "color", 3)
    _check_color(color)
    return [
        COLOR, *color, SPHERE, *pos, radius
    ]


def _expect_length(values, name, length):
    if len(values) != length:
        raise IndexError(
            f"'{name}' has {len(values)} values, but {length} were expected"
        )


def _check_color(color):
    if np.any(color) < 0 or np.any(color) > 1:
        raise ValueError("Colors must be in range (0, 1)")