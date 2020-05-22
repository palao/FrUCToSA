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

from fructosa.logs import setup_logging

from fructosa.constants import (
    HEARTBEAT_RECEIVE_MSG_TEMPLATE, HEARTBEAT_SEND_MSG_TEMPLATE,
)

def encode_beat_number(num):
    return num.to_bytes(length=64, byteorder="big", signed=False)


def decode_beat_number(data):
    return int.from_bytes(data,  byteorder="big", signed=False)


class HeartbeatClientProtocol:
    _next_beat_number = 0 #  should be a descriptor?
    
    def __init__(self, on_con_lost, logging_conf):
        self.on_con_lost = on_con_lost
        self.transport = None
        self.logger = setup_logging(
            self.__class__.__name__,
            rotatingfile_conf=logging_conf
        )
        
    @property
    def beat_number(self):
        return self._next_beat_number
    
    @property
    def message(self):
        return encode_beat_number(self.beat_number)
    
    def connection_made(self, transport):
        self.transport = transport
        self.transport.sendto(self.message)
        self.__class__._next_beat_number += 1
        log_msg = HEARTBEAT_SEND_MSG_TEMPLATE.format(
            message_number=self.beat_number)
        self.logger.info(log_msg)
        self.transport.close()

    def connection_lost(self, exc):
        self.on_con_lost.set_result(True)


class HeartbeatServerProtocol:
    def __init__(self, logging_conf):
        self.logger = setup_logging(
            self.__class__.__name__,
            rotatingfile_conf=logging_conf
        )
    
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        num = decode_beat_number(data)
        self.logger.info(
            HEARTBEAT_RECEIVE_MSG_TEMPLATE.format(
                host=addr, message_number=num
            )
        )
