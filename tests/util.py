# This source code is part of the Biotite package and is distributed
# under the 3-Clause BSD License. Please see 'LICENSE.rst' for further
# information.

import os.path
import pymol
from pymol import cmd
from biotite2pymol import launch_pymol


def launch_pymol_for_test():
    # Do not use script-only interface (-c),
    # as this extremely slows down the tests
    launch_pymol(["-qixF", "-W", "100", "-H", "100"])


data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")