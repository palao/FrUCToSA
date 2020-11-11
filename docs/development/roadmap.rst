*******
Roadmap
*******

The roadmap is a summary of planned changes. It is splitted into two parts:

* :ref:`Future`
* :ref:`Past`

The difference between :ref:`Past` and the :ref:`CHANGELOG` is the point of view:
:ref:`CHANGELOG` is intended for *end users* whereas :ref:`Past` is mainly for
developers.

Time estimations
----------------

* I use the PERT methodology (beta distribution).
* time units are hours
  

.. _Future:

Future
======

0.4.0
-----

* [R07] Basic sensors for jobs (Slurm).  Using ``pyslurm`` to collect data 
  and ``redis`` to store data.

  * collect info about running jobs and store it in redis
  * sbatch script (later?)
  * stats (later?)
  * ...

    
Time estimation
^^^^^^^^^^^^^^^

+--------------------+-------------+-----------+-------------+--------+-------+-------------+
|  Task              |  Optimistic |  Nominal  |  Pesimistic |   mu   | sigma |  measured   |
+====================+=============+===========+=============+========+=======+=============+
| FT                 |      1      |    2      |      6      |   2.5  | 0.83  |             |
+--------------------+-------------+-----------+-------------+--------+-------+-------------+
| Redis interface    |      2      |    3      |      4      |   3.0  | 0.33  |             |
+--------------------+-------------+-----------+-------------+--------+-------+-------------+
| Pyslurm interface  |      1      |    2      |      3      |   2.0  | 0.33  |             |
+--------------------+-------------+-----------+-------------+--------+-------+-------------+
| Sensor destination |      1      |    2      |      4      |   2.17 | 0.50  |             |
+--------------------+-------------+-----------+-------------+--------+-------+-------------+

Total:  9.67 +- 1.08 h



0.5.0
-----

* [R08.2] Grafana dashboards for jobs

  
Time estimation
^^^^^^^^^^^^^^^

+--------------------+-------------+-----------+-------------+--------+-------+-------------+
|  Task              |  Optimistic |  Nominal  |  Pesimistic |   mu   | sigma |  measured   |
+====================+=============+===========+=============+========+=======+=============+
| FT                 |      1      |    2      |      5      |  2.33  |  0.66 |             |
+--------------------+-------------+-----------+-------------+--------+-------+-------------+
| Dahsboard by hand  |      1      |    2      |      3      |  2.00  |  0.33 |             |
+--------------------+-------------+-----------+-------------+--------+-------+-------------+
| Implementation     |      2      |    3      |      6      |  3.33  |  0.66 |             |
+--------------------+-------------+-----------+-------------+--------+-------+-------------+

Total:  7.67 +- 1.00 h



0.6.0
-----

* [R12] PerA: agent to *cook* raw data I

  * compute global metrics for the full cluster

    
Time estimation
^^^^^^^^^^^^^^^

+--------------------+-------------+-----------+-------------+--------+-------+-------------+
|  Task              |  Optimistic |  Nominal  |  Pesimistic |   mu   | sigma |  measured   |
+====================+=============+===========+=============+========+=======+=============+
| Decide metrics     |      1      |    2      |      3      |  2.00  |  0.33 |             |
+--------------------+-------------+-----------+-------------+--------+-------+-------------+
| Initial Design     |      1      |    2      |      3      |  2.00  |  0.33 |             |
+--------------------+-------------+-----------+-------------+--------+-------+-------------+
| FT                 |      2      |    4      |      8      |  4.33  |  1.00 |             |
+--------------------+-------------+-----------+-------------+--------+-------+-------------+
| Implementation     |      6      |   16      |     24      | 15.67  |  3.00 |             |
+--------------------+-------------+-----------+-------------+--------+-------+-------------+

Total:  24.00 +- 3.18 h



0.7.0
-----

* [R08.3] Grafana dashboards for the full cluster

  
Time estimation
^^^^^^^^^^^^^^^

