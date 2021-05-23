#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Evgenii sopov <mrseakg@gmail.com>

# pylint: disable=relative-beyond-top-level,missing-function-docstring

""" reader for config """

import json

class RoadMapGen2dConfig:
    """ class for read config of generation image """
    # default values
    __map_width = 50
    __map_height = 50
    __tex_road_width = 120
    __tex_road_height = 120
    __map_width_px = 5000
    __map_height_px = 5000
    __random_max_points = 100 
    __create_video = False
    __create_last_frame_as_image = True
    def __init__(self):
        self.__filepath = 'roadmapgen2d-config.json'

    def load_from_file(self, filepath):
        self.__filepath = filepath
        with open(self.__filepath,) as file_cfg:
            data = json.load(file_cfg)
            self.__tex_road_width = data['texture-tail-road-width-px']
            self.__tex_road_height = data['texture-tail-road-height-px']
            self.__map_width_px = data['map-width-px']
            self.__map_height_px = data['map-height-px']
            self.__map_width = int(self.__map_width_px/self.__tex_road_width)
            self.__map_height = int(self.__map_height_px/self.__tex_road_height)
            self.__create_video = data['create-video']
            self.__random_max_points = data['random-max-points']
            self.__create_last_frame_as_image = data['create-last-frame-as-image']
            return True
        return False

    def get_map_width(self):
        return self.__map_width

    def get_map_height(self):
        return self.__map_height

    def is_create_video(self):
        return self.__create_video

    def get_random_max_points(self):
        return self.__random_max_points
