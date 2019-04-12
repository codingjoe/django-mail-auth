"""Sphinx configuration file."""
import os
import sys

import django
from pkg_resources import get_distribution

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.testapp.settings")
sys.path.insert(0, os.path.abspath('..'))
django.setup()

project = "Django Mail Auth"
copyright = "2019, Johannes Hoppe"
release = get_distribution('django-mail-auth').version
version = '.'.join(release.split('.')[:2])

master_doc = 'index'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.doctest',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'django': ('https://docs.djangoproject.com/en/stable/',
               'https://docs.djangoproject.com/en/stable/_objects/'),
}
