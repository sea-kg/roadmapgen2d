#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Evgenii sopov <mrseakg@gmail.com>

# pylint: disable=relative-beyond-top-level

""" class base-modificator """

from roadmapgen2d.roadmapgen2d_config import RoadMapGen2dConfig
from roadmapgen2d.roadmapgen2d_write_map_to_image import RoadMapGen2dWriteMapToImage

class RoadMapGen2dModBase:
    """ class base-modificator """
    # private
    __name = "Base"
    # protected
    _imager: RoadMapGen2dWriteMapToImage = None
    _config: RoadMapGen2dConfig = None

    def __init__(self, config, imager, name):
        self.__name = name
        self._imager = imager
        self._config = config

    def get_name(self):
        """ return name """
        return self.__name

    def modify(self, _map):
        """ empty modify """
