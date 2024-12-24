from enum import Enum

import os, re

from path import Path


from PromAlerts import PromAlerts


#hyperdrive_http_bytes_reclaimable_free_space.json:                    "__name__": "hyperdrive_http_bytes_reclaimable_free_space",
#hyperdrive_relocation_byte_reclaimed_total.json:                    "__name__": "hyperdrive_relocation_byte_reclaimed_total",
#hyperdrive_http_bytes_net.json
#hyperdrive_http_key_net.json
#hyperdrive_index_capacity.json
# hyperdrive_index_free.json
#hyperdrive_index_nbkeys.json

class SosAlerts:

    sosalerts = None
    datastore = []

    def __init__(self, sosarchive):
        self.sosalerts = sosarchive +'/sos_commands/metalk8s/metrics/'

    def extractAlerts(self):
        print("=======================  ALERTS  =======================")
        alerts = PromAlerts(self.sosalerts+'/ALERTS.json')
        print(alerts.listAlerts())
