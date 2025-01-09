#!python
import sys, getopt, argparse, json
from path import Path
from SosUsage import SosUsage
from SosTopo import SosTopo
from SosAlerts import SosAlerts
from SosTraffic import SosTraffic
from enum import Enum
from ListPods import SosPods


class STAT(Enum):
    ALL=1
    TOPO=2
    USAGE=3
    ALERTS=4
    PODS = 5
    TRAFFIC=6

def getARTESCAVersion(sosarchive):
    with open(sosarchive+"/sos_commands/metalk8s/by-namespaces/artesca-ui/deployment/artesca-ui_get.json", 'r') as file:
        ui = json.load(file)
        return ui["metadata"]["annotations"]["artesca.scality.com/version"]

parser = argparse.ArgumentParser(description="Parse ARTESCA sosreport",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("sosarchive", type=str, help="sosreport archive folder")
parser.add_argument("-s", "--stat", type=str, choices=[i.name for i in STAT], default=STAT.ALL.name, help="stat to extract")


args = parser.parse_args()
stat=STAT[args.stat]


if Path(args.sosarchive).is_dir():
    sosarchive=args.sosarchive
else:
    print(args.sosarchive + " does not exist")
    exit(1)

print("############### ARTESCA VERSION: "+getARTESCAVersion(sosarchive) + " ###############")

if stat == STAT.USAGE:
    parser = SosUsage(sosarchive)
    parser.extractUsage()
elif stat == STAT.TOPO:
    parser = SosTopo(sosarchive)
    parser.extractTopo()
elif stat == STAT.ALERTS:
    parser = SosAlerts(sosarchive)
    parser.extractAlerts()
elif stat == STAT.PODS:
    parser = SosPods(sosarchive)
    parser.list_pods()
elif stat == STAT.TRAFFIC:
    parser = SosTraffic(sosarchive)
    parser.printResult()
elif stat == STAT.ALL:
    parser = SosUsage(sosarchive)
    parser.extractUsage()
    parser = SosTopo(sosarchive)
    parser.extractTopo()
    parser = SosAlerts(sosarchive)
    parser.extractAlerts()
    # Extract pods
    parser = SosPods(sosarchive)
    parser.list_pods()
    parser = SosTraffic(sosarchive)
    parser.printResult()
else:
    raise Exception('Unsupported stats :' + stat)
