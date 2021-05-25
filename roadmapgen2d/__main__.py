#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Evgenii sopov <mrseakg@gmail.com>

"""Library for roadmapgen2d"""

import os
import sys
import json
from random import randrange

# from roadmapgen2d.roadmapgen2d import RoadMapGen2D
from roadmapgen2d.__pkginfo__ import version
from roadmapgen2d.__pkginfo__ import name
from roadmapgen2d.roadmapgen2d_config import RoadMapGen2dConfig
from roadmapgen2d.roadmapgen2d_map import RoadMapGen2dMap
from roadmapgen2d.roadmapgen2d_write_map_to_image import RoadMapGen2dWriteMapToImage
from roadmapgen2d.roadmapgen2d_mod_random_points import RoadMapGen2dModRandomPoints

MAP = None
IMAGER = None

def print_map():
    """ print map to console """
    for line in MAP.ypixelmap:
        res_line = ''
        for i in line:
            if i is True:
                _format = '0;30;47'
            else:
                _format = '2;31;40'
            res_line += '\x1b[%sm  \x1b[0m' % (_format)
        print(res_line)

def get_around_count(point_x, point_y):
    """ get_around_count """
    if MAP.is_border(point_x, point_y):
        return 4
    ret = 0
    for point_dx in range(3):
        for point_dy in range(3):
            point_x0 = point_x + point_dx - 1
            point_y0 = point_y + point_dy - 1
            if point_x0 == point_x and point_y0 == point_y:
                continue
            if MAP.ypixelmap[point_x0][point_y0]:
                ret += 1
    return ret

def is_single_point(point_x, point_y):
    """ is_single_point """
    if MAP.is_border(point_x, point_y):
        return False
    if not MAP.ypixelmap[point_x][point_y]:
        return False
    if get_around_count(point_x, point_y) == 0:
        return True
    return False

def find_single_points():
    """ find_single_points """
    single_points = []
    point_x = 0
    for x_line in MAP.ypixelmap:
        point_y = 0
        for _ in x_line:
            if is_single_point(point_x, point_y):
                single_points.append({"x": point_x, "y": point_y})
            point_y += 1
        point_x += 1
    return single_points

def is_deadlock_point(point_x, point_y):
    """ is_deadlock_point """
    if MAP.is_border(point_x, point_y):
        return False
    if not MAP.ypixelmap[point_x][point_y]:
        return False
    around = [
        MAP.ypixelmap[point_x-1][point_y],
        MAP.ypixelmap[point_x+1][point_y],
        MAP.ypixelmap[point_x  ][point_y+1],
        MAP.ypixelmap[point_x  ][point_y-1],
    ]
    count = 0
    for has_points in around:
        if has_points:
            count += 1
    return count == 1

def find_deadlock_points():
    """ find_deadlock_points """
    deadlock_points = []
    point_x = 0
    for x_line in MAP.ypixelmap:
        point_y = 0
        for _ in x_line:
            if is_deadlock_point(point_x, point_y):
                deadlock_points.append({"x": point_x, "y": point_y})
            point_y += 1
        point_x += 1
    return deadlock_points

def check_and_random_move(_config, point_x, point_y):
    """ check_and_random_move """
    if MAP.is_border(point_x, point_y):
        return False
    ret = 0
    b11 = MAP.ypixelmap[point_x  ][point_y  ]
    b12 = MAP.ypixelmap[point_x  ][point_y+1]
    b22 = MAP.ypixelmap[point_x+1][point_y+1]
    b21 = MAP.ypixelmap[point_x+1][point_y  ]
    if b11 and b22 and not b12 and not b21:
        ret += 1
        MAP.ypixelmap[point_x+1][point_y+1] = False
        if randrange(2) == 0:
            MAP.try_change_to_true(_config, point_x, point_y+1)
        else:
            MAP.try_change_to_true(_config, point_x+1, point_y)
    if not b11 and not b22 and b12 and b21:
        ret += 1
        MAP.ypixelmap[point_x][point_y+1] = False
        if randrange(2) == 0:
            MAP.try_change_to_true(_config, point_x, point_y)
        else:
            MAP.try_change_to_true(_config, point_x+1, point_y+1)
    return ret

def move_diagonal_tails(_config):
    """ move_diagonal_tails """
    point_x = 0
    ret = 0
    for x_line in MAP.ypixelmap:
        point_y = 0
        for _ in x_line:
            ret += check_and_random_move(_config, point_x, point_y)
            point_y += 1
        point_x += 1
    return ret

def move_diagonal_tails_loop(_config):
    """ move_diagonal_tails_loop """
    mdt = move_diagonal_tails(_config)
    while mdt > 0:
        mdt = move_diagonal_tails(_config,)

