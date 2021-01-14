#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import BatteriesMining

setup(

    name='BatteriesMining',

    version=BatteriesMining.__version__,

    packages=find_packages(),

    author="Hassna EL-BOUSIYDY",

    author_email="hassna@gmail.com",

    description="Add your description ...",

    long_description=open('README.md').read(),

    long_description_content_type='text/markdown',

    include_package_data=True,

    url='https://github.com/helbousiydy/BatteriesMining',

    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Topic :: Communications",
    ],

    license="Licence PINE", install_requires=['nltk', 'xlsxwriter', 'pdfminer', 'tika']

)