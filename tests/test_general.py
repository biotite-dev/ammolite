import sys
import numpy as np
import biotite
import biotite.structure as struc
import biotite.structure.io as strucio
import biotite.structure.io.mmtf as mmtf
from biotite2pymol import set_model, get_model, select, convert_to_atom_array
import pymol
from pymol import cmd



def test_both_conversions():
    ref_array = strucio.load_structure(
        "/home/kunzmann/Documents/coding/biotite/tests/structure/data/1l2y.mmtf",
        model=1,
        include_bonds=True
    )

    pymol.finish_launching(["pymol", "-qc"])
    set_model("test", ref_array)
    test_array = get_model("test", include_bonds=True)

    for cat in ref_array.get_annotation_categories():
        assert (
            test_array.get_annotation(cat) == ref_array.get_annotation(cat)
        ).all()
    assert np.allclose(test_array.coord, ref_array.coord)
    assert test_array.bonds == ref_array.bonds



def test_general():
    array = strucio.load_structure(
        "/home/kunzmann/Documents/coding/biotite/tests/structure/data/1l2y.mmtf",
        model=1,
        include_bonds=True
    )
    ###
    #mmtf_file = mmtf.MMTFFile()
    #mmtf_file.read("/home/kunzmann/Documents/coding/biotite/tests/structure/data/1l2y.mmtf")
    #for group in mmtf_file["groupList"]:
    #    if group["groupName"] == "ASN":
    #        print(group)
    #        print()
    #        for i in range(len(group["bondAtomList"])//2):
    #            print(group["bondAtomList"][2*i], group["bondAtomList"][2*i+1])
    #        print()
    ###
    ###
    #arg = array[(array.res_id == 1)]
    #print(arg)
    #print()
    #for i, j, _ in arg.bonds.as_array():
    #    print(arg.atom_name[i], arg.atom_name[j])
    #array = arg
    ###


    #pymol.finish_launching(["pymol", "-qix"])
    #pymol.finish_launching(["pymol", "-qc"])
    pymol.finish_launching(["pymol", "-q"])

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
    #array.bonds.add_bond(0, 8, 1)
    #array.bonds.add_bond(0, 10, 1)
    #extra_bonds = array2.bonds.as_set() - array.bonds.as_set()
    #assert array.bonds == array2.bonds
    print()
    print("Success")
    #import time
    #time.sleep(20)


if __name__ == "__main__":
    test_both_conversions()