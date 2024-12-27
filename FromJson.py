from enum import Enum
from path import Path
import sys, getopt, argparse, json, datetime, re


class FromJson:

    fromJson = None

    def __init__(self, jsonFile):
        if(Path(jsonFile).is_file()):
            with open(jsonFile, 'r') as file:
                self.fromJson = json.load(file)
        else:
            print("No json file found: " + jsonFile)
