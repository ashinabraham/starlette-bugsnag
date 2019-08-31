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


def get_long_description():
    """
    Return the README.
    """
    with open("README.md", encoding="utf8") as f:
        return f.read()


setup(
    name="starlette-bugsnag",
    python_requires=">=3.6",
    version=get_version("starlette_bugsnag"),
    url="https://github.com/ashinabraham/starlette-bugsnag",
    author="Ashin E Abraham",
    license="MIT",
    author_email="ashineabraham@gmail.com",
    data_files=[("", ["LICENSE"])],
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["bugsnag"],
    classifiers=[
        "Natural Language :: English",
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    zip_safe=False,
)
