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

from tests.functional.base_start_stop import MultiProgramBaseStartStop


class BasicSlurmTestCase(MultiProgramBaseStartStop, unittest.TestCase):
    """First FT for Slurm. It assumes that Slurm and Redis are running and 
    checks that Redis gets messages from FrUCToSA with data from Slurm.

    Why MultiProgramBaseStartStop? As of version 0.4.0 this has only to
    do with lagent. But later it will have to make 'pera' enter into the 
    game because data will be sent to it to be processed."""

    default_config_files = (LAGENT_DEFAULT_CONFIGFILE,)
    _WITH_SLURM = True
    _WITH_REDIS = True
    
    def test_error_behaviour_of_pidfile_functionality(self):
        #  I want to skip this test from the Base because in that test, the
        # functionality of the program is tested, BUT the BasicSlurmTestCase
        # is about testing integration between slurm and FrUCToSA
        pass

    def test_logging_section_of_config_file_basic(self):
        #  Same as before
        pass

    def test_logging_section_of_config_file_more_details(self):
        #  Same as before
        pass

    def test_config_file_can_be_changed_from_command_line(self):
        # and again
        pass

    def test_configuration_read_is_reported_in_the_logs(self):
        # once more
        pass
    
    def test_info_from_jobs_in_slurm_arrive_to_redis(self):
        #  Tux has been told by the developers that FrUCToSA can communicate with
        # Slurm: it can collect data from slurm. He wants to check this feature, that
        # he finds promising.
        # So he prepares a config file for lagent:
        #lmaster = LMasterWrapper(pidfile=LMASTER_DEFAULT_PIDFILE)
        lagent = LAgentWrapper(pidfile=LAGENT_DEFAULT_PIDFILE)
        #programs = (lmaster, lagent)
        programs = (lagent,)
        if self.ft_env.name == LOCALHOST_FT_ENVIRONMENT:
            #simple_conf_files = ("lmaster-slurm.1.conf", "lagent-test.1.conf")
            simple_conf_files = ("lagent-slurm.1.conf",)
        elif self.ft_env.name == DOCKER_FT_ENVIRONMENT:
            #simple_conf_files = ("lmaster-slurm.docker.1.conf", "lagent-test.docker.1.conf")
            simple_conf_files = ("lagent-slurm.docker.1.conf",)
        confs = [
            self.prepare_config_from_file(
                conf4test, default_configfile=def_conf, program=prog,
            ) for conf4test, def_conf, prog in zip(
                simple_conf_files, self.default_config_files, programs)
        ]
        # he restarts slurm, to be sure that there is no cache contaminating the test
        # and when he launches the program lagent
        #lmaster.args = ("start",)
        # aquin: ¿cómo hago para ejecutar lagent en el contenedor?
        # ¿Empiezo el contenedor 
        lagent.args = ("start",)
        trying_slurm_conn = TO_SLURM_CONNECTING_MSG.format(
            host_key=SLURM_HOST_KEY,
            host=confs[0][SLURM_SECTION][SLURM_HOST_KEY],
            port_key=SLURM_CARBON_RECEIVER_PICKLE_PORT_KEY,
            port=confs[0][SLURM_SECTION][SLURM_CARBON_RECEIVER_PICKLE_PORT_KEY],
        )
        slurm_connected = TO_SLURM_CONNECTED_MSG
        slurm_lines = (trying_slurm_conn, slurm_connected)
        proto_wrong_value_from_slurm_line = "{} ({})".format(
            WRONG_MESSAGE_TO_SLURM_MSG, WRONG_MESSAGE_TO_SLURM_DETAIL_MSG
        )
        wrong_value_from_slurm_line = proto_wrong_value_from_slurm_line.format(
            sensor="Users", measurement="_MEASUREMENT_"
        ).split("_MEASUREMENT_")[0]
        slurm_error_lines = (wrong_value_from_slurm_line,)
        self.setup_logparser(target_strings=slurm_lines+slurm_error_lines)

        with self.ft_env(*programs) as slurm_lagent:
            # he can see that after waiting some little time the connection with slurm
            # is announced in the logs
            self.wait_for_environment(15)
            new_lines = self.tmplogparser.get_new_lines()
            new_lines_summary = self.tmplogparser._line_counting_history[-1]
            for target in slurm_lines:
                for line in new_lines:
                    if target in line:
                        break
                else:
                    self.fail("'{}' not found in the logs".format(target))
            # and actually three sensors have reported several measurements:
            #time.sleep(1.1)
            ncpus = os.cpu_count()
            hostname = lagent.hostname
            targets = []
            for icpu in range(ncpus):
                targets.append(f"{hostname}.CPUPercent.{icpu}")
            targets.append(f"{hostname}.VirtualMemory.percent")
            targets.append(f"{hostname}.BootTime")
            for target in targets:
                slurm_data = get_data_from_slurm_render_api(target).strip()
                print(".>.> '{}' = '{}'".format(target, slurm_data))
                result = slurm_data.split("|")[1]
                self.assertNotEqual(result, "None")
                self.assertNotEqual(result, "")
            # but the other one is missing, as expected (it is not a time series!):
            targets = []
            targets.append(f"{hostname}.Users")
            for target in targets:
                slurm_data = get_data_from_slurm_render_api(target).strip()
                try:
                    result = slurm_data.split("|")[1]
                except IndexError:
                    pass
            # and actually the logs report an error about that sensor:
            for target in slurm_error_lines:
                for line in new_lines:
                    if target in line:
                        break
                else:
                    print("The lines in the log:")
                    print(new_lines)
                    print()
                    self.fail("'{}' not found in the logs".format(target))

