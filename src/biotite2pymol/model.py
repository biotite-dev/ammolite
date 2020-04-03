import biotite
import biotite.structure as struc
import biotite.structure.io as strucio
import pymol
from pymol import cmd


def set_model(model_name, atoms):
    temp_file_name = biotite.temp_file("cif")
    strucio.save_structure(temp_file_name, atoms)
    cmd.load(temp_file_name, model_name)


def convert_to_atom_array(chempy_model):
    print(type(chempy_model))


def convert_to_chempy_model(atom_array):
    pass