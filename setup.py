#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Setup package
"""
from glob import glob
from os.path import basename, splitext

from setuptools import find_packages
from setuptools import setup


def readme():
    
    with open('README.md', encoding='utf-8') as f:

        return f.read()


setup(
    name='glanvup',
    version='0.1',
    license='MIT License',
    description='Global Assessment of Natural Hazards towards Vulnerable and Unconnected Population',
    long_description=readme(),
    long_description_content_type="text/markdown",
    author='Bonface Osoro',
    author_email='bosoro@gmu.edu',
    url='https://github.com/Bonface-Osoro/saleos',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Utilities',
    ],
    keywords=[
        'natural hazards','connectivity', 'broadband', 'population'
    ],
    setup_requires=[
        'setuptools_scm'
    ],
    install_requires=[
        'numpy>=1.16.4',
    ],
    entry_points={
        'console_scripts': [
            # eg: 'snkit = snkit.cli:main',
        ]
    },
)
