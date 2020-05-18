__name__ = "ammolite"
__author__ = "Patrick Kunzmann"
__all__ = ["PyMOLObject", "NonexistentObjectError", "ModifiedObjectError"]

from functools import wraps
import numpy as np
import biotite.structure as struc
from pymol import cmd as default_cmd
from .convert import convert_to_atom_array, convert_to_chempy_model


def validate(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._check_existence()
        new_atom_count = self._cmd.count_atoms(f"model {self._name}")
        if new_atom_count != self._atom_count:
            raise ModifiedObjectError(
                f"The number of atoms in the object changed "
                f"from the original {self._atom_count} atoms "
                f" to {new_atom_count} atoms"
            )
        return method(self, *args, **kwargs)
    return wrapper


class PyMOLObject:
    """
    A wrapper around a *PyMOL object* (*PyMOL model*), usually created
    by the static :meth:`from_structure()` method.

    This class is primarily used to create *PyMOL* selection strings
    from boolean masks of an corresponding :class:`AtomArray` or
    :class:`AtomArrayStack` via the :meth:`where()`.
    Additionally, objects of this class provide wrapper methods for
    common *PyMOL* commands (e.g. ``show()`` or ``color()``), that
    directly support boolean masks for the ``selection`` parameter.

    Instances of this class become invalid, when atoms are added to or
    are deleted from the underlying *PyMOL* object.
    Calling methods of such an an invalidated object raises an
    :exc:`ModifiedObjectError`.
    Likewise, calling methods of an object, of which the underlying
    *PyMOL* object does not exist anymore, raises an
    :exc:`NonexistentObjectError`.

    Parameters
    ----------
    name : str
        The name of the *PyMOL* object.
    pymol_instance : PyMOL, optional
        When using the object-oriented *PyMOL* API the :class:`PyMOL`
        object must be given here.
    delete : PyMOL, optional
        If set to true, the underlying *PyMOL* object will be removed
        from the *PyMOL* session,
        when this object is garbage collected.
    
    Attributes
    ----------
    name : str
        The name of the *PyMOL* object.
    """
    
    _object_counter = 0
    _color_counter = 0
    

    def __init__(self, name, pymol_instance=None, delete=True):
        self._name = name
        self._pymol = pymol_instance
        self.delete = delete
        if pymol_instance is None:
            self._cmd = default_cmd
        else:
            self._cmd = pymol_instance.cmd
        self._check_existence()
        self._atom_count = self._cmd.count_atoms(f"model {self._name}")

    def __del__(self):
        self._cmd.delete(self._name)



    @staticmethod
    def from_structure(atoms, name=None, pymol_instance=None, delete=True):
        """
        Create a :class:`PyMOLObject` from an :class:`AtomArray` or
        :class:`AtomArrayStack` and add it to the *PyMOL* session.

        Parameters
        ----------
        atoms : AtomArray or AtomArrayStack
            The structure to be converted.
        name : str, optional
            The name of the newly created *PyMOL* object.
            If omitted, a unique name is generated.
        pymol_instance : PyMOL, optional
            When using the object-oriented *PyMOL* API the :class:`PyMOL`
            object must be given here.
        delete : PyMOL, optional
            If set to true, the underlying *PyMOL* object will be removed
            from the *PyMOL* session, when this object is garbage collected.
        """
        if pymol_instance is None:
            cmd = default_cmd
        else:
            cmd = pymol_instance.cmd
        
        if name is None:
            name = f"ammolite_obj_{PyMOLObject._object_counter}"
            PyMOLObject._object_counter += 1
        
        if isinstance(atoms, struc.AtomArray) or \
        (isinstance(atoms, struc.AtomArrayStack) and atoms.stack_depth == 1):
                model = convert_to_chempy_model(atoms)
                cmd.load_model(model, name)
        elif isinstance(atoms, struc.AtomArrayStack):
            # Use first model as template
            model = convert_to_chempy_model(atoms[0])
            cmd.load_model(model, name)
            # Append states corresponding to all following models
            for coord in atoms.coord[1:]:
                cmd.load_coordset(coord, name)
        else:
            raise TypeError("Expected 'AtomArray' or 'AtomArrayStack'")

        return PyMOLObject(name, pymol_instance, delete)

    def to_structure(self, state=None, altloc="all", extra_fields=None,
                     include_bonds=False):
        """
        Convert this object into an :class:`AtomArray` or
        :class:`AtomArrayStack`.

        Parameters
        ----------
        state : int, optional
            If this parameter is given, the function will return an
            :class:`AtomArray` corresponding to the given state of the
            *PyMOL* object.
            If this parameter is omitted, an :class:`AtomArrayStack`
            containing all states will be returned, even if the *PyMOL*
            object contains only one state.
        altloc : {'first', 'occupancy', 'all'}
            This parameter defines how *altloc* IDs are handled:
                - ``'first'`` - Use atoms that have the first
                  *altloc* ID appearing in a residue.
                - ``'occupancy'`` - Use atoms that have the *altloc* ID
                  with the highest occupancy for a residue.
                - ``'all'`` - Use all atoms.
                  Note that this leads to duplicate atoms.
                  When this option is chosen, the ``altloc_id``
                  annotation array is added to the returned structure.
        extra_fields : list of str, optional
            The strings in the list are optional annotation categories
            that should be stored in the output atom array (stack).
            ``'b_factor'``, ``'occupancy'`` and``'charge'`` are valid
            values.
        include_bonds : bool, optional
            If set to true, an associated :class:`BondList` will be created
            for the returned atom array (stack).
        
        Returns
        -------
        structure : AtomArray or AtomArrayStack
            The converted structure.
            Wheather an :class:`AtomArray` or :class:`AtomArrayStack` is
            returned depends on the `state` parameter.
        """
        if state is None:
            model = self._cmd.get_model(self._name, state=1)
            template = convert_to_atom_array(
                model, altloc, extra_fields, include_bonds
            )
            expected_length = None
            coord = []
            for i in range(self._cmd.count_states(self._name)):
                state_coord = self._cmd.get_coordset(self._name, state=i+1)
                if expected_length is None:
                    expected_length = len(state_coord)
                elif len(state_coord) != expected_length:
                    raise ValueError(
                        "The models have different numbers of atoms"
                    )
                coord.append(state_coord)
            coord = np.stack(coord)
            return struc.from_template(template, coord)
        else:
            model = self._cmd.get_model(self._name, state=state)
            return convert_to_atom_array(
                model, altloc, extra_fields, include_bonds
            )


    
    @property
    def name(self):
        return self._name
    

    def exists(self):
        return self._name in self._cmd.get_object_list()

    def _check_existence(self):
        if not self.exists():
            raise NonexistentObjectError(
                f"A PyMOL object with the name {self._name} "
                f"does not exist anymore"
            )


    @validate
    def where(self, mask):
        """
        Convert a boolean mask for atom selection into a *PyMOL*
        selection string.

        Parameters
        ----------
        mask : ndarray, dtype=bool
            The boolean mask to be converted into a selection string.
        
        Returns
        -------
        selection : str
            A *PyMOL* compatible selection string.
        """
        if len(mask) != self._atom_count:
            raise IndexError(
                f"Mask has length {len(mask)}, but the number of atoms in the "
                f"PyMOL model is {atom_count}"
            )

        # Indices where the mask changes from True to False
        # or from False to True
        # The '+1' makes each index refer to the position after the change
        # i.e. the new value
        changes = np.where(np.diff(mask))[0] + 1
        # If first element is True, insert index 0 at start
        # -> the first change is always from False to True
        if mask[0]:
            changes = np.concatenate(([0], changes))
        # If the last element is True, insert append length of mask
        # as exclusive stop index
        # -> the last change is always from True to False
        if mask[-1]:
            changes = np.concatenate((changes, [len(mask)]))
        # -> Changes are alternating (F->T, T->F, F->T, ..., F->T, T->F)
        # Reshape into pairs of changes ([F->T, T->F], [F->T, T->F], ...)
        # -> these are the intervals where the mask is True
        intervals = np.reshape(changes, (-1, 2))

        # Convert interval into selection string
        # Two things to note:
        # - PyMOLs indexing starts at 1-> 'start+1'
        # - Stop index in 'intervals' is exclusive -> 'stop+1-1' -> 'stop'
        index_selection = " or ".join(
            [f"index {start+1}-{stop}" for start, stop in intervals]
        )
        # Constrain the selection to given object name
        complete_selection = f"model {self._name} and ({index_selection})"
        return complete_selection


    # TODO: def alter()
    # TODO: def cartoon()
    # TODO: def center()
    # TODO: def clip()
    # TODO: def color()
    # TODO: def desaturate()
    # TODO: def disable()
    # TODO: def distance()
    # TODO: def dss()
    # TODO: def enable()
    # TODO: def hide()
    # TODO: def indicate()
    # TODO: def orient()
    # TODO: def origin()
    # TODO: def select()
    # TODO: def set()
    # TODO: def set_bond()
    # TODO: def show()
    # TODO: def show_as()
    # TODO: def smooth()
    # TODO: def spectrum()
    # TODO: def unset()
    # TODO: def unset_bond()
    # TODO: def valence()
    # TODO: def zoom()



class NonexistentObjectError(Exception):
    pass

class ModifiedObjectError(Exception):
    pass