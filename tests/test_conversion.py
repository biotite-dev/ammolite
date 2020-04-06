import glob
from os.path import join
import itertools
import numpy as np
import pytest
import biotite.structure as struc
import biotite.structure.io.pdbx as pdbx
from biotite2pymol import launch, select, \
                          set_model, get_model, convert_to_atom_array
from .util import data_dir, unique_model_name


@pytest.mark.parametrize(
    "path, state",
    itertools.product(
        glob.glob(join(data_dir, "1l2y.cif")),
        # AtomArray or AtomArrayStack
        [1, None]
    )
)
def test_conversions_both_dir(path, state):
    pdbx_file = pdbx.PDBxFile()
    pdbx_file.read(path)
    ref_array = pdbx.get_structure(pdbx_file, model=state)
    ref_array.bonds = struc.connect_via_residue_names(ref_array)

    #launch(no_window=True)
    launch()
    model_name = unique_model_name()
    set_model(model_name, ref_array)
    test_array = get_model(model_name, state, include_bonds=True)
    
    for cat in ref_array.get_annotation_categories():
        assert (
            test_array.get_annotation(cat) == ref_array.get_annotation(cat)
        ).all()
    assert np.allclose(test_array.coord, ref_array.coord)
    assert test_array.bonds == ref_array.bonds