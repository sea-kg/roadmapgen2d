#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Evgenii sopov <mrseakg@gmail.com>

# pylint: disable=relative-beyond-top-level,missing-function-docstring

""" writer map to image """

import png
from roadmapgen2d.roadmapgen2d_config import RoadMapGen2dConfig

class RoadMapGen2dWriteMapToImage:
    """ class for write map to image """
    __config: RoadMapGen2dConfig = None
    __number = 0
    __max_width = 1
    __max_height = 1
    def __init__(self, config):
        self.__config = config
        self.__max_width = config.get_map_width()
        self.__max_height = config.get_map_height()
        self.__number = 0

    def __next_filename(self):
        """ pad_str """
        _filename = str(self.__number)
        while len(_filename) < 6:
            _filename = "0" + _filename
        _filename = '.roads-generation/roadmap' + _filename + '.png'
        self.__number += 1
        return _filename

    def get_number_of_frames(self):
        return self.__number

    def __write_frame(self, _ypixelmap, _filename):
        print("Write to file " + _filename)
        cell_size = 10
        img = []
        point_y = 0
        for line in _ypixelmap:
            rows = []
            point_x = 0
            for i in range(cell_size):
                rows.append(())
            for cell in line:
                _cell = self.__config.get_color_rgb_background()
                if cell is True:
                    _cell = self.get_color_rgb_line_road(point_y, point_x)
                for i in range(cell_size):
                    for _ in range(cell_size):
                        rows[i] += _cell
                point_x += 1
            for i in range(cell_size):
                img.append(rows[i])
            point_y += 1
        with open(_filename, 'wb') as _file:
            _png = png.Writer(
                self.__max_width*cell_size,
                self.__max_height*cell_size,
                greyscale=False
            )
            _png.write(_file, img)

    def write_map_to_image(self, _ypixelmap):
        # filename
        _filename = self.__next_filename()
        if not self.__config.is_create_video():
            return
        self.__write_frame(_ypixelmap, _filename)

    def write_last_frame_to_image(self, _ypixelmap):
        if not self.__config.is_create_last_frame_as_image():
            return
        _filename = 'roadmapgen2d-result.png'
        self.__write_frame(_ypixelmap, _filename)

    def get_color_rgb_line_road(self, point_y, point_x):
        if not self.__config.is_color_line_road_use_gradient():
            return self.__config.get_color_rgb_line_road()
        _red = int(point_y*256 / self.__max_height)
        _green = int(point_x*256 / self.__max_width)
        _blue = 255
        return (_red, _green, _blue)
