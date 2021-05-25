#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Evgenii sopov <mrseakg@gmail.com>

# pylint: disable=relative-beyond-top-level,missing-function-docstring

""" class modificator for make rooms (fill closes roads) """
from roadmapgen2d.roadmapgen2d_mod_base import RoadMapGen2dModBase

class RoadMapGen2dModMakeRooms(RoadMapGen2dModBase):
    """ class modificator for make rooms (fill closes roads) """

    def __init__(self, config, imager):
        super().__init__(config, imager, "Make rooms")

    def modify(self, _map):
        """ fill closes roads """
        # TO DO
        print("------- " + self.get_name() + " -------")
        _map.print_map()
