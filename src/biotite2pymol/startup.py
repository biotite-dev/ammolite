import pymol
from pymol import cmd


def launch_pymol(options):
    if isinstance(options, str):
        options = [options]
    pymol.finish_launching(["pymol"] + options)
    cmd.reinitialize()

    # The selections only work properly,
    # if the order stays the same after adding a model to PyMOL
    cmd.set("retain_order", 1)


def quit_pymol():
    cmd.quit()