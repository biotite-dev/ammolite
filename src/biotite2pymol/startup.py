import pymol
from pymol import cmd


def launch_pymol(*args):
    pymol.finish_launching(["pymol"] + list(args))
    cmd.reinitialize()

    # The selections only work properly,
    # if the order stays the same after adding a model to PyMOL
    cmd.set("retain_order", 1)


def quit_pymol():
    cmd.quit()