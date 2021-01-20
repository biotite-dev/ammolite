"""
Ampicillin as ball-and-stick model
==================================

This example shows a *ball-and-stick* model of the beta-lactam antibiotic
ampicillin.
"""

import biotite.structure as struc
import biotite.structure.info as info
import ammolite


PNG_SIZE = (600, 600)


ampicillin = info.residue("AIC")

pymol_obj = ammolite.PyMOLObject.from_structure(ampicillin)
ammolite.show(PNG_SIZE)
