# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Net Bits'
copyright = '2024, Samuel Hulme'
author = 'Samuel Hulme'
release = '0.0.1'

import os
import sys
pth = os.path.abspath('../../')
print(f"\n{pth}\n")
sys.path.insert(0, pth)

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.coverage',
    'sphinx.ext.napoleon'
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ['_static']
html_theme_options = {
    "source_repository": "https://github.com/ajh123/netbits/",
    "source_branch": "main",
    "source_directory": "docs/",
}