def drawline_by_y(_config, point_x0, point_x1, point_y):
    """ drawline_by_y """
    ret = 0
    iter_x = min(point_x0,point_x1)
    max_x = max(point_x0,point_x1)
    while iter_x <= max_x:
        if not MAP.ypixelmap[iter_x][point_y]:
            if MAP.try_change_to_true(_config, iter_x, point_y):
                ret += 1
        iter_x += 1
    return ret

def drawline_by_x(_config, point_y0, point_y1, point_x):
    """ drawline_by_x """
    ret = 0
    iter_y = min(point_y0,point_y1)
    max_y = max(point_y0,point_y1)
    while iter_y <= max_y:
        if not MAP.ypixelmap[point_x][iter_y]:
            if MAP.try_change_to_true(_config, point_x,iter_y):
                ret += 1
        iter_y += 1
    return ret

def connect_points(_config, point0, point1):
    """ connect_points """
    ret = 0
    point_x0 = point0['x']
    point_y0 = point0['y']
    point_x1 = point1['x']
    point_y1 = point1['y']
    rand_n = randrange(2)
    if rand_n == 0:
        ret += drawline_by_y(_config, point_x0, point_x1, point_y0)
        ret += drawline_by_x(_config, point_y0, point_y1, point_x1)
    else:
        ret += drawline_by_x(_config, point_y0, point_y1, point_x0)
        ret += drawline_by_y(_config, point_x0, point_x1, point_y1)
    return ret

def remove_single_points(_config):
    """ remove_single_points """
    _points = find_single_points()
    for _point in _points:
        point_x = _point['x']
        point_y = _point['y']
        MAP.ypixelmap[point_x][point_y] = False
        IMAGER.write_map_to_image(MAP.ypixelmap)

def is_rame(point_x, point_y):
    """ is_rame """
    if MAP.is_border(point_x, point_y):
        return False
    if not MAP.ypixelmap[point_x][point_y]:
        return False
    b00 = MAP.ypixelmap[point_x-1][point_y-1]
    b01 = MAP.ypixelmap[point_x-1][point_y]
    b02 = MAP.ypixelmap[point_x-1][point_y+1]
    b10 = MAP.ypixelmap[point_x  ][point_y-1]
    # b11 = ypixelmap[x  ][y]
    b12 = MAP.ypixelmap[point_x  ][point_y+1]
    b20 = MAP.ypixelmap[point_x+1][point_y-1]
    b21 = MAP.ypixelmap[point_x+1][point_y]
    b22 = MAP.ypixelmap[point_x+1][point_y+1]

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
    """ remove_rames """
    point_x = 0
    for x_line in MAP.ypixelmap:
        point_y = 0
        for _ in x_line:
            if is_rame(point_x, point_y):
                MAP.ypixelmap[point_x][point_y] = False
                IMAGER.write_map_to_image(MAP.ypixelmap)
            point_y += 1
        point_x += 1

def can_connect_close_points(point_x, point_y):
    """ can_connect_close_points """
    if MAP.is_border(point_x, point_y):
        return False
    if MAP.ypixelmap[point_x][point_y]:
        return False
    if MAP.ypixelmap[point_x][point_y+1] and MAP.ypixelmap[point_x][point_y-1]:
        return True
    if MAP.ypixelmap[point_x+1][point_y] and MAP.ypixelmap[point_x-1][point_y]:
        return True
    return False

def connect_all_close_points(_config):
    """ connect_all_close_points """
    point_x = 0
    for x_line in MAP.ypixelmap:
        point_y = 0
        for _ in x_line:
            _around_n = get_around_count(point_x, point_y)
            if can_connect_close_points(point_x, point_y) and _around_n < 6:
                MAP.try_change_to_true(_config, point_x, point_y)
            point_y += 1
        point_x += 1

def remove_all_short_cicles(_config):
    """ remove_all_short_cicles """
    ret = 0
    point_x = 0
    for x_line in MAP.ypixelmap:
        point_y = 0
        for _ in x_line:
            if get_around_count(point_x,point_y) == 8 and not MAP.ypixelmap[point_x][point_y]:
                rand_n = randrange(4)
                if rand_n == 0:
                    MAP.ypixelmap[point_x][point_y+1] = False
                elif rand_n == 1:
                    MAP.ypixelmap[point_x][point_y-1] = False
                elif rand_n == 2:
                    MAP.ypixelmap[point_x+1][point_y] = False
                elif rand_n == 3:
                    MAP.ypixelmap[point_x-1][point_y] = False
                ret += 1
                IMAGER.write_map_to_image(MAP.ypixelmap)
            point_y += 1
        point_x += 1
    return ret

def remove_all_short_cicles_loop(_config):
    """ remove_all_short_cicles_loop """
    while remove_all_short_cicles(_config) > 0:
        pass

