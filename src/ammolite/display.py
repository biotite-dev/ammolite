__name__ = "ammolite"
__author__ = "Patrick Kunzmann"
__all__ = ["show", "TimeoutError"]

import tempfile
import time
import datetime
from os.path import join, getsize
from .startup import launch_pymol, _get_pymol, _set_pymol


INTERVAL = 0.1


def show(size=None, use_ray=False, timeout=60.0, pymol_instance=None):
    """
    Render an image of the PyMOL session and display it in the current
    *Jupyter* notebook.

    Note that this function works only in a *Jupyter* notebook.

    Parameters
    ----------
    size : tuple of (int, int), optional
        The width and height of the rendered image.
        By default, the size of the current *PyMOL* viewport is used.
    use_ray : bool, optional
        If set to true, the a ray-traced image is created.
        This will also increase the rendering time.
    timeout : float
        The number of seconds to wait for image output from *PyMOL*. 
    pymol_instance : module or SingletonPyMOL or PyMOL, optional
        If *PyMOL* is used in library mode, the :class:`PyMOL`
        or :class:`SingletonPyMOL` object is given here.
        If otherwise *PyMOL* is used in GUI mode, the :mod:`pymol`
        module is given.
        By default the currently used *PyMOL* instance
        (``ammolite.pymol``) is used.
        If no *PyMOL* instance is currently running,
        *PyMOL* is started in library mode.
    
    Raises
    ------
    TimeoutError
        If no image was created after expiry of the `timeout` limit.
    """
    try:
        from IPython.display import Image
    except ImportError:
        raise ImportError("IPython is not installed")

    if pymol_instance is None:
        pymol_instance = _get_pymol()
        if pymol_instance is None:
            # No PyMOL session has been started yet
            pymol_instance = launch_pymol()
            _set_pymol(pymol_instance)
    cmd = pymol_instance.cmd
    
    if size is None:
        width = 0
        height = 0
    else:
        width, height = size
    
    if use_ray:
        ray = 1
    else:
        ray = 0
    
    image_file = tempfile.NamedTemporaryFile(
        delete=False, prefix="ammolite_", suffix=".png"
    )
    image_file.close()
    
    start_time = datetime.datetime.now()

    cmd.png(image_file.name, width, height, ray=ray)
    
    while True:
        # After 'timeout' seconds the loop exits with an error
        if (datetime.datetime.now() - start_time).total_seconds() > timeout:
            raise TimeoutError(
                "No PNG image was output within the expected time limit"
            )
        
        # Check if PyMOL has already written image data to file
        if getsize(image_file.name) > 0:
            break

        time.sleep(INTERVAL)
    
    return Image(image_file.name)


class TimeoutError(Exception):
    """
    Exception that is raised after time limit expiry in :func:`show()`.
    """
    pass