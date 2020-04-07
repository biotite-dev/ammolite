import pymol
from pymol import cmd


def launch_pymol(no_startup_message=True, no_window=False,
                 no_internal_gui=False, no_external_gui=False,
                 explicit_cli_options=None):
    cli_command = ["pymol"]
    
    if explicit_cli_options is None:
        if no_startup_message:
            cli_command.append("-q")
        if no_window:
            cli_command.append("-c")
    else:
        cli_command.extend(explicit_cli_options)
    
    pymol.finish_launching(cli_command)
    
    # The selections only work properly,
    # if the order stays the same after adding a model to PyMOL
    cmd.set("retain_order", 1)