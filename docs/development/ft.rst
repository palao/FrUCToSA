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

The image used is ``palao/slurm-docker-cluster`` cloned from
``giovtorres/slurm-docker-cluster`` and modified to suit the requirements
of the current project (which means to have the devel version of ``FrUCToSA``
installed, along with a recent version of Python).

The FTs require the image to be built. To build the image::

  $ git clone git@github.com:palao/slurm-docker-cluster.git
  $ cd slurm-docker-cluster
  $ docker build -t slurm-for-fructosa -t slurm-for-fructosa:19.05.1 -t slurm-for-fructosa:19.05.1.2 .


Afterwards the FTs should run smoothly... hopefully.

If you are curious, have a look at the ``docker-compose.yml`` file in the
github repo (``palao/slurm-docker-cluster``) to learn how this image is
used in the FTs (although this is not necessary to run the FTs).


Work flow
=========

Environment
-----------

There are two environments for FT:

* `LocalhostFTEnvironmentType`
* `DockerFTEnvironmentType`


``DockerFTEnvironmentType``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
