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


"""Script that replaces strings coming from the QULo project and converts them 
to a convenient form for the FrUCToSA project.
"""

import sys
import argparse
import os
from glob import iglob
import shutil

PATTERNS = ("**/*.py", "**/*.conf")


def parse_conf():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directories', metavar='DIRs', type=str, nargs='+',
                        help='space separated list of target input directories')
    parser.add_argument("-w", '--write', dest='write', action='store_true',
                        default=False, help='Write back modified files')
    args = parser.parse_args()
    return args

def collect_files(conf):
    files = set()
    for rootd in conf.directories:
        for pat in PATTERNS:
            for e in iglob(os.path.join(rootd, pat), recursive=True):
                files.add(e)
    return files

def backup(filename):
    new_filename = filename+".back"
    shutil.copy2(filename, new_filename)

def read_file(target_file):
    with open(target_file) as f:
        for l in f:
            yield l

def fix_copyright(lines):
    for l in lines:
        if l.startswith("# Copyright (C)"):
            yield "# Copyright (C) 2020 David Palao\n"
        else:
            yield l

def fix_package_name(lines):
    for l in lines:
        yield l.replace("QULo", "FrUCToSA")
        
def fix_qagent(lines):
    for l in lines:
        yield l.replace("qagent", "lagent").replace("QAgent", "LAgent").replace("QAGENT", "LAGENT")
        
def fix_qmaster(lines):
    for l in lines:
        yield l.replace("qmaster", "lmaster").replace("QMaster", "LMaster").replace("QMASTER", "LMASTER")
        
def fix_qulo(lines):
    for l in lines:
        yield l.replace("qulo", "fructosa").replace("Qulo", "Fructosa").replace("QULO", "FRUCTOSA")

        
def process_file(target_file, do_write):
    if do_write:
        backup(target_file)
    raw = read_file(target_file)
    copyright_fixed = fix_copyright(raw)
    name_fixed = fix_package_name(copyright_fixed)
    qagent_replaced = fix_qagent(name_fixed)
    # for l in raw:
    #     print(l.strip())
    
    
def main():
    conf = parse_conf()
    target_files = collect_files(conf)
    for target_file in target_files:
        process_file(target_file, conf.write)

    
if __name__ == "__main__":
    sys.exit(main())
