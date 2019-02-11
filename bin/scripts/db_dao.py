# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#from __future__ import division
import os
HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(HOME)
sys.path.append(os.path.join(os.path.dirname(HOME), 'conf'))

from qfcommon.base import logger
log = logger.install('stdout')

from qfcommon.base import loader
loader.loadconf_argv(HOME)

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



def start():
    userids = []
    with get_connection('wxmp_customer') as db:
        _sql = " select appid,nick_name from `mp_conf` where status = 1 and appid != '' order by id desc "
        userids = db.query(_sql)
    if not userids: return

    appids = set()
    with get_connection('qf_solar') as db:
        appid_list = db.select('app_conf', fields='appid')
        appids = {i['appid'] for i in appid_list}

    # 入库
    value_list = []
    for xy in userids:
        value = {}
        value['appid'] = xy['appid']
        value['appname'] = xy['nick_name']
        if value['appid'] not in appids:
            value_list.append(value)
    if value_list:
        with get_connection('qf_solar') as db:
            db.insert_list(table='app_conf', values_list=value_list)

if __name__ == '__main__':
    start()