+--------------------+-------------+-----------+-------------+--------+-------+-------------+
|  Task              |  Optimistic |  Nominal  |  Pesimistic |   mu   | sigma |  measured   |
+====================+=============+===========+=============+========+=======+=============+
| FT                 |      1      |    2      |      5      |  2.33  |  0.66 |             |
+--------------------+-------------+-----------+-------------+--------+-------+-------------+
| Dahsboard by hand  |      1      |    2      |      3      |  2.00  |  0.33 |             |
+--------------------+-------------+-----------+-------------+--------+-------+-------------+
| Implementation     |      2      |    3      |      6      |  3.33  |  0.66 |             |
+--------------------+-------------+-----------+-------------+--------+-------+-------------+

Total:  7.67 +- 1.00 h


  
0.8.0
-----

* [R14.1] Improved sensors

  * docs: command line mechanism to get info about sensors
  * parameters: implement mechanism to pass params to sensors

  
Time estimation
^^^^^^^^^^^^^^^

+--------------------+-------------+-----------+-------------+--------+-------+-------------+
|  Task              |  Optimistic |  Nominal  |  Pesimistic |   mu   | sigma |  measured   |
+====================+=============+===========+=============+========+=======+=============+
| FT                 |      1      |    2      |      4      |  2.17  |  0.50 |             |
+--------------------+-------------+-----------+-------------+--------+-------+-------------+
| docs               |      1      |    2      |      3      |  2.00  |  0.33 |             |
+--------------------+-------------+-----------+-------------+--------+-------+-------------+
| Parameters         |      1      |    2      |      4      |  2.17  |  0.50 |             |
+--------------------+-------------+-----------+-------------+--------+-------+-------------+

Total:  6.33 +- 0.78 h


0.9.0
-----

* [R01] Central management

  * OpenRC (also systemd?) script to start the system: ``fructosa``
  * ``fructosa`` starts the manager daemon ``fructosad``
  * ``fructosad`` manages ``LiMon`` and ``PerA``

    * ``LiMon`` is managed by ``lmaster`` that starts in turn the needed ``lagent``\ s
    * ``PerA`` is run by the ``perad`` daemon (?)

    
Time estimation
^^^^^^^^^^^^^^^

+--------------------+-------------+-----------+-------------+--------+-------+-------------+
|  Task              |  Optimistic |  Nominal  |  Pesimistic |   mu   | sigma |  measured   |
+====================+=============+===========+=============+========+=======+=============+
| Architecture       |      1      |    2      |      3      |  2.00  |  0.33 |             |
+--------------------+-------------+-----------+-------------+--------+-------+-------------+
| Initial Design     |      1      |    2      |      3      |  2.00  |  0.33 |             |
+--------------------+-------------+-----------+-------------+--------+-------+-------------+
| FT                 |      3      |    6      |      8      |  5.83  |  0.83 |             |
+--------------------+-------------+-----------+-------------+--------+-------+-------------+
| Implementation     |      4      |    8      |     16      |  8.66  |  2.00 |             |
+--------------------+-------------+-----------+-------------+--------+-------+-------------+

Total:  18.50 +- 2.22 h

      
0.10.0
------

* [R13] Agent for jobs (Slurm) II

  * it can link data from slurm (jobs) to data from other agents (nodes)

  
0.11.0
------

* [R09] Automatic generation of plots for HKHLR and loewemon


0.12.0
------

* [R10] ML analysis of collected data to classify jobs (PerA)


0.13.0
------

* [R14.2] Improved sensors (II)

  * modular sensors: sensor availability depends dynamically on reachable
    modules


1.0.0
-----

* [R15] Documentation

  * sensors
  * configuration files
  * command line options
  * man page
  * etc


.. _Past:

Past
====

0.2.0
-----

* [R08.1] Grafana dashboards for nodes
* Initial structure for docs
* Started using sphinx
  
  
0.3.0
-----

* [R11] Architecture's revamp I

  * heartbeat mechanism
  * agents send data directly to destination(s)


