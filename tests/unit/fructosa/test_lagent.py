#!/bin/env python

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
from unittest.mock import patch, MagicMock, call, mock_open, PropertyMock
from inspect import signature, Parameter
import logging

from tests.unit.fructosa.aio_tools import asyncio_run, AsyncioMock

import fructosa.lagent
from fructosa.constants import (
    LAGENT_TO_LMASTER_DATA_PORT_KEY, LMASTER_HOST_KEY,
    LAGENT_TO_LMASTER_CONNECTING_MSG, LAGENT_TO_LMASTER_CONNECTED_MSG,
    ACTION_STR, PIDFILE_STR, OWN_LOG_FILE_KEY, OWN_LOG_SECTION, 
)


class InventedException(Exception):
    pass


class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.main = fructosa.lagent.main
        
    def test_is_executable(self):
        self.assertIn("__call__", dir(self.main))

    def test_takes_no_arguments(self):
        s = signature(self.main)
        parameters = s.parameters
        self.assertEqual(len(parameters), 0)

    @patch("fructosa.lagent.generic_main")
    @patch("fructosa.lagent.LAgent")
    @patch("fructosa.lagent.LAgentConf")
    def test_calls_generic_main(self, pagentconf, pagent, pgeneric_main):
        self.main()
        pgeneric_main.assert_called_once_with(pagentconf, pagent)

        
