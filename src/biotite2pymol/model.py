import warnings
import numpy as np
import biotite
from biotite.sequence import ProteinSequence
import biotite.structure as struc
import biotite.structure.io as strucio
import pymol
from pymol import cmd as default_cmd
from chempy.models import Indexed as IndexedModel
from chempy import Atom, Bond


def to_biotite(object_name, state=None, extra_fields=None,
               include_bonds=False, pymol_instance=None):
    """
    Convert a *PyMOL* object into an :class:`AtomArray` or
    :class:`AtomArrayStack`.

    Parameters
    ----------
    object_name : str
        The name of the *PyMOL* object to be converted.
    state : int, optional
        If this parameter is given, the function will return an
        :class:`AtomArray` corresponding to the given state of the
        *PyMOL* object.
        If this parameter is omitted, an :class:`AtomArrayStack`
        containing all states will be returned, even if the *PyMOL*
        object contains only one state.
    extra_fields : list of str, optional
        The strings in the list are optional annotation categories
        that should be stored in the output atom array (stack).
        ``'b_factor'``, ``'occupancy'`` and``'charge'`` are valid
        values.
    include_bonds : bool, optional
        If set to true, an associated :class:`BondList` will be created
        for the returned atom array (stack).
    pymol_instance : PyMOL, optional
        When using the object-oriented *PyMOL* API the :class:`PyMOL`
        object must be given here.
    
    Returns
    -------
    structure : AtomArray or AtomArrayStack
        The converted structure.
        Wheather an :class:`AtomArray` or :class:`AtomArrayStack` is
        returned depends on the `state` parameter.
    """
    if pymol_instance is None:
        cmd = default_cmd
    else:
        cmd = pymol_instance.cmd
    
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


def to_pymol(object_name, atoms, pymol_instance=None):
    """
    Convert an :class:`AtomArray` or :class:`AtomArrayStack` into a
    *PyMOL* object and add it to the *PyMOL* session.

    Parameters
    ----------
    object_name : str
        The name of the newly created *PyMOL* object.
    atoms : AtomArray or AtomArrayStack
        The structure to be converted.
    pymol_instance : PyMOL, optional
        When using the object-oriented *PyMOL* API the :class:`PyMOL`
        object must be given here.
    """
    if pymol_instance is None:
        cmd = default_cmd
    else:
        cmd = pymol_instance.cmd
    
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
    """
    Convert a :class:`chempy.models.Indexed`
    object into an :class:`AtomArray`.

    Parameters
    ----------
    chempy_model : Indexed
        The ``chempy`` model.
    extra_fields : list of str, optional
        The strings in the list are optional annotation categories
        that should be stored in the output atom array.
        ``'b_factor'``, ``'occupancy'`` and``'charge'`` are valid
        values.
    include_bonds : bool, optional
        If set to true, an associated :class:`BondList` will be created
        for the returned atom array.
    
    Returns
    -------
    atom_array : AtomArray
        The converted structure.
    """
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
    """
    Convert an :class:`AtomArray` into a :class:`chempy.models.Indexed`
    object.

    Returns
    -------
    chempy_model : Indexed
        The converted structure.
    """
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
    else:
        warnings.warn(
            "The given atom array (stack) has no associated bond information"
        )
    

    return model