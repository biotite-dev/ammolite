"""
Close the small PyMOL window at the end of all tests.
"""

from pymol import cmd


def pytest_addoption(parser):
    parser.addoption(
        "--keep-pymol", action="store_true",
        help="Keep the PyMOL window opened at the end of all tests"
    )

def pytest_unconfigure(config):
    if not config.getoption("--keep-pymol"):
        cmd.quit()