#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test server api leaks"""

# Copyright (c) 2020 Evgenii Sopov <mrseakg@gmail.com>

# pylint: disable=relative-beyond-top-level,wrong-import-position,import-error

import sys
sys.path.insert(0,'..') # Adds higher directory to python modules path.

# from roadmapgen2d.roadmapgen2d_write_map_to_image import RoadMapGen2dWriteMapToImage
from roadmapgen2d.roadmapgen2d_config import RoadMapGen2dConfig

def test_hex_to_rgb():
    """ test hex like 'FF00DD' to (255, 0, 221) """
    _convert_colors = {
        'FFFFFF': (255,255,255),
        'FF00DD': (255, 0, 221),
        'AA00EE': (170, 0, 238),
    }
    for _hex in _convert_colors:
        _rgb = RoadMapGen2dConfig.hex_to_rgb(_hex)
        assert _rgb == _convert_colors[_hex]
