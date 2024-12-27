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


    nodes = []
    datastore = []

    def __init__(self, sosarchive):
        sosnodes = sosarchive +'/sos_commands/metalk8s/by-resources/node/'
        with open(sosnodes + "/list.txt", 'r') as file:
            next(file)
            for line in file:
                self.nodes.append(line)
        #files = os.listdir(self.sosnodes)
        #for file in files:
    #        if (re.search("(.*)eval_db.getCollection___infost", file)):
    #                self.datastore.append(sosarchive +'/sos_commands/artesca/' + str(file))


    def extractTopo(self):
        print("=======================  TOPO  =======================")
        self.extractNodeTopo()
        #self.extractMongoTopo()

    def extractNodeTopo(self):
        for node in self.nodes:
            print(node)

    #def extractMongoTopo(self):
    #    sosmongos= sosarchive +'/sos_commands/artecsa/'
    #    files = os.listdir(sosmongos)
    #    for mongostatuses in files:
    #        with open(mongostatuses, 'r') as file:
    #            jsonMongoStatuses = json.load(file)
