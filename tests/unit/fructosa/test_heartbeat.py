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
from unittest.mock import MagicMock, patch

from fructosa.heartbeat import HeartbeatClientProtocol


class HeartbeatClientProtocolTestCase(unittest.TestCase):
    def setUp(self):
        self.on_con_lost = "funny future"
        self.logging_conf = MagicMock()
        with patch("fructosa.heartbeat.setup_logging") as psetup_logging:
            self.proto = HeartbeatClientProtocol(
                self.on_con_lost, self.logging_conf
            )
        self.psetup_logging = psetup_logging

    def test_intance_creation_sets_needed_attributes(self):
        self.assertEqual(self.proto._counter, 0)
        self.assertEqual(self.proto.on_con_lost, self.on_con_lost)
        self.assertIs(self.proto.transport, None)
        self.assertEqual(self.proto.logger, self.psetup_logging.return_value)

    def test_instance_init_sets_up_logging_properly(self):
        self.psetup_logging.assert_called_once_with(
            self.proto.__class__.__name__, rotatingfile_conf=self.logging_conf
        )
        
    def test_connection_made(self):
        transport = MagicMock()
        self.proto.connection_made(transport)
        self.assertEqual(self.proto.transport, transport)
        transport.sendto.assert_called_once_with(self.proto.message)
        self.proto.logger.info.assert_called_once_with("caca")
