#!/usr/bin/python
# coding=utf-8
import os
import sys
import logging
import logging.config
import ConfigParser

ROOT = os.path.abspath(os.path.split(__file__)[0])
sys.path.insert(0, ROOT)

cf = ConfigParser.ConfigParser()
if not cf.read("../ibserver.conf"):
    cf.read("ibserver.conf")

if not os.path.exists('../logs/'):
    os.makedirs('../logs/')

logging.config.fileConfig(os.path.join(ROOT, 'logging.conf'))
logger = logging.getLogger("sizeLogger")

logger.setLevel(int(cf.get("log", "level")))  # 设置日志级别

SERVER_PORT = 8080
