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

import unittest
import functools

from .utils import run_program

from fructosa.constants import MAKE_DASHBOARD_PROGRAM


make_fructosa_dashboard = functools.partial(run_program, MAKE_DASHBOARD_PROGRAM)


class CreationOfGrafanaDashboardsTestCase(unittest.TestCase):
    def test_executable_to_create_json_grafana_dashboards(self):
        #  After starting the FrUCToSA system, Tux would like to connect
        # it to Grafana. He finds out that there is an executable shipped
        # with the package that can create a dashboard importable by
        # Grafana. Great! Time to find out more about it:
        with make_fructosa_dashboard("-h") as result_mk_fruct_dash:
            self.assertIn(
                "HOST file required",
                result_mk_fruct_dash.stdout.decode()
            )
