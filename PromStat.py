from enum import Enum
import sys, getopt, argparse, json, datetime, re

#            date = datetime.datetime.fromtimestamp(value[0], tz=datetime.timezone.utc)

class AGGR(Enum):
    MAX=1
    MIN=2
    AVG=3
    LAST=4
    SUM=5

promStats = None

class PromStat:

    def __init__(self, metricFile):
        with open(metricFile, 'r') as file:
            self.promStats = json.load(file)

    def extractFilteredMetric(self, filterKey, filterValue, timeAggrOp, instanceAggrOp):
        metricValues = []
        for metric in self.promStats["data"]["result"]:
            if(re.search(filterValue, metric["metric"][filterKey])):
                metricValues.append(self.aggregate(self.promValuesToNumArray(metric["values"]), timeAggrOp))
        metricValue = self.aggregate(metricValues, instanceAggrOp)
        return float(metricValue)

    def extractMetric(self, timeAggrOp, instanceAggrOp):
        metricValues = []
        for metric in self.promStats["data"]["result"]:
            metricValues.append(self.aggregate(self.promValuesToNumArray(metric["values"]), timeAggrOp))
        metricValue= self.aggregate(metricValues, instanceAggrOp)
        return float(metricValue)

    def aggregate(self, numValues, aggrOp):
        metricValue = None
        if aggrOp == AGGR.AVG:
            metricValue = self.getAvg(numValues)
        elif aggrOp == AGGR.MAX:
            metricValue = self.getMax(numValues)
        elif aggrOp == AGGR.MIN:
            metricValue = self.getMin(numValues)
        elif aggrOp == AGGR.LAST:
            metricValue = self.getLast(numValues)
        elif aggrOp == AGGR.SUM:
            metricValue = self.getSum(numValues)
        return metricValue


    def getMax(self, values):
        metricValue = None
        for value in values:
            if metricValue == None:
                metricValue = value
            else:
                metricValue = max(metricValue, value)
        return metricValue

    def getMin(self, values):
        metricValue = None
        for value in values:
            if metricValue == None:
                metricValue = value
            else:
                metricValue = min(metricValue, value)
        return metricValue

    def getAvg(self, values):
        metricValue = 0
        for value in values:
            metricValue += value
        return metricValue / len(values)

    def getSum(self, values):
        metricValue = 0
        for value in values:
            metricValue += float(value)
        return metricValue

    def getLast(self, values):
        size = len(values)
        return float(values[size-1])

    def promValuesToNumArray(self, values):
        numValues = []
        for value in values:
            numValues.append(value[1])
        return numValues