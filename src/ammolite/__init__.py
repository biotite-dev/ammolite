# This source code is part of the Biotite package and is distributed
# under the 3-Clause BSD License. Please see 'LICENSE.rst' for further
# information.

"""
Visualize structure data from Biotite with PyMOL.
"""

__version__ = "0.6.0"
__name__ = "ammolite"
__author__ = "Patrick Kunzmann"

from .convert import *
from .display import *
from .object import *
from .startup import *
from .startup import _get_pymol, _set_pymol


# Make the PyMOL instance accessible via `ammolite.pymol`
# analogous to a '@property' of a class, but on module level instead
def __getattr__(name):
    if name == "pymol":
        _pymol = _get_pymol()
        if _pymol is None:
            # No PyMOL session has been started yet
            _pymol = launch_pymol()
            _set_pymol(_pymol)
        return _pymol
    elif name == "cmd":
        return __getattr__("pymol").cmd
    elif name in list(globals().keys()):
        return globals()["name"]
    else:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

def __dir__():
    return list(globals().keys()) + ["pymol", "cmd"]