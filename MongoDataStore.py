from enum import Enum
import sys, getopt, argparse, json, datetime, re

class AGGR(Enum):
    MAX=1
    MIN=2
    AVG=3
    LAST=4
    SUM=5

class MongoDataStore:

    objects = float('nan')
    previous_usage = float('nan')
    current_usage = float('nan')
    measuredOn = "NaN"
    buckets = float('nan')

    def __init__(self, mongodbDataStoreFiles):
        for mongodbDataStoreFile in mongodbDataStoreFiles:
            with open(mongodbDataStoreFile, 'r') as file:
                try:
                    notjson = file.read()
                    jsonStr = re.sub(r'([_]*[a-zA-Z]+):', r'"\1":', notjson)
                    jsonStr = jsonStr.replace("\'", "\"")
                    jsonStr = re.sub(r'( Long\(\"[0-9]+\"\))', "\"NaN\"", jsonStr)
                    jsonStr = re.sub(r'( NumberLong\([0-9]+\))', "\"NaN\"", jsonStr)
                    jsonStr = re.sub(r'( NumberLong\(\"[0-9]+\"\))', "\"NaN\"", jsonStr)
                    if (re.search(r"\}\n\{", jsonStr)):
                        jsonStr = re.sub(r"\}\n\{", "},{", jsonStr)
                        jsonStr = f"[{jsonStr}]"
                    jsonStr = jsonStr.replace("Type \"it\" for more","")
                    dsStats = json.loads(jsonStr)
                    self.parseJsonArray(dsStats)
                except Exception as e:
#                    print(e)
                    continue

    def parseJsonArray(self, dsStats):
        for dsStat in dsStats:
            try:
                self.parseJson(dsStat)
            except:
                self.parseMeasuredOn(dsStat)
            finally:
                continue

    def parseMeasuredOn(self, dsStat):
        self.measuredOn = dsStat["measuredOn"]

    def parseJson(self, dsStat):
        self.objects = dsStat["value"]["objects"]
        self.buckets = dsStat["value"]["buckets"]
        self.previous_usage = dsStat["value"]["dataManaged"]["total"]["prev"]
        self.current_usage = dsStat["value"]["dataManaged"]["total"]["curr"]
