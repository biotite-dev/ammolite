import tempfile
from os.path import join
import pymol
from pymol import cmd as default_cmd


def show(size=None, use_ray=False, pymol_instance=None):
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
    
    ###
    cmd.png("temp.png", width, height, ray=ray)
    import time
    time.sleep(1)
    
    return Image("temp.png")
    ###
    
    image_file = tempfile.NamedTemporaryFile(
        delete=False, prefix="biotite2pymol", suffix=".png"
    )
    image_file.close()
    cmd.png(image_file.name, width, height, ray=ray)
    import time
    time.sleep(5)
    image = Image(image_file.name)
    
    return image