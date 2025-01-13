import os, re, json

from path import Path

class S3ActionStats():

    ops = 0
    elapsed = 0
    sysErr = 0
    usrErr = 0
    success = 0
    size = 0

    def addStatFromJson(self, jsonLog):
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

    def addStatFromActionStat(self, stat):
        self.ops += stat.ops
        self.elapsed += stat.elapsed
        self.sysErr += stat.sysErr
        self.usrErr += stat.usrErr
        self.success += stat.success
        self.size += stat.size

    def getLatency(self):
        return self.elapsed/self.ops


    def getResult(self):
        return ("ops: "+str(self.ops)+", success: " + '{:.1f}%'.format(self.success/self.ops*100)
        + ", usrErr: "+ '{:.1f}%'.format(self.usrErr/self.ops*100)
        + ", sysErr: "+ '{:.3f}%'.format(self.sysErr/self.ops*100)
        + ", avgObjSize: "+ '{:.1f}'.format(self.size/self.ops) + " bytes"
        + ", avgLatency: "+ '{:.1f}'.format(self.elapsed/self.ops) + " ms")


class SosTraffic:

    cslogs = []
    pattern = re.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]+[+-]{1}[0-9]{2}:[0-9]{2} (.*)")
    stats = dict()
    sosarchive = None

    def __init__(self, sosarchive):
        self.sosarchive = sosarchive
        csLogsdir = sosarchive +'/sos_commands/metalk8s/by-resources/pod/zenko/'
        if Path(csLogsdir).is_dir():
            files = os.listdir(csLogsdir)
            for file in files:
                if (re.search("artesca-data-connector-cloudserver-(.*)-(.*)_logs.txt", file)):
                    self.cslogs.append(csLogsdir + str(file))
        else:
            print("No cs log files found")
        self.parseCSLogs()


#    def loadS3ServiceMetrics(self):
#        ops = PromStat(self.sosmetrics+'/s3_cloudserver_http_requests_total.json')
#        mongodb_capa = capacity.extractMetricFilteredOnKey("persistentvolumeclaim", 'datadir-data-db-mongodb-sharded-shard[0-9]-data-[0-9]', AGGR.MAX, AGGR.MAX)


    def parseCSLogs(self):
        for logFile in self.cslogs:
            with open(logFile, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if (re.search(",\"message\":\"responded(.*)", line)):
                        jsonStr = self.extractJsonContentFromCSLog(line)
                        jsonLog = json.loads(jsonStr)
                        self.addS3OperationStat(jsonLog)

    def extractJsonContentFromCSLog(self, line):
        result = self.pattern.search(line)
        jsonStr = result.group(1)
        return jsonStr

    def addS3OperationStat(self, jsonLog):
        if("bucketName" in jsonLog and "accountName" in jsonLog):
            accountName = jsonLog["accountName"]
            bucketName = jsonLog["bucketName"]
            action = jsonLog["action"]
            key = accountName+"-"+bucketName
            #print(accountName+"-"+bucketName+"-"+action+"-"+str(httpCode)+"-"+str(bytesReceived))
            if(self.stats.get(key) is None):
                self.stats[key] = dict()
            if(self.stats[key].get(action) is None):
                self.stats[key][action] = S3ActionStats()
            self.stats[key][action].addStatFromJson(jsonLog)

    def printResult(self):
        print("==============================  TRAFFIC  ===============================")
        print("### Display stats per bucket when latency > 100ms or when sysErr > 0 ###")
        total = dict()
        for key in self.stats:
            print(key)
            for action in self.stats.get(key):
                if( self.stats[key][action].getLatency() > 100 or self.stats[key][action].sysErr > 0):
                  print("  "+ action + ": " + self.stats[key][action].getResult())
                if(total.get(action) is None):
                    total[action] = S3ActionStats()
                total[action].addStatFromActionStat(self.stats[key][action])
        print("Total:")
        for action in total:
            print("  "+ action + ": " + total[action].getResult())
