import glob
from os.path import join
import itertools
import numpy as np
import pytest
import biotite.structure as struc
import biotite.structure.io.pdbx as pdbx
from pymol import cmd
from ammolite import PyMOLObject, convert_to_chempy_model, reset
from .util import data_dir


@pytest.mark.parametrize(
    "path, altloc, state",
    itertools.product(
        glob.glob(join(data_dir, "*.cif")),
        ["first", "occupancy", "all"],
        # AtomArray or AtomArrayStack
        [1, None]
    )
)
def test_to_biotite(path, altloc, state):
    pdbx_file = pdbx.PDBxFile.read(path)
    ref_array = pdbx.get_structure(pdbx_file, model=state, altloc=altloc)
    
    reset()
    cmd.load(path, "test")
    test_array = PyMOLObject("test").to_structure(state=state, altloc=altloc)

    for cat in [
        c for c in ref_array.get_annotation_categories() if c != "altloc_id"
    ]:
        assert (
            test_array.get_annotation(cat) == ref_array.get_annotation(cat)
        ).all()
    assert np.allclose(test_array.coord, ref_array.coord)
    # Do not test bonds,
    # as PyMOL determines bonds in another way than Biotite


@pytest.mark.parametrize("path", glob.glob(join(data_dir, "*.cif")))
def test_to_pymol(path):
    reset()
    cmd.load(path, "test")
    ref_model = cmd.get_model("test", 1)
    
    pdbx_file = pdbx.PDBxFile.read(path)
    atom_array = pdbx.get_structure(
        pdbx_file, model=1,
        extra_fields=["b_factor", "occupancy", "charge"]
    )
    test_model = convert_to_chempy_model(atom_array)
    
    test_atoms = test_model.atom
    ref_atoms = [atom for atom in ref_model.atom if atom.alt in ("", "A")]
    assert len(test_atoms) == len(ref_atoms)
    for test_atom, ref_atom in zip(test_atoms, ref_atoms):
        assert test_atom.symbol == ref_atom.symbol
        assert test_atom.name == ref_atom.name
        assert test_atom.resn == ref_atom.resn
        assert test_atom.ins_code == ref_atom.ins_code
        assert test_atom.resi_number == ref_atom.resi_number
        assert test_atom.b == pytest.approx(ref_atom.b)
        assert test_atom.q == pytest.approx(ref_atom.q)
        assert test_atom.hetatm == ref_atom.hetatm
        assert test_atom.chain == ref_atom.chain
        assert test_atom.coord == pytest.approx(ref_atom.coord)
        # Charge information is not included in the CIF files
        #assert test_atom.formal_charge == ref_atom.formal_charge 


@pytest.mark.parametrize(
    "path, state",
    itertools.product(
        glob.glob(join(data_dir, "*.cif")),
        # AtomArray or AtomArrayStack
        [1, None]
    )
)
def test_both_directions(path, state):
    pdbx_file = pdbx.PDBxFile.read(path)
    ref_array = pdbx.get_structure(pdbx_file, model=state)
    ref_array.bonds = struc.connect_via_residue_names(ref_array)

    reset()
    test_array = PyMOLObject.from_structure(ref_array) \
                            .to_structure(state=state, include_bonds=True)
    
    for cat in ref_array.get_annotation_categories():
        assert (
            test_array.get_annotation(cat) == ref_array.get_annotation(cat)
        ).all()
    assert np.allclose(test_array.coord, ref_array.coord)
    
    # PyMOL does not distinguish between 'normal' and aromatic bonds
    test_array.bonds.remove_aromaticity()
    ref_array.bonds.remove_aromaticity()
    assert test_array.bonds.as_set() == ref_array.bonds.as_set()