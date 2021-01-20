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

########################################################################

ampicillin = info.residue("AIC")

pymol_obj = ammolite.PyMOLObject.from_structure(ampicillin)
ammolite.show(PNG_SIZE)

########################################################################

ammolite.cmd.orient()
ammolite.cmd.zoom(buffer=2.0)
ammolite.show(PNG_SIZE)

########################################################################

pymol_obj.show("spheres")
pymol_obj.color("black", ampicillin.element == "C")
ammolite.cmd.set("stick_radius", 0.15)
ammolite.cmd.set("sphere_scale", 0.25)
ammolite.cmd.set("sphere_quality", 4)
ammolite.cmd.set("stick_color", "grey80")
ammolite.show(PNG_SIZE)
# sphinx_gallery_thumbnail_number = 3