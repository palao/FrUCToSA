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

from inspect import iscoroutinefunction
import unittest
from unittest.mock import MagicMock, Mock, patch
import asyncio

from .aio_tools import AsyncioMock, asyncio_run

from fructosa.heartbeat import (
    HeartbeatProtocolFactory,
    HeartbeatClientProtocol, HeartbeatServerProtocol,
    HeartbeatSource,
    encode_beat_number, decode_beat_number,
)

from fructosa.constants import (
    HEARTBEAT_RECEIVE_MSG_TEMPLATE, HEARTBEAT_SEND_MSG_TEMPLATE,
    HEARTBEAT_INTERVAL_SECONDS
)


class InventedException(Exception):
    ...
    

class HeartbeatClientProtocolFactoryTestCase(unittest.TestCase):
    def setUp(self):
        self.protocol_class = Mock()
        self.logging_conf = MagicMock()
        with patch("fructosa.heartbeat.setup_logging") as psetup_logging:
            self.factory = HeartbeatProtocolFactory(
                self.protocol_class, self.logging_conf
            )
        self.psetup_logging = psetup_logging

    def test_intance_creation_defines_needed_attributes(self):
        self.assertEqual(self.factory._protocol_class, self.protocol_class)
        self.assertEqual(self.factory.logger, self.psetup_logging.return_value)

    def test_instance_init_sets_up_logging_properly(self):
        self.psetup_logging.assert_called_once_with(
            "Heartbeat", rotatingfile_conf=self.logging_conf
        )

    def test_instance_calls_return_protocol_instance(self):
        proto = self.factory()
        self.assertEqual(proto, self.factory._protocol_class.return_value)
        self.factory._protocol_class.assert_called_once_with(
            self.factory.logger
        )


class HeartbeatClientProtocolTestCase(unittest.TestCase):
    def setUp(self):
        self.logger = MagicMock()
        self.future = Mock()
        with patch("fructosa.heartbeat.asyncio.get_running_loop") as mloop:
            mloop.return_value.create_future.return_value = self.future
            self.proto = HeartbeatClientProtocol(self.logger)
        self.mloop = mloop
        
    def tearDown(self):
        HeartbeatClientProtocol._next_beat_number = 0

    def test_intance_creation_defines_needed_attributes(self):
        self.assertEqual(self.proto.beat_number, 0)
        self.assertEqual(self.proto.on_sent, self.future)
        self.assertIs(self.proto.transport, None)
        self.assertEqual(self.proto.logger, self.logger)

    def test_connection_made_increases_beat_number(self):
        mock_transport = Mock()
        self.proto.connection_made(mock_transport)
        self.proto.connection_made(mock_transport)
        self.assertEqual(self.proto.beat_number, 2)
        
    def test_connection_made_from_another_instance_increases_beat_number(self):
        mock_transport = Mock()
        self.proto.connection_made(mock_transport)
        with patch(
                "fructosa.heartbeat.asyncio.get_running_loop", new=self.mloop):
            another_proto = HeartbeatClientProtocol(self.logger)
        self.assertEqual(another_proto.beat_number, self.proto.beat_number)

    ######################################################################
    # I'd like to have this test, but I think I need a FT to justify it:
    # def test_connection_made_increases_beat_number_even_if_error(self):
    #     mock_transport = Mock()
    #     class MyException(Exception): pass
    #     mock_transport.sendto.side_effect = MyException()
    #     self.proto.connection_made(mock_transport)
    #     self.assertEqual(self.proto.beat_number, 1)
        
    def test_connection_made(self):
        transport = MagicMock()
        msg = self.proto.message
        expected_beat_number = self.proto.beat_number
        self.proto.connection_made(transport)
        self.assertEqual(self.proto.transport, transport)
        transport.sendto.assert_called_once_with(msg)
        expected_msg = HEARTBEAT_SEND_MSG_TEMPLATE.format(
            message_number=expected_beat_number)
        self.proto.logger.info.assert_called_once_with(expected_msg)
        self.proto.on_sent.set_result.assert_called_once_with(True)
        
    def test_message(self):
        with patch("fructosa.heartbeat.encode_beat_number") as pencode:
            res = self.proto.message
        pencode.assert_called_once_with(self.proto.beat_number)
        self.assertEqual(res, pencode.return_value)


class HeartbeatServerProtocolTestCase(unittest.TestCase):
    def setUp(self):
        self.logger = MagicMock()
        self.proto = HeartbeatServerProtocol(self.logger)

    def test_intance_creation_sets_needed_attributes(self):
        self.assertEqual(self.proto.logger, self.logger)

    def test_connection_made_sets_transport(self):
        with self.assertRaises(AttributeError):
            self.proto.transport
        transport = Mock()
        self.proto.connection_made(transport)
        self.assertEqual(self.proto.transport, transport)

    def test_datagram_received(self):
        num = 2348
        data = Mock()
        addr = "remote-host"
        expected_msg = HEARTBEAT_RECEIVE_MSG_TEMPLATE.format(
            host=addr, message_number=num
        )
        with patch("fructosa.heartbeat.decode_beat_number") as pdecode:
            pdecode.return_value = num
            self.proto.datagram_received(data, addr)
        pdecode.assert_called_once_with(data)
        self.proto.logger.info.assert_called_once_with(expected_msg)


class EncodeBeatNumberTestCase(unittest.TestCase):
    def test_result(self):
        raw_number = Mock()
        result = encode_beat_number(raw_number)
        raw_number.to_bytes.assert_called_once_with(
            length=64, byteorder="big", signed=False
        )
        self.assertEqual(result, raw_number.to_bytes.return_value)


