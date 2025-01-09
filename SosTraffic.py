import os, re, json

from path import Path

class Stats():

    ops = 0
    elapsed = 0
    sysErr = 0
    usrErr = 0
    success = 0
    size = 0

    def addStat(self, jsonLog):
        bytesReceived = jsonLog["bytesReceived"]
        httpCode = jsonLog["httpCode"]
        latency = jsonLog["elapsed_ms"]
        if("contentLength" in jsonLog):
            objSize = jsonLog["contentLength"]
            self.size += objSize
        elif("bodyLength" in jsonLog):
            objSize = jsonLog["bodyLength"]
            self.size += objSize
        self.ops += 1
        self.elapsed += latency

        if(httpCode < 300):
            self.success += 1
        elif(httpCode < 500):
            self.usrErr += 1
        elif(httpCode >= 500):
            self.sysErr += 1

    def addUnitStat(self, stat):
        self.ops += stat.ops
        self.elapsed += stat.elapsed
        self.sysErr += stat.sysErr
        self.usrErr += stat.usrErr
        self.success += stat.success
        self.size += stat.size


    def getResult(self):
        return ("ops: "+str(self.ops)+", success: " + '{:.1f}%'.format(self.success/self.ops*100)
        + ", usrErr: "+ '{:.1f}%'.format(self.usrErr/self.ops*100)
        + ", sysErr: "+ '{:.1f}%'.format(self.sysErr/self.ops*100)
        + ", avgObjSize: "+ '{:.1f}'.format(self.size/self.ops) + " bytes"
        + ", avgLatency: "+ '{:.1f}'.format(self.elapsed/self.ops) + " ms")


class SosTraffic:

    cslogs = []
    pattern = re.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]+[+-]{1}[0-9]{2}:[0-9]{2} (.*)")
    stats = dict()


    def __init__(self, sosarchive):
        csLogsdir = sosarchive +'/sos_commands/metalk8s/by-resources/pod/zenko/'
        if Path(csLogsdir).is_dir():
            files = os.listdir(csLogsdir)
            for file in files:
                if (re.search("artesca-data-connector-cloudserver-(.*)-(.*)_logs.txt", file)):
                    self.cslogs.append(csLogsdir + str(file))
        else:
            print("No cs log files found")
        self.parseLogs()


    def parseLogs(self):
        for logFile in self.cslogs:
            with open(logFile, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if (re.search(",\"message\":\"responded(.*)", line)):
                        jsonStr = self.extractJsonContent(line)
                        jsonLog = json.loads(jsonStr)
                        self.addStat(jsonLog)

    def extractJsonContent(self, line):
        result = self.pattern.search(line)
        jsonStr = result.group(1)
        return jsonStr

    def addStat(self, jsonLog):
        if("bucketName" in jsonLog and "accountName" in jsonLog):
            accountName = jsonLog["accountName"]
            bucketName = jsonLog["bucketName"]
            action = jsonLog["action"]
            key = accountName+"-"+bucketName
            #print(accountName+"-"+bucketName+"-"+action+"-"+str(httpCode)+"-"+str(bytesReceived))
            if(self.stats.get(key) is None):
                self.stats[key] = dict()
            if(self.stats[key].get(action) is None):
                self.stats[key][action] = Stats()
            self.stats[key][action].addStat(jsonLog)

    def printResult(self):
        print("=======================  TRAFFIC  =======================")
        total = dict()
        for key in self.stats:
            print(key)
            for action in self.stats.get(key):
                print("  "+ action + ": " + self.stats[key][action].getResult())
                if(total.get(action) is None):
                    total[action] = Stats()
                total[action].addUnitStat(self.stats[key][action])
        print("Total:")
        for action in total:
            print("  "+ action + ": " + total[action].getResult())
