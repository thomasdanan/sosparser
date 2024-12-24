from enum import Enum

import os, re

from path import Path


from PromStat import PromStat, AGGR
from MongoDataStore import MongoDataStore


#hyperdrive_http_bytes_reclaimable_free_space.json:                    "__name__": "hyperdrive_http_bytes_reclaimable_free_space",
#hyperdrive_relocation_byte_reclaimed_total.json:                    "__name__": "hyperdrive_relocation_byte_reclaimed_total",
#hyperdrive_http_bytes_net.json
#hyperdrive_http_key_net.json
#hyperdrive_index_capacity.json
# hyperdrive_index_free.json
#hyperdrive_index_nbkeys.json

class SosTopo:

    sosnodes = None
    datastore = []

    def __init__(self, sosarchive):
        self.sosnodes = sosarchive +'/sos_commands/metalk8s/by-resources/node/'

    def extractTopo(self):
        print("=======================  TOPO  =======================")
