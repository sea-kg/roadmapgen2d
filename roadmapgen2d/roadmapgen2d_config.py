#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Evgenii sopov <mrseakg@gmail.com>

# pylint: disable=relative-beyond-top-level,missing-function-docstring

""" reader for config """

import json

class RoadMapGen2dConfig:
    """ class for read config of generation image """
    # default values
    __map_size = {"width": 50, "height": 50 }
    __tex_road_size_px = {"width": 120, "height": 120 }
    __map_width_px = 5000
    __map_height_px = 5000
    __random_max_points = 100
    __create_video = False
    __create_last_frame_as_image = True
    __color_hex_background = "000000"
    __color_rgb_background = (1,1,1)
    __color_hex_line_road = "FFFFFF"
    __color_rgb_line_road = (254,254,254)

    def __init__(self):
        self.__filepath = 'roadmapgen2d-config.json'
        self.__prepare_colors()

    def load_from_file(self, filepath):
        self.__filepath = filepath
        with open(self.__filepath,) as file_cfg:
            data = json.load(file_cfg)
            self.__tex_road_size_px['width'] = data['texture-tail-road-width-px']
            self.__tex_road_size_px['height'] = data['texture-tail-road-height-px']
            self.__map_width_px = data['map-width-px']
            self.__map_height_px = data['map-height-px']
            self.__map_size["width"] = int(self.__map_width_px / self.__tex_road_size_px['width'])
            self.__map_size["height"] = int(
                self.__map_height_px / self.__tex_road_size_px['height']
            )
            self.__create_video = data['create-video']
            self.__random_max_points = data['random-max-points']
            self.__create_last_frame_as_image = data['create-last-frame-as-image']
            self.__color_hex_background = data['color-hex-background']
            self.__color_hex_line_road = data['color-hex-line-road']
            self.__prepare_colors()
            return True
        return False

    def __prepare_colors(self):
        self.__color_rgb_line_road = self.hex_to_rgb(self.__color_hex_line_road)
        self.__color_rgb_background = self.hex_to_rgb(self.__color_hex_background)

    @staticmethod
    def hex_to_rgb(_hex):
        _color = int(_hex, 16)
        _red = _color >> 16 & 0xFF
        _green = _color >> 8 & 0xFF
        _blue = _color & 0xFF
        return (_red, _green, _blue)

    def get_map_width(self):
        return self.__map_size["width"]

    def get_map_height(self):
        return self.__map_size["height"]

    def is_create_video(self):
        return self.__create_video

    def is_create_last_frame_as_image(self):
        return self.__create_last_frame_as_image

    def get_random_max_points(self):
        return self.__random_max_points

    def get_color_rgb_background(self):
        return self.__color_rgb_background

    def get_color_rgb_line_road(self):
        return self.__color_rgb_line_road
