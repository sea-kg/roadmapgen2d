"""Generic Setup script, takes package info from __pkginfo__.py file."""

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='roadmapgen2d',
    version='0.0.1',
    install_requires=[],
    keywords=['roadmap', 'generator', '2d'],
    author='Evgenii Sopov',
    author_email='mrseakg@gmail.com',
    description='Python App for Generating Roads 2d Maps',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sea-kg/roadmapgen2d',
    packages=['roadmapgen2d'],
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ),
    python_requires='>=3.6',
)
