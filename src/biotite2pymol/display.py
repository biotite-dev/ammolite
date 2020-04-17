import tempfile
import time
import datetime
from os.path import join, getsize
import pymol
from pymol import cmd as default_cmd


INTERVAL = 0.1


def show(size=None, use_ray=False, pymol_instance=None, timeout=60):
    try:
        from IPython.display import Image
    except ImportError:
        raise ImportError("IPython is not installed")

    if pymol_instance is None:
        cmd = default_cmd
    else:
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
        delete=False, prefix="biotite2pymol", suffix=".png"
    )
    image_file.close()
    
    start_time = datetime.datetime.now()

    cmd.png(image_file.name, width, height, ray=ray)
    
    while True:
        # After 'timeout' seconds the loop exits with an error
        if (datetime.datetime.now() - start_time).total_seconds() > timeout:
            raise TimeoutError(
                "No PNG image was output within the expected time"
            )
        
        # Check if PyMOL has already written image data to file
        if getsize(image_file.name) > 0:
            break

        time.sleep(INTERVAL)
    
    return Image(image_file.name)


def TimeoutError(Exception):
    pass