#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Evgenii sopov <mrseakg@gmail.com>

# pylint: disable=relative-beyond-top-level

""" class modificator for random points on map """
from random import randrange
from roadmapgen2d.roadmapgen2d_mod_base import RoadMapGen2dModBase

class RoadMapGen2dModRandomPoints(RoadMapGen2dModBase):
    """ class modificator for random points on map """

    def __init__(self, config, imager):
        super().__init__(config, imager, "Random Points")

    def modify(self, _map):
        """ random points """
        immp = 0
        max_pw = self._config.get_map_width()
        max_ph = self._config.get_map_height()
        while immp < self._config.get_random_max_points():
            point_x = randrange(max_pw - 2) + 1
            point_y = randrange(max_ph - 2) + 1
            if _map.try_change_to_true(self._config, point_x, point_y):
                immp += 1
        print("------- " + self.get_name() + " -------")
        _map.print_map()
