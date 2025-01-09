from enum import Enum

import os, re

from path import Path


from PromStat import PromStat, AGGR
from MongoDataStore import MongoDataStore

class SosTopo:


    nodes = []
    datastore = []

    def __init__(self, sosarchive):
        sosnodes = sosarchive +'/sos_commands/metalk8s/by-resources/node/'
        with open(sosnodes + "/list.txt", 'r') as file:
            next(file)
            for line in file:
                self.nodes.append(line.strip())

    def extractTopo(self):
        print("=======================  TOPO  =======================")
        self.extractNodeTopo()
        #self.extractMongoTopo()

    def extractNodeTopo(self):
        for node in self.nodes:
            print(node)
