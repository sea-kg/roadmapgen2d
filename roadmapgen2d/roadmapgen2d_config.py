#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Evgenii sopov <mrseakg@gmail.com>

# pylint: disable=relative-beyond-top-level

""" reader for config """

import os
import json
from roadmapgen2d.roadmapgen2d_size import RoadMapGen2dSize
from roadmapgen2d.roadmapgen2d_color import RoadMapGen2dColor

class RoadMapGen2dConfig:
    """ class for read config of generation image """
    # default values
    __map_size = RoadMapGen2dSize(50,50)
    __tex_road_size_px = RoadMapGen2dSize(120, 120)
    __tex_path = "textures/road0.png"
    __map_size_px = RoadMapGen2dSize(5000, 5000)
    __random_max_points = 100
    __create_video = False
    __create_last_frame_as_image = True
    __color_background = RoadMapGen2dColor("000000")
    __color_line_road = RoadMapGen2dColor("FFFFFF")
    __color_line_road_use_gradient = False

    def __init__(self):
        self.__filepath = 'roadmapgen2d-config.json'

    def load_from_file(self, filepath):
        """ load config from a file """
        self.__filepath = filepath
        if os.path.isfile(self.__filepath):
            return False
        with open(self.__filepath,) as file_cfg:
            data = json.load(file_cfg)
            self.__tex_road_size_px.set_width(data['texture-tail-road-width-px'])
            self.__tex_road_size_px.set_height(data['texture-tail-road-height-px'])
            self.__tex_path = data['texture-path']
            self.__map_size_px.parse_from_json(data, 'map-', '-px')
            self.__map_size.set_width(
                int(self.__map_size_px.get_width() / self.__tex_road_size_px.get_width())
            )
            self.__map_size.set_height(
                int(self.__map_size_px.get_height() / self.__tex_road_size_px.get_height())
            )
            self.__create_video = data['create-video']
            self.__random_max_points = data['random-max-points']
            self.__create_last_frame_as_image = data['create-last-frame-as-image']
            self.__color_background.parse_from_json(data, 'color-hex-background')
            self.__color_line_road.parse_from_json(data, 'color-hex-line-road')
            self.__color_line_road_use_gradient = data["color-line-road-use-gradient"]
            return True

    def get_map_width(self):
        """ get_map_width """
        return self.__map_size.get_width()

    def get_map_height(self):
        """ get_map_height """
        return self.__map_size.get_height()

    def is_create_video(self):
        """ is_create_video """
        return self.__create_video

    def is_create_last_frame_as_image(self):
        """ is_create_last_frame_as_image """
        return self.__create_last_frame_as_image

    def get_random_max_points(self):
        """ get_random_max_points """
        return self.__random_max_points

    def get_color_rgb_background(self):
        """ get_color_rgb_background """
        return self.__color_background.get_rgb()

    def get_color_rgb_line_road(self):
        """ get_color_rgb_line_road """
        return self.__color_line_road.get_rgb()

    def is_color_line_road_use_gradient(self):
        """ is_color_line_road_use_gradient """
        return self.__color_line_road_use_gradient

    def get_texture_path(self):
        """ get_texture_path """
        return self.__tex_path

    def get_texture_width(self):
        """ get_texture_width """
        return self.__tex_road_size_px.get_width()

    def get_texture_height(self):
        """ get_texture_height """
        return self.__tex_road_size_px.get_height()
