"""
Contact sites of protein-DNA interaction
========================================

This script identifies which amino acids of the phage 434 repressor are
in contact with its corresponding DNA operator.
*In contact* is defined as a pairwise atom distance below a given
threshold (in this case 4.0 Å).

The identified contact residues are highlighted as sticks. 
"""

# Code source: Patrick Kunzmann
# License: BSD 3 clause

import numpy as np
import biotite.structure as struc
import biotite.structure.io.mmtf as mmtf
import biotite.database.rcsb as rcsb
from biotite2pymol import launch_pymol, select, to_pymol
from pymol import cmd


# The maximum distance between an atom in the repressor and an atom in
# the DNA for them to be considered 'in contact'
THRESHOLD_DISTANCE = 4.0


# Fetch and load structure
mmtf_file = mmtf.MMTFFile()
mmtf_file.read(rcsb.fetch("2or1", "mmtf"))
structure = mmtf.get_structure(mmtf_file, model=1, include_bonds=True)
structure = structure[structure.res_name != "HOH"]


# Separate structure into the DNA and the two identical protein chains
dna = structure[
    np.isin(structure.chain_id, ["A", "B"]) & (structure.hetero == False)
]
protein_l = structure[
    (structure.chain_id == "L") & (structure.hetero == False)
]
protein_r = structure[
    (structure.chain_id == "R") & (structure.hetero == False)
]
# Quick check if the two protein chains are really identical
assert len(struc.get_residues(protein_l)) == len(struc.get_residues(protein_r))


# Fast identification of contacts via a cell list:
# The cell list is initiliazed with the coordinates of the DNA
# and later provided with the atom coordinates of the two protein chains
cell_list = struc.CellList(dna, cell_size=THRESHOLD_DISTANCE)

# Sets to store the residue IDs of contact residues
# for each protein chain
id_set_l = set()
id_set_r = set()

for protein, res_id_set in zip((protein_l, protein_r), (id_set_l, id_set_r)):
    # For each atom in the protein chain,
    # find all atoms in the DNA that are in contact with it
    contacts = cell_list.get_atoms(protein.coord, radius=THRESHOLD_DISTANCE)
    # Only retain atoms in the protein with contact
    # to at least one atom of the DNA
    contact_indices = np.where((contacts != -1).any(axis=1))[0]
    # Get residue IDs for the atoms in the protein
    contact_res_ids = protein.res_id[contact_indices]
    # Put the residue IDs into the set,
    # duplicate IDs are automatically removed in this process
    res_id_set.update(contact_res_ids)

# Only consider residues that show contacts in both peptide chains
# -> intersection of sets
common_ids = sorted(id_set_l & id_set_r)



launch_pymol("-qxF", "-W", "1000", "-H", "1000")

# Load structure in PyMOL
to_pymol("test", structure)

# Define colors
cmd.set_color("biotite_brightorange", [255/255, 181/255, 105/255])
cmd.set_color("biotite_dimorange",    [220/255, 112/255,   0/255])
cmd.set_color("biotite_lightgreen",   [111/255, 222/255,  76/255])
cmd.set_color("biotite_darkgreen",    [ 56/255, 154/255,  26/255])

# Set overall colors
cmd.color("gray", select("test", np.isin(structure.chain_id, ["A","B"])))
cmd.color("biotite_brightorange", select("test", structure.chain_id == "L"))
cmd.color("biotite_lightgreen", select("test", structure.chain_id == "R"))

# Highlight contacts
id_mask = np.isin(structure.res_id, common_ids)
cmd.show("sticks", select(
    "test",
    id_mask & np.isin(structure.chain_id, ["L", "R"])
))
for chain, color in zip(
    ("L", "R"),
    ("biotite_dimorange", "biotite_darkgreen")
):
    cmd.color(color, select(
        "test",
        id_mask & (structure.chain_id == chain) & (structure.atom_name != "CA")
    ))

# Save image
#cmd.ray(1000, 550)
#cmd.png("contact_sites.png")
