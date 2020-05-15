from os.path import join
import numpy as np
import pytest
import biotite.structure as struc
import biotite.structure.io.pdbx as pdbx
from pymol import cmd
from ammolite import launch_pymol, select, to_biotite, to_pymol
from .util import data_dir, launch_pymol_for_test


SAMPLE_COUNT = 20
@pytest.mark.parametrize("random_seed", [i for i in range(SAMPLE_COUNT)])
def test_select(random_seed):
    pdbx_file = pdbx.PDBxFile.read(join(data_dir, "1l2y.cif"))
    array = pdbx.get_structure(pdbx_file, model=1)
    # Add bonds to avoid warning
    array.bonds = struc.connect_via_residue_names(array)
    
    launch_pymol_for_test()
    # Use B factor as indicator if the selection was correctly applied
    array.set_annotation("b_factor", np.zeros(array.array_length()))
    to_pymol("test", array)
    
    np.random.seed(random_seed)
    ref_mask = np.random.choice([False, True], array.array_length())
    
    # The function that is actually tested
    test_selection = select("test", ref_mask)
    # Set B factor of all masked atoms to 1
    cmd.alter(test_selection, "b=1.0")
    test_b_factor = to_biotite(
        "test", state=1, extra_fields=["b_factor"]
    ).b_factor
    # Get the mask from the occupancy back again
    test_mask = (test_b_factor == 1.0)

    assert np.array_equal(test_mask, ref_mask)