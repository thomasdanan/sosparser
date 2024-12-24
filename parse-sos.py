#!python
import sys, getopt, argparse, json
from path import Path
from SosUsage import SosUsage
from SosTopo import SosTopo
from SosAlerts import SosAlerts
from enum import Enum


class STAT(Enum):
    ALL=1
    TOPO=2
    USAGE=3
    ALERTS=4

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


if stat == STAT.USAGE:
    parser = SosUsage(sosarchive)
    parser.extractUsage()
elif stat == STAT.TOPO:
    parser = SosTopo(sosarchive)
    parser.extractTopo()
elif stat == STAT.ALERTS:
    parser = SosAlerts(sosarchive)
    parser.extractAlerts()
elif stat == STAT.ALL:
    parser = SosUsage(sosarchive)
    parser.extractUsage()
    parser = SosTopo(sosarchive)
    parser.extractTopo()
    parser = SosAlerts(sosarchive)
    parser.extractAlerts()
else:
    raise Exception('Unsupported stats :' + stat)
