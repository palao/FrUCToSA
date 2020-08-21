******************
Functional testing
******************

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
