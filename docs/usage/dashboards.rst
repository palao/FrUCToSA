HOWTO create Grafana dashboards
-------------------------------

Grafana_ is a nice solution to present data collected by FrUCToSA.
FrUCToSA is shipped with a little tool to produce dashboards ready to be imported
in Grafana.

The procedure to create and use the dashboards, is as follows:

1. Install FrUCToSA
2. Install Graphite
3. Install Grafana
4. `Configure Grafana`_.

   a. Set a provisioning path for Grafana. This is done by setting a value for
      ``/etc/grafana/grafana.ini``. For example::

	...
	[paths]
	...
	provisioning = /etc/grafana/provisioning
	...

   b. Make that directory and the directory where the providers go, if they do
      not exist yet::

	# mkdir -p /etc/grafana/provisioning/dashboards

   c. Create a provider. For instance::

	# cat /etc/grafana/provisioning/dashboards/fructosa.yml
	apiVersion: 1

	providers:
	# <string> an unique provider name
	- name: 'FrUCToSA'
	  # <int> org id. will default to orgId 1 if not specified
	  orgId: 1
	  # <string, required> name of the dashboard folder. Required
	  folder: 'nodes'
	  # <string> folder UID. will be automatically generated if not specified
	  #folderUid: ''
	  # <string, required> provider type. Required
	  type: file
	  # <bool> disable dashboard deletion
	  disableDeletion: false
	  # <bool> enable dashboard editing
	  editable: true
	  # <int> how often Grafana will scan for changed dashboards
	  updateIntervalSeconds: 10
	  # <bool> allow updating provisioned dashboards from the UI
	  allowUiUpdates: false
	  options:
	    # <string, required> path to dashboard files on disk. Required
	    path: /var/lib/grafana/dashboards

   d. Create this path, where the dashboards will be stored::

	# mkdir /var/lib/grafana/dashboards

5. Make the dashboards to visualize data from FrUCTosa using Grafana:

   a. Prepare a file with host names in it. For instance::

	$ cat fructosa-dashboards.ini
	[hosts]
	host1
	host2
	host3

   b. Use ``make-fructosa-dashboard`` to produce a json file with a dashboard
      for each host ::

	$ make-fructosa-dashboard fructosa-dashboards.ini

   c. Copy the produced json files to the proper location::

	# cp host1.json host2.json host3.json /var/lib/grafana/dashboards

6. Launch Graphite, FrUCToSA and Grafana
7. Connect to the Grafana site and, enjoy!
	

.. _Grafana: https://grafana.com/
.. _`Configure Grafana`: https://grafana.com/docs/grafana/latest/installation/configuration/
