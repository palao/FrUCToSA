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

from fructosa.slurm import Slurm
from fructosa.constants import SLURM_USABLE, SLURM_NOT_USABLE


@patch("fructosa.slurm.importlib.import_module")
class SlurmTestCase(unittest.TestCase):
    def test_construction_if_pyslurm_found(self, pimport):
        logger = MagicMock()
        s = Slurm(logger)
        slurm_mod = pimport.return_value
        pimport.assert_called_once_with("pyslurm")
        self.assertEqual(slurm_mod, s._pyslurm)
        logger.info.assert_called_once_with(SLURM_USABLE)

    def test_construction_if_pyslurm_not_importable(self, pimport):
        pimport.side_effect = ModuleNotFoundError
        logger = MagicMock()
        s = Slurm(logger)
        self.assertIs(s._pyslurm, None)
        logger.error.assert_called_once_with(SLURM_NOT_USABLE)

    def test_jobs_method(self, pimport):
        s = Slurm(MagicMock())
        jobs = s.jobs()
        slurm_mod = pimport.return_value
        self.assertEqual(jobs, slurm_mod.job.return_value.get.return_value)

    def test_jobs_method_returns_empty_dict_if_no_pyslurm(self, pimport):
        s = Slurm(MagicMock())
        s._pyslurm = None
        jobs = s.jobs()
        self.assertEqual(jobs, {})
