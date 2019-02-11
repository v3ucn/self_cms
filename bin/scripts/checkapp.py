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
    now = int(time.time())
    userids = []
    userids.append({"appid":"wxeb6e671f5571abce","nickname":u"好近"})

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    bfore_yesterday = today - datetime.timedelta(days=2)

    client = ThriftClient(config.WX_SERVER, QFMP, framed=False)
    client.raise_except = True
    open_ids = []

    b_30 = today - datetime.timedelta(days=60)

    tlist = []

    newfans = []
    with get_connection('qf_mis') as db:
        sql = "select channelid,channelname from channel_crm where channelid = 20395 "
        newfans = db.query(sql)

    print newfans
    exit(-1)

    # newfans = []
    # with get_connection('open_user') as db:
    #     sql = "select count(1) as newfan, userid as uid,appid,`chnluserid` as mchnt_id from `subscribe` where ctime between '2018-06-14 00:00:00' and '2018-06-14 23:59:59' and userid in (2104049) group by userid,appid,chnluserid "
    #     newfans = db.query(sql)
    #
    # print newfans
    # exit(-1)

    # r = Urllib2Client().get("http://192.20.20.12:8097/findChnlInfo")
    # r_j = json.loads(r)
    # ls = r_j['data']
    #
    # for xy in ls:
    #     tlist.append(xy['chnlTypeCode'])
    #
    # tlist = set(tlist)
    # print tlist  2235043


    # qudao_list = []
    # with get_connection('qf_core') as db:
    #
    #     #sql = "update profile set user_state = 1 where userid = 2235043  "
    #     sql = "select userid,idenddate from profile where userid = 2235826  "
    #
    #     # sql = "update apply set usertype = 1 where user in (1322810,1659877,1680586,2118907,2125555,2128594,2138725,2199637,2217508,2218048,2222098,2224777,2224822,2224864);"
    #     qudao_list = db.query(sql)
    #
    # print qudao_list
    #
    # exit(-1)


    # qudao_list = []
    # with get_connection('qf_audit') as db:
    #     sql = "select userid,ext,id from salesman_event where ext like '%\"oldusertype\": null%'  "
    #     #sql = "update apply set usertype = 1 where user in (1322810,1659877,1680586,2118907,2125555,2128594,2138725,2199637,2217508,2218048,2222098,2224777,2224822,2224864);"
    #     qudao_list = db.query(sql)
    #
    # print qudao_list



    deals = []
    with get_connection('qf_solar') as db:
        _sql = "select * from `mchnt_list` where  ctime between 20180613 and 20180613   and uid in (1987190)"
        deals = db.query(_sql)
    print deals

    exit(-1)

    # _data = client.call('access_token','wx2af0f30b8b10de0a')
    # _token = _data.access_token
    #
    # print _token
    # exit(-1)

    #获取微信数据
    # for xy in userids:
    #
    #     _data = client.call('access_token',xy['appid'])
    #     _token = _data.access_token
    #
    #     #总粉丝数
    #     r = Urllib2Client().get("https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=" % _token)
    #     r_j = json.loads(r)
    #     xy['allfan'] = r_j["total"]
    #     open_ids = r_j['data']['openid']
    #
    #     #新增粉丝数
    #     _params = {"begin_date":str(yesterday).replace("-",''),"end_date":str(yesterday).replace("-",'')}
    #     r = Urllib2Client().post_json("https://api.weixin.qq.com/datacube/getusersummary?access_token=%s" % _token, _params,escape=False )
    #     r_j = json.loads(r)
    #     print r_j
    #     newfan = 0
    #     if r_j['list'][-1]:
    #         newfan = r_j['list'][-1]["new_user"]
    #
    #     xy['newfan'] = newfan
    # print userids
    #exit(-1)

        # #查看来源
        #
        # for jc in open_ids:
        #
        #     r = Urllib2Client().get("https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN" % (_token,str(jc)))
        #     r_j = json.loads(r)
        #     print r_j["subscribe_scene"]  2230180



    #获取交易笔数


    # deals = []
    # with get_connection('qf_audit') as db:
    #     _sql = "select userid,ext,state,type from `salesman_event` where type =2 and userid = 2192593  "
    #     deals = db.query(_sql)
    #
    # print deals
    # exit(-1)
    #
    # newfans = []
    # with get_connection('qf_solar') as db:
    #     #sql = "select count(1) as newfan, userid as uid,appid,`chnluserid` as mchnt_id from `subscribe` where DATE_FORMAT(ctime,'%%Y-%%m-%%d') = '2018-06-11'  group by userid,appid,chnluserid limit 10"
    #     #sql = "select * from salesman_event where userid = 2230180 and type = 1 "
    #     sql = "select chnlcode from app_rule   "
    #     newfans = db.query(sql)
    #
    # print newfans
    # exit(-1)
    #
    #
    # with get_connection('open_user') as db:
    #     #sql = "select count(1) as newfan, userid as uid,appid,`chnluserid` as mchnt_id from `subscribe` where DATE_FORMAT(ctime,'%%Y-%%m-%%d') = '2018-06-11'  group by userid,appid,chnluserid limit 10"
    #     sql = "select * from `subscribe` where chnluserid != '' order by userid desc limit 2"
    #     newfans = db.query(sql)
    #
    # print newfans
    # exit(-1)

    # deals = []
    # with get_connection('qf_solar') as db:
    #     _sql = "select * from `mchnt_list` where   ctime between 20180610 and 20180610   and uid in (1572440)"
    #     deals = db.query(_sql)
    #
    # print deals
    # exit(-1)


    # 获取交易笔数
    # deals = []
    # with get_connection('qf_solar') as db:
    #     _sql = "select count(DISTINCT `mchnt_id`) from `mchnt_list` where   id != 0  and ctime between 20180412 and 20180523 "
    #     deals = db.query(_sql)
    #
    # print deals
    # exit(-1)


    # deals = []
    # with get_connection('qf_audit') as db:
    #     _sql = "select userid,ext,state from `salesman_event` where userid = 1587465  "
    #     deals = db.query(_sql)
    #
    # print deals
    # exit(-1)1668004

    #slist = [1322810,1659877,1680586,2118907,2125555,2128594,2138725,2199637,2217508,2218048,2222098,2224777,2224822,2224864]
    slist = [2224858,1709404,2224648,2075924,2224402,2209915 ,2200336
]


    # for xy in slist:
    #
    #
    #     with get_connection('qf_mis') as db:
    #         sql = "select userid,name,imgname from mis_voucher_history where userid =  %s and name = 'shopphoto' order by id desc limit 1 " % xy
    #         qudao_list = db.query(sql)
    #
    #     print qudao_list
    #
    #
    #     with get_connection('qf_mis') as db:
    #         sql = "update mis_upgrade_voucher set imgname = '%s' where user_id =  %s and name = 'shopphoto' " % (qudao_list[0]['imgname'],qudao_list[0]['userid'])
    #         db.query(sql)
    #
    # exit(-1)


    #
    # qudao_list = []
    # with get_connection('qf_audit') as db:
    #     sql = "select userid,ext,id from salesman_event where ext like '%\"oldusertype\": null%'"
    #     #sql = "update apply set usertype = 1 where user in (1322810,1659877,1680586,2118907,2125555,2128594,2138725,2199637,2217508,2218048,2222098,2224777,2224822,2224864);"
    #     qudao_list = db.query(sql)
    #
    # for xy in qudao_list:
    #     _ext = json.loads(xy['ext'])
    #     del _ext['oldusertype']
    #     _ext = json.dumps(_ext,ensure_ascii=False)
    #     _sql = "update salesman_event set ext = '%s' where id = %s " % (_ext,xy['id'])
    #     db.query(_sql)
    #
    # print qudao_list
    # exit(-1)
    #
    # deals = []
    # with get_connection('qf_trade') as db:
    #     sql = "select count(1) as deal,userid as uid,chnluserid as mchnt_id,chnlid from `%s` where sysdtm between '2018-05-31 00:00:00' and '2018-05-31 23:59:59'  and `status` = 1 and `busicd` in ('800201','800207','800208') and chnluserid = '226801000004003759372'  " % (
    #     'record_201805')
    #     print sql
    #     deals = db.query(sql)
    #
    #
    #
    # print deals
    # exit(-1)

    # deals = []
    # with get_connection('qf_mis') as db:
    #     _sql = "select user,ext,state from `salesman_event` where userid = 1587465  "
    #     deals = db.query(_sql)
    #
    # print deals
    # exit(-1)
    #
    # #2108593
    #
    #
    # with get_connection('qf_mis') as db:
    #     _sql = "select user_id,`name`,imgname from  `mis_upgrade_voucher` where user_id in (2170012) and name in ('checkstand_alipay','checkstand_weixin','checkin_weixin','checkin_alipay','licensephoto','goodsphoto','shopphoto')"
    #     img_list = db.query(_sql)
    #
    # def replace_img(imgname, userid):
    #     ret = 'http://pic.qfpay.com/userprofile/%d/%d/%s' % (int(userid) / 10000, int(userid), imgname)
    #     return ret
    #
    # dict_img = {'checkstand_alipay': '收银台照片_支付宝蓝海', 'checkstand_weixin': '收银台照片_微信绿洲'
    #     , 'checkin_weixin': '餐饮平台入驻照_微信绿洲', 'checkin_alipay': '餐饮平台入驻照_支付宝蓝海', 'goodsphoto': '店铺内景照片'
    #     , 'shopphoto': '店铺外景照片', 'licensephoto': '营业执照'}
    #
    # CUR_PATH = '../static/common/zip'
    #
    # for xy in img_list:
    #     img_src = replace_img(xy['imgname'], xy['user_id'])
    #     print img_src
    #     try:
    #         urllib.urlretrieve(img_src, "%s/%s_%s.jpg" % (CUR_PATH, str(xy['user_id']), dict_img[xy['name']]))
    #     except Exception, e:
    #         print e
    #         log.debug(str(e))
    # exit(-1)


    # deals = []
    # with get_connection('qf_mis') as db:
    #     _sql = "select user_id,`name`,imgname from  `mis_upgrade_voucher` where user_id in (2170012) and name in ('checkstand_alipay','checkstand_weixin','checkin_weixin','checkin_alipay','licensephoto','goodsphoto','shopphoto')"
    #     deals = db.query(_sql)
    #
    # print deals
    # exit(-1)
    #
    # deals = []
    # with get_connection('qf_core') as db:
    #     _sql = "select userid,feeratio from account where userid in (2206156) "
    #     deals = db.query(_sql)
    #
    # print deals
    # exit(-1)

    # deals = []
    # with get_connection('qf_audit') as db:
    #     _sql = "update `salesman_event` set state = 2,memo = '测试失败' where userid in (1993892,2086667)  "
    #     deals = db.query(_sql)
    #
    # print deals
    # exit(-1)

    #print yesterday


    # 获取交易笔数
    # deals = []
    # with get_connection('qf_mis') as db:
    #     _sql = "select user_id,detail from mis_oplog where admin_id = 320293 and action_time between '2018-04-25 00:00:00' and '2018-04-25 23:59:59'"
    #     deals = db.query(_sql)
    #
    # for xy in deals:
    #     _str = "%s|%s" % (xy['user_id'],xy['detail'])
    #     w = file('/home/qfpay/solar/1/bin/scripts/jobs.txt','a')
    #     w.write("%s\n" % _str)
    #     w.close()
    #
    # print deals


    # newfans = []
    # with get_connection('open_user') as db:
    #     sql = "select count(1) as newfan, userid as uid,appid,customer_id from `subscribe` where DATE_FORMAT(ctime,'%%Y-%%m-%%d') = '%s' and userid = 2086718 group by userid,appid,customer_id " % (
    #     yesterday)
    #     newfans = db.query(sql)
    #
    # print newfans



    #select `uid`,`id` from `mchnt_list` where   id != 0  and ctime between 20180411 and 20180411   and uid in (451869)

    # deals = []
    # with get_connection('qf_weifutong') as db:
    #      _sql = "select userid as uid,MAX(`ctime`) as stime  from `amchnl_bind` where userid = 2070263 and `state` = 1 group by userid order by stime desc "
    #      deals = db.query(_sql)

    #
    #  deals = []
    # with get_connection('open_user') as db:
    #     sql = "select count(1) as deal,userid as uid,ctime as dtime,`appid` from `open_user`.`subscribe` where ctime between '%s 00:00:00' and '%s 23:59:59' and userid = 2070263  group by userid order by ctime desc" % (
    #     b_30, yesterday)
    #     deals = db.query(sql)
    #
    # print deals


    #
    #  userids = []
    # with get_connection('wxmp_customer') as db:
    #     _sql = " select appid,nick_name from `mp_conf` where status = 1 and nick_name = '' "
    #     userids = db.query(_sql)
    # print userids  800100090148461

    # userids = [{'appid':'wxeb6e671f5571abce','name':u'好近'}]
    #
    # deals = []
    # with get_connection('qf_trade') as db:
    #     sql = "select count(1) as deal,userid as uid,chnluserid as mchnt_id,chnlid,`busicd`,`paydtm` from `%s` where  DATE_FORMAT(paydtm,'%%Y-%%m-%%d') = '2018-05-08'  and `status` = 1  and `busicd` in ('800201','800207','800208') group by mchnt_id " % (
    #     "record_201805")
    #     print sql
    #     deals = db.query(sql)
    #
    # _mchids = ""
    # for xy in deals:
    #     _mchids += "'%s'," % str(xy['mchnt_id'])
    # _mchids = _mchids.rstrip(",")
    #
    # newfans = []
    # with get_connection('qf_weifutong') as db:
    #     sql = "select `mchnt_id`,`subscribe_appid` as appid from `amchnl_bind` where  state = 1 and subscribe_appid != '' and mchnt_id in (%s)  group by  `mchnt_id`,`subscribe_appid` " % (
    #     _mchids)
    #     newfans = db.query(sql)
    #
    # for xy in userids:
    #     xy['mchnt_id'] = []
    #     for jx in newfans:
    #         if xy['appid'] == jx['appid']:
    #             xy['mchnt_id'].append(jx['mchnt_id'])
    #
    # for xy in userids:
    #     _shop = 0
    #     _deal = 0
    #
    #     _shop = len(xy['mchnt_id'])
    #
    #     for jx in deals:
    #         for jc in xy['mchnt_id']:
    #             if str(jc) == str(jx['mchnt_id']):
    #                 _deal += int(jx['deal'])
    #     xy['deal'] = _deal
    #     xy['shop'] = _shop
    #
    # print userids
    #
    #
    # exit(-1)

    #
    #  deals = []
    # with get_connection('qf_weifutong') as db:
    #      _sql = "select userid,mchnt_id from `amchnl_bind` where mchnt_id = '800100090148461' and `state` = 1 "
    #      deals = db.query(_sql)
    #
    # print deals

    # newfans = []
    # with get_connection('open_user') as db:
    #     sql = "select count(*) as newfan,userid as uid from (select * from (select openid,appid,userid from `subscribe` where DATE_FORMAT(ctime,'%%Y-%%m-%%d') = '%s' and userid = %s group by userid,appid) a WHERE NOT EXISTS  (select appid,userid from `subscribe` where DATE_FORMAT(ctime,'%%Y-%%m-%%d') <= '%s' and userid = %s group by userid,appid  ) ) c " % (
    #     yesterday,1336107, bfore_yesterday,1336107)
    #     print sql
    #     newfans = db.query(sql)
    # print newfans

    #1722811

    # newfans = []
    # with get_connection('qf_core') as db:
    #     sql = "select code,name from `channel`"
    #     newfans = db.query(sql)
    # print newfans

    # deals1 = []
    #
    # with get_connection('qf_weifutong') as db:
    #      _sql = "select `subscribe_appid`,`ctime` from `amchnl_bind` where `state` = 1 and userid = 2070263 order by ctime desc "
    #      deals1 = db.query(_sql)
    #
    # print deals1

    # ops = ''
    # for xy in open_ids:
    #     ops += "'%s'," % xy
    # ops = ops.rstrip(",")
    #
    # deals_openid = []
    # with get_connection('open_user') as db:
    #     _sql = "select openid,userid,appid from `subscribe` where DATE_FORMAT(ctime,'%%Y-%%m-%%d') = '%s' and openid in (%s) group by openid " % (str(yesterday),str(ops))
    #     deals_openid = db.query(_sql)
    exit(-1)

    for xy in userids:
        _shop = 0
        _deal = 0
        for jx in deals:
            if xy['appid'] == jx['appid']:
                _shop = int(jx['shop'])
                _deal = int(jx['deal'])
        if _deal == 0:
            _fan = "0%"
        else:
            _fan = "%s%%" % str( round(int(xy['newfan']) / int(_deal),4))

        xy['shop'] = _shop
        xy['deal'] = _deal
        xy['fan'] = _fan





if __name__ == '__main__':
    start()
