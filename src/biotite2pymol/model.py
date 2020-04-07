import re
import numpy as np
import biotite
from biotite.sequence import ProteinSequence
import biotite.structure as struc
import biotite.structure.io as strucio
import pymol
from pymol import cmd
from chempy.models import Indexed as IndexedModel
from chempy import Atom, Bond


def to_biotite(object_name, state=None, extra_fields=None,
               include_bonds=False):
    if state is None:
        model = cmd.get_model(object_name, state=1)
        template = convert_to_atom_array(model, extra_fields, include_bonds)
        coord = np.stack(
            [cmd.get_coordset(object_name, state=i+1)
             for i in range(cmd.count_states(object_name))]
        )
        return struc.from_template(template, coord)
    else:
        model = cmd.get_model(object_name, state=state)
        return convert_to_atom_array(model, extra_fields, include_bonds)


def to_pymol(object_name, atoms):
    if isinstance(atoms, struc.AtomArray) or \
       (isinstance(atoms, struc.AtomArrayStack) and atoms.stack_depth == 1):
            model = convert_to_chempy_model(atoms)
            cmd.load_model(model, object_name)
    elif isinstance(atoms, struc.AtomArrayStack):
        # Use first model as template
        model = convert_to_chempy_model(atoms[0])
        cmd.load_model(model, object_name)
        # Append states corresponding to all following models
        for coord in atoms.coord[1:]:
            cmd.load_coordset(coord, object_name)
    else:
        raise TypeError("Expected 'AtomArray' or 'AtomArrayStack'")


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
        [a.resi_number for a in atoms],
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


def convert_to_chempy_model(atom_array):
    model = IndexedModel()

    annot_cat = atom_array.get_annotation_categories()


    for i in range(atom_array.array_length()):
        atom = Atom()

        atom.segi = atom_array.chain_id[i]
        atom.chain = atom_array.chain_id[i]

        atom.resi_number = atom_array.res_id[i]

        atom.ins_code = atom_array.ins_code[i]
        
        res_name = atom_array.res_name[i]
        atom.resn = res_name
        if len(res_name) == 1:
            atom.resn_code = res_name
        else:
            try:
                atom.resn_code = ProteinSequence.convert_letter_3to1(res_name)
            except KeyError:
                atom.resn_code = "X"

        atom.hetatm = 1 if atom_array.hetero[i] else 0

        atom.name = atom_array.atom_name[i]

        atom.symbol = atom_array.element[i]
        
        if "b_factor" in annot_cat:
            atom.b = atom_array.b_factor[i]
        
        if "occupancy" in annot_cat:
            atom.q = atom_array.occupancy[i]
        
        if "charge" in annot_cat:
            atom.formal_charge = atom_array.charge[i]
        
        atom.coord = tuple(atom_array.coord[..., i, :])

        atom.index = i+1

        model.add_atom(atom)
    

    if atom_array.bonds is not None:
        for i, j, order in atom_array.bonds.as_array():
            bond = Bond()

            if order != 0:
                bond.order = order
            else:
                # If bond order is not defined,
                # use a single bond as default
                bond.order = 1
            
            bond.index = [i, j]

            model.add_bond(bond)
    

    return model