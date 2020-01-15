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

import logging

PROTO_STARTING_PROGRAM_MSG = "Starting {program}..."
PROTO_STOPPED_PROGRAM_MSG = "{program} stopped"
PROTO_CANT_STOP_MSG = "{program} could not be stopped"
NOT_RUNNING_MESSAGE = "Not running"
START_STOP_ERROR = 1
ALREADY_RUNNING_MSG = 'It looks it is already running'

CONFIGFILE_STR = "config_file"

DEFAULT_PID_DIR = "/run"
DEFAULT_PROTO_PIDFILE = "{program}.pid"
FRUCTOSAD_PROGRAM = "fructosad"
FRUCTOSAD_DESCRIPTION = "fructosa program"
FRUCTOSAD_DEFAULT_CONFIGFILE = "/etc/fructosa/fructosad.conf"
LAGENT_DEFAULT_CONFIGFILE = "/etc/fructosa/lagent.conf"
LMASTER_DEFAULT_CONFIGFILE = "/etc/fructosa/lmaster.conf"

LAGENT_PROGRAM = "lagent"
LAGENT_DESCRIPTION = """fructosa agent is a daemon program that measures performance data in the host computer
and transfers that data to the fructosa master program"""

LMASTER_PROGRAM = "lmaster"
LMASTER_DESCRIPTION = "fructosa master program"
SERVING_PROTO_MESSAGE = "Serving on {}"
INITIAL_LMASTER_SERVER_PACKET_SIZE = 8192

ACTION_STR = "action"
ACTION_HELP = "action to perform."
ACTION_START = "start"
ACTION_STOP = "stop"
ACTION_CHOICES = [ACTION_START, ACTION_STOP]

PIDFILE_OPTION_ALIASES = ("-p", "--pidfile")
PIDFILE_STR = "pidfile"
PIDFILE_HELP = "provide an alternative PID file name (default: %(default)s)"
PIDFILE_ACTION_CREATED = "created"
PIDFILE_ACTION_ACCESSED = "accessed"
PROTO_NO_PERMISSION_PIDFILE = "Pidfile ('{pidfile}') cannot be {action}"
PIDFILE_EXISTS = "Pidfile ('{pidfile}') already exists"
PROCESS_DOES_NOT_EXIST = "The process with PID={pid} does not seem to exist"
RUNNING_PROCESS_FOUND = "There is a running process with PID={pid}"
NO_PID_FOUND = "No PID found"
PIDFILE_NOT_FOUND = "Pidfile ('{pidfile}') does not exist"
INVALID_PID = "PID='{pid}' is invalid"

CONFIGFILE_STR = "file"
CONFIGFILE_OPTION_ALIASES = ("-c", "--config")
CONFIGFILE_HELP = "provide an alternative config file name (default: %(default)s)"
DEFAULT_CONFIG_FILE = FRUCTOSAD_DEFAULT_CONFIGFILE
CONF_READ_MSG = "Global conf read from file {config_file}"

GENERIC_CONNECTED_MSG = " ...connection established"

# Logging:
LOGGER_LEVEL = logging.DEBUG
OWN_LOG_SECTION = "logging"
OWN_LOG_FILE_KEY = "filename"
OWN_LOG_MAXBYTES_KEY = "maxBytes"
OWN_LOG_MAXBYTES_TYPE = int
OWN_LOG_BACKUPCOUNT_KEY = "backupCount"
OWN_LOG_BACKUPCOUNT_TYPE = int
OWN_LOG_LEVEL_KEY = "level"
DEFAULT_OWN_FILE_LOGGER_LEVEL = logging.DEBUG
DEFAULT_OWN_FILE_LOGGING_PATH = "/var/log/fructosa.log"
DEFAULT_OWN_FILE_BACKUP_COUNT = 5
DEFAULT_OWN_FILE_MAXBYTES = 134217728
SYSLOG_LOGGER_LEVEL = logging.WARNING
FILE_LOGGING_FORMAT = "%(levelname)s [%(asctime)s][%(name)s] ---> %(message)s"
CANNOT_USE_LOG_HANDLER = "I cannot log! Try to change the log file in the configuration file."

PROTO_SENSOR_STARTED_MSG = "{sensor_name} sensor starts on {host} (freq: 1/{frequency}s)"
PROTO_MEASUREMENT_MSG = "measurement: {}"
PROTO_MEASUREMENT_RECEIVED_MSG = "received from {}: {}"
PROTO_INVALID_SENSOR_MSG = "{sensor_name}: invalid sensor name; ignored"
PROTO_MSG_TO_GRAPHITE = "[to graphite] {}"

DEFAULT_HOST_KEY = "host"
LMASTER_HOST_KEY = DEFAULT_HOST_KEY
LMASTER_HOST = "127.0.0.1"

LAGENT_TO_LMASTER_DATA_PORT_KEY = "incoming data port"
LAGENT_TO_LMASTER_DATA_PORT = 7888

LAGENT_TO_LMASTER_CONNECTING_MSG = (
    "Connecting to lmaster ({host_key}={host}, {port_key}={port}) to send data from sensors..."
)
LAGENT_TO_LMASTER_CONNECTED_MSG = GENERIC_CONNECTED_MSG

GRAPHITE_SECTION = "Graphite"
GRAPHITE_HOST_KEY = DEFAULT_HOST_KEY
GRAPHITE_HOST = "localhost"
GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY = "carbon receiver pickle port"
GRAPHITE_CARBON_RECEIVER_PICKLE_PORT = 2004
LMASTER_TO_GRAPHITE_CONNECTED_MSG = GENERIC_CONNECTED_MSG
LMASTER_TO_GRAPHITE_CONNECTING_MSG = (
    "Connecting to Graphite ({host_key}={host}, {port_key}={port}) to send data from sensors..."
)
LMASTER_TO_GRAPHITE_RETRY_MSG = "... connection to {host} failed. Retrying."
WRONG_MESSAGE_TO_GRAPHITE_MSG = "Measurement from '{sensor}' cannot be delivered to Graphite"
WRONG_MESSAGE_TO_GRAPHITE_DETAIL_MSG = "[sensor={sensor}] measurement={measurement}"
