# roadmapgen2d

[![PyPI version](https://badge.fury.io/py/roadmapgen2d.svg)](https://badge.fury.io/py/roadmapgen2d) [![Build Status](https://api.travis-ci.com/sea-kg/roadmapgen2d.svg?branch=main)](https://travis-ci.com/sea-kg/roadmapgen2d) [![Total alerts](https://img.shields.io/lgtm/alerts/g/sea-kg/roadmapgen2d.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/sea-kg/roadmapgen2d/alerts/) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/sea-kg/roadmapgen2d.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/sea-kg/roadmapgen2d/context:python) 

Road Map Generator for 2d Maps

![screen](https://raw.githubusercontent.com/sea-kg/roadmapgen2d/main/screen.png)

## Install

```
$ pip3 install roadmapgen2d
```
or 
```
$ pip3 install --upgrade roadmapgen2d
```

Create the some dir with file `roadmapgen2d-config.json`:
```
{
    "map-width-px": 5000,
    "map-height-px": 5000,
    "texture-tail-road-width-px": 120,
    "texture-tail-road-height-px": 120,
    "texture-path": "textures/road0.png",
    "random-max-points": 100,
    "color-hex-background": "000000",
    "color-hex-line-road": "FFFFFF",
    "color-line-road-use-gradient": false,
    "create-video": false,
    "create-last-frame-as-image": true
}
```

And than in this directory run:
```
$ python3 -m roadmapgen2d .
```

## Create video for algorithm work

Requirements:

* ffmpeg

How it works:

In this progress, script will be write frames (step by step) to `.roads-generation/.roads-generation/roadmap*.png`

and then script will be call `ffmpeg` command:

```
ffmpeg -f image2 -r 15 -i .roads-generation/roadmap%06d.png video.mp4
```
