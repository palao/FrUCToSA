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

import json

from ..ui.cl import CLConf
from ..constants import (
    MAKE_DASHBOARD_DESCRIPTION, MAKE_DASHBOARD_HOSTS_HELP, HOSTS_FILE_STR,
    HOSTS_FILE_METAVAR, HOSTS_SECTION_STR, HOSTS_SECTION_SHORT_OPTION,
    HOSTS_SECTION_LONG_OPTION, HOSTS_SECTION_METAVAR, HOSTS_SECTION_HELP,
)


HOSTS_FILE_ARG = (
    HOSTS_FILE_STR,
    ((HOSTS_FILE_STR,),
         dict(help=MAKE_DASHBOARD_HOSTS_HELP, metavar=HOSTS_FILE_METAVAR))
)
HOSTS_SECTION_ARG = (
    HOSTS_SECTION_STR,
    ((HOSTS_SECTION_SHORT_OPTION, HOSTS_SECTION_LONG_OPTION),
         dict(help=HOSTS_SECTION_HELP, metavar=HOSTS_SECTION_METAVAR))
)


def _collect_hosts():
    pass


def _render_dashboard_template():
    pass


def make_dashboard():
    conf = CLConf(
        description=MAKE_DASHBOARD_DESCRIPTION,
        arguments=(HOSTS_FILE_ARG, HOSTS_SECTION_ARG)
    )
    hosts = _collect_hosts(conf[HOSTS_FILE_STR])
    dashboard_dict = _render_dashboard_template(hosts)
    dashboard_json = json.dumps(dashboard_dict)
    print(dashboard_json)
