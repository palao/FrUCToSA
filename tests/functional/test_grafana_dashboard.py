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

from fructosa.constants import (
    MAKE_DASHBOARD_PROGRAM, HOSTS_FILE_METAVAR, MAKE_DASHBOARD_HOSTS_HELP,
    HOSTS_SECTION_SHORT_OPTION, HOSTS_SECTION_LONG_OPTION,
    HOSTS_SECTION_METAVAR, HOSTS_SECTION_HELP,
    
)


make_fructosa_dashboard = functools.partial(run_program, MAKE_DASHBOARD_PROGRAM)


class CreationOfGrafanaDashboardsTestCase(unittest.TestCase):
    def test_executable_to_create_json_grafana_dashboards(self):
        uphosts = HOSTS_FILE_METAVAR
        hosts_help = MAKE_DASHBOARD_HOSTS_HELP
        short_section = HOSTS_SECTION_SHORT_OPTION
        long_section = HOSTS_SECTION_LONG_OPTION
        section_meta = HOSTS_SECTION_METAVAR
        section_help = HOSTS_SECTION_HELP
        #  After starting the FrUCToSA system, Tux would like to connect
        # it to Grafana. He finds out that there is an executable shipped
        # with the package that can create a dashboard importable by
        # Grafana. Great! Time to find out more about it:
        with make_fructosa_dashboard() as result_mk_fruct_dash:
            
            self.assertIn(
                f"the following arguments are required: {uphosts}",
                result_mk_fruct_dash.stderr.decode()
            )
        # Okay, okay. He tries the "-h" option:
        with make_fructosa_dashboard("-h") as result_mk_fruct_dash:
            # <streaming cl output>
            joined_out = result_mk_fruct_dash.stdout.decode().replace("\n", " ")
            while True:
                new_joined = joined_out.replace("\t", " ")
                new_new_joined = new_joined.replace("  ", " ")
                if new_new_joined == joined_out:
                    break
                else:
                    joined_out = new_new_joined
            # </streaming cl output>
            self.assertIn(
                f"positional arguments: {uphosts} {hosts_help}",
                joined_out
            )
            self.assertIn(
                (f"optional arguments: -h, --help show this help message and exit"
                 f" {short_section} {section_meta}"
                 f", {long_section} {section_meta} {section_help}"
                ),
                joined_out
            )
            # Fine, so he prepares a hosts file
        #...
        # and creates a dashboard from it:
        #...
        # it looks good. Let us try to validate it:
        # ...
        # Now he can import the created dashboard in Grafana and use it!
            
