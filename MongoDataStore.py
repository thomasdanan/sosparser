from enum import Enum
import sys, getopt, argparse, json, datetime, re

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
buckets = None


class MongoDataStore:

    def __init__(self, mongodbDataStoreFiles):
        for mongodbDataStoreFile in mongodbDataStoreFiles:
            with open(mongodbDataStoreFile, 'r') as file:
                braket = 0
                jsonStr = ""
                for line in file:
                    if (re.search("(.*)measuredOn(.*)", line)):
                        self.measuredOn = line.split("\"")[3]
                        braket = 0
                        jsonStr = ""
                        break;
                    jsonStr = jsonStr + line.strip()
                    if (re.search("(.*){(.*)", line)):
                        braket+=1
                    elif (re.search("(.*)}(.*)", line)):
                        braket-=1
                    if braket == 0:
                        try:
                            dsStats = json.loads(jsonStr)
                            self.parseJson(dsStats)
                        except:
                            break
                        finally:
                            jsonStr = ""

    def parseJson(self, dsStats):
        self.objects = dsStats["value"]["objects"]
        self.buckets = dsStats["value"]["buckets"]
        self.previous_usage = dsStats["value"]["dataManaged"]["total"]["prev"]
        self.current_usage = dsStats["value"]["dataManaged"]["total"]["curr"]
