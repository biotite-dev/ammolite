import sys
import biotite
import biotite.structure as struc
import biotite.structure.io as strucio
from biotite2pymol import set_model, select
import pymol
from pymol import cmd as pymol_cmd


def test_general():
    array = strucio.load_structure(
        "/home/kunzmann/Documents/coding/biotite/tests/structure/data/1l2y.mmtf",
        model=1
    )

    #pymol.finish_launching(["pymol", "-qix"])
    #pymol.finish_launching(["pymol", "-qc"])
    pymol.finish_launching(["pymol", "-q"])

    set_model("test", array)
    selection = select("test", (array.res_id == 1) | (array.res_id > 15))
    print()
    print(selection)

    pymol_cmd.color("red", selection)
    pymol_cmd.zoom()
    pymol_cmd.ray(300, 200)
    pymol_cmd.png('test.png')
    pymol_cmd.zoom()
    print()
    print("Success")
    #import time
    #time.sleep(20)
    raise ValueError("Errs")