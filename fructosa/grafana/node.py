node_template_dict = {
    'annotations': {
        'list': [
            {
                'builtIn': 1,
                'datasource': '-- Grafana --',
                'enable': True,
                'hide': True,
                'iconColor': 'rgba(0, 211, 255, 1)',
                'name': 'Annotations & Alerts',
                'type': 'dashboard'
            }
        ]
    },
    'description': 'node performance dashboard',
    'editable': True,
    'gnetId': None,
    'graphTooltip': 0,
    'id': 2,
    'links': [],
    'panels': [
        {
            'collapsed': False,
            'gridPos': {'h': 1, 'w': 24, 'x': 0, 'y': 0},
            'id': 14,
            'panels': [],
            'title': 'Global',
            'type': 'row'
        },
        {
            'gridPos': {'h': 8, 'w': 4, 'x': 1, 'y': 1},
            'id': 36,
            'options': {
                'fieldOptions': {
                    'calcs': ['lastNotNull'],
                    'defaults': {
                        'mappings': [],
                        'max': 100,
                        'min': 0,
                        'thresholds': [
                            {
                                'color': 'green',
                                'value': None
                            },
                            {
                                'color': 'red',
                                'value': 80
                            }
                        ],
                        'title': '$__series_name',
                        'unit': 'percent'
                    },
                    'override': {},
                    'values': False
                },
                'orientation': 'auto',
                'showThresholdLabels': False,
                'showThresholdMarkers': True
            },
            'pluginVersion': '6.3.5',
            'targets': [
                {
                    'refId': 'A',
                    'target': 'averageSeries(terminus.CPUPercent.*, *)'
                }
            ],
            'timeFrom': None,
            'timeShift': None,
            'title': 'CPU',
            'type': 'gauge'
        },
        {
            'gridPos': {'h': 8, 'w': 4, 'x': 5, 'y': 1},
            'id': 37,
            'options': {
                'fieldOptions': {
                    'calcs': ['lastNotNull'],
                    'defaults': {
                        'mappings': [],
                        'max': 100,
                        'min': 0,
                        'thresholds': [
                            {'color': 'green', 'value': None},
                            {'color': 'red', 'value': 80}
                        ],
                        'title': '$__series_name',
                        'unit': 'percent'
                    },
                    'override': {},
                    'values': False
                },
                'orientation': 'auto',
                'showThresholdLabels': False,
                'showThresholdMarkers': True
            },
            'pluginVersion': '6.3.5',
            'targets': [
                {
                    'refId': 'A',
                    'target': 'terminus.VirtualMemory.percent'
                }
            ],
            'timeFrom': None,
            'timeShift': None,
            'title': 'Virtual Memory',
            'type': 'gauge'
        },
        {
            'gridPos': {'h': 8, 'w': 4, 'x': 9, 'y': 1},
            'id': 38,
            'options': {
                'fieldOptions': {
                    'calcs': ['lastNotNull'],
                    'defaults': {
                        'mappings': [],
                        'max': 100,
                        'min': 0,
                        'thresholds': [
                            {'color': 'green', 'value': None},
                            {'color': 'red', 'value': 80}
                        ],
                        'title': '$__series_name',
                        'unit': 'percent'
                    },
                    'override': {},
                    'values': False
                },
                'orientation': 'auto',
                'showThresholdLabels': False,
                'showThresholdMarkers': True
            },
            'pluginVersion': '6.3.5',
            'targets': [
                {'refId': 'A', 'target': 'terminus.DiskUsage.percent'}], 'timeFrom': None, 'timeShift': None, 'title': 'Disk', 'type': 'gauge'}, {'collapsed': False, 'gridPos': {'h': 1, 'w': 24, 'x': 0, 'y': 9}, 'id': 2, 'panels': [], 'title': 'CPU', 'type': 'row'}, {'aliasColors': {}, 'bars': False, 'dashLength': 10, 'dashes': False, 'fill': 1, 'fillGradient': 0, 'gridPos': {'h': 10, 'w': 16, 'x': 1, 'y': 10}, 'id': 12, 'legend': {'avg': False, 'current': False, 'max': False, 'min': False, 'show': True, 'total': False, 'values': False}, 'lines': True, 'linewidth': 1, 'links': [], 'nullPointMode': 'null', 'options': {'dataLinks': []}, 'percentage': False, 'pointradius': 5, 'points': False, 'renderer': 'flot', 'seriesOverrides': [], 'spaceLength': 10, 'stack': False, 'steppedLine': False, 'targets': [{'refId': 'A', 'target': 'averageSeries(terminus.CPUPercent.*, *)'}], 'thresholds': [], 'timeFrom': None, 'timeRegions': [], 'timeShift': None, 'title': 'Total CPU load', 'tooltip': {'shared': True, 'sort': 0, 'value_type': 'individual'}, 'type': 'graph', 'xaxis': {'buckets': None, 'mode': 'time', 'name': None, 'show': True, 'values': []}, 'yaxes': [{'format': 'percent', 'label': None, 'logBase': 1, 'max': '100', 'min': '0', 'show': True}, {'format': 'short', 'label': None, 'logBase': 1, 'max': None, 'min': None, 'show': True}], 'yaxis': {'align': False, 'alignLevel': None}}, {'aliasColors': {}, 'bars': False, 'dashLength': 10, 'dashes': False, 'description': 'Percentage of CPU used on terminus', 'fill': 1, 'fillGradient': 0, 'gridPos': {'h': 9, 'w': 16, 'x': 1, 'y': 20}, 'id': 4, 'legend': {'alignAsTable': True, 'avg': False, 'current': False, 'max': False, 'min': False, 'rightSide': False, 'show': True, 'total': False, 'values': False}, 'lines': True, 'linewidth': 1, 'links': [], 'nullPointMode': 'null', 'options': {'dataLinks': []}, 'percentage': False, 'pointradius': 5, 'points': False, 'renderer': 'flot', 'seriesOverrides': [], 'spaceLength': 10, 'stack': False, 'steppedLine': False, 'targets': [{'refId': 'A', 'target': 'terminus.CPUPercent.*'}], 'thresholds': [], 'timeFrom': None, 'timeRegions': [], 'timeShift': None, 'title': 'CPU percent', 'tooltip': {'shared': True, 'sort': 0, 'value_type': 'individual'}, 'type': 'graph', 'xaxis': {'buckets': None, 'mode': 'time', 'name': None, 'show': True, 'values': []}, 'yaxes': [{'format': 'percent', 'label': None, 'logBase': 1, 'max': '100', 'min': '0', 'show': True}, {'format': 'short', 'label': None, 'logBase': 1, 'max': '100', 'min': '0', 'show': True}], 'yaxis': {'align': False, 'alignLevel': None}}, {'aliasColors': {}, 'bars': False, 'dashLength': 10, 'dashes': False, 'description': 'How the CPU time is divided into different operation modes', 'fill': 1, 'fillGradient': 0, 'gridPos': {'h': 11, 'w': 16, 'x': 1, 'y': 29}, 'id': 22, 'legend': {'alignAsTable': True, 'avg': False, 'current': False, 'max': False, 'min': False, 'rightSide': False, 'show': True, 'total': False, 'values': False}, 'lines': True, 'linewidth': 1, 'links': [], 'nullPointMode': 'null', 'options': {'dataLinks': []}, 'percentage': False, 'pointradius': 5, 'points': False, 'renderer': 'flot', 'seriesOverrides': [], 'spaceLength': 10, 'stack': False, 'steppedLine': False, 'targets': [{'refId': 'A', 'target': 'terminus.CPUTimesPercent.*'}], 'thresholds': [], 'timeFrom': None, 'timeRegions': [], 'timeShift': None, 'title': 'CPU time', 'tooltip': {'shared': True, 'sort': 0, 'value_type': 'individual'}, 'type': 'graph', 'xaxis': {'buckets': None, 'mode': 'time', 'name': None, 'show': True, 'values': []}, 'yaxes': [{'format': 'percent', 'label': None, 'logBase': 1, 'max': '100', 'min': None, 'show': True}, {'format': 'short', 'label': None, 'logBase': 1, 'max': None, 'min': None, 'show': True}], 'yaxis': {'align': False, 'alignLevel': None}}, {'aliasColors': {}, 'bars': False, 'dashLength': 10, 'dashes': False, 'description': 'Interrupts and ctx switches', 'fill': 1, 'fillGradient': 0, 'gridPos': {'h': 8, 'w': 16, 'x': 1, 'y': 40}, 'id': 6, 'legend': {'alignAsTable': True, 'avg': False, 'current': False, 'max': False, 'min': False, 'rightSide': False, 'show': True, 'total': False, 'values': False}, 'lines': True, 'linewidth': 1, 'links': [], 'nullPointMode': 'null', 'options': {'dataLinks': []}, 'percentage': False, 'pointradius': 5, 'points': False, 'renderer': 'flot', 'seriesOverrides': [], 'spaceLength': 10, 'stack': False, 'steppedLine': False, 'targets': [{'refId': 'A', 'target': 'terminus.CPUStats.*'}], 'thresholds': [], 'timeFrom': None, 'timeRegions': [], 'timeShift': None, 'title': 'CPU stats', 'tooltip': {'shared': True, 'sort': 0, 'value_type': 'individual'}, 'type': 'graph', 'xaxis': {'buckets': None, 'mode': 'time', 'name': None, 'show': True, 'values': []}, 'yaxes': [{'format': 'short', 'label': None, 'logBase': 1, 'max': None, 'min': None, 'show': True}, {'format': 'short', 'label': None, 'logBase': 1, 'max': None, 'min': None, 'show': True}], 'yaxis': {'align': False, 'alignLevel': None}}, {'aliasColors': {}, 'bars': False, 'dashLength': 10, 'dashes': False, 'fill': 1, 'fillGradient': 0, 'gridPos': {'h': 8, 'w': 16, 'x': 1, 'y': 48}, 'id': 34, 'legend': {'alignAsTable': True, 'avg': False, 'current': False, 'max': False, 'min': False, 'rightSide': False, 'show': True, 'total': False, 'values': False}, 'lines': True, 'linewidth': 1, 'links': [], 'nullPointMode': 'null', 'options': {'dataLinks': []}, 'percentage': False, 'pointradius': 5, 'points': False, 'renderer': 'flot', 'seriesOverrides': [], 'spaceLength': 10, 'stack': False, 'steppedLine': False, 'targets': [{'refId': 'A', 'target': 'terminus.CPUFreq.*'}], 'thresholds': [], 'timeFrom': None, 'timeRegions': [], 'timeShift': None, 'title': 'CPU Frequency', 'tooltip': {'shared': True, 'sort': 0, 'value_type': 'individual'}, 'type': 'graph', 'xaxis': {'buckets': None, 'mode': 'time', 'name': None, 'show': True, 'values': []}, 'yaxes': [{'format': 'hertz', 'label': None, 'logBase': 1, 'max': None, 'min': None, 'show': True}, {'format': 'short', 'label': None, 'logBase': 1, 'max': None, 'min': None, 'show': True}], 'yaxis': {'align': False, 'alignLevel': None}}, {'collapsed': False, 'gridPos': {'h': 1, 'w': 24, 'x': 0, 'y': 56}, 'id': 18, 'panels': [], 'title': 'Network', 'type': 'row'}, {'aliasColors': {}, 'bars': False, 'dashLength': 10, 'dashes': False, 'fill': 1, 'fillGradient': 0, 'gridPos': {'h': 9, 'w': 16, 'x': 1, 'y': 57}, 'id': 16, 'legend': {'alignAsTable': True, 'avg': False, 'current': False, 'max': False, 'min': False, 'show': True, 'total': False, 'values': False}, 'lines': True, 'linewidth': 1, 'links': [], 'nullPointMode': 'null', 'options': {'dataLinks': []}, 'percentage': False, 'pointradius': 5, 'points': False, 'renderer': 'flot', 'seriesOverrides': [], 'spaceLength': 10, 'stack': False, 'steppedLine': False, 'targets': [{'refId': 'A', 'target': 'terminus.NetIOCounters.*'}], 'thresholds': [], 'timeFrom': None, 'timeRegions': [], 'timeShift': None, 'title': 'Network IO counters', 'tooltip': {'shared': True, 'sort': 0, 'value_type': 'individual'}, 'type': 'graph', 'xaxis': {'buckets': None, 'mode': 'time', 'name': None, 'show': True, 'values': []}, 'yaxes': [{'format': 'short', 'label': None, 'logBase': 1, 'max': None, 'min': None, 'show': True}, {'format': 'short', 'label': None, 'logBase': 1, 'max': None, 'min': None, 'show': True}], 'yaxis': {'align': False, 'alignLevel': None}}, {'collapsed': False, 'gridPos': {'h': 1, 'w': 24, 'x': 0, 'y': 66}, 'id': 8, 'panels': [], 'title': 'Memory', 'type': 'row'}, {'aliasColors': {}, 'bars': False, 'dashLength': 10, 'dashes': False, 'description': 'active, used, total, etc', 'fill': 1, 'fillGradient': 0, 'gridPos': {'h': 16, 'w': 16, 'x': 1, 'y': 67}, 'id': 10, 'legend': {'alignAsTable': True, 'avg': False, 'current': False, 'max': False, 'min': False, 'rightSide': False, 'show': True, 'total': False, 'values': False}, 'lines': True, 'linewidth': 1, 'links': [], 'nullPointMode': 'null', 'options': {'dataLinks': []}, 'percentage': False, 'pointradius': 5, 'points': False, 'renderer': 'flot', 'seriesOverrides': [], 'spaceLength': 10, 'stack': False, 'steppedLine': False, 'targets': [{'refId': 'A', 'target': 'terminus.VirtualMemory.*'}], 'thresholds': [], 'timeFrom': None, 'timeRegions': [], 'timeShift': None, 'title': 'Virtual memory', 'tooltip': {'shared': True, 'sort': 0, 'value_type': 'individual'}, 'type': 'graph', 'xaxis': {'buckets': None, 'mode': 'time', 'name': None, 'show': True, 'values': []}, 'yaxes': [{'format': 'bytes', 'label': None, 'logBase': 1, 'max': None, 'min': None, 'show': True}, {'format': 'short', 'label': None, 'logBase': 1, 'max': None, 'min': None, 'show': True}], 'yaxis': {'align': False, 'alignLevel': None}}, {'collapsed': False, 'gridPos': {'h': 1, 'w': 24, 'x': 0, 'y': 83}, 'id': 28, 'panels': [], 'title': 'Disk', 'type': 'row'}, {'aliasColors': {}, 'bars': False, 'dashLength': 10, 'dashes': False, 'fill': 1, 'fillGradient': 0, 'gridPos': {'h': 9, 'w': 16, 'x': 1, 'y': 84}, 'id': 32, 'legend': {'alignAsTable': False, 'avg': False, 'current': False, 'max': False, 'min': False, 'show': True, 'total': False, 'values': False}, 'lines': True, 'linewidth': 1, 'links': [], 'nullPointMode': 'null', 'options': {'dataLinks': []}, 'percentage': False, 'pointradius': 5, 'points': False, 'renderer': 'flot', 'seriesOverrides': [], 'spaceLength': 10, 'stack': False, 'steppedLine': False, 'targets': [{'refId': 'A', 'target': 'terminus.DiskUsage.percent'}], 'thresholds': [], 'timeFrom': None, 'timeRegions': [], 'timeShift': None, 'title': 'Disk Used', 'tooltip': {'shared': True, 'sort': 0, 'value_type': 'individual'}, 'type': 'graph', 'xaxis': {'buckets': None, 'mode': 'time', 'name': None, 'show': True, 'values': []}, 'yaxes': [{'format': 'percent', 'label': None, 'logBase': 1, 'max': '100', 'min': '0', 'show': True}, {'format': 'short', 'label': None, 'logBase': 1, 'max': None, 'min': None, 'show': True}], 'yaxis': {'align': False, 'alignLevel': None}}, {'aliasColors': {}, 'bars': False, 'dashLength': 10, 'dashes': False, 'fill': 1, 'fillGradient': 0, 'gridPos': {'h': 9, 'w': 16, 'x': 1, 'y': 93}, 'id': 30, 'legend': {'avg': False, 'current': False, 'max': False, 'min': False, 'show': True, 'total': False, 'values': False}, 'lines': True, 'linewidth': 1, 'links': [], 'nullPointMode': 'null', 'options': {'dataLinks': []}, 'percentage': False, 'pointradius': 5, 'points': False, 'renderer': 'flot', 'seriesOverrides': [], 'spaceLength': 10, 'stack': False, 'steppedLine': False, 'targets': [{'refCount': 0, 'refId': 'A', 'target': 'terminus.DiskUsage.free'}, {'refCount': 0, 'refId': 'B', 'target': 'terminus.DiskUsage.used'}, {'refCount': 0, 'refId': 'C', 'target': 'terminus.DiskUsage.total'}], 'thresholds': [], 'timeFrom': None, 'timeRegions': [], 'timeShift': None, 'title': 'Disk Usage', 'tooltip': {'shared': True, 'sort': 0, 'value_type': 'individual'}, 'type': 'graph', 'xaxis': {'buckets': None, 'mode': 'time', 'name': None, 'show': True, 'values': []}, 'yaxes': [{'format': 'decbytes', 'label': None, 'logBase': 1, 'max': None, 'min': None, 'show': True}, {'format': 'short', 'label': None, 'logBase': 1, 'max': None, 'min': None, 'show': True}], 'yaxis': {'align': False, 'alignLevel': None}}, {'aliasColors': {}, 'bars': False, 'dashLength': 10, 'dashes': False, 'fill': 1, 'fillGradient': 0, 'gridPos': {'h': 8, 'w': 16, 'x': 1, 'y': 102}, 'id': 24, 'legend': {'avg': False, 'current': False, 'max': False, 'min': False, 'show': True, 'total': False, 'values': False}, 'lines': True, 'linewidth': 1, 'links': [], 'nullPointMode': 'null', 'options': {'dataLinks': []}, 'percentage': False, 'pointradius': 5, 'points': False, 'renderer': 'flot', 'seriesOverrides': [], 'spaceLength': 10, 'stack': False, 'steppedLine': False, 'targets': [{'refId': 'A', 'target': 'terminus.DiskIOCounters.*'}], 'thresholds': [], 'timeFrom': None, 'timeRegions': [], 'timeShift': None, 'title': 'Global Disk parameters', 'tooltip': {'shared': True, 'sort': 0, 'value_type': 'individual'}, 'type': 'graph', 'xaxis': {'buckets': None, 'mode': 'time', 'name': None, 'show': True, 'values': []}, 'yaxes': [{'format': 'short', 'label': None, 'logBase': 1, 'max': None, 'min': None, 'show': True}, {'format': 'short', 'label': None, 'logBase': 1, 'max': None, 'min': None, 'show': True}], 'yaxis': {'align': False, 'alignLevel': None}}], 'refresh': '10s', 'schemaVersion': 19, 'style': 'dark', 'tags': ['terminus', 'goethe', 'FrUCToSA'], 'templating': {'list': []}, 'time': {'from': 'now-6h', 'to': 'now'}, 'timepicker': {'refresh_intervals': ['5s', '10s', '30s', '1m', '5m', '15m', '30m', '1h', '2h', '1d'], 'time_options': ['5m', '15m', '1h', '6h', '12h', '24h', '2d', '7d', '30d']}, 'timezone': '', 'title': 'terminus', 'uid': 'unXAjo5Wk', 'version': 38}

