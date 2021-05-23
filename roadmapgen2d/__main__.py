#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Evgenii sopov <mrseakg@gmail.com>

"""Library for roadmapgen2d"""

import os
import sys
import json
from random import randrange
import math
import png

# from roadmapgen2d.roadmapgen2d import RoadMapGen2D
from roadmapgen2d.__pkginfo__ import version
from roadmapgen2d.__pkginfo__ import name
from roadmapgen2d.roadmapgen2d_config import RoadMapGen2dConfig
from roadmapgen2d.roadmapgen2d_map import RoadMapGen2dMap
from roadmapgen2d.roadmapgen2d_write_map_to_image import RoadMapGen2dWriteMapToImage

read0_texture = "textures/road0.png"
read0_texture_width = 120
read0_texture_height = 120

max_pw = 0
max_ph = 0

MAP = None
IMAGER = None

def random_main_points(_map, _config):
    """ random_main_points """
    immp = 0
    while immp < _config.get_random_max_points():
        x = randrange(max_pw - 2) + 1
        y = randrange(max_ph - 2) + 1
        if _map.try_change_to_true(_config, x,y):
            immp += 1

def print_map():
    """ print map to console """
    for line in MAP.ypixelmap:
        res_line = ''
        for i in line:
            if i == True:
                _format = '0;30;47'
            else:
                _format = '2;31;40'
            res_line += '\x1b[%sm  \x1b[0m' % (_format)
        print(res_line)



def get_around_count(x, y):
    if MAP.is_border(x, y):
        return 4
    ret = 0
    for dx in range(3):
        for dy in range(3):
            x0 = x + dx - 1 
            y0 = y + dy - 1
            if x0 == x and y0 == y:
                continue
            if MAP.ypixelmap[x0][y0]:
                ret += 1
    return ret

def is_single_point(x,y):
    if MAP.is_border(x, y):
        return False
    if not MAP.ypixelmap[x][y]:
        return False
    if get_around_count(x,y) == 0:
        return True
    return False

def find_single_points():
    single_points = []
    x = 0
    for x_line in MAP.ypixelmap:
        y = 0
        for _ in x_line:
            if is_single_point(x, y):
                single_points.append({"x": x, "y": y})
            y += 1
        x += 1
    return single_points

def is_deadlock_point(x,y):
    if MAP.is_border(x, y):
        return False
    if not MAP.ypixelmap[x][y]:
        return False
    around = [
        MAP.ypixelmap[x-1][y],
        MAP.ypixelmap[x+1][y],
        MAP.ypixelmap[x][y+1],
        MAP.ypixelmap[x][y-1],
    ]
    count = 0
    for b in around:
        if b:
            count += 1
    return count == 1

def find_deadlock_points():
    deadlock_points = []
    x = 0
    for x_line in MAP.ypixelmap:
        y = 0
        for _ in x_line:
            if is_deadlock_point(x, y):
                deadlock_points.append({"x": x, "y": y})
            y += 1
        x += 1
    return deadlock_points

def check_and_random_move(_config, x,y):
    if MAP.is_border(x, y):
        return False
    ret = 0
    if MAP.ypixelmap[x][y] and MAP.ypixelmap[x+1][y+1] and not MAP.ypixelmap[x][y+1] and not MAP.ypixelmap[x+1][y]:
        ret += 1
        MAP.ypixelmap[x+1][y+1] = False
        if randrange(2) == 0:
            MAP.try_change_to_true(_config, x,y+1)
        else:
            MAP.try_change_to_true(_config, x+1,y)
    if not MAP.ypixelmap[x][y] and not MAP.ypixelmap[x+1][y+1] and MAP.ypixelmap[x][y+1] and MAP.ypixelmap[x+1][y]:
        ret += 1
        MAP.ypixelmap[x][y+1] = False
        if randrange(2) == 0:
            MAP.try_change_to_true(_config, x,y)
        else:
            MAP.try_change_to_true(_config, x+1,y+1)
    return ret

def move_diagonal_tails(_config):
    x = 0
    ret = 0
    for x_line in MAP.ypixelmap:
        y = 0
        for _ in x_line:
            ret += check_and_random_move(_config, x, y)
            y += 1
        x += 1
    return ret

def move_diagonal_tails_loop(_config):
    """ move_diagonal_tails_loop """
    mdt = move_diagonal_tails(_config)
    while mdt > 0:
        mdt = move_diagonal_tails(_config,)

def drawline_by_y(_config, x0, x1, y):
    ret = 0
    ix = min(x0,x1)
    mx = max(x0,x1)
    while ix <= mx:
        if not MAP.ypixelmap[ix][y]:
            if MAP.try_change_to_true(_config, ix,y):
                ret += 1
        ix += 1
    return ret