class LAgentTestCase(unittest.TestCase):
    def setUp(self):
        self.test_class = fructosa.lagent.LAgent
        self.mocked_conf = MagicMock()
        setattr(self.mocked_conf, ACTION_STR, "")
        setattr(self.mocked_conf, PIDFILE_STR, "")
        self.simple_logging = {OWN_LOG_FILE_KEY: "/dev/null"}
        setattr(self.mocked_conf, OWN_LOG_SECTION, self.simple_logging)
        self.simple_instance = self.test_class(self.mocked_conf)

    def test_LAgent_is_subclass_of_FructosaD(self):
        from fructosa.fructosad import FructosaD
        self.assertTrue(issubclass(self.test_class, FructosaD))

    def test_instance_defines_some_strings(self):
        from fructosa.lagent import (
            LAGENT_STARTING_MESSAGE, LAGENT_STOP_MESSAGE, LAGENT_CANT_STOP_MESSAGE
        )
        inst = self.simple_instance
        self.assertEqual(inst._starting_message, LAGENT_STARTING_MESSAGE)
        self.assertEqual(inst._stopped_message, LAGENT_STOP_MESSAGE)
        self.assertEqual(inst._cant_stop_message, LAGENT_CANT_STOP_MESSAGE)

    def test_instance_sensors_attribute_defined_from_conf(self):
        sensors = MagicMock()
        self.mocked_conf.sensors = sensors
        instance = self.test_class(self.mocked_conf)
        instance._conf = self.mocked_conf
        self.assertEqual(instance.sensors, sensors)

    @patch("fructosa.lagent.asyncio.Queue")
    def test_init_created_queues(self, pQueue):
        #queue = MagicMock()
        #pQueue.return_value = queue
        conf = self.mocked_conf
        expected_calls = [call(), call()]
        instance = self.test_class(conf)
        pQueue.assert_has_calls(expected_calls)

    @patch("fructosa.lagent.asyncio.Queue")
    def test_init_created_sensors_queue_and_to_master_queue(self, pQueue):
        sensors_queue = MagicMock()
        to_master_queue = MagicMock()
        pQueue.side_effect = [sensors_queue, to_master_queue]
        instance = self.test_class(self.mocked_conf)
        self.assertEqual(instance._sensors_queue, sensors_queue)
        self.assertEqual(instance._to_master_queue, to_master_queue)

    @patch("fructosa.lagent.FructosaD.__init__")
    def test_init_calls_super_init(self, pinit):
        conf = MagicMock()
        instance = self.test_class(conf)
        pinit.assert_called_once_with(conf)
        
    @patch("fructosa.lagent.FructosaD.run")
    @patch("fructosa.lagent.LAgent.submit_task")
    def test_run_calls_submit_task_for_each_sensor(self, psubmit_task, prun):
        sensors_collection = [[MagicMock() for _ in range(num)] for num in range(4)]
        mocked_sensors = PropertyMock()
        type(self.simple_instance).sensors = mocked_sensors
        for sensors in sensors_collection:
            expected_calls = [call(sensor, self.simple_instance._sensors_queue) for sensor in sensors]
            mocked_sensors.return_value = sensors
            #self.simple_instance.sensors = sensors
            self.simple_instance.run()
            psubmit_task.assert_has_calls(expected_calls, any_order=True)

    @patch("fructosa.lagent.LAgent.report_data")
    @patch("fructosa.lagent.FructosaD.run")
    @patch("fructosa.lagent.LAgent.submit_task")
    def test_run_calls_submit_task_with_report_data(self, psubmit_task, prun, report_data):
        mocked_sensors = PropertyMock()
        type(self.simple_instance).sensors = mocked_sensors
        self.simple_instance.run()
        psubmit_task.assert_has_calls([call(self.simple_instance.report_data)])
        
    @patch("fructosa.lagent.LAgent.send_to_master")
    @patch("fructosa.lagent.FructosaD.run")
    @patch("fructosa.lagent.LAgent.submit_task")
    def test_run_calls_submit_task_with_send_to_master(self, psubmit_task, prun, send_to_master):
        mocked_sensors = PropertyMock()
        type(self.simple_instance).sensors = mocked_sensors
        self.simple_instance.run()
        psubmit_task.assert_has_calls([call(self.simple_instance.send_to_master)])
        
    @patch("fructosa.lagent.FructosaD.run")
    @patch("fructosa.lagent.LAgent.submit_task")
    def test_run_calls_fructosad_run(self, psubmit_task, prun):
        mocked_sensors = PropertyMock()
        type(self.simple_instance).sensors = mocked_sensors
        self.simple_instance.run()
        prun.assert_called_once_with()
        
    def test_sensors_is_property(self):
        sensors = MagicMock()
        mocked_sensors = PropertyMock(return_value=sensors)
        type(self.simple_instance).sensors = mocked_sensors
        self.simple_instance.sensors
        mocked_sensors.assert_called_once_with()

    def test_report_data_is_a_coroutine(self):
        from inspect import iscoroutinefunction
        self.assertTrue(iscoroutinefunction(self.test_class.report_data))

    @patch("fructosa.lagent.pickle.dumps")
    def test_report_data_awaits_in_queue_get_and_out_queue_put(self, dumps):
        import pickle
        self.simple_instance._sensors_queue = MagicMock()
        self.simple_instance._to_master_queue = MagicMock()
        for num in 4,1,3:
            values = [MagicMock() for _ in range(num)] + [InventedException()]
            dumped_values = [MagicMock() for _ in range(num)] + [InventedException()]
            dumps.side_effect = dumped_values[:-1]
            self.simple_instance._sensors_queue.get = AsyncioMock(side_effect=values)
            self.simple_instance._to_master_queue.put = AsyncioMock()
            expected_calls_get = [call() for value in values[:-1]]
            expected_calls_put = [call(value) for value in dumped_values[:-1]]
            with self.assertRaises(InventedException):
                asyncio_run(self.simple_instance.report_data())
            self.simple_instance._sensors_queue.get.mock.assert_has_calls(expected_calls_get)
            self.simple_instance._to_master_queue.put.mock.assert_has_calls(expected_calls_put)
            self.simple_instance._sensors_queue.get.mock.reset_mock()
            self.simple_instance._to_master_queue.put.mock.reset_mock()

    @patch("fructosa.lagent.pickle.dumps")
    def test_report_data_logs_data_from_queue(self, dumps):
        from fructosa.constants import PROTO_MEASUREMENT_MSG
        in_queue = MagicMock()
        out_queue = MagicMock()
        log = MagicMock()
        self.simple_instance.logger = log
        for num in 3,2,1,5:
            values = [MagicMock() for _ in range(num)] + [InventedException()]
            dumped_values = [MagicMock() for _ in range(num)] + [InventedException()]
            dumps.side_effect = dumped_values[:-1]
            in_queue.get = AsyncioMock(side_effect=values)
            out_queue.put = AsyncioMock()
            self.simple_instance._sensors_queue = in_queue
            self.simple_instance._to_master_queue = out_queue
            expected_calls = [
                call(PROTO_MEASUREMENT_MSG.format(value)) for value in values[:-1]
            ]
            with self.assertRaises(InventedException):
                asyncio_run(self.simple_instance.report_data())
            log.debug.assert_has_calls(expected_calls)
            log.debug.reset_mock()

    def test_send_to_master_is_a_coroutine(self):
        from inspect import iscoroutinefunction
        self.assertTrue(iscoroutinefunction(self.test_class.send_to_master))

    def test_send_to_master_awaits_in_queue_get(self):
        with patch(
                "fructosa.lagent.asyncio.open_connection", new=AsyncioMock()
                ) as open_connection:
            reader = MagicMock()
            writer = MagicMock()
            open_connection.mock.return_value = (reader, writer)
            self.simple_instance._to_master_queue = MagicMock()
            for num in 2,5,1:
                values = [MagicMock() for _ in range(num)] + [InventedException()]
                self.simple_instance._to_master_queue.get = AsyncioMock(
                    side_effect=values)
                expected_calls_get = [call() for value in values[:-1]]
                with self.assertRaises(InventedException):
                    asyncio_run(self.simple_instance.send_to_master())
                self.simple_instance._to_master_queue.get.mock.assert_has_calls(
                    expected_calls_get)
                self.simple_instance._to_master_queue.get.mock.reset_mock()

    def test_send_to_master_awaits_open_connection(self):
        with patch(
                "fructosa.lagent.asyncio.open_connection", new=AsyncioMock()
                ) as open_connection:
            reader = MagicMock()
            writer = MagicMock()
            open_connection.mock.return_value = (reader, writer)
            self.simple_instance._to_master_queue = MagicMock()
            mock_conf = MagicMock()
            self.simple_instance._conf = mock_conf
            host = "wandalon"
            port = 111223
            def getitem(value):
                return {LMASTER_HOST_KEY: host, LAGENT_TO_LMASTER_DATA_PORT_KEY: port}[value]
            mock_conf.lmaster.__getitem__.side_effect = getitem
            for num in 3,1,4:
                values = [MagicMock() for _ in range(num)] + [InventedException()]
                self.simple_instance._to_master_queue.get = AsyncioMock(
                    side_effect=values
                )
                with self.assertRaises(InventedException):
                    asyncio_run(self.simple_instance.send_to_master())
                open_connection.mock.assert_called_once_with(
                    host, port,
                    loop=self.simple_instance._event_loop
                )
                open_connection.mock.reset_mock()

    def test_send_to_master_calls_writer_write(self):
        with patch(
                "fructosa.lagent.asyncio.open_connection", new=AsyncioMock()
                ) as open_connection:
            reader = MagicMock()
            writer = MagicMock()
            open_connection.mock.return_value = (reader, writer)
            self.simple_instance._to_master_queue = MagicMock()
            for num in 3,1,4:
                values = [MagicMock() for _ in range(num)] + [InventedException()]
                self.simple_instance._to_master_queue.get = AsyncioMock(side_effect=values)
                expected_calls = [call(value) for value in values[:-1]]
                with self.assertRaises(InventedException):
                    asyncio_run(self.simple_instance.send_to_master())
                writer.write.assert_has_calls(expected_calls)
                writer.write.reset_mock()

    def test_send_to_master_logs_messages(self):
        with patch(
                "fructosa.lagent.asyncio.open_connection", new=AsyncioMock()
                ) as open_connection:
            reader = MagicMock()
            writer = MagicMock()
            open_connection.mock.return_value = (reader, writer)
            self.simple_instance._to_master_queue = MagicMock()
            values = [InventedException()]
            self.simple_instance._to_master_queue.get = AsyncioMock(
                side_effect=values
            )
            mock_conf = MagicMock()
            self.simple_instance._conf = mock_conf
            host = "aylasole"
            port = 19633
            def getitem(value):
                return {LMASTER_HOST_KEY: host, LAGENT_TO_LMASTER_DATA_PORT_KEY: port}[value]
            mock_conf.lmaster.__getitem__.side_effect = getitem
            msgs = [
                LAGENT_TO_LMASTER_CONNECTING_MSG.format(
                    host_key=LMASTER_HOST_KEY, host=host, 
                    port_key=LAGENT_TO_LMASTER_DATA_PORT_KEY, port=port
                ),
                LAGENT_TO_LMASTER_CONNECTED_MSG
            ]
            logger = self.simple_instance.__class__.__name__
            with self.assertLogs(logger, level=logging.INFO) as log:
                try:
                    asyncio_run(self.simple_instance.send_to_master())
                except InventedException:
                    pass
            for imsg, msg in enumerate(msgs):
                self.assertIn(msg, log.output[imsg])
                
    def test_send_to_master_doesnt_log_connection_established_if_error(self):
        with patch(
                "fructosa.lagent.asyncio.open_connection", new=AsyncioMock()
                ) as open_connection:
            open_connection.mock.side_effect = InventedException()
            mock_conf = MagicMock()
            self.simple_instance._conf = mock_conf
            host = "comomapuesto"
            port = 87266
            def getitem(value):
                return {LMASTER_HOST_KEY: host, LAGENT_TO_LMASTER_DATA_PORT_KEY: port}[value]
            mock_conf.lmaster.__getitem__.side_effect = getitem
            msg = LAGENT_TO_LMASTER_CONNECTED_MSG
            logger = self.simple_instance.__class__.__name__
            with self.assertLogs(logger, level=logging.INFO) as log:
                try:
                    asyncio_run(self.simple_instance.send_to_master())
                except InventedException:
                    pass
            for log_line in log.output:
                self.assertNotIn(msg, log_line)


if __name__ == "__main__":
    unittest.main()
