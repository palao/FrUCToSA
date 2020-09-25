******************
Functional testing
******************

External components
===================

Some functionality provided by ``FrUCToSA`` makes use of third party
components, like

* Graphite
* Grafana
* Slurm
* Redis

In order to interact with them during testing, the relevant services are
run within Docker containers using ``docker-compose``.

Slurm
-----

The image used is ``giovtorres/slurm-docker-cluster``


Work flow
=========

Environment
-----------

There are two environments for FT:

* `LocalhostFTEnvironmentType`
* `DockerFTEnvironmentType`


`DockerFTEnvironmentType`
^^^^^^^^^^^^^^^^^^^^^^^^^

How it is defined and used

Example::

  programs = (self.program,)
  with self.ft_env(*programs) as start_command:
      self.wait_for_environment(1)
      new_lines = self.tmplogparser.get_new_lines()

Also a list of hostnames is accepted::
  
  with self.ft_env(self.program, hostnames=("himalaya",)) as start_command:
      self.wait_for_environment(1)
      new_lines = self.tmplogparser.get_new_lines()
