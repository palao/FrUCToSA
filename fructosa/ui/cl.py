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

import argparse


class CLConf:
    def __init__(self, description, arguments, defaults):
        self.description = description
        self.arguments = arguments
        self.defaults = defaults
        self._create_cl_parser()
        self._add_arguments()
        self._parse_arguments()

    def _create_cl_parser(self):
        parser = argparse.ArgumentParser(description=self.description)
        self._cl_parser = parser

    def _add_arguments(self):
        for name, arg in self.arguments:
            args, kwargs = arg
            if name in self.defaults:
                kwargs["default"] = self.defaults[name]
            self._cl_parser.add_argument(*args, **kwargs)

    def _parse_arguments(self):
        args = self._cl_parser.parse_args()
        self._command_line_conf = vars(args)

