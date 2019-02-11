# -*- coding: utf-8 -*-
from __future__ import division
import sys
reload(sys)
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
import string
import datetime
import traceback
import json
import config
from qfcommon.base import dbpool
dbpool.install(config.DATABASE)

from requests import post,get
from qfcommon.base.dbpool import with_database,get_connection_exception,get_connection
from qfcommon.server.client import ThriftClient
import logging
import time
import datetime

from qfcommon.thriftclient.qf_wxmp import QFMP
from qfcommon.thriftclient.qf_wxmp.ttypes import WXToken


log = logging.getLogger()



def start():
    now = int(time.time())

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    _table_name = "record_%s" % str(str(yesterday).replace("-",""))[0:6]
    bfore_yesterday = today - datetime.timedelta(days=2)
    b_30 = today - datetime.timedelta(days=60)

    #新增粉丝数 newfan

    # newfans = []
    # with get_connection('open_user') as db:
    #     sql = "select count(*) as newfan,userid as uid from (select * from (select openid,appid,userid from `subscribe` where DATE_FORMAT(ctime,'%%Y-%%m-%%d') = '%s' group by openid,userid,appid) a WHERE NOT EXISTS  (select openid,appid,userid from `subscribe` where DATE_FORMAT(ctime,'%%Y-%%m-%%d') <= '%s' and openid = a.openid and userid = a.userid and appid = a.appid group by openid,userid,appid  ) ) c " % (yesterday,bfore_yesterday)
    #     newfans = db.query(sql)
    #
    # print len(newfans)
    # log.debug(len(newfans))

    newfans = []
    with get_connection('open_user') as db:
        sql = "select count(1) as newfan, userid as uid,appid,`chnluserid` as mchnt_id from `subscribe` where DATE_FORMAT(ctime,'%%Y-%%m-%%d') = '%s' group by userid,appid,chnluserid " % (yesterday)
        newfans = db.query(sql)



    #交易笔数 交易时间
    # deals = []
    # with get_connection('open_user') as db:
    #     sql = "select count(1) as deal,userid as uid,MAX(ctime) as dtime,`appid` from `open_user`.`subscribe` where ctime between '%s 00:00:00' and '%s 23:59:59'  group by userid order by dtime desc" % (b_30,yesterday)
    #     deals = db.query(sql)


    deals = []
    with get_connection('qf_trade') as db:
        sql = "select count(1) as deal,userid as uid,chnluserid as mchnt_id,chnlid from `%s` where sysdtm between '%s 00:00:00' and '%s 23:59:59'  and `status` = 1 and `busicd` in ('800201','800207','800208') group by mchnt_id,userid " % (_table_name,yesterday,yesterday)
        deals = db.query(sql)

    str_uids = ''
    str_mids = ''
    for xy in deals:
        str_uids += '%s,' % str(xy['uid'])
        str_mids += "'%s'," % str(xy['mchnt_id'])
    str_uids = str_uids.rstrip(",")
    str_mids = str_mids.rstrip(",")

    #档案表数据
    profile_list = []
    with get_connection('qf_core') as db:
        sql = "select userid as uid,nickname,`mcc`,`province` as pro,`city` from `profile` where userid in (%s) " % (str_uids)
        profile_list = db.query(sql)

    #渠道数据
    qudao_list = []
    with get_connection('qf_qudao') as db:
        sql = "select a.mchnt_uid as uid,a.qd_uid as groupid,b.`type` as group_type from `mchnt_user` a left join `qd_user` b on a.qd_uid = b.qd_uid  where a.mchnt_uid in (%s) " % (str_uids)
        qudao_list = db.query(sql)

    old_list = []
    with get_connection('qf_mis') as db:
        sql = "select `user` as uid,groupid from `apply` where `user` in (%s) " % (
        str_uids)
        old_list = db.query(sql)

    #关注时间
    stime_list = []
    with get_connection('qf_weifutong') as db:
        sql = "select `ctime` as stime,`subscribe_appid` as `appid`,mchnt_id  from `amchnl_bind` where mchnt_id in (%s)   and  state = 1 group by mchnt_id " % (str_mids)
        stime_list = db.query(sql)

    #入库
    for xy in deals:
        values = {}

        values['uid'] = xy['uid']
        values['deal'] = xy['deal']

        values['mchnt_id'] = xy['mchnt_id']
        values['chnlcode'] = xy['chnlid']

        _ctime = str(yesterday).replace("-","")
        _ctime = int(_ctime)
        values['ctime'] = _ctime



        _deal = int(xy['deal'])

        _nickname = ''
        _mcc = 0
        _pro = ''
        _city = ''

        for jx in profile_list:
            if xy['uid'] == jx['uid']:
                _nickname = jx['nickname']
                _mcc= jx['mcc']
                _pro = jx['pro']
                _city = jx['city']

        values['nickname'] = _nickname
        values['mcc'] = _mcc
        values['pro'] = _pro
        values['city'] = _city

        _groupid = 0
        _group_type = 0

        for jx in qudao_list:
            if xy['uid'] == jx['uid']:
                _groupid = jx['groupid']
                _group_type = jx['group_type']

        if _groupid == 0:
            for jx in old_list:
                if xy['uid'] == jx['uid']:
                    _groupid = jx['groupid']


        values['groupid'] = _groupid
        values['group_type'] = _group_type

        _stime = ''
        _appid = ''

        for jx in stime_list:
            if str(xy['mchnt_id']) == str(jx['mchnt_id']):
                _stime = jx['stime']
                _appid = jx['appid']

        values['stime'] = _stime
        values['appid'] = _appid

        _newfan = 0
        for jx in newfans:
            #if xy['uid'] == jx['uid'] and values['appid'] == jx['appid']:
            if xy['uid'] == jx['uid'] and str(values['mchnt_id']) == str(jx['mchnt_id']):
                _newfan = jx['newfan']

        values['newfan'] = _newfan

        # with get_connection('qf_solar') as db:
        #     db.insert(table='mchnt_list', values=values)

        try:
            with get_connection('qf_solar') as db:
                db.insert(table='mchnt_list', values=values)
        except:
            print traceback.format_exc()
        else:
            with get_connection('qf_solar') as db:
                db.update('mchnt_list',
                          values={
                'deal':values['deal'],
                              'newfan': values['newfan'],
                              'nickname': values['nickname'],
                              'mcc': values['mcc'],
                              'pro': values['pro'],
                              'city': values['city'],
                              'groupid': values['groupid'],
                              'appid': _appid,
                              'group_type': values['group_type'],
                              'mchnt_id': values['mchnt_id'],
                              'chnlcode': values['chnlcode'],
                              'stime': _stime
                          },
                          where={
                              'uid': values['uid'],
                              'mchnt_id': values['mchnt_id'],
                              'ctime': values['ctime']
                          })

if __name__ == '__main__':
    start()
