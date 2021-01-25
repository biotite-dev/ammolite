import tempfile
import os
from os.path import isfile, join
import biotite.structure as struc
import biotite.structure.io.pdbx as pdbx
from ammolite import PyMOLObject, reset, cmd, launch_interactive_pymol
from .util import data_dir


def test_rendering():
    #reset()
    launch_interactive_pymol()
    pdbx_file = pdbx.PDBxFile.read(join(data_dir, "1l2y.cif"))
    structure = pdbx.get_structure(pdbx_file)
    structure.bonds = struc.connect_via_residue_names(structure)
    pymol_obj = PyMOLObject.from_structure(structure)
    
    PNG_SIZE = (100, 100)
    temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    #cmd.ray(*PNG_SIZE)
    import time
    time.sleep(0.1)
    cmd.png(temp_file.name, *PNG_SIZE, ray=1)

    assert isfile(temp_file.name)
    #os.remove(temp_file.name)