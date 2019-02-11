# -*- coding: utf-8 -*-
from __future__ import division
import os
import sys
HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(HOME)
sys.path.append(os.path.join(os.path.dirname(HOME), 'conf'))

from qfcommon.base import logger
log = logger.install('stdout')

#from qfcommon.base import loader
#loader.loadconf_argv(HOME)

import urllib2
import urllib
import logging
import string
import datetime
import traceback
import json
import config
from qfcommon.base import dbpool
dbpool.install(config.DATABASE)

#from requests import post,get
from qfcommon.base.http_client import Urllib2Client
from qfcommon.base.dbpool import with_database,get_connection_exception,get_connection
from qfcommon.server.client import ThriftClient
import logging
import time
import datetime

from qfcommon.thriftclient.qf_wxmp import QFMP
from qfcommon.thriftclient.qf_wxmp.ttypes import WXToken



if __name__ == '__main__':
    _os = ['2018-05-11','2018-05-12','2018-05-17']
    for xy in _os:
        os.system("/home/qfpay/python/bin/python ./insert_applist_fix.py %s" % xy)