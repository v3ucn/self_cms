# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import datetime
import time
import json
import traceback
from qfcommon.base.dbpool import with_database,get_connection_exception,get_connection
from tools import checkIsLogin
from qfcommon.web import template
from qfcommon.web import core
import logging
from utils.misc import utf82unicode,now2str,unicode2utf8,convert_to_comma_delimited_string
from utils.redis_util import get_app_conf_set, get_app_conf_dict, APP_PREF, APP_CUSTOM

from qfcommon.base.tools import thrift_callex
from qfcommon.thriftclient.apollo import ApolloServer
from qfcommon.thriftclient.audit import AuditServer
from qfcommon.thriftclient.audit.ttypes import Audit
from qfcommon.server.client import ThriftClient

from qfcommon.thriftclient.qudao import QudaoServer

from requests import post,get
import config

from qfcommon.thriftclient.weifutong import weifutong
from qfcommon.thriftclient.weifutong.ttypes import WechatConf,WechatConfUpdateItem,WechatConfUpdateArg


import uuid

log = logging.getLogger()


class BaseHandler(core.Handler):
    def __init__(self, app, req):
        super(BaseHandler, self).__init__(app, req)
        self.resp.mimetype = 'application/json'
        self.resp.headers['Content-Type'] = '%s; charset=%s' % (
            self.resp.mimetype, self.resp.charset)




