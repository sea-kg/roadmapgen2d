#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Evgenii sopov <mrseakg@gmail.com>

# pylint: disable=relative-beyond-top-level,missing-function-docstring

""" reader for config """

import json

class RoadMapGen2dConfig:
    """ class for read config of generation image """
    __width = 50 # default
    __height = 50 # default
    def __init__(self):
        self.__filepath = 'roadmapgen2d-config.json'

    def load_from_file(self, filepath):
        self.__filepath = filepath
        with open(self.__filepath,) as file_map:
            data = json.load(file_map)
            self.__width = data['width']
            self.__height = data['height']
            return True
        return False
