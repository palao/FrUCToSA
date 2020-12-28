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
import json

from tests.functional.base_start_stop import MultiProgramBaseStartStop
from tests.common.program import LMasterWrapper, LAgentWrapper, ProgramWrapper
from tests.functional.environment import (
    LOCALHOST_FT_ENVIRONMENT, DOCKER_FT_ENVIRONMENT,
)

from fructosa.constants import (
    LMASTER_DEFAULT_CONFIGFILE, LAGENT_DEFAULT_CONFIGFILE,
    SLURM_UP_AND_RUNNING_MSG, 
)
from fructosa.conf import LMASTER_DEFAULT_PIDFILE, LAGENT_DEFAULT_PIDFILE

from redis import Redis


class BasicSlurmTestCase(MultiProgramBaseStartStop, unittest.TestCase):
    """First FT for Slurm. It assumes that Slurm and Redis are running and 
    checks that Redis gets messages from FrUCToSA with data from Slurm.
    """
    
    default_config_files = (
        LMASTER_DEFAULT_CONFIGFILE, LAGENT_DEFAULT_CONFIGFILE)
    _WITH_SLURM = True
    _WITH_REDIS = True

    def submit_dummy_job(self):
        job_script = "test_job.sbatch"
        full_source_sbatch = self._make_test_conf_file_name(
            job_script, relative_dir="data/slurm"
        )
        self.ft_env.cp_to_container(
            full_source_sbatch, f"/{job_script}", "slurmctld"
        )
        sbatch = ProgramWrapper(exe="sbatch")
        sbatch.args = job_script
        self.ft_env.run_in_container(sbatch, "slurmctld")
        
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
        if self.ft_env.name == LOCALHOST_FT_ENVIRONMENT:
            simple_conf_files = ("lmaster-redis.0.conf", "lagent-slurm.0.conf")
        elif self.ft_env.name == DOCKER_FT_ENVIRONMENT:
            simple_conf_files = ("lmaster-redis.docker.0.conf", "lagent-slurm.docker.0.conf")
        confs = [
            self.prepare_config_from_file(
                conf4test, default_configfile=def_conf, program=prog,
            ) for conf4test, def_conf, prog in zip(
                simple_conf_files, self.default_config_files, (lmaster, lagent))
        ]
        # he restarts slurm, to be sure that there is no cache contaminating the test
        # and when he launches the program lagent
        lmaster.args = ("start",)
        lagent.args = ("start",)
        #slurm_other = SLURM_OTHER_MSG
        slurm_lines = (SLURM_UP_AND_RUNNING_MSG,) # "Submitted batch job")
        # slurm_error_lines = (wrong_value_from_slurm_line,)
        self.setup_logparser(target_strings=slurm_lines) # +slurm_error_lines)
        with self.ft_env():
            # he can see that after waiting some little time the connection
            # with slurm is announced in the logs
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
            for i in range(3):
                self.submit_dummy_job()
            # and he checks that the new jobs have been detected by lagent
            # since they are recorded in Redis:
            r = Redis(db=13)
            job_list = r.keys("job:*")
            self.assertEqual(len(job_list), 3)
            # the job states agree with what he expects, 2 are running
            # and a third one is pending:
            jobs = [json.loads(r.get(j)) for j in job_list]
            self.assertEqual(
                sum(1 for j in jobs if j["job_state"] == "RUNNING"), 2)
            self.assertEqual(
                sum(1 for j in jobs if j["job_state"] == "PENDING"), 1)