#消息列表页面
class start_page_list(BaseHandler):
    @checkIsLogin
    def GET(self):
        uname = self.get_cookie('uname')
        data = {}
        data['uname'] = uname
        conf_name = APP_CUSTOM

        # app_id = 48
        # conf_id = 13
        # conf_dict = get_app_conf_dict(app_id, conf_id, app_conf=conf_name)
        # print conf_dict

        import redis
        # 连接，可选不同数据库
        r = redis.Redis(host='172.100.102.101', port=6379, db=7)

        data = {'id': '123'}

        r.hset('rekey', 123, data)

        all_audits = r.hgetall('rekey')

        # for (d,x) in all_audits.items():
        #     print x


        # -------------------------------------------
        # 看信息
        #keys = r.keys()
        #print type(keys)
        #print r.exists('appcustom_appid12_confid39_dict')
        #print r.hget('appcustom_appid12_confid39_dict')

        # with get_connection('qf_core') as db:
        #     profiles = db.select(
        #         table='profile',
        #         fields='userid',
        #         where={'userid': (' = ',10516)}
        #     )
        #     userids = [i['userid'] for i in profiles or []]
        # print len(userids)

        #keys = r.keys()
        #print type(keys)

        #[{'addr': ('172.100.101.107', 6900), 'timeout': 2000}, ]

        #client = ThriftClient([{'addr': ('127.0.0.1',7100), 'timeout': 6000}, ], AuditServer)
        #client = ThriftClient([{'addr': ('172.100.101.110', 7100), 'timeout': 6000}, ], AuditServer)

        #client = ThriftClient([{'addr': ('172.100.101.107', 6900), 'timeout': 2000}, ], ApolloServer)

        _info = '{"usertype":"1","mobile":"18650005057","nickname":"萌宠乐园宠物用品店","licensenumber":"92350205MA2YNJ287E","legalperson":"法人代表","idnumber":"350204199411150028","dishonestyinfo":"0","idnumbertime":"2017-01-01到2017-01-09","src":"签约宝","shoptype":"分店","otherid":"业务员","nickname":"收据名称","mcc":"1005","shop_province":"北京","shop_city":"北京","shop_address":"厦门市沧林东一里573号","telephone":"1231231","email":"123@123.net","banktype":"1","bankuser":"1123123","account_province":"北京","account_city":"北京","headbankname":"北京银行","bankname":"北京银行","bankcode":"12312","channel_type":"合伙人","salesmanname":"你好","salesmanname":"你好","channel_name":"你好","channel_province":"北京","channel_city":"北京","memo":"无","risk_level":"123","risk_level":"123","alipay_ratio": 0.0038,"qqpay_ratio": 0.0038,"tenpay_ratio": 0.0038,"jdpay_ratio": 0.006,"fee_ratio": 0.006,"credit_ratio": 0.006,"bankaccount":6217231510001346967,"cardstart":"2017-03-05","cardend":"2017-05-01","usertags":["123","456"],"salesman_memo":"234","audit_record":[{"operator":"0","audit_result":"自动审核成功","audit_time":"2017-10-01","audit_memo":"自动审核成功"}],"piclist":[{"name":"idcardfront","src":"http://pic.qfpay.com/userprofile/205/2053691/middle_5fb259576ad455e4949f6767f20ca297.jpg"},{"name":"idcardback","src":"http://pic.qfpay.com/userprofile/205/2053691/middle_5fb259576ad455e4949f6767f20ca297.jpg"}]}'

        #client.raise_except = True
        #re = client.call('add_audit', Audit(audit_type='signup',userid=10516,groupid=10,info=_info))
        _m = '{"nickname":"123","usertags":["777"],"audit_record":{"operator":"123","audit_result":"123","audit_time":"123","audit_memo":"123"}}'
        #re = client.call('audit_api',id='6366572138127548259',type='4',modify=_m)


        #re = thrift_callex([{'addr': ('172.100.101.110',7100), 'timeout': 6000}, ], AuditServer, 'ping')

        #client = ThriftClient([{'addr': ('172.100.108.65',7100), 'timeout': 16000}, ], AuditServer,framed=False)


        _info = {}

        _piclist = []


        # for i in range(20):
        #     _piclist.append({"name": str('123'), "src": str('至'), "cert_type": str(100)})

        # _info["piclist"] = _piclist
        # _info["nickname"] = '123123你好'
        # _info["mcc"] = "12313"
        # _info["src"] = u"12313"
        # _info["tenpay_ratio"] = "12313"
        # _info["alipay_ratio"] = "12313"
        # _info = byteify(_info)
        # _info = json.dumps(_info,ensure_ascii=False)

        #测试成都
        #101.204.228.105:6221

        # from qfcommon.thriftclient.weifutong.ttypes import WechatConf,WechatConfUpdateItem,WechatConfUpdateArg,CHNLCODE
        #
        # client = ThriftClient([{'addr':('101.204.228.105',6221),'timeout': 8000},],weifutong,framed=True)
        # client.raise_except = True
        # s_list = []
        # _wc = WechatConf(jsapipath='["http://123"]',sub_appid='wx087a3fc3f3757766',subscribe_appid='wx087a3fc3f3757766')
        # _va = WechatConfUpdateItem(userid=21006662,wechat_conf=_wc,chnlcode=9)
        # s_list.append(_va)
        # client.call('wechatconf_update',arg=WechatConfUpdateArg(batch_id='1231234567899090123',src='audit.1',wechatconf_list=s_list))

        client = ThriftClient([{'addr': ('172.100.101.110', 7100), 'timeout': 8000}, ], AuditServer, framed=False)
        #client = ThriftClient([{'addr': ('172.100.101.107', 7200), 'timeout': 8000}, ], AuditServer, framed=False)
        #client = ThriftClient([{'addr': ('127.0.0.1',7100), 'timeout': 6000}, ],AuditServer, framed=False)
        # client = ThriftClient([{'addr': ('192.10.2.150',7201), 'timeout': 6000}, ], AuditServer, framed=False)
        # client.raise_except = True
        list = client.call('app_api',[704263],5)
        print list

        #测试威富通通道结果
        from qfcommon.thriftclient.weifutong import weifutong
        from qfcommon.thriftclient.weifutong.ttypes import CHNLCODE, QueryMeta, AddMchntQueryArg

        TONGDAOS = [CHNLCODE.CITIC, CHNLCODE.ZXWC, CHNLCODE.FUIOU, CHNLCODE.HUIYI, CHNLCODE.HYQK,
                    CHNLCODE.WANGSHANG,
                    CHNLCODE.DAZEPOINT,
                    CHNLCODE.YEEPAY,
                    CHNLCODE.HUITONG,
                    CHNLCODE.WEIXIN,
                    CHNLCODE.FUIOU_LVZHOU,
                    CHNLCODE.HELIBAO
                    ]

        client = ThriftClient([{'addr': ('192.10.2.150', 6221), 'timeout': 2000}, ], weifutong, framed=True)
        client.raise_except = True

        _uids = [2202982]

        merchant_dic = {}
        queryMeta = QueryMeta()
        queryMeta.offset = 0
        queryMeta.count = 10
        queryMeta.orderby = 'utime desc'

        addMchntQueryArg = AddMchntQueryArg()
        addMchntQueryArg.query_meta = queryMeta
        addMchntQueryArg.userid_list = _uids
        addMchntQueryArg.chnlcode_list = TONGDAOS
        record_ids_l = client.call('addmchnt_query', addMchntQueryArg)

        addMchntRecord_d = client.call('addmchnt_get', record_ids_l)
        l1 = []
        for (key, ve) in addMchntRecord_d.items():
            l1.append({'state':ve.state,'errmsg':ve.errmsg,'chnlcode':ve.chnlcode,'ctime':ve.ctime})
        l1.sort(key=lambda k: (k.get('ctime', 0)),reverse=True)
        l4 = []
        l4.append(l1[0])
        for dict in l1:
            # print len(l4)
            k = 0
            for item in l4:
                # print 'item'
                if dict['chnlcode'] != item['chnlcode']:
                    k = k + 1
                    # continue
                else:
                    break
                if k == len(l4):
                    l4.append(dict)
        print l1


        #print addMchntRecord_d[6389763976217181206].chnlcode




        #client = ThriftClient([{'addr': ('172.100.101.107', 7200), 'timeout': 8000}, ], AuditServer, framed=False)

        #client = ThriftClient([{'addr': ('127.0.0.1',7100), 'timeout': 6000}, ], AuditServer, framed=False)

        #re = client.call('ping')
        #re = client.call('add_audit', Audit(audit_type='signup', userid=10516, groupid=10,info=_info))


        #client = ThriftClient([{'addr':('192.30.2.173', 8001), 'timeout':50000}], QudaoServer, framed=True)
        #client.raise_except = True
        #QudaoBaseInfo = client.call('qd_get_hierarchy',[1764616,1778227],1)

        #list = client.call('app_api',[21006662])
        #print list['wx087a3fc3f3757766'].jsapipath
        #from qfcommon.thriftclient.audit.ttypes import AppInfo
        #AppInfo = list[0]
        #print AppInfo.pay_appid
        #print AppInfo.appid
        #print AppInfo.jsapipath
        #print AppInfo.uid

        # _zhi = {'id': 1, 'type': 123}
        #
        # json_data = json.dumps(_zhi)
        #
        # r.lpush("1",json_data)
        #
        # data1 = r.brpop("1")
        #
        # print data1

        #r.set("name",'123')


        # with get_connection('open_user') as db:
        #     userids = db.select(
        #         table='amchnl_bind',
        #         fields='subscribe_appid,ctime')


        # from qfcommon.thriftclient.qf_wxmp import QFMP
        # from qfcommon.thriftclient.qf_wxmp.ttypes import WXToken
        #
        # weixin_server = [{'addr': ('192.30.2.168', 6150), 'timeout': 8000},]
        # weixin_server = [{'addr': ('172.100.101.107', 6120), 'timeout': 8000},]
        #
        # client = ThriftClient(weixin_server,QFMP,framed=False)
        # client.raise_except = True
        # _data = client.call('access_token','wx087a3fc3f3757766')
        #
        # print _data.access_token


        return json.dumps({'data': '123'}, ensure_ascii=False)

