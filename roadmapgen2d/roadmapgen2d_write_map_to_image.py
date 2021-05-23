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

    def write_map_to_image(self, _ypixelmap):
        # filename
        filename = self.__next_filename()
        if not self.__config.is_create_video():
            return
        print("Write to file " + filename)
        cell_size = 10
        img = []
        for line in _ypixelmap:
            rows = []
            for i in range(cell_size):
                rows.append(())
            for cell in line:
                _cell = (0, 0, 0)
                if cell is True:
                    _cell = (255, 255, 255)
                for i in range(cell_size):
                    for _ in range(cell_size):
                        rows[i] += _cell

            for i in range(cell_size):
                img.append(rows[i])
        with open(filename, 'wb') as f:
            w = png.Writer(self.__max_width*cell_size, self.__max_height*cell_size, greyscale=False)
            w.write(f, img)
