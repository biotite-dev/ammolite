from glob import glob
import shutil
import tempfile
import datetime
from os.path import getsize
from sphinx_gallery.scrapers import figure_rst

NO_ASSIGN = "___"


def pymol_scraper(block, block_vars, gallery_conf):
    block_type,_, _ = block
    if block_type == "code":
        globals = block_vars["example_globals"]
        # Look for replaced show() output:
        # a string representing a file name
        # Since this output is not assigned to any variable, it is
        # internally assigned to the '___' variable
        if NO_ASSIGN in globals and isinstance(globals[NO_ASSIGN], str):
            image_path = globals[NO_ASSIGN]
            # Copy the images into the 'gallery' directory under a canonical
            # sphinx-gallery name
            image_path_iterator = block_vars['image_path_iterator']
            image_destination = image_path_iterator.next()
            shutil.copy(image_path, image_destination)
            return figure_rst([image_destination], gallery_conf['src_dir'])
    return figure_rst([], gallery_conf['src_dir'])


def overwrite_display_func(gallery_conf, fname):
    import ammolite

    def show(size=None, use_ray=False, timeout=60.0, pymol_instance=None):
        INTERVAL = 0.1
        
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

        ammolite.cmd.png(image_file.name, width, height, ray=ray)
        
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
        
        return image_file.name

    ammolite.show = show
    ammolite.cmd.reinitialize()
    ammolite.setup_parameters(ammolite.pymol)