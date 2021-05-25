#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Evgenii sopov <mrseakg@gmail.com>

# pylint: disable=relative-beyond-top-level

""" class for keep size  """

class RoadMapGen2dSize:
    """ class for keep size """
    __width = None
    __height = None
    def __init__(self, width, height):
        self.__width = width
        self.__height = height

    def get_width(self):
        """ return width """
        return self.__width

    def get_height(self):
        """ return height """
        return self.__height

    def set_width(self, width):
        """ set width """
        self.__width = width

    def set_height(self, height):
        """ set height """
        self.__height = height

    def parse_from_json(self, data, prefix, suffix):
        """ load width and height from json """
        self.__width = data[prefix + 'width' + suffix]
        self.__height = data[prefix + 'height' + suffix]
