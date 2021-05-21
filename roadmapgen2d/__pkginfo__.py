#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2021 Evgenii Sopov <mrseakg@gmail.com>

# pylint: disable=redefined-builtin,invalid-name

"""roadmapgen2d packaging information"""

# For an official release, use dev_version = None
numversion = (0, 0, 1)

version = ".".join(str(num) for num in numversion)
name = "roadmapgen2d"

dependency_links = []

license = "MIT"
description = "Road Map Generate for 2d Maps"
web = "https://github.com/sea-kg/roadmapgen2d"
mailinglist = "mailto:mrseakg@gmail.com"
author = "Evgenii Sopov"
author_email = "mrseakg@gmail.com"

classifiers = [
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: Implementation :: PyPy"
]
