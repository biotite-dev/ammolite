from os.path import join
import numpy as np
import pytest
import biotite.structure as struc
import biotite.structure.io.pdbx as pdbx
from ammolite import PyMOLObject, launch_interactive_pymol
from .util import data_dir



def test_interactive_pymol_launch():
    """
    Simply check that PyMOL does not crash and no exception is raised.
    """
    launch_interactive_pymol("-qixkF", "-W", "100", "-H", "100")
    pdbx_file = pdbx.PDBxFile.read(join(data_dir, "1l2y.cif"))
    structure = pdbx.get_structure(pdbx_file)
    structure.bonds = struc.connect_via_residue_names(structure)
    pymol_obj = PyMOLObject.from_structure(structure)