#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Evgenii sopov <mrseakg@gmail.com>

# pylint: disable=relative-beyond-top-level,missing-function-docstring

""" simple map """


class RoadMapGen2dMap:
    """ class for read config of generation image """
    __width = None
    __height = None
    ypixelmap = []
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__reset_map()

    def __reset_map(self):
        self.ypixelmap = []
        ipw = 0
        while ipw < self.__width:
            iph = 0
            self.ypixelmap.append([])
            while iph < self.__height:
                self.ypixelmap[ipw].append(False)
                iph += 1
            ipw += 1
