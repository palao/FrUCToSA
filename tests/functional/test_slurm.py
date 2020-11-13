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
    """
    
    default_config_files = (
        LMASTER_DEFAULT_CONFIGFILE, LAGENT_DEFAULT_CONFIGFILE)
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
        lmaster = LMasterWrapper(pidfile=LMASTER_DEFAULT_PIDFILE)
        lagent = LAgentWrapper(pidfile=LAGENT_DEFAULT_PIDFILE)
        # programs = (lmaster, lagent)
        if self.ft_env.name == LOCALHOST_FT_ENVIRONMENT:
            simple_conf_files = ("lmaster-redis.0.conf", "lagent-slurm.0.conf")
        elif self.ft_env.name == DOCKER_FT_ENVIRONMENT:
            simple_conf_files = ("lmaster-redis.docker.0.conf", "lagent-slurm.docker.0.conf")
        confs = [
            self.prepare_config_from_file(
                conf4test, default_configfile=def_conf, program=prog,
            ) for conf4test, def_conf, prog in zip(
                simple_conf_files, self.default_config_files, programs)
        ]
        # he restarts slurm, to be sure that there is no cache contaminating the test
        # and when he launches the program lagent
        lmaster.args = ("start",)
        lagent.args = ("start",)
        slurm_ready = SLURM_UP_AND_RUNNING_MSG
        #slurm_other = SLURM_OTHER_MSG
        slurm_lines = (slurm_ready,) #  Other?
        # slurm_error_lines = (wrong_value_from_slurm_line,)
        self.setup_logparser(target_strings=slurm_lines) # +slurm_error_lines)
        with self.ft_env():
            # he can see that after waiting some little time the connection with slurm
            # is announced in the logs
            self.wait_for_environment(15)
            self.ft_env.run_in_container(lmaster, "redis4fructosa")
            self.ft_env.run_in_container(lagent, "slurmctld")
            new_lines = self.tmplogparser.get_new_lines()
            new_lines_summary = self.tmplogparser._line_counting_history[-1]
            for target in slurm_lines:
                for line in new_lines:
                    if target in line:
                        break
                else:
                    self.fail("'{}' not found in the logs".format(target))
            # he submits several jobs
            # aquin
            
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

