# pylint: skip-file

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys, os
sys.path.append(os.path.abspath('../../src/appFOM'))

from appFOM import LISA_GB_configuration
from appFOM import LISA_noise_configuration
from appFOM import utils

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'FOM application'
copyright = '2024, Yves Lemiere, Maude Lejeune, Côme Badet'
author = 'Yves Lemiere, Maude Lejeune, Côme Badet'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.autodoc',
    'sphinx.ext.githubpages',
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ["_static"]
