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
    MAKE_DASHBOARD_DESCRIPTION, MAKE_DASHBOARD_HOSTS_HELP, HOSTS_FILE_METAVAR
)


class MakeDashboardTestCase(unittest.TestCase):
    def test_creates_CLConf_object(self):
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
        )
        with patch("fructosa.grafana.dashboard.CLConf") as pCLConf:
            make_dashboard()
            
        pCLConf.assert_called_once_with(
            description=MAKE_DASHBOARD_DESCRIPTION,
            arguments=expected_args,
        )
