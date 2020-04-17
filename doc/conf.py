# This source code is part of the Biotite package and is distributed
# under the 3-Clause BSD License. Please see 'LICENSE.rst' for further
# information.

__author__ = "Patrick Kunzmann"

from os.path import realpath, dirname, join, basename
import sys


# Include 'src/' in PYTHONPATH
# in order to import the 'biotite' package
doc_path = dirname(realpath(__file__))
package_path = join(dirname(doc_path), "src")
sys.path.insert(0, package_path)
import biotite2pymol


#### General ####

extensions = ["sphinx.ext.autodoc",
              "sphinx.ext.autosummary",
              "sphinx.ext.doctest",
              "sphinx.ext.mathjax",
              "sphinx.ext.viewcode",
              "numpydoc"]

templates_path = ["templates"]
source_suffix = [".rst"]
master_doc = "index"

project = "biotite2pymol"
copyright = "2020, the Biotite contributors. " \
            "PyMOL is a trademark of Schrodinger, LLC"
version = biotite2pymol.__version__

exclude_patterns = ["build"]

pygments_style = "sphinx"

todo_include_todos = False

# Prevents numpydoc from creating an autosummary which does not work
# properly due to Biotite's import system
numpydoc_show_class_members = False

autodoc_member_order = "bysource"


#### HTML ####

html_theme = "alabaster"
html_static_path = ["static"]
html_css_files = [
    "biotite.css",
    "https://fonts.googleapis.com/css?" \
        "family=Crete+Round|Fira+Sans|&display=swap",
]
html_favicon = "static/assets/biotite2pymol_icon_32p.png"
htmlhelp_basename = "Biotite2PymolDoc"
# No sidebar
html_sidebars = {"**": []}
html_theme_options = {
    "description"   : "From Biotite to PyMOL - and back again",
    "logo"          : "assets/biotite2pymol_logo.svg",
    "logo_name"     : "false",
    "github_user"   : "biotite-dev",
    "github_repo"   : "biotite2pymol",
    "github_banner" : "true",
}