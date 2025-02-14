# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import errno
import os
import shutil
import subprocess
import sys

from natsort import natsorted
from recommonmark.parser import CommonMarkParser

sys.path.insert(0, os.path.abspath("../../"))

repodir = os.path.abspath(os.path.join(__file__, r"../../.."))
gitdir = os.path.join(repodir, r".git")

# -- Project information -----------------------------------------------------

project = "Merlin Core"
copyright = "2022, NVIDIA"  # pylint: disable=redefined-builtin
author = "NVIDIA"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_multiversion",
    "sphinx_rtd_theme",
    "recommonmark",
    "sphinx_markdown_tables",
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

source_parsers = {".md": CommonMarkParser}
source_suffix = [".rst", ".md"]

if os.path.exists(gitdir):
    tag_refs = subprocess.check_output(["git", "tag", "-l", "v*"]).decode("utf-8").split()
    tag_refs = natsorted(tag_refs)[-6:]
    smv_tag_whitelist = r"^(" + r"|".join(tag_refs) + r")$"
else:
    smv_tag_whitelist = r"^v.*$"

smv_branch_whitelist = r"^main$"


intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "cudf": ("https://docs.rapids.ai/api/cudf/stable/", None),
    "distributed": ("https://distributed.dask.org/en/latest/", None),
}

autodoc_inherit_docstrings = False
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": False,
    "member-order": "bysource",
}

autosummary_generate = True


def copy_files(src: str):
    """
    src_dir: A path, specified as relative to the
             docs/source directory in the repository.
             The source can be a directory or a file.
             Sphinx considers all directories as relative
             to the docs/source directory.

             TIP: Add these paths to the .gitignore file.
    """
    src_path = os.path.abspath(src)
    if not os.path.exists(src_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), src_path)
    out_path = os.path.basename(src_path)
    out_path = os.path.abspath("{}/".format(out_path))

    print(
        r"Copying source documentation from: {}".format(src_path),
        file=sys.stderr,
    )
    print(r"  ...to destination: {}".format(out_path), file=sys.stderr)

    if os.path.exists(out_path) and os.path.isdir(out_path):
        shutil.rmtree(out_path, ignore_errors=True)
    if os.path.exists(out_path) and os.path.isfile(out_path):
        os.unlink(out_path)

    if os.path.isdir(src_path):
        shutil.copytree(src_path, out_path)
    else:
        shutil.copyfile(src_path, out_path)


copy_files(r"../../README.md")
