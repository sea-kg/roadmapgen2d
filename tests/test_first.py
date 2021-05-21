#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test server api leaks"""

# Copyright (c) 2020 Evgenii Sopov <mrseakg@gmail.com>

# pylint: disable=relative-beyond-top-level,wrong-import-position,import-error

import sys
sys.path.insert(0,'..') # Adds higher directory to python modules path.

from roadmapgen2d.roadmapgen2d_write_map_to_image import RoadMapGen2dWriteMapToImage

def test_first():
    """Simple line parse"""
    print(test_first.__doc__)