def drawline_by_x(_config, y0, y1, x):
    """ drawline_by_x """
    ret = 0
    iy = min(y0,y1)
    my = max(y0,y1)
    while iy <= my:
        if not MAP.ypixelmap[x][iy]:
            if MAP.try_change_to_true(_config, x,iy):
                ret += 1
        iy += 1
    return ret

def connect_points(_config, point0, point1):
    """ connect_points """
    ret = 0
    x0 = point0['x']
    y0 = point0['y']
    x1 = point1['x']
    y1 = point1['y']
    n = randrange(2)
    if n == 0:
        ret += drawline_by_y(_config, x0, x1, y0)
        ret += drawline_by_x(_config, y0, y1, x1)
    else:
        ret += drawline_by_x(_config, y0, y1, x0)
        ret += drawline_by_y(_config, x0, x1, y1)
    return ret

def remove_single_points(_config):
    """ remove_single_points """
    _points = find_single_points()
    for _point in _points:
        x = _point['x']
        y = _point['y']
        MAP.ypixelmap[x][y] = False
        IMAGER.write_map_to_image(MAP.ypixelmap)

def is_rame(x, y):
    """ is_rame """
    if MAP.is_border(x, y):
        return False
    if not MAP.ypixelmap[x][y]:
        return False
    b00 = MAP.ypixelmap[x-1][y-1]
    b01 = MAP.ypixelmap[x-1][y]
    b02 = MAP.ypixelmap[x-1][y+1]
    b10 = MAP.ypixelmap[x  ][y-1]
    # b11 = ypixelmap[x  ][y]
    b12 = MAP.ypixelmap[x  ][y+1]
    b20 = MAP.ypixelmap[x+1][y-1]
    b21 = MAP.ypixelmap[x+1][y]
    b22 = MAP.ypixelmap[x+1][y+1]

    if b00 and b01 and b02 and not b10 and not b12 and not b20 and not b21 and not b22:
        return True
    if b20 and b21 and b22 and not b00 and not b01 and not b02 and not b10 and not b12:
        return True
    if b00 and b10 and b20 and not b02 and not b12 and not b22 and not b01 and not b21:
        return True
    if b02 and b12 and b22 and not b00 and not b10 and not b20 and not b01 and not b21:
        return True
    return False

def remove_rames(_config):
    x = 0
    for x_line in MAP.ypixelmap:
        y = 0
        for _ in x_line:
            if is_rame(x, y):
                MAP.ypixelmap[x][y] = False
                IMAGER.write_map_to_image(MAP.ypixelmap)
            y += 1
        x += 1

def can_connect_close_points(x,y):
    if MAP.is_border(x, y):
        return False
    if MAP.ypixelmap[x][y]:
        return False
    if MAP.ypixelmap[x][y+1] and MAP.ypixelmap[x][y-1]:
        return True
    if MAP.ypixelmap[x+1][y] and MAP.ypixelmap[x-1][y]:
        return True
    return False

def connect_all_close_points(_config):
    x = 0
    for x_line in MAP.ypixelmap:
        y = 0
        for _ in x_line:
            _around_n = get_around_count(x, y)
            if can_connect_close_points(x, y) and _around_n < 6:
                MAP.try_change_to_true(_config, x,y)
            y += 1
        x += 1

def remove_all_short_cicles(_config):
    ret = 0
    x = 0
    for x_line in MAP.ypixelmap:
        y = 0
        for _ in x_line:
            if get_around_count(x, y) == 8 and not MAP.ypixelmap[x][y]:
                n = randrange(4)
                if n == 0:
                    MAP.ypixelmap[x][y+1] = False
                elif n == 1:
                    MAP.ypixelmap[x][y-1] = False
                elif n == 2:
                    MAP.ypixelmap[x+1][y] = False
                elif n == 2:
                    MAP.ypixelmap[x-1][y] = False
                ret +=1
                IMAGER.write_map_to_image(MAP.ypixelmap)
            y += 1
        x += 1
    return ret

def remove_all_short_cicles_loop(_config):
    while remove_all_short_cicles(_config) > 0:
        pass

def find_short_point_from(p0, points):
    x0 = p0['x']
    y0 = p0['y']
    found_x1 = x0
    found_y1 = y0
    dist = len(MAP.ypixelmap) + len(MAP.ypixelmap[0]) + 1 # max dist
    for p1 in points:
        x1 = p1['x']
        y1 = p1['y']
        if x1 == x0 and y1 == y0:
            continue
        x_max = max(x0, x1)
        x_min = min(x0, x1)
        y_max = max(y0, y1)
        y_min = min(y0, y1)
        new_dist = (x_max - x_min) + (y_max - y_min)
        if new_dist < dist:
            dist = new_dist
            found_x1 = x1
            found_y1 = y1
    return {'x': found_x1, 'y': found_y1}

