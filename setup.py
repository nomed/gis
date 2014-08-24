# -*- coding: utf-8 -*-
import sys, os

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

install_requires=[
    "TurboGears2 >= 2.1.4",
    "tgext.pluggable",
    "mailchimp"
]

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''

setup(
    name='gis',
    version='0.1',
    description='',
    long_description=README,
    author='',
    author_email='',
    #url='',
    keywords='turbogears2.application',
    packages=find_packages(exclude=['ez_setup']),
    install_requires=install_requires,
    include_package_data=True,
    package_data={'tgapp.gis': ['i18n/*/LC_MESSAGES/*.mo',
                                 'templates/*/*',
                                 'public/*/*']},
    entry_points={
        'gearbox.commands': [
            'gis-sync-mc = gis.commands.sync:GisSyncCommand',
            'gis-test = gis.commands.main:Files',
        ],
    },
    zip_safe=False
)
