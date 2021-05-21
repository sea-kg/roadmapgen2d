#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Evgenii sopov <mrseakg@gmail.com>

"""Library for roadmapgen2d"""

import os
import sys
from roadmapgen2d.roadmapgen2d import RoadMapGen2D
from roadmapgen2d.__pkginfo__ import version
from roadmapgen2d.__pkginfo__ import name

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit('ERROR: Expected argument. Try --help for mor details')

    if sys.argv[1] == '--version':
        print(name + ' v' + version)
        sys.exit(0)
    if sys.argv[1] == '--help':
        print("""
""" + name + ' v' + version + """
Arg can be:
--version - print version
--help - print help
""")
        sys.exit(0)

    ROOT_DIR = os.path.abspath(sys.argv[1])
    if not os.path.isdir(ROOT_DIR):
        sys.exit('ERROR: Directory "' + sys.argv[1] + '" did not exists.')

    print("Start on dir: " + ROOT_DIR)

    # TODO
    sys.exit(0)
