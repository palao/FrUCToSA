#!/bin/env python3

#######################################################################
#
# Copyright (C) 2020 David Palao
#
# This file is part of FrUCToSA.
#
#  FrUCToSA is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  FrUCToSA is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with FrUCToSA.  If not, see <http://www.gnu.org/licenses/>.
#
#######################################################################


"""Script that replaces rename file names removing .back suffixes.
"""

import sys
import argparse
import os
from glob import iglob, glob
import shutil

SUFFIX = ".back"
PATTERNS = ("**/*"+SUFFIX,)


def parse_conf():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directories', metavar='DIRs', type=str, nargs='+',
                        help='space separated list of target input directories')
    args = parser.parse_args()
    return args

def collect_files(conf):
    files = set()
    for rootd in conf.directories:
        for pat in PATTERNS:
            for e in iglob(os.path.join(rootd, pat), recursive=True):
                if os.path.isfile(e):
                    files.add(e)
                else:
                    print("*** Unknwon type of file:", e)
    return files

def restore_backup(filename):
    if filename.endswith(".back"):
        new_filename = filename[:-5]
        shutil.move(filename, new_filename)

def main():
    conf = parse_conf()
    target_files = collect_files(conf)
    for target_file in target_files:
        restore_backup(target_file)

    
if __name__ == "__main__":
    sys.exit(main())
