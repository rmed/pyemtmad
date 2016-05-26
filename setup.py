#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pyemtmad, EMT API wrapper - https://github.com/rmed/pyemtmad
# Copyright (C) 2016  Rafael Medina García <rafamedgar@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "DESCRIPTION.rst")) as f:
    long_description = f.read()


setup(
        name='pyemtmad',
        version='0.1.0',

        description='(Kind of) sane wrapper for the EMT API',
        long_description=long_description,

        author='Rafael Medina García',
        author_email='rafamedgar@gmail.com',
        url='https://github.com/rmed/pyemtmad',

        license='GPLv2+',

        packages=find_packages(),
        install_requires=[
            'six >= 1.10.0',
            'requests >= 2.9.1'
            ],

        keywords='madrid transport travel bus geo open data api'
        )
