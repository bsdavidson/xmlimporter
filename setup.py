import os
from setuptools import setup


with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                       'xmlimporter', '_version.py'), 'r') as version_file:
    exec(version_file.read())

setup(
    name=__name__,  # noqa -- flake8 should ignore this line
    version=__version__,  # noqa
    description='Script to load data from an XML file into a MySQL DB.',
    url='https://github.com/bsdavidson/xmlimporter',
    packages=['xmlimporter'],
    scripts=['scripts/xmlimporter'],
    install_requires=['PyMySQL==0.6.2'],
    extras_require={
        'tests': ['tox==1.9.2']
    }
)
