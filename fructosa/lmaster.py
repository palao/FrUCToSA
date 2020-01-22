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

import asyncio
import pickle
import struct
#from asyncio import open_connection

from fructosa.fructosad import FructosaD
from fructosa.conf import LMasterConf
from fructosa.maind import generic_main
from fructosa.lmessage import LMessage, LMessageError

from fructosa.constants import (
    PROTO_STARTING_PROGRAM_MSG, PROTO_STOPPED_PROGRAM_MSG, PROTO_CANT_STOP_MSG,
    START_STOP_ERROR, NOT_RUNNING_MESSAGE, LMASTER_PROGRAM, PROTO_MEASUREMENT_MSG,
    SERVING_PROTO_MESSAGE, INITIAL_LMASTER_SERVER_PACKET_SIZE,
    PROTO_MEASUREMENT_RECEIVED_MSG, LAGENT_TO_LMASTER_DATA_PORT_KEY,
    LMASTER_HOST_KEY, GRAPHITE_HOST_KEY, GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY,
    PROTO_MSG_TO_GRAPHITE, LMASTER_TO_GRAPHITE_CONNECTING_MSG,
    LMASTER_TO_GRAPHITE_CONNECTED_MSG, LMASTER_TO_GRAPHITE_RETRY_MSG,
)

LMASTER_STARTING_MESSAGE = PROTO_STARTING_PROGRAM_MSG.format(program=LMASTER_PROGRAM)
LMASTER_STOP_MESSAGE = PROTO_STOPPED_PROGRAM_MSG.format(program=LMASTER_PROGRAM)
LMASTER_CANT_STOP_MESSAGE = PROTO_CANT_STOP_MSG.format(program=LMASTER_PROGRAM)


class LMaster(FructosaD):
    _starting_message = LMASTER_STARTING_MESSAGE
    _stopped_message = LMASTER_STOP_MESSAGE
    _cant_stop_message = LMASTER_CANT_STOP_MESSAGE

    def __init__(self, conf):
        super().__init__(conf)
        self._to_graphite_queue = asyncio.Queue()
        
    def run(self):
        """LMaster.run is the place to submit asyncio tasks: that is
        the reason why the messages come from LAgent instances to
        LMaster: because LMaster might have instructions to dispatch
        messages to different locations.
        """
        server = self._create_server()
        self._run_server(server)
        self.submit_task(self._send_to_graphite)
        #  More tasks can be added here
        super().run()
    
    def _create_server(self):
        host = self._conf.lmaster[LMASTER_HOST_KEY]
        port = self._conf.lmaster[LAGENT_TO_LMASTER_DATA_PORT_KEY]
        return asyncio.start_server(
            self._handle_connection, host, port, loop=self._event_loop
        )

    def _run_server(self, server_coroutine):
        self.server = self._event_loop.run_until_complete(server_coroutine)
        self.logger.info(
            SERVING_PROTO_MESSAGE.format(self.server.sockets[0].getsockname())
        )
        
    async def _handle_connection(self, reader, writer):
        addr = writer.get_extra_info('peername')
        while True:
            data = await reader.read(INITIAL_LMASTER_SERVER_PACKET_SIZE)
            await self._to_graphite_queue.put(data)
            message = pickle.loads(data)
            log_msg = PROTO_MEASUREMENT_RECEIVED_MSG.format(addr, message)
            self.logger.debug(log_msg)

    def _clean_up(self):
        self.server.close()
        self._event_loop.run_until_complete(self.server.wait_closed())
        super()._clean_up()

    async def _send_to_graphite(self):
        # This should be refactored: 1) create connection, and 2) write data
        host = self._conf.graphite[GRAPHITE_HOST_KEY]
        port = self._conf.graphite[GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY]
        msg = LMASTER_TO_GRAPHITE_CONNECTING_MSG.format(
            host_key=GRAPHITE_HOST_KEY, host=host,
            port_key=GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY, port=port,
        )
        self.logger.info(msg)
        while True:
            try:
                reader, writer = await asyncio.open_connection(
                    host, port, loop=self._event_loop
                )
            except ConnectionRefusedError:
                self.logger.info(LMASTER_TO_GRAPHITE_RETRY_MSG.format(host=host))
                await asyncio.sleep(1)
            #except OSError:
            # if graphite is not there, OSError can happen
            #    self.logger.error("OSError")
            else:
                self.logger.info(LMASTER_TO_GRAPHITE_CONNECTED_MSG)
                break
        while True:
            raw_message = await self._to_graphite_queue.get()
            self.logger.debug(PROTO_MSG_TO_GRAPHITE.format(raw_message))
            try:
                message = LMessage(raw_message).to_graphite()
            except LMessageError as e:
                self.logger.error(e)
            else:
            #try:#This requires a FT -> killing Graphite while the system runs, and maybe restarting it
                writer.write(message)
            #except graphite is not there: (maybe it crashed)
            # 1. log (connection to graphite lost),
            # 2. submit task again (self.submit_task(self._send_to_graphite))
            # 3. and exit
 
    
def main():
    generic_main(LMasterConf, LMaster)

