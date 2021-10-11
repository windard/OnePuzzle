# -*- coding: utf-8 -*-

import setuptools
from setuptools import setup

from one_puzzle import __version__, __name__

with open("README.md", "r") as fh:
    long_description = fh.read()


entry_points = {
    'console_scripts': ['one_puzzle=one_puzzle.solver:main'],
}

setup(
    name=__name__,
    version=__version__,
    author='Windard Yang',
    author_email='windard@qq.com',
    description='Solve puzzle "A Puzzle A Day", get one or all result, show in graphical PyQt5',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/windard/OnePuzzle',
    packages=setuptools.find_packages(),
    install_requires=['PyQt5==5.15.4', 'click==8.0.1'],
    license="MIT",
    keywords=['puzzle'],
    entry_points=entry_points,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
