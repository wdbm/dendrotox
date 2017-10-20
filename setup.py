#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import setuptools

def main():

    setuptools.setup(
        name             = "dendrotox",
        version          = "2017.10.20.0010",
        description      = "Python interface to Tox distributed communications",
        long_description = long_description(),
        url              = "https://github.com/wdbm/dendrotox",
        author           = "Will Breaden Madden",
        author_email     = "wbm@protonmail.ch",
        license          = "GPLv3",
        py_modules       = [
                           "dendrotox"
                           ],
        install_requires = [
                           "docopt",
                           "megaparsex",
                           ],
        scripts          = [
                           "dendrotox.py",
                           "dendrotox_alert.py"
                           ],
        entry_points     = """
                           [console_scripts]
                           dendrotox = dendrotox:dendrotox
                           """
    )

def long_description(
    filename = "README.md"
    ):

    if os.path.isfile(os.path.expandvars(filename)):
        try:
            import pypandoc
            long_description = pypandoc.convert_file(filename, "rst")
        except ImportError:
            long_description = open(filename).read()
    else:
        long_description = ""
    return long_description

if __name__ == "__main__":
    main()
