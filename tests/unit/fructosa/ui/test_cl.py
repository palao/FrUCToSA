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
from unittest.mock import patch, MagicMock

from fructosa.ui.cl import CLConf


@patch("fructosa.ui.cl.CLConf._parse_arguments")
@patch("fructosa.ui.cl.CLConf._add_arguments")
@patch("fructosa.ui.cl.CLConf._create_cl_parser")
class CLConfInitTestCase(unittest.TestCase):
    def setUp(self):
        self.desc = "my Funny description"
        self.arguments = ("some", "arguments")
        
    def test_init_sets_some_attributes(self,
          pcreate_cl_parser, padd_arguments, pparse_arguments):
        instance = CLConf(description=self.desc, arguments=self.arguments)
        self.assertEqual(instance.description, self.desc)
        self.assertEqual(instance.arguments, self.arguments)
        
    def test_instance_creates_cl_parser_first_off(
            self, pcreate_cl_parser, padd_arguments, pparse_arguments):
        pcreate_cl_parser.side_effect = Exception
        with self.assertRaises(Exception):
            instance = CLConf(description=self.desc, arguments=self.arguments)
        pcreate_cl_parser.assert_called_once_with()
        padd_arguments.assert_not_called()
        pparse_arguments.assert_not_called()

    def test_get_conf_from_command_line_calls_add_arguments_in_second_place(
            self, pcreate_cl_parser, padd_arguments, pparse_arguments):
        padd_arguments.side_effect = Exception
        with self.assertRaises(Exception):
            instance = CLConf(description=self.desc, arguments=self.arguments)
        pcreate_cl_parser.assert_called_once_with()
        padd_arguments.assert_called_once_with()
        pparse_arguments.assert_not_called()

    def test_get_conf_from_command_line_calls_parse_arguments_last(
            self, pcreate_cl_parser, padd_arguments, pparse_arguments):
        instance = CLConf(description=self.desc, arguments=self.arguments)
        pcreate_cl_parser.assert_called_once_with()
        padd_arguments.assert_called_once_with()
        pparse_arguments.assert_called_once_with()


class InitializedCLConfMixIn:
    def setUp(self):
        ARG_ONE = (
            "somethong",
            (("-s", "--somethong"), dict(help="somethong help")),
        )
        ARG_TWO = (
            "anicing",
            (("-a", "--anicing"), dict(help="anicing help")),
        )
        self.desc = "another description"
        self.arguments = (ARG_ONE, ARG_TWO)
        self.instance = CLConf(description=self.desc, arguments=self.arguments)
        
        
@patch("fructosa.ui.cl.argparse.ArgumentParser")
class CLConfCreateCLParserTestCase(InitializedCLConfMixIn, unittest.TestCase):
    def test_create_cl_parser_creates_ArgumentParser_instance(self, pArgumentParser):
        self.instance._create_cl_parser()
        pArgumentParser.assert_called_once_with(description=self.desc)
        
    def test_create_cl_parser_sets_cl_parser(self, pArgumentParser):
        parser = MagicMock()
        pArgumentParser.return_value = parser
        self.instance._create_cl_parser()
        self.assertEqual(self.instance._cl_parser, parser)


class CLConfParseArgumentsTestCase(unittest.TestCase, InitializedCLConfMixIn):
    def test_add_arguments_add_expected_arguments_to_cl_parser(self):
        from fructosa.conf import (
            ACTION_ARGUMENT, PIDFILE_ARGUMENT, FRUCTOSAD_DEFAULT_PIDFILE,
            CONFIGFILE_ARGUMENT, FRUCTOSAD_DEFAULT_CONFIGFILE, 
        )
        conf = self.empty_init_instance
        conf._add_arguments()
        PIDFILE_ARGUMENT[1][1]["default"] = FRUCTOSAD_DEFAULT_PIDFILE
        CONFIGFILE_ARGUMENT[1][1]["default"] = FRUCTOSAD_DEFAULT_CONFIGFILE
        calls = []
        for name, args in ACTION_ARGUMENT, PIDFILE_ARGUMENT, CONFIGFILE_ARGUMENT:
            calls.append(call(*args[0], **args[1]))
        conf._cl_parser.add_argument.assert_has_calls(calls, any_order=True)

    def test_parse_arguments_calls_cl_parsers_parse_args_method(self):
        argv = MagicMock()
        conf = self.empty_init_instance
        conf._argv = argv
        conf._parse_arguments()
        conf._cl_parser.parse_args.assert_called_once_with(argv)

    def test_parse_arguments_sets_command_line_conf_attribute(self):
        args = MagicMock()
        conf = self.empty_init_instance
        conf._cl_parser.parse_args.return_value = args
        conf._argv = MagicMock()
        conf._parse_arguments()
        self.assertEqual(conf._command_line_conf, vars(args))

