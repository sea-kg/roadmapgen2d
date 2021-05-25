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
        if point_x in (0, self.__max_width - 1):
            return True
        if point_y in (0, self.__max_height - 1):
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

    def has_right_column3(self, point_x, point_y):
        """ has right column3 """
        b20 = self.ypixelmap[point_x+1][point_y-1]
        b21 = self.ypixelmap[point_x+1][point_y]
        b22 = self.ypixelmap[point_x+1][point_y+1]
        return b20 and b21 and b22

    def has_not_right_column3(self, point_x, point_y):
        """ has not right column3 """
        b20 = self.ypixelmap[point_x+1][point_y-1]
        b21 = self.ypixelmap[point_x+1][point_y]
        b22 = self.ypixelmap[point_x+1][point_y+1]
        return not b20 and not b21 and not b22

    def has_left_column3(self, point_x, point_y):
        """ has left column3 """
        b00 = self.ypixelmap[point_x-1][point_y-1]
        b01 = self.ypixelmap[point_x-1][point_y]
        b02 = self.ypixelmap[point_x-1][point_y+1]
        return b00 and b01 and b02

    def has_not_left_column3(self, point_x, point_y):
        """ has left column3 """
        b00 = self.ypixelmap[point_x-1][point_y-1]
        b01 = self.ypixelmap[point_x-1][point_y]
        b02 = self.ypixelmap[point_x-1][point_y+1]
        return not b00 and not b01 and not b02

    def has_top_row3(self, point_x, point_y):
        """ has top row3 """
        b00 = self.ypixelmap[point_x-1][point_y-1]
        b10 = self.ypixelmap[point_x  ][point_y-1]
        b20 = self.ypixelmap[point_x+1][point_y-1]
        return b00 and b10 and b20

    def has_not_top_row3(self, point_x, point_y):
        """ has not top row3 """
        b00 = self.ypixelmap[point_x-1][point_y-1]
        b10 = self.ypixelmap[point_x  ][point_y-1]
        b20 = self.ypixelmap[point_x+1][point_y-1]
        return not b00 and not b10 and not b20

    def has_bottom_row3(self, point_x, point_y):
        """ has bottom row3 """
        b02 = self.ypixelmap[point_x-1][point_y+1]
        b12 = self.ypixelmap[point_x  ][point_y+1]
        b22 = self.ypixelmap[point_x+1][point_y+1]
        return b02 and b12 and b22

    def has_not_bottom_row3(self, point_x, point_y):
        """ has not bottom row3 """
        b02 = self.ypixelmap[point_x-1][point_y+1]
        b12 = self.ypixelmap[point_x  ][point_y+1]
        b22 = self.ypixelmap[point_x+1][point_y+1]
        return not b02 and not b12 and not b22

    def print_map(self):
        """ print map to console """
        for line in self.ypixelmap:
            res_line = ''
            for i in line:
                if i is True:
                    _format = '0;30;47'
                else:
                    _format = '2;31;40'
                res_line += '\x1b[%sm  \x1b[0m' % (_format)
            print(res_line)