def find_short_point_from(_point0, _points):
    """ find_short_point_from """
    point_x0 = _point0['x']
    point_y0 = _point0['y']
    found_x1 = point_x0
    found_y1 = point_y0
    dist = len(MAP.ypixelmap) + len(MAP.ypixelmap[0]) + 1 # max dist
    for point1 in points:
        point_x1 = point1['x']
        point_y1 = point1['y']
        if point_x1 == point_x0 and point_y1 == point_y0:
            continue
        x_max = max(point_x0, point_x1)
        x_min = min(point_x0, point_x1)
        y_max = max(point_y0, point_y1)
        y_min = min(point_y0, point_y1)
        new_dist = (x_max - x_min) + (y_max - y_min)
        if new_dist < dist:
            dist = new_dist
            found_x1 = point_x1
            found_y1 = point_y1
    return {'x': found_x1, 'y': found_y1}

def connect_deadlocks_loop(_config):
    """ connect_deadlocks_loop """
    deadlocks = find_deadlock_points()
    len_deadlocks = len(deadlocks)
    safe_max_loop = 10
    safe_loop = 0
    while len_deadlocks > 0:
        safe_loop += 1
        if safe_loop > safe_max_loop:
            break
        if len_deadlocks == 1:
            point_x = deadlocks[0]['x']
            point_y = deadlocks[0]['y']
            safe_loop -= 1
            MAP.ypixelmap[point_x][point_y] = False
            IMAGER.write_map_to_image(MAP.ypixelmap)
        else:
            pn0 = randrange(len_deadlocks)
            point0 = deadlocks[pn0]
            point1 = find_short_point_from(point0, deadlocks)
            # print(p0, p1)
            connected = connect_points(_config, point0, point1)
            if connected == 0:
                safe_loop -= 1
                point_x = point0['x']
                point_y = point0['y']
                MAP.ypixelmap[point_x][point_y] = False
                IMAGER.write_map_to_image(MAP.ypixelmap)
            else:
                safe_loop -= 1
        deadlocks = find_deadlock_points()
        len_deadlocks = len(deadlocks)

def remove_deadlocks_loop(_config):
    """ remove_deadlocks_loop """
    deadlocks = find_deadlock_points()
    len_deadlocks = len(deadlocks)
    while len_deadlocks > 0:
        point_x = deadlocks[0]['x']
        point_y = deadlocks[0]['y']
        MAP.ypixelmap[point_x][point_y] = False
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
        TIPS = ""
        if not os.path.isfile('roadmapgen2d-config.json'):
            TIPS = "\n  Note: for create use a --create-example-config"
        sys.exit(
            "ERROR: could not load roadmapgen2d-config.json" + TIPS
        )

    IMAGER = RoadMapGen2dWriteMapToImage(config)
    MAP = RoadMapGen2dMap(config, IMAGER)
    mod_random = RoadMapGen2dModRandomPoints(config, IMAGER)

    if not os.path.isdir(".roads-generation"):
        os.mkdir('.roads-generation')

    os.system("rm -rf .roads-generation/*.png")

    with open('roadmapgen2d-config.json',) as file_map:
        data = json.load(file_map)
        mod_random.modify(MAP)
        print_map()
        move_diagonal_tails_loop(config)
        print_map()
        AGAIN = True
        while AGAIN:
            points = find_single_points()
            LEN_POINTS = len(points)
            if LEN_POINTS <= 1:
                AGAIN = False
                break
            print(LEN_POINTS)
            p0 = points[randrange(LEN_POINTS)]
            p1 = points[randrange(LEN_POINTS)]
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
        print_map()
        print("------- remove_rames -------")
        remove_rames(config)
        print_map()

        print("------- move_diagonal_tails_loop -------")
        move_diagonal_tails_loop(config)
        print_map()

        print("------- connect_deadlocks_loop -------")
        connect_deadlocks_loop(config)
        # move_diagonal_tails_loop(config)
        print_map()

        print("------- remove_all_short_cicles_loop -------")
        remove_all_short_cicles_loop(config)
        print_map()

        remove_rames(config)
        move_diagonal_tails_loop(config)
        remove_deadlocks_loop(config)
        remove_single_points(config)
        remove_rames(config)
        print_map()
        print("------- done -------")
        IMAGER.write_map_to_image(MAP.ypixelmap)
        print_map()

    print("All frames: " + str(IMAGER.get_number_of_frames()))
    FRAMES_PER_SECOND = 15

    # make video
    if os.path.isfile('video.avi'):
        os.remove('video.avi')

    IMAGER.write_last_frame_to_image(MAP.ypixelmap)

    if config.is_create_video():
        # last frame in last 5 seconds
        for _ in range(FRAMES_PER_SECOND*5):
            IMAGER.write_map_to_image(MAP.ypixelmap)

        print("Frames per second: " + str(FRAMES_PER_SECOND))
        FFMPEG_COMMAND = 'ffmpeg -f image2 -r ' + str(FRAMES_PER_SECOND)
        FFMPEG_COMMAND += ' -i .roads-generation/roadmap%06d.png video.mp4'
        os.system(FFMPEG_COMMAND)