class DecodeBeatNumberTestCase(unittest.TestCase):
    def test_result(self):
        test_nums = [234, 44, 0, 132948]
        for num in test_nums:
            data = encode_beat_number(num)
            with self.subTest(data=data, expected=num):
                result = decode_beat_number(data)
                self.assertEqual(result, num)


class HeartbeatSourceTestCase(unittest.TestCase):
    def setUp(self):
        self.host = "culandron"
        self.port = 34569
        self.logging_conf = "my logging conf"
        with patch("fructosa.heartbeat.setup_logging") as psetup_logging:
            with patch("fructosa.heartbeat.HeartbeatProtocolFactory") as hbpf:
                self.instance = HeartbeatSource(
                    dest_host=self.host, dest_port=self.port,
                    logging_conf=self.logging_conf
                )
        self.psetup_logging = psetup_logging
        self.hb_factory = hbpf

    def create_one_usage_instance(self):
        with patch("fructosa.heartbeat.setup_logging") as psetup_logging:
            with patch("fructosa.heartbeat.HeartbeatProtocolFactory") as hbpf:
                instance = HeartbeatSource(
                    dest_host=self.host, dest_port=self.port,
                    logging_conf=self.logging_conf
                )
        return instance
    
    def test_instance_sets_attributes_from_input(self):
        self.assertEqual(self.instance._host, self.host)
        self.assertEqual(self.instance._port, self.port)
        self.assertEqual(
            self.instance._logger, self.psetup_logging.return_value
        )
        self.assertEqual(
            self.instance._hb_factory,
            self.hb_factory.return_value
        )
        
    def test_logging_properly_configured(self):
        self.psetup_logging.assert_called_once_with(
            "Heartbeat", rotatingfile_conf=self.logging_conf
        )

    def test_hb_factory_correctly_called(self):
        self.hb_factory.assert_called_once_with(
            HeartbeatClientProtocol, self.logging_conf
        )
        
    def test_call_is_coroutine(self):
        self.assertTrue(iscoroutinefunction(self.instance.__call__))

    def test_call_sequence_step1(self):
        instance = self.create_one_usage_instance()
        pcreate_datagram_endpoint = AsyncioMock(
            side_effect=InventedException()
        )
        instance.create_datagram_endpoint = pcreate_datagram_endpoint
        with self.assertRaises(InventedException):
            asyncio_run(instance())

    def test_call_sequence_step2(self):
        instance = self.create_one_usage_instance()
        pcreate_datagram_endpoint = AsyncioMock()
        pcomplete_sending = AsyncioMock(
            side_effect=InventedException()
        )
        instance.create_datagram_endpoint = pcreate_datagram_endpoint
        instance.complete_sending = pcomplete_sending
        with self.assertRaises(InventedException):
            asyncio_run(instance())

    def test_call_sequence_step3(self):
        instance = self.create_one_usage_instance()
        pcreate_datagram_endpoint = AsyncioMock()
        pcomplete_sending = AsyncioMock()
        psleep = AsyncioMock(side_effect=InventedException())
        instance.create_datagram_endpoint = pcreate_datagram_endpoint
        instance.complete_sending = pcomplete_sending
        with patch("fructosa.heartbeat.asyncio.sleep", new=psleep):
            with self.assertRaises(InventedException):
                asyncio_run(instance())
        psleep.mock.assert_called_once_with(HEARTBEAT_INTERVAL_SECONDS)
        
    def test_create_datagram_endpoint_is_coroutine(self):
        self.assertTrue(
            iscoroutinefunction(self.instance.create_datagram_endpoint)
        )

    def test_create_datagram_endpoint_sets_transport_and_protocol(self):
        create_datagram_endpoint = AsyncioMock()
        protocol = MagicMock()
        transport = MagicMock()
        def fake_cde(factory, remote_addr):
            return transport, protocol
        create_datagram_endpoint.mock.side_effect = fake_cde
        loop = asyncio.get_event_loop()
        loop.create_datagram_endpoint = create_datagram_endpoint
        asyncio_run(self.instance.create_datagram_endpoint())
        self.assertEqual(self.instance._transport, transport)
        self.assertEqual(self.instance._protocol, protocol)

    def test_future_method_returns_protocols_future(self):
        instance = self.create_one_usage_instance()
        instance._protocol = MagicMock()
        self.assertEqual(
            instance._protocol.on_sent,
            instance.future()
        )
    def test_complete_sending_is_coroutine(self):
        self.assertTrue(
            iscoroutinefunction(self.instance.complete_sending)
        )

    def test_complete_sending_closes_transport(self):
        pfuture = AsyncioMock()
        instance = self.create_one_usage_instance()
        instance._transport = MagicMock()
        instance._protocol = Mock()
        instance._protocol.on_sent = AsyncioMock()
        with patch("fructosa.heartbeat.HeartbeatSource.future", new=pfuture):
            asyncio_run(instance.complete_sending())
        instance._transport.close.assert_called_once_with()

    def test_complete_sending_closes_transport_even_if_exception(self):
        pfuture = AsyncioMock(side_effect=InventedException())
        instance = self.create_one_usage_instance()
        instance._transport = MagicMock()
        with patch("fructosa.heartbeat.HeartbeatSource.future", new=pfuture):
            with self.assertRaises(InventedException):
                asyncio_run(instance.complete_sending())
        instance._transport.close.assert_called_once_with()
        
    def test_complete_sending_awaits_for_on_sent(self):
        pfuture = AsyncioMock(side_effect=InventedException())
        instance = self.create_one_usage_instance()
        instance._transport = MagicMock()
        with patch("fructosa.heartbeat.HeartbeatSource.future", new=pfuture):
            with self.assertRaises(InventedException):
                asyncio_run(instance.complete_sending())


