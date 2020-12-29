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

import importlib

from .constants import SLURM_USABLE, SLURM_NOT_USABLE


class Slurm:
    """Wrapper around 'pyslurm'. 'pyslurm' must be imported in the
    constructor since it is not warrantied to be installable unless
    'slurm' itself is present.
    """
    def __init__(self, logger):
        self._logger = logger
        try:
            pyslurm = importlib.import_module("pyslurm")
        except ModuleNotFoundError:
            pyslurm = None
            self._logger.error(SLURM_NOT_USABLE)
        else:
            self._logger.info(SLURM_USABLE)
        self._pyslurm = pyslurm
        
    def jobs(self):
        try:
            jobs = self._pyslurm.job().get()
        except AttributeError:
            jobs = {}
        return jobs
