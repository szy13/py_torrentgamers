from setuptools import setup, find_packages
from os.path import join, dirname

import torrentgamers

attrs = {
    'name': torrentgamers.__name__,
    'version': torrentgamers.__version__,
    'author': torrentgamers.__author__,
    'author_email': torrentgamers.__email__,
    'url': torrentgamers.__url__,
    'long_description': open(join(dirname(__file__), 'README.md')).read(),
    'packages': find_packages(),
    'install_requires': [
        'requests',
        'bs4'
    ]
}

setup(**attrs)
