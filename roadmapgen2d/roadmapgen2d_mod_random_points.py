#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Evgenii sopov <mrseakg@gmail.com>

# pylint: disable=relative-beyond-top-level,missing-function-docstring

""" simple map """
from random import randrange
from roadmapgen2d.roadmapgen2d_config import RoadMapGen2dConfig
from roadmapgen2d.roadmapgen2d_write_map_to_image import RoadMapGen2dWriteMapToImage

class RoadMapGen2dModRandomPoints:
    """ class for read config of generation image """
    __max_width = None
    __max_height = None
    __name = "Random Points"
    __imager: RoadMapGen2dWriteMapToImage = None
    __config: RoadMapGen2dConfig = None
    ypixelmap = []

    def __init__(self, config, imager):
        self.__imager = imager
        self.__config = config

    def get_name(self):
        """ return mod name """
        return self.__name

    def modify(self, _map):
        """ random points """
        immp = 0
        max_pw = self.__config.get_map_width()
        max_ph = self.__config.get_map_height()
        while immp < self.__config.get_random_max_points():
            point_x = randrange(max_pw - 2) + 1
            point_y = randrange(max_ph - 2) + 1
            if _map.try_change_to_true(self.__config, point_x, point_y):
                immp += 1
