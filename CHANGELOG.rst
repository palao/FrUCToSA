*****************************************
What changes are included in each version
*****************************************

0.2.0
=====

(WIP)

* Documuentation improved

  * roadmap
  * deployment
  * architecture
  * development
    
* [devel] CL options factorized out from main conf class:

    ``FructosaDConf`` -> ``FructosaDConf`` + ``CLConf``

  This change should be transparent for customers of the ``FructosaDConf`` class.
  

0.1.0
=====

* migrated from QULo_
* [testing:FTs] The location of the project can be controlled with an environment
  variable: ``FRUCTOSA_PROJECT_PATH``, if unset, the location is inferred from
  the location of the ``environment.py`` file (which lives in ``tests/functional/``).
  This feature is needed to create the docker compose files neceessary to run
  the FTs inside containers.

.. _QULo: https://itp.uni-frankfurt.de/~palao/software/QULo/
