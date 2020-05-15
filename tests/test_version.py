import re
from os.path import join, dirname, realpath
from bioview import __version__


def test_version():
    pyproject_file_path = join(
        dirname(dirname(realpath(__file__))),
        "pyproject.toml"
    )
    with open(pyproject_file_path) as file:
        lines = file.read().splitlines()
    
    ref_version = None
    for line in lines:
        if line.lstrip().startswith("version"):
            version_match = re.search('".*"', line)
            if version_match:
                # Remove quotes
                ref_version = version_match.group(0)[1 : -1]
    if ref_version is None:
        raise ValueError("No version is specified in 'pyproject.toml'")

    assert __version__ == ref_version
