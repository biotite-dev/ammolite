__name__ = "biotite2pymol"
__author__ = "Patrick Kunzmann"
__all__ = ["select"]


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
    index_selection = " or ".join(
        [f"index {i+1}" for i, is_selected in enumerate(mask) if is_selected]
    )
    complete_selection = f"model {object_name} and ({index_selection})"
    return complete_selection