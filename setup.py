#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="starlette_bugsnag",
    python_requires=">=3.6",
    url="https://github.com/ashinabraham/starlette-bugsnag",
    author="Ashin E Abraham",
    license='MIT',
    author_email="ashineabraham@gmail.com",
    data_files=[("", ["LICENSE"])],
    packages=find_packages(),
    install_requires=['bugsnag'],
    classifiers=[
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ]
)
