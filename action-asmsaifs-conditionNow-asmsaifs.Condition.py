#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    import requests
    
    res = requests.get(
      "http://blynk.fiqraat.com:8080/ba55ee0ee2fd4bc29bd63e538040826c/get/V10")
    res2 = requests.get(
      "http://blynk.fiqraat.com:8080/ba55ee0ee2fd4bc29bd63e538040826c/get/V11")
    if res.status_code == 200 and res2.status_code == 200:
      say = "Current temperature is {0} degree celcius and humidity is {1} percent." \
          .format(str(res.json()[0]), str(res2.json()[0]))
      hermes.publish_end_session(intentMessage.session_id, say)
    


if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("asmsaifs:conditionNow", subscribe_intent_callback) \
         .start()
