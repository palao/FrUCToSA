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
from unittest.mock import patch

from fructosa.slurm import Slurm


@patch("fructosa.slurm.importlib.import_module")
class SlurmTestCase(unittest.TestCase):
    def test_defines__pyslurm_attribute(self, pimport):
        s = Slurm()
        slurm_mod = pimport.return_value
        pimport.assert_called_once_with("pyslurm")
        self.assertEqual(slurm_mod, s._pyslurm)

    def test_jobs_method(self, pimport):
        s = Slurm()
        jobs = s.jobs()
        slurm_mod = pimport.return_value
        self.assertEqual(jobs, slurm_mod.job.return_value.get.return_value)
