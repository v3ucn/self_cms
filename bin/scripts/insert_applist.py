# -*- coding: utf-8 -*-
from __future__ import division
import os
import sys
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
    now = int(time.time())
    userids = []
    with get_connection('wxmp_customer') as db:
        _sql = " select appid,nick_name from `mp_conf` where status = 1 and appid != '' "
        userids = db.query(_sql)
    if not userids: return

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    _table_name = "record_%s" % str(str(yesterday).replace("-", ""))[0:6]
    client = ThriftClient(config.WX_SERVER, QFMP, framed=False)
    client.raise_except = True

    #获取微信数据
    for xy in userids:

        try:
            _data = client.call('access_token',xy['appid'])
            _token = _data.access_token

            #总粉丝数
            r = Urllib2Client().get("https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=" % _token)
            r_j = json.loads(r)
            xy['allfan'] = r_j["total"]

            #新增粉丝数
            _params = {"begin_date":str(yesterday).replace("-",''),"end_date":str(yesterday).replace("-",'')}
            r = Urllib2Client().post_json("https://api.weixin.qq.com/datacube/getusersummary?access_token=%s" % _token, _params,escape=False )
            r_j = json.loads(r)
            newfan = 0
            cuser = 0
            for gcc in r_j['list']:
                if gcc['user_source'] == 51:
                    newfan = gcc['new_user']
                    cuser = gcc['cancel_user']

            auser = newfan - cuser


            xy['newfan'] = newfan
            xy['cuser'] = cuser
            xy['auser'] = auser
        except Exception, e:
            print e
            xy['allfan'] = 0
            xy['newfan'] = 0
            xy['cuser'] = 0
            xy['auser'] = 0

    deals = []
    with get_connection('qf_trade') as db:
        sql = "select count(1) as deal,chnluserid as mchnt_id from `%s` where  DATE_FORMAT(paydtm,'%%Y-%%m-%%d') = '%s'  and `status` = 1 and `busicd` in ('800201','800207','800208') group by mchnt_id " % (
        _table_name, yesterday)
        deals = db.query(sql)


    _mchids = ""
    for xy in deals:
        _mchids += "'%s'," % str(xy['mchnt_id'])
    _mchids = _mchids.rstrip(",")

    newfans = []
    with get_connection('qf_weifutong') as db:
        sql = "select `mchnt_id`,`subscribe_appid` as appid from `amchnl_bind` where  state = 1 and subscribe_appid != '' and mchnt_id in (%s)  group by  `mchnt_id`,`subscribe_appid` " % (_mchids)
        newfans = db.query(sql)


    for xy in userids:
        xy['mchnt_id'] = []
        for jx in newfans:
            if xy['appid'] == jx['appid']:
                xy['mchnt_id'].append(jx['mchnt_id'])

    for xy in userids:
        _shop = 0
        _deal = 0

        _shop = len(xy['mchnt_id'])

        for jx in deals:
            for jc in xy['mchnt_id']:
                if str(jc) == str(jx['mchnt_id']):
                    _deal += int(jx['deal'])


        if _deal == 0:
            _fan = "0%"
        else:
            _fan = "%s%%" % str( round(int(xy['newfan']) / int(_deal),4))

        xy['shop'] = _shop
        xy['deal'] = _deal
        xy['fan'] = _fan

        #入库

        values = {}
        values['appid'] = xy['appid']
        values['appname'] = xy['nick_name']
        values['belong'] = '钱方银通'
        values['shop'] = int(xy['shop'])
        values['deal'] = int(xy['deal'])
        values['newfan'] = int(xy['newfan'])
        values['allfan'] = int(xy['allfan'])
        values['fan'] = xy['fan']
        values['ctime'] = str(yesterday).replace("-",'')
        values['auser'] = int(xy['auser'])
        values['cuser'] = int(xy['cuser'])
        try:
            with get_connection('qf_solar') as db:
                db.insert(table='app_list', values=values)
        except:
            print traceback.format_exc()
        else:
            with get_connection('qf_solar') as db:
                db.update('app_list',
                          values={
                              'shop':int(xy['shop']),
                            'deal':int(xy['deal']),
                                     'newfan':int(xy['newfan']),
                              'auser': int(xy['auser']),
                              'cuser': int(xy['cuser']),
                                        'allfan':int(xy['allfan'])
                            ,'fan':xy['fan']
                          },
                          where={
                              'appid': values['appid'],
                              'ctime': values['ctime']
                          })



if __name__ == '__main__':
    start()
