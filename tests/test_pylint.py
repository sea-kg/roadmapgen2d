#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test server api leaks"""

# Copyright (c) 2020 Evgenii Sopov <mrseakg@gmail.com>

# pylint: disable=relative-beyond-top-level,wrong-import-position,import-error

import os
from subprocess import Popen,PIPE,STDOUT

def test_pylint_library():
    """ Test pylint library """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    list_files_for_pylint = [
        '../roadmapgen2d/',
    ]
    for _filepath in list_files_for_pylint:
        _filepath = os.path.join(current_dir, _filepath)
        with Popen(
            ["python3", "-m", "pylint", _filepath],
            stderr=STDOUT,
            stdout=PIPE
        ) as p_out:
            output = p_out.communicate()[0]
            exit_code = p_out.returncode
            if exit_code != 0:
                print(output.decode("utf-8"))
            assert exit_code == 0
