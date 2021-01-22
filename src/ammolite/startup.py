__name__ = "ammolite"
__author__ = "Patrick Kunzmann"
__all__ = ["launch_pymol", "launch_interactive_pymol", "reset",
           "setup_parameters", "DuplicatePyMOLException"]


_pymol = None

def _get_pymol():
    return _pymol

def _set_pymol(pymol):
    _pymol = pymol


def is_launched():
    """
    Check whether a *PyMOL* session is already running.

    Returns
    -------
    running : bool
        True, if a *PyMOL* instance is already running, false otherwise.
    """
    return _pymol is not None


def launch_pymol():
    """
    Launch *PyMOL* in object-oriented library mode.

    This is the recommended way to launch *PyMOL* if no GUI is
    required.
    This function simply creates a :class:`SingletonPyMOL` object,
    calls its :func:`start()` method and sets up necessary parameters using
    :func:`setup_parameters()`.

    Parameters
    ----------
    *args : str
        The command line options given to *PyMOL*.
    
    Returns
    -------
    pymol : SingletonPyMOL
        The started *PyMOL* instance.
        *PyMOL* commands can be invoked by using its :attr:`cmd`
        attribute.
    """
    from pymol2 import SingletonPyMOL
    global _pymol

    if _pymol is not None:
        raise DuplicatePyMOLException(
            "A PyMOL instance is already running"
        )
    else:
        _pymol = SingletonPyMOL()
        _pymol.start()
        setup_parameters(_pymol)
    return _pymol


def launch_interactive_pymol(*args):
    """
    Launch a *PyMOL* GUI with the given command line arguments.

    It starts *PyMOL* by calling :func:`pymol.finish_launching()`,
    reinitializes *PyMOL* to clear the workspace and sets up necessary
    parameters using :func:`setup_parameters()`.

    Parameters
    ----------
    *args : str
        The command line options given to *PyMOL*.
    
    Returns
    -------
    pymol : module
        The :mod:`pymol` module.
        *PyMOL* commands can be invoked by using its :attr:`cmd`
        attribute.
    """
    import pymol
    global _pymol

    if _pymol is not None:
        if _pymol is not pymol:
            raise DuplicatePyMOLException(
                "PyMOL is already running in library mode"
            )
        else:
            raise DuplicatePyMOLException(
                "A PyMOL instance is already running"
            )
    else:
        pymol.finish_launching(["pymol"] + list(args))
        _pymol = pymol
        pymol.cmd.reinitialize()
        setup_parameters(_pymol)
    return pymol


def reset():
    """
    Delete all objects in the PyMOL workspace and reset parameters to
    defaults.

    If *PyMOL* is not yet running, launch *PyMOL* in object-oriented
    library mode.
    """
    global _pymol

    if _pymol is None: 
        _pymol = launch_pymol()
    _pymol.cmd.reinitialize()
    setup_parameters(_pymol)


def setup_parameters(pymol_instance):
    """
    Sets *PyMOL* parameters that are necessary for *ammolite* to interact
    properly with *PyMOL*.

    pymol_instance : module or SingletonPyMOL or PyMOL, optional
        If *PyMOL* is used in library mode, the :class:`PyMOL`
        or :class:`SingletonPyMOL` object is given here.
        If otherwise *PyMOL* is used in GUI mode, the :mod:`pymol`
        module is given.
    """
    # The selections only work properly,
    # if the order stays the same after adding a model to PyMOL
    pymol_instance.cmd.set("retain_order", 1)


class DuplicatePyMOLException(Exception):
    pass