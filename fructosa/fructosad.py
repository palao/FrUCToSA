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

import sys
import argparse
import os
import signal
import time
import asyncio

from fructosa.daemon import daemonize
from fructosa.logs import setup_logging
from fructosa.constants import (
    PROTO_STARTING_PROGRAM_MSG, PROTO_STOPPED_PROGRAM_MSG, PROTO_CANT_STOP_MSG,
    START_STOP_ERROR, NOT_RUNNING_MESSAGE, FRUCTOSAD_PROGRAM, PIDFILE_NOT_FOUND,
    PROTO_NO_PERMISSION_PIDFILE, PIDFILE_ACTION_CREATED, PIDFILE_ACTION_ACCESSED,
    INVALID_PID, PROCESS_DOES_NOT_EXIST, 
)
from fructosa.maind import generic_main
from fructosa.conf import ACTION_STR, PIDFILE_STR, FructosaDConf

#from fructosa.messages.fructosad import (STARTING, STARTING_SERVER)

FRUCTOSAD_STARTING_MESSAGE = PROTO_STARTING_PROGRAM_MSG.format(program=FRUCTOSAD_PROGRAM)
FRUCTOSAD_STOP_MESSAGE = PROTO_STOPPED_PROGRAM_MSG.format(program=FRUCTOSAD_PROGRAM)
FRUCTOSAD_CANT_STOP_MESSAGE = PROTO_CANT_STOP_MSG.format(program=FRUCTOSAD_PROGRAM)


class FructosaD:
    _starting_message = FRUCTOSAD_STARTING_MESSAGE
    _stopped_message = FRUCTOSAD_STOP_MESSAGE
    _cant_stop_message = FRUCTOSAD_CANT_STOP_MESSAGE
    
    def __init__(self, conf):
        self._conf = conf
        self.action = conf[ACTION_STR]
        self.pidfile = conf[PIDFILE_STR]
        self.logger = setup_logging(
            logger_name=self.__class__.__name__, rotatingfile_conf=self._conf.logging
        )
        self._event_loop = asyncio.get_event_loop()
        
    def __call__(self):
        # note: need to be careful here: to only allow the execution of certain methods
        #       a FT-driven protection measure must be implemented.
        getattr(self, self.action)()
        #return getattr(self, self.action)()#return

    def start(self):
        try:
            daemonize(self.pidfile)
            # daemonize(self.pidfile, stdout="/tmp/fructosad.log", stderr="/tmp/fructosad.log")
        except RuntimeError as e:
            self.logger.error(e)
            for warn_msg in e.to_warning:
                self.logger.warning(warn_msg)
            raise SystemExit(START_STOP_ERROR)
        except PermissionError as e:
            self.logger.warning("Exception message: "+str(e))
            self.logger.error(e.to_error)
            raise SystemExit(START_STOP_ERROR)
        self.logger.warning(self._starting_message)
        self.run()

    def stop(self):
        error_msg = None
        try:
            with open(self.pidfile) as f:
                pid = f.read().strip()
            pid = int(pid)
            os.kill(pid, signal.SIGTERM)
        except FileNotFoundError:
            error_msg = PIDFILE_NOT_FOUND.format(pidfile=self.pidfile)
        except PermissionError:
            error_msg = PROTO_NO_PERMISSION_PIDFILE.format(
                pidfile=self.pidfile, action=PIDFILE_ACTION_ACCESSED
            )
        except (ValueError, OverflowError):# as e:
            error_msg = INVALID_PID.format(pid=pid)#+str(e)
        except ProcessLookupError:
            error_msg = PROCESS_DOES_NOT_EXIST.format(pid=pid)
        else:
            self.logger.warning(self._stopped_message)
        if error_msg:
            self.logger.error(
                "{}: {}".format(self._cant_stop_message, error_msg)
            )
            raise SystemExit(START_STOP_ERROR)
        
        # #############################
        # New, EAFP approach:
        # 
        # try:
        #     with open(...):
        #         os.kill(...)
        # except FileNotFoundError:#the pidfile is not there
        #     ...
        # except PermissionError:#cannot
        #     ...
        # except ValueError:
        #     ...
        # except ProcesLookupError:
        #     ... # if the would-be pid is not a valid one
        # else:
        #     os.logger.warning...
        #
        # #############################
        #  It used to be...
        #
        # if os.path.exists(self.pidfile):# this is LBYL!!!
        #     with open(self.pidfile) as f:
        #         os.kill(int(f.read()), signal.SIGTERM)
        #     self.logger.warning(self._stopped_message)
        # else:
        #     self.logger.error(
        #         "{}: {}".format(self._cant_stop_message, NOT_RUNNING_MESSAGE)
        #     )
        #     raise SystemExit(START_STOP_ERROR)
        
    def run(self):
        self._run_loop()

    def _run_loop(self):
        try:
            self._event_loop.run_forever()
        finally:
            self._clean_up()

    def _clean_up(self):
        self._event_loop.close()
    
    def submit_task(self, task, *args, **kwargs):
        self._event_loop.create_task(task(*args, **kwargs))

        
def main():
    #return generic_main(FructosaDConf, FructosaD)#return
    generic_main(FructosaDConf, FructosaD)
