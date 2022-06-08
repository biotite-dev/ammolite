__name__ = "ammolite"
__author__ = "Patrick Kunzmann"
__all__ = ["draw_arrows"]

import numpy as np
from .cgo import draw_cgo, get_cylinder_cgo, get_cone_cgo


def draw_arrows(start, end, radius=0.1, head_radius=0.20,
                head_length=0.5, color=(0.5, 0.5, 0.5), head_color=None,
                name=None, pymol_instance=None):
    """
    Draw three-dimensional arrows using *Compiled Graphics Objects*
    (CGOs).

    Parameters
    ----------
    start, end : array-like, shape=(n,3)
        The start and end position of each arrow.
    radius, head_radius: float or array-like, shape=(n,), optional
        The radius of the tail and head for each arrow.
        Uniform for all arrows, if a single value is given.
    head_length: float or array-like, shape=(n,), optional
        The length of each arrow head.
        Uniform for all arrows, if a single value is given.
    color, head_color : array-like, shape=(3,) or shape=(n,3), optional
        The color of the tail and head for each arrow, given as RGB
        values in the range *(0, 1)*.
        Uniform for all arrows, if a single value is given.
        If no `head_color` is given, the arrows are single-colored.
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
    if head_color is None:
        head_color = color
    
    start = np.asarray(start)
    end = np.asarray(end)
    if start.ndim != 2 or end.ndim != 2:
        raise IndexError("Expected 2D array for start and end positions")
    if len(start) != len(end):
        raise IndexError(
            f"Got {len(start)} start positions, "
            f"but expected {len(end)} end positions"
        )
    expected_length = len(start)
    radius = _arrayfy(radius, expected_length, 1)
    head_radius = _arrayfy(head_radius, expected_length, 1)
    head_length = _arrayfy(head_length, expected_length, 1)
    color = _arrayfy(color, expected_length, 2)
    head_color = _arrayfy(head_color, expected_length, 2)
    
    normal = (end-start) / np.linalg.norm(end-start, axis=-1)[:, np.newaxis]
    middle = end - normal * head_length[:, np.newaxis]

    cgo_list = []
    for i in range(len(start)):
        cgo_list.extend([
            get_cylinder_cgo(
                start[i], middle[i], radius[i],
                color[i], color[i]
            ),
            get_cone_cgo(
                middle[i], end[i], head_radius[i], 0.0,
                head_color[i], head_color[i],
                True, False
            ),
        ])
    
    draw_cgo(cgo_list, name, pymol_instance)


def _arrayfy(value, length, min_dim):
    value = np.array(value, ndmin=min_dim)
    if len(value) == 1 and length > 1:
        value = np.repeat(value, length, axis=0)
    elif len(value) != length:
        raise IndexError(f"Expected {length} values, but got {len(value)}")
    return value