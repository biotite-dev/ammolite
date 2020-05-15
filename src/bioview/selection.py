__name__ = "bioview"
__author__ = "Patrick Kunzmann"
__all__ = ["select"]

import numpy as np


def select(object_name, mask):
    """
    Convert a boolean mask for atom selection into a *PyMOL* selection
    string.

    Parameters
    ----------
    object_name : str
        The name of the *PyMOL* object to select the atoms from.
        Usually this is the same name used in a previous
        :func:`to_pymol()` call, where the atom array (stack) the given
        `mask` corresponds to was transferred to *PyMOL*.
    mask : ndarray, dtype=bool
        The boolean mask to be converted into a selection string.
    
    Returns
    -------
    selection : str
        A *PyMOL* compatible selection string.
    """
    # Indices where the mask changes from True to False
    # or from False to True
    # The '+1' makes each index refer to the position after the change
    # i.e. the new value
    changes = np.where(np.diff(mask))[0] + 1
    # If first element is True, insert index 0 at start
    # -> the first change is always from False to True
    if mask[0]:
        changes = np.concatenate(([0], changes))
    # If the last element is True, insert append length of mask
    # as exclusive stop index
    # -> the last change is always from True to False
    if mask[-1]:
        changes = np.concatenate((changes, [len(mask)]))
    # -> Changes are alternating (F->T, T->F, F->T, ..., F->T, T->F)
    # Reshape into pairs of changes ([F->T, T->F], [F->T, T->F], ...)
    # -> these are the intervals where the mask is True
    intervals = np.reshape(changes, (-1, 2))

    # Convert interval into selection string
    # Two things to note:
    # - PyMOLs indexing starts at 1-> 'start+1'
    # - Stop index in 'intervals' is exclusive -> 'stop+1-1' -> 'stop'
    index_selection = " or ".join(
        [f"index {start+1}-{stop}" for start, stop in intervals]
    )
    # Constrain the selection to given object name
    complete_selection = f"model {object_name} and ({index_selection})"
    return complete_selection