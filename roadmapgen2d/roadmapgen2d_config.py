#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Evgenii sopov <mrseakg@gmail.com>

# pylint: disable=relative-beyond-top-level,missing-function-docstring

""" reader for config """

import json

class RoadMapGen2dConfig:
    """ class for read config of generation image """
    __map_width = 50 # default
    __map_height = 50 # default
    __random_max_points = 100 # default
    __create_video = False
    def __init__(self):
        self.__filepath = 'roadmapgen2d-config.json'

    def load_from_file(self, filepath):
        self.__filepath = filepath
        with open(self.__filepath,) as file_cfg:
            data = json.load(file_cfg)
            self.__map_width = data['map-width']
            self.__map_height = data['map-height']
            self.__create_video = data['create-video']
            self.__random_max_points = data['random-max-points']
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
