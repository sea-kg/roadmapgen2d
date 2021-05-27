#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Evgenii sopov <mrseakg@gmail.com>

# pylint: disable=relative-beyond-top-level

""" writer map to json """

import sys
import json
from roadmapgen2d.roadmapgen2d_config import RoadMapGen2dConfig

class RoadMapGen2dExportToJson:
    """ class for write map to json file """
    __config: RoadMapGen2dConfig = None
    __ypixelmap = None
    __roadpart = {
        # left, right, top, bottom
        (True , True, True, True): "cross",
        (True , True, False, False): "horizontal",
        (True , False, False, True): "left-down",
        (True , False, True, False): "left-up",
        (True , False, True, True): "left-up-down",
        (True , True, False, True): "left-right-down",
        (True , True, True, False): "left-right-up",
        (False, False, True, True): "vertical",
        (False, True, False, True): "right-down",
        (False, True, True, False): "right-up",
        (False, True, True, True): "right-up-down",
    }

    def __init__(self, config, _ypixelmap):
        self.__config = config
        self.__ypixelmap = _ypixelmap

    def get_road_part(self, point_x, point_y):
        """ get_road_part """
        if not self.__ypixelmap[point_x][point_y]:
            print("Error")
            sys.exit(-1)

        left =   self.__ypixelmap[point_x  ][point_y-1]
        right =  self.__ypixelmap[point_x  ][point_y+1]
        top =    self.__ypixelmap[point_x-1][point_y  ]
        bottom = self.__ypixelmap[point_x+1][point_y  ]

        item = (left,right,top,bottom)
        if item in self.__roadpart:
            return self.__roadpart[item]
        print("Error")
        sys.exit(-1)

    def prepare_output_json(self):
        """ prepare_output_json """
        return {
            "roads": [{
                "texture": self.__config.get_texture_path(),
                "width": self.__config.get_texture_width(),
                "height": self.__config.get_texture_height(),
                "fill": [],
            }]
        }

    def write_map_to_json(self, _filename):
        """ write_map_to_json """
        export_to_json = self.prepare_output_json()
        fills = []
        point_x = 0
        for x_line in self.__ypixelmap:
            point_y = 0
            for _ in x_line:
                if self.__ypixelmap[point_x][point_y]:
                    fills.append({
                        "y": point_x*120,
                        "x": point_y*120 + 160, # why x?
                        "road-part": self.get_road_part(point_x, point_y),
                    })
                point_y += 1
            point_x += 1
        export_to_json['roads'][0]['fill'] = fills

        with open(_filename, 'w') as outfile:
            json.dump(export_to_json, outfile, indent=4)