def connect_deadlocks_loop(_config):
    deadlocks = find_deadlock_points()
    len_deadlocks = len(deadlocks)
    safe_max_loop = 10
    safe_loop = 0
    while len_deadlocks > 0:
        safe_loop += 1
        if safe_loop > safe_max_loop:
            break
        if len_deadlocks == 1:
            x = deadlocks[0]['x']
            y = deadlocks[0]['y']
            safe_loop -= 1
            MAP.ypixelmap[x][y] = False
            IMAGER.write_map_to_image(MAP.ypixelmap)
        else:
            pn0 = randrange(len_deadlocks)
            p0 = deadlocks[pn0]
            p1 = find_short_point_from(p0, deadlocks)
            # print(p0, p1)
            connected = connect_points(_config, p0, p1)
            if connected == 0:
                safe_loop -= 1
                x = p0['x']
                y = p0['y']
                MAP.ypixelmap[x][y] = False
                IMAGER.write_map_to_image(MAP.ypixelmap)
            else:
                safe_loop -= 1
        deadlocks = find_deadlock_points()
        len_deadlocks = len(deadlocks)

def remove_deadlocks_loop(_config):
    deadlocks = find_deadlock_points()
    len_deadlocks = len(deadlocks)
    while len_deadlocks > 0:
        x = deadlocks[0]['x']
        y = deadlocks[0]['y']
        MAP.ypixelmap[x][y] = False
        IMAGER.write_map_to_image(MAP.ypixelmap)
        deadlocks = find_deadlock_points()
        len_deadlocks = len(deadlocks)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit('ERROR: Expected argument. Try --help for mor details')

    if sys.argv[1] == '--version':
        print(name + ' v' + version)
        sys.exit(0)
    if sys.argv[1] == '--create-example-config':
        print("TODO")
        sys.exit(0)
    if sys.argv[1] == '--help':
        print("""
""" + name + ' v' + version + """
Arg can be:
--version - print version
--help - print help
--create-example-config - create example config (roadmapgen2d-config.json)
""")
        sys.exit(0)
    ROOT_DIR = os.path.abspath(sys.argv[1])
    if not os.path.isdir(ROOT_DIR):
        sys.exit('ERROR: Directory "' + sys.argv[1] + '" did not exists.')
    print("Start on dir: " + ROOT_DIR)
    config = RoadMapGen2dConfig()
    if not config.load_from_file('roadmapgen2d-config.json'):
        tips = ""
        if not os.path.isfile('roadmapgen2d-config.json'):
            tips = "\n  Note: for create use a --create-example-config"
        sys.exit(
            "ERROR: could not load roadmapgen2d-config.json" + tips
        )

    IMAGER = RoadMapGen2dWriteMapToImage(config)
    MAP = RoadMapGen2dMap(config, IMAGER)
    

    if not os.path.isdir(".roads-generation"):
        os.mkdir('.roads-generation')

    os.system("rm -rf .roads-generation/*.png")
    max_pw = config.get_map_width()
    max_ph = config.get_map_height()

    with open('roadmapgen2d-config.json',) as file_map:
        data = json.load(file_map)
        random_main_points(MAP, config)
        print_map()
        move_diagonal_tails_loop(config)
        print_map()
        again = True
        while again:
            points = find_single_points()
            len_points = len(points)
            if len_points <= 1:
                again = False
                break
            print(len_points)
            p0 = points[randrange(len_points)]
            p1 = points[randrange(len_points)]
            print(p0,p1)
            connect_points(config, p0,p1)
            move_diagonal_tails_loop(config)
            print_map()

        # remove last single point
        remove_single_points(config)
        remove_rames(config)
        connect_all_close_points(config)

        print_map()
        print("------- remove_all_short_cicles -------")
        remove_all_short_cicles_loop(config)
        remove_rames(config)
        move_diagonal_tails_loop(config)

        print_map()

        print("------- connect_deadlocks_loop -------")
        connect_deadlocks_loop(config)
        # move_diagonal_tails_loop(config)

        remove_all_short_cicles_loop(config)
        remove_rames(config)
        move_diagonal_tails_loop(config)
        remove_deadlocks_loop(config)
        remove_single_points(config)
        remove_rames(config)
        print_map()
        print("------- done -------")
        IMAGER.write_map_to_image(MAP.ypixelmap)
        print_map()

    frames_per_secons = IMAGER.get_number_of_frames()
    print("All frames: " + str(frames_per_secons))
    frames_per_secons = round(frames_per_secons / 82)
    

    # make video
    if os.path.isfile('video.avi'):
        os.remove('video.avi')

    if config.is_create_video():
        # last frame in last 5 seconds
        for _ in range(frames_per_secons*5):
            IMAGER.write_map_to_image(MAP.ypixelmap)

        print("Frames per second: " + str(frames_per_secons))
        os.system('ffmpeg -f image2 -r ' + str(frames_per_secons) + ' -i .roads-generation/roadmap%06d.png -i "../app/music/sea5kg - 02 Diphdo.ogg" -acodec libmp3lame -b 192k video.avi')
