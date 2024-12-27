from enum import Enum
import sys, getopt, argparse, json, datetime, re
from FromJson import FromJson


class PromAlerts(FromJson):

#    promAlerts = None

    def __init__(self, alertFile):
        FromJson.__init__(self, alertFile)

    def listAlerts(self):
        alerts = dict()
        if self.fromJson is not None:
            for metric in self.fromJson["data"]["result"]:
                alertname = metric["metric"]["alertname"]
                if(alerts.get(alertname) is None):
                    alerts[alertname] = 1
                else:
                    alerts[alertname] = alerts[alertname] + 1
        return alerts
