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
from unittest.mock import MagicMock

from fructosa.heartbeat import HeartbeatClientProtocol


class HeartbeatClientProtocolTestCase(unittest.TestCase):
    def setUp(self):
        self.on_con_lost = "funny future"
        self.msg = MagicMock()
        self.proto = HeartbeatClientProtocol(self.msg, self.on_con_lost)
        
    def test_intance_creation(self):
        self.assertEqual(self.proto.message, self.msg)
        self.assertEqual(self.proto.on_con_lost, self.on_con_lost)
        self.assertIs(self.proto.transport, None)

    def test_connection_made(self):
        transport = MagicMock()
        self.connection_made(transport)
        self.assertEqual(self.proto.transport, transport)
        transport.sendto.assert_called_once_with(self.proto.msg.encode())
