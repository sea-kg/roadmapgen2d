#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Evgenii sopov <mrseakg@gmail.com>

# pylint: disable=relative-beyond-top-level,missing-function-docstring

""" simple map """
from roadmapgen2d.roadmapgen2d_config import RoadMapGen2dConfig
from roadmapgen2d.roadmapgen2d_write_map_to_image import RoadMapGen2dWriteMapToImage

class RoadMapGen2dMap:
    """ class for read config of generation image """
    __max_width = None
    __max_height = None
    __imager: RoadMapGen2dWriteMapToImage = None
    __config: RoadMapGen2dConfig = None
    ypixelmap = []
    def __init__(self, config, imager):
        self.__imager = imager
        self.__config = config
        self.__max_width = self.__config.get_map_width()
        self.__max_height = self.__config.get_map_height()
        self.reset_map()

    def reset_map(self):
        """ reset map """
        self.ypixelmap = []
        ipw = 0
        while ipw < self.__max_width:
            iph = 0
            self.ypixelmap.append([])
            while iph < self.__max_height:
                self.ypixelmap[ipw].append(False)
                iph += 1
            ipw += 1

    def is_border(self, point_x, point_y):
        """ is_border """
        if point_x == 0 or point_x == self.__max_width - 1:
            return True
        if point_y == 0 or point_y == self.__max_height - 1:
            return True
        return False

    def is_allowed(self, point_x, point_y):
        """ is_allowed """
        if self.is_border(point_x, point_y):
            return False
        point_x = point_x - 1
        point_y = point_y - 1
        for point_x0 in range(2):
            for point_y0 in range(2):
                _b1 = self.ypixelmap[point_x + point_x0  ][point_y + point_y0]
                _b2 = self.ypixelmap[point_x + point_x0+1][point_y + point_y0]
                _b3 = self.ypixelmap[point_x + point_x0+1][point_y + point_y0+1]
                _b4 = self.ypixelmap[point_x + point_x0  ][point_y + point_y0+1]
                if _b1 and _b2 and _b3 and _b4:
                    return False
        return True

    def try_change_to_true(self, _config, point_x, point_y):
        """ try_change_to_true """
        self.ypixelmap[point_x][point_y] = True
        self.__imager.write_map_to_image(self.ypixelmap)
        if not self.is_allowed(point_x, point_y):
            self.ypixelmap[point_x][point_y] = False
            self.__imager.write_map_to_image(self.ypixelmap)
            return False
        return True
