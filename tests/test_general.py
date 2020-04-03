import sys
import numpy as np
import biotite
import biotite.structure as struc
import biotite.structure.io as strucio
import biotite.structure.io.mmtf as mmtf
from biotite2pymol import set_model, select
import pymol
from pymol import cmd
from chempy.models import Indexed as Model
from chempy import Atom, Bond




def test_general():
    array = strucio.load_structure(
        "/home/kunzmann/Documents/coding/biotite/tests/structure/data/1l2y.mmtf",
        model=1,
        include_bonds=True
    )


    #pymol.finish_launching(["pymol", "-qix"])
    pymol.finish_launching(["pymol", "-qc"])
    #pymol.finish_launching(["pymol", "-q"])

    set_model("test", array)
    selection = select("test", (array.res_id == 1) | (array.res_id > 15))

    cmd.color("red", selection)
    cmd.zoom()
    model = cmd.get_model("test")
    cmd.load_model(model, "test2")
    #cmd.ray(300, 200)
    #cmd.png('test.png')
    #cmd.zoom()
    print("\n" * 5)
    array2 = convert_to_atom_array(model, include_bonds=True)
    for cat in array.get_annotation_categories():
        assert (array.get_annotation(cat) == array2.get_annotation(cat)).all()
    assert np.allclose(array.coord, array2.coord)
    array.bonds.add_bond(0, 8, 1)
    array.bonds.add_bond(0, 10, 1)
    print(array2.bonds.as_set() - array.bonds.as_set())
    assert array.bonds == array2.bonds
    print()
    print("Success")
    #import time
    #time.sleep(20)


if __name__ == "__main__":
    def convert_to_atom_array(chempy_model, extra_fields=None, 
                              include_bonds=False):
        if extra_fields is None:
            extra_fields = []
        
        
        atoms = chempy_model.atom
        # Ignore alternative locations
        atoms = [atom for atom in atoms if atom.alt in ("", "A")]

        bonds = chempy_model.bond

        
        atom_array = struc.AtomArray(len(atoms))
        
        
        atom_array.chain_id = np.array(
            [a.chain for a in atoms],
            dtype="U3"
        )
        atom_array.res_id = np.array(
            [a.resi for a in atoms],
            dtype=int
        )
        atom_array.ins_code = np.array(
            [a.ins_code for a in atoms],
            dtype="U1"
        )
        atom_array.res_name = np.array(
            [a.resn for a in atoms],
            dtype="U3"
        )
        atom_array.hetero = np.array(
            [a.hetatm for a in atoms],
            dtype=bool
        )
        atom_array.atom_name = np.array(
            [a.name for a in atoms],
            dtype="U6"
        )
        atom_array.element = np.array(
            [a.symbol for a in atoms],
            dtype="U2"
        )
        
        if "b_factor" in extra_fields:
            atom_array.b_factor = np.array(
                [a.b for a in atoms],
                dtype=float
            )
        if "occupancy" in extra_fields:
            atom_array.occupancy = np.array(
                [a.q for a in atoms],
                dtype=float
            )
        if "charge" in extra_fields:
            atom_array.charge = np.array(
                [a.formal_charge for a in atoms],
                dtype=int
            )
        

        atom_array.coord = np.array(
            [a.coord for a in atoms],
            dtype=np.float32
        )


        if include_bonds:
            bond_array = np.array(
                [[b.index[0], b.index[1], b.order] for b in bonds],
                dtype=np.uint32
            )
            atom_array.bonds = struc.BondList(len(atoms), bond_array)
        

        return atom_array

    
    test_general()