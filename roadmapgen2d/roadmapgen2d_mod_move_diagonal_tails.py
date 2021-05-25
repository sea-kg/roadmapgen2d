#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Evgenii sopov <mrseakg@gmail.com>

# pylint: disable=relative-beyond-top-level,missing-function-docstring

""" simple map """
from random import randrange
from roadmapgen2d.roadmapgen2d_mod_base import RoadMapGen2dModBase

class RoadMapGen2dModMoveDiagonalTails(RoadMapGen2dModBase):
    """ class modificator move diagonal tails """

    def __init__(self, config, imager):
        super().__init__(config, imager, "Move Diagonal Tails")

    def modify(self, _map):
        """ move_diagonal_tails loop """
        mdt = self.move_diagonal_tails(_map)
        while mdt > 0:
            mdt = self.move_diagonal_tails(_map)
        print("------- " + self.get_name() + " -------")
        _map.print_map()

    def move_diagonal_tails(self, _map):
        """ move_diagonal_tails """
        point_x = 0
        ret = 0
        for x_line in _map.ypixelmap:
            point_y = 0
            for _ in x_line:
                ret += self.check_and_random_move(_map, point_x, point_y)
                point_y += 1
            point_x += 1
        return ret

    def check_and_random_move(self, _map, point_x, point_y):
        """ check_and_random_move """
        if _map.is_border(point_x, point_y):
            return False
        ret = 0
        b11 = _map.ypixelmap[point_x  ][point_y  ]
        b12 = _map.ypixelmap[point_x  ][point_y+1]
        b22 = _map.ypixelmap[point_x+1][point_y+1]
        b21 = _map.ypixelmap[point_x+1][point_y  ]
        if b11 and b22 and not b12 and not b21:
            ret += 1
            _map.ypixelmap[point_x+1][point_y+1] = False
            if randrange(2) == 0:
                _map.try_change_to_true(self._config, point_x, point_y+1)
            else:
                _map.try_change_to_true(self._config, point_x+1, point_y)
        if not b11 and not b22 and b12 and b21:
            ret += 1
            _map.ypixelmap[point_x][point_y+1] = False
            if randrange(2) == 0:
                _map.try_change_to_true(self._config, point_x, point_y)
            else:
                _map.try_change_to_true(self._config, point_x+1, point_y+1)
        return ret
