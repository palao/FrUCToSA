#################
Development notes
#################


**************
Some decisions
**************

Structure of code
=================

* ``fructosad.py``, ``lagent.py`` and ``lmaster.py`` contain code to trivially create executables
  via their main functions.


Functional Tests
================

In general, it is expected that ``lmaster`` and ``lagent`` (and other executables in the package)
run with privileges. Therefore to isolate and limit the impact of the functional tests on the
host, it was decided to run the daemons for FTing inside containers.

This behaviour can be controlled with an environment varaible called ``FRUCTOSA_FT_ENVIRONMENT``.

* Setting ``FRUCTOSA_FT_ENVIRONMENT=docker`` (default) makes the FTs run the programs under
  test inside docker containers.
* With ``FRUCTOSA_FT_ENVIRONMENT=host`` the FTs run directly in the host.
* The location of the project need to be set somehow to install it in the containers. This
  can be controlled with an environment variable: ``FRUCTOSA_PROJECT_PATH``.
  If unset, the location is inferred from the location of the ``environment.py`` file
  (which lives in ``tests/functional/``).

How to run the Functional Tests (FTs)
-------------------------------------

In ``devel`` there is a dockerfile that can be used to create the image needed to run
the FTs inside containers::

  $ cd devel/
  $ docker build --tag fructosa:auto --tag fructosa:latest -f FrUCToSA-dev.df .

With that, the FTs should run smothly (hopefully!) with::

  $ pytest tests/functional/

Or with::

  $ tox

  

****************
Daemon processes
****************

* typically accept command line options for
  * configuration file
  * logging file/directory
  * pidfile (?)
* general logging messages to a specific log file (like ``/var/log/fructosad.log``); errors
  go to syslog (``/var/log/syslog``) -- done anyway by the Linux logging system
* Catch SIGHUP to allow re-reading of configuration
  

**************************
File locking and PID files
**************************

Ref. [Rago2013]_, pag. 473 (see also p. 494 for a definition of the ``lockfile`` function)
explains how to create a locked PID file.

Probably better explained can be found in ref. [Kerrisk2010]_, page 1142. The code for
``lockRegion`` can be found on page 1134.

In Python, one can use ``os.lockf``. See the docs. The meaning of the possible values for
``cmd`` can be seen with ``man 3 lockf``. Also the other parameters are explained, of course.


**********************
AsyncIO and unit tests
**********************

A simple approach is described by Miguel Grinberg in his blog:
https://blog.miguelgrinberg.com/post/unit-testing-asyncio-code
I implemented my own version of his _run and AsyncMock in ``test/unit/fructosa/aio_tools.py``.


************
Bibliography
************

[Rago2013] R. Stevens, S. Rago "Advanced Programming in the UNIX Environment", 3rd ed.
  Addison Wesley, 2013

[Kerrisk2010] M. Kerrisk, "The Linux Programming Interface", No Starch Press Press, 2010
