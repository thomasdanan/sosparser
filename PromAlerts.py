from enum import Enum
import sys, getopt, argparse, json, datetime, re


class PromAlerts:

    promAlerts = None


    def __init__(self, metricFile):
        with open(metricFile, 'r') as file:
            self.promAlerts = json.load(file)

    def listAlerts(self):
        alerts = dict()
        for metric in self.promAlerts["data"]["result"]:
            alertname = metric["metric"]["alertname"]
            if(alerts.get(alertname) is None):
                alerts[alertname] = 1
            else:
                alerts[alertname] = alerts[alertname] + 1
        return alerts
