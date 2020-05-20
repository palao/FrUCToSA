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
from unittest.mock import MagicMock, Mock, patch

from fructosa.heartbeat import HeartbeatClientProtocol, encode_beat_number


class HeartbeatClientProtocolTestCase(unittest.TestCase):
    def setUp(self):
        self.on_con_lost = "funny future"
        self.logging_conf = MagicMock()
        with patch("fructosa.heartbeat.setup_logging") as psetup_logging:
            self.proto = HeartbeatClientProtocol(
                self.on_con_lost, self.logging_conf
            )
        self.psetup_logging = psetup_logging

    def tearDown(self):
        HeartbeatClientProtocol._next_beat_number = 0
        
    def test_intance_creation_sets_needed_attributes(self):
        self.assertEqual(self.proto.beat_number, 0)
        self.assertEqual(self.proto.on_con_lost, self.on_con_lost)
        self.assertIs(self.proto.transport, None)
        self.assertEqual(self.proto.logger, self.psetup_logging.return_value)

    def test_instance_init_sets_up_logging_properly(self):
        self.psetup_logging.assert_called_once_with(
            self.proto.__class__.__name__, rotatingfile_conf=self.logging_conf
        )
        
    def test_connection_made_increases_beat_number(self):
        mock_transport = Mock()
        self.proto.connection_made(mock_transport)
        self.proto.connection_made(mock_transport)
        self.assertEqual(self.proto.beat_number, 2)
        
    def test_connection_made_from_another_instance_increases_beat_number(self):
        with patch("fructosa.heartbeat.setup_logging") as psetup_logging:
            mock_transport = Mock()
            self.proto.connection_made(mock_transport)
            another_proto = HeartbeatClientProtocol(
                self.on_con_lost, self.logging_conf
            )
        self.assertEqual(another_proto.beat_number, self.proto.beat_number)
        
    # def test_connection_made_increases_beat_number_even_if_error(self):
    #     mock_transport = Mock()
    #     class MyException(Exception): pass
    #     mock_transport.sendto.side_effect = MyException()
    #     self.proto.connection_made(mock_transport)
    #     self.assertEqual(self.proto.beat_number, 1)
        
    def test_connection_made(self):
        transport = MagicMock()
        msg = self.proto.message
        self.proto.connection_made(transport)
        self.assertEqual(self.proto.transport, transport)
        transport.sendto.assert_called_once_with(msg)
        self.proto.logger.info.assert_called_once_with("caca")
        self.proto.transport.close.assert_called_once_with()
        
    def test_message(self):
        with patch("fructosa.heartbeat.encode_beat_number") as pencode:
            res = self.proto.message
        pencode.assert_called_once_with(self.proto.beat_number)
        self.assertEqual(res, pencode.return_value)

    def test_connection_lost(self):
        self.proto.connection_lost(Mock())
        

class EncodeBeatNumberTestCase(unittest.TestCase):
    def test_result(self):
        raw_number = Mock()
        result = encode_beat_number(raw_number)
        raw_number.to_bytes.assert_called_once_with(
            length=64, byteorder="big", signed=False
        )
        self.assertEqual(result, raw_number.to_bytes.return_value)
