import pymol
from pymol import cmd as default_cmd


def launch_pymol(*args):
    """
    Launch *PyMOL* with the given command line arguments.

    This is the recommended way to start *PyMOL* in GUI mode.
    It starts *PyMOL* by calling :func:`pymol.finish_launching()`,
    reinitializes *PyMOL* to clear the workspace and sets up necessary
    parameters using :func:`setup_parameters()`.
    """
    pymol.finish_launching(["pymol"] + list(args))
    default_cmd.reinitialize()
    setup_parameters()


def setup_parameters(pymol_instance=None):
    if pymol_instance is None:
        cmd = default_cmd
    else:
        cmd = pymol_instance.cmd
    
    # The selections only work properly,
    # if the order stays the same after adding a model to PyMOL
    cmd.set("retain_order", 1)