#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Evgenii sopov <mrseakg@gmail.com>

# pylint: disable=relative-beyond-top-level

""" helper class for color """

class RoadMapGen2dColor:
    """ class for keep size """
    __hex = None
    __rgb = None
    def __init__(self, _hex):
        self.__hex = _hex
        self.__update_rgb()

    def __update_rgb(self):
        """ convert hex to rgb triple """
        _color = int(self.__hex, 16)
        _red = _color >> 16 & 0xFF
        _green = _color >> 8 & 0xFF
        _blue = _color & 0xFF
        self.__rgb =  (_red, _green, _blue)

    def get_rgb(self):
        """ return rgb """
        return self.__rgb

    def get_hex(self):
        """ return hex """
        return self.__hex

    def parse_from_json(self, data, name):
        """ load width and height from json """
        self.__hex = data[name]
        self.__update_rgb()
