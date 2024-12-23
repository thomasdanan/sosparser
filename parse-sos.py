#!python
import sys, getopt, argparse, json
from SosUsage import SosUsage
from enum import Enum


class STAT(Enum):
    USAGE=1

parser = argparse.ArgumentParser(description="Parse ARTESCA sosreport",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("sosarchive", type=str, help="sosreport archive folder")
parser.add_argument("stat", type=str, choices=[i.name for i in STAT], help="stat to extract")


args = parser.parse_args()
stat=STAT[args.stat]
sosarchive=args.sosarchive

if stat == STAT.USAGE:
    parser = SosUsage(sosarchive)
    parser.extractUsage()
else:
    raise Exception('Unknown command :' + stat)
