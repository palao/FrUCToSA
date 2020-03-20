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
from unittest.mock import patch

from fructosa.grafana.dashboard import make_dashboard
from fructosa.constants import (
    MAKE_DASHBOARD_DESCRIPTION, MAKE_DASHBOARD_HOSTS_HELP,
    HOSTS_FILE_STR, HOSTS_FILE_METAVAR,
    HOSTS_SECTION_SHORT_OPTION, HOSTS_SECTION_LONG_OPTION,
    HOSTS_SECTION_METAVAR, HOSTS_SECTION_HELP,
)
from fructosa.grafana.node import node_template_dict


@patch("fructosa.grafana.dashboard._collect_hosts")
@patch("fructosa.grafana.dashboard._render_dashboard_template")
@patch("fructosa.grafana.dashboard.CLConf")
@patch("fructosa.grafana.dashboard.json.dumps")
@patch("fructosa.grafana.dashboard.print")
class MakeDashboardTestCase(unittest.TestCase):
    def test_creates_CLConf_object(
            self, mprint, mdumps, pCLConf, mrender_template, mcollect_hosts):
        expected_args = (
            (
                "hosts",
                (
                    ("hosts",),
                    {
                        "metavar": HOSTS_FILE_METAVAR,
                        "help": MAKE_DASHBOARD_HOSTS_HELP
                    }
                )
            ),
            (
                "section",
                (
                    (HOSTS_SECTION_SHORT_OPTION, HOSTS_SECTION_LONG_OPTION),
                    {
                        "metavar": HOSTS_SECTION_METAVAR,
                        "help": HOSTS_SECTION_HELP
                    }
                )
            ),
        )
        make_dashboard()
            
        pCLConf.assert_called_once_with(
            description=MAKE_DASHBOARD_DESCRIPTION,
            arguments=expected_args,
        )

    def test_print_out_result(
            self, mprint, mdumps, pCLConf, mrender_template, mcollect_hosts):
        make_dashboard()
        mprint.assert_called_once_with(mdumps.return_value)

    def test_json_created_from_rendered_template(
            self, mprint, mdumps, pCLConf, mrender_template, mcollect_hosts):
        make_dashboard()
        mdumps.assert_called_once_with(mrender_template.return_value)

    def test_render_dashboard_template_called(
            self, mprint, mdumps, pCLConf, mrender_template,
            mcollect_hosts):
        make_dashboard()
        mrender_template.assert_called_once_with(mcollect_hosts.return_value)

    def test_collect_hosts_called(
            self, mprint, mdumps, pCLConf, mrender_template,
            mcollect_hosts):
        make_dashboard()
        mcollect_hosts.assert_called_once_with(pCLConf.return_value[HOSTS_FILE_STR])


class RenderDashboardTemplateTestCase(unittest.TestCase):
    def test_returns_result_of_what(self):
        self.fail()
