from enum import Enum
import sys, getopt, argparse, json, datetime, re

#            date = datetime.datetime.fromtimestamp(value[0], tz=datetime.timezone.utc)

class AGGR(Enum):
    MAX=1
    MIN=2
    AVG=3
    LAST=4
    SUM=5

objects = None
previous_usage = None
current_usage = None
measuredOn = None

class MongoDataStore:

    def __init__(self, mongodbDataStoreFiles):
        for mongodbDataStoreFile in mongodbDataStoreFiles:
            with open(mongodbDataStoreFile, 'r') as file:
                for line in file:
                    if(re.search("(.*)objects: (.*),", line)):
                        self.extractObjects(line)
                    if(re.search("(.*)buckets: (.*),", line)):
                        self.extractBuckets(line)
                    if(re.search("(.*)total: { curr:(.*),", line)):
                        self.extractCurrentCapa(line)
                        self.extractPreviousCapa(line)
                    if(re.search("(.*)measuredOn:(.*),", line)):
                        self.extractMeasuredOn(line)


    def extractObjects(self, line):
        objects = line.split(":")[1]
        self.objects = objects.split(",")[0]

    def extractBuckets(self, line):
        buckets = line.split(":")[1]
        self.buckets = buckets.split(",")[0]

    def extractCurrentCapa(self, line):
        current = line.split(":")[2]
        self.current_usage = float(current.split(",")[0])

    def extractPreviousCapa(self, line):
        previous = line.split(":")[3]
        self.previous_usage = float(previous.split("}")[0])

    def extractMeasuredOn(self, line):
        date = line.split(":")[1]
        self.measuredOn = date.split(",")[0]
