#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

from setuptools import setup, find_packages


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    with open(os.path.join(package, "__init__.py")) as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)


setup(
    name="starlette-bugsnag",
    python_requires=">=3.6",
    version=get_version("starlette_bugsnag"),
    url="https://github.com/ashinabraham/starlette-bugsnag",
    author="Ashin E Abraham",
    license="MIT",
    author_email="ashineabraham@gmail.com",
    data_files=[("", ["LICENSE"])],
    packages=find_packages(),
    install_requires=["bugsnag"],
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    zip_safe=False,
)
