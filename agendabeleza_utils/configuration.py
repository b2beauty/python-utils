#!/usr/bin/python

import yaml
import os,sys


def loadConfigFile(relPath,configPath = "/../../config.yaml"):
    configDir   = os.path.dirname(relPath)+configPath
    configFile  = open(configDir, 'r')
    return yaml.load(configFile)
