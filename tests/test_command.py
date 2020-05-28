from os.path import join
import numpy as np
import pytest
import biotite.structure as struc
import biotite.structure.io.pdbx as pdbx
from ammolite import PyMOLObject
from .util import data_dir, launch_pymol_for_test


pdbx_file = pdbx.PDBxFile.read(join(data_dir, "1l2y.cif"))
structure = pdbx.get_structure(pdbx_file)
mask = structure.res_id < 10
expr = "resi 1-10"


@pytest.mark.parametrize(
    "command_name, kwargs",
    [
        ("alter", {
            "selection": mask,
            "expression": "chain='B'",
        }),
        
        ("cartoon", {
            "type": "tube",
        }),
        ("cartoon", {
            "type": "tube",
            "selection": expr,
        }),
        ("cartoon", {
            "type": "tube",
            "selection": mask,
        }),
        
        ("center", {
        }),
        ("center", {
            "selection": mask,
            "state": 1,
            "origin": True,
        }),
        
        ("clip", {
            "mode": "near",
            "distance": 1.0,
            "state": 1,
        }),
        
        ("color", {
            "color": "green",
        }),
        ("color", {
            "color": (0.0, 1.0, 1.0),
        }),
        ("color", {
            "color": [0.0, 1.0, 1.0],
        }),
        
        # Not available in Open Source PyMOL
        #("desaturate", {
        #}),
        
        ("disable", {
        }),
        
        ("distance", {
            "name": "dist1",
            "selection1": mask,
            "selection2": mask,
            "mode": 4
        }),
        
        ("dss", {
        }),
        ("dss", {
            "state": 1
        }),
        
        ("hide", {
            "representation": "cartoon",
        }),
        
        ("indicate", {
        }),
        
        ("orient", {
        }),
        ("orient", {
            "state": 1,
        }),

        ("origin", {
        }),
        ("origin", {
            "state": 1,
        }),
        
        ("select", {
            "name": "selection1",
        }),
        
        ("set", {
            "name": "sphere_color",
            "value": "green",
        }),

        ("set_bond", {
            "name": "stick_color",
            "value": "green",
        }),
        
        ("show", {
            "representation": "sticks",
        }),

        ("show_as", {
            "representation": "sticks",
        }),
        
        ("smooth", {
        }),
        
        ("unset", {
            "name": "sphere_color",
        }),
        
        ("unset", {
            "name": "line_color",
        }),
        
        ("zoom", {
        }),
    ]
)
def test_command(command_name, kwargs):
    ###
    if command_name == "":
        return
    ###
    pdbx_file = pdbx.PDBxFile.read(join(data_dir, "1l2y.cif"))
    structure = pdbx.get_structure(pdbx_file)
    structure.bonds = struc.connect_via_residue_names(structure)
    launch_pymol_for_test()
    pymol_obj = PyMOLObject.from_structure(structure)
    command = getattr(PyMOLObject, command_name)
    command(pymol_obj, **kwargs)