********************
The FrUCToSA package
********************

Introduction
============

**FrUCToSA** stands for **Fr**\ ankfurt **U**\ niversity **C**\ luster **T**\ ool **o**\ f
**S**\ oftware **A**\ nalysis.
It is a simple tool to collect and analyze data from software running on a cluster and to
analyze that data with performance "in mind". **FrUCToSA** is developed in Python.

The package contains:

* ``lagent``: customizable service/daemon that collects performance data from the a node on the
  cluster. It runs locally and collects data from sensors that can be activated and configured via
  a configuration file.
* ``lmaster``: a service/daemon that controls the agents and collects data from them. It runs in a
  master node of the cluster; it is controled via a configuration file.


  
Installation
============
   
Just install the FrUCToSA package from PyPI:
::

  $ pip install FrUCToSA


  
Usage
=====

1. Start ``lmaster``
   ::

      # lmaster start

   By default the configuration file is ``/etc/fructosa/lmaster.conf``, but can be changed from the
   command line. A typical configuration might be:
   ::

      [lmaster]
      host = localhost
      incoming data port = 7888
      
      [Graphite]
      host = localhost
      carbon receiver pickle port = 2004
      
      [logging]
      filename = /tmp/lmaster.log
      maxBytes = 1073741824
      backupCount = 10
      level = DEBUG

   No option is mandatory. In the file ``fructosa/constants.py`` the defaults are defined.
2. Start ``lagent``
   ::

      # lagent start

   By default the configuration file is ``/etc/fructosa/lagent.conf``, but can be changed from the
   command line. In this configuration file is where a *sensor* is activated. A typical
   configuration with all sensors active is:
   ::
      
      [lmaster]
      host = localhost
      incoming data port = 7888
      
      [logging]
      filename = /tmp/lagent.log
      maxBytes = 1073741824
      backupCount = 10
      level = DEBUG

      [sensor:CPUPercent]
      time_interval = 10
      
      [sensor:VirtualMemory]
      time_interval = 30
      
      [sensor:CPUTimes]
      time_interval = 30
      
      [sensor:CPUTimesPercent]
      time_interval = 10
      
      [sensor:CPUCount]
      time_interval = 300
      
      [sensor:CPUStats]
      time_interval = 30
      
      [sensor:CPUFreq]
      time_interval = 300
      
      [sensor:SwapMemory]
      time_interval = 60
      
      [sensor:DiskPartitions]
      time_interval = 60
      
      [sensor:DiskUsage]
      time_interval = 30
      #path = /
      
      [sensor:DiskIOCounters]
      time_interval = 20
      
      [sensor:NetIOCounters]
      time_interval = 10
      
      [sensor:NetConnections]
      time_interval = 20
      
      [sensor:NetIFAddrs]
      time_interval = 30
      
      [sensor:NetIFStats]
      time_interval = 30
      
      [sensor:SensorsTemperatures]
      time_interval = 30
      
      [sensor:SensorsFans]
      time_interval = 30
      
      [sensor:SensorsBattery]
      time_interval = 30
      
      [sensor:BootTime]
      time_interval = 300
      
      [sensor:Users]
      time_interval = 10

   Again, no option is mandatory. But if ``lagent`` must measure anything, some sensor must
   be explicitly given. In the file ``fructosa/constants.py`` the defaults are defined.
   The *time* given in the ``time_interval`` option is understood to be in *seconds*.
      
3. Start Graphite and inspect the dashboard to see the data.

   

TODO
====

* ``lagent`` should have an option to display the available sensors and some help for each sensor.
* Sensors should accept options: the mechanism is almost there, but need to be completed.
* Add sensors to read data from GPUs.
* Connect to Slurm.  
* Add configuration options to manage ``Graphite``:

  * send data to it or not? (yes by default)

* openrc scripts to manage the whole system:

  * *start* 

    1. start graphite
    2. start grafana (?)
    3. start lmaster
    4. start lagents where needed

  * *stop*

    1. stop lagents
    2. stop lmaster
    3. stop grafana (?)
    4. stop graphite


       
