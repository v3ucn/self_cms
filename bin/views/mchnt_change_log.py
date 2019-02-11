# -*- coding: utf-8 -*-
from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import datetime
import time
import json
import traceback
from push_helper import push_msg2, set_custom, set_custom_dict, push_msg_v3
from push_helper import SEND_MODE_ALL, SEND_MODE_USERID, SEND_MODE_USERID
from qfcommon.base.dbpool import with_database,get_connection_exception,get_connection
from tools import checkIsLogin
from qfcommon.web import template
from qfcommon.web import core
import logging
from utils.misc import utf82unicode,now2str,unicode2utf8,convert_to_comma_delimited_string
from msg_center import MerchantMessageHandler, gen_mcht_msg
from social.social_message import gen_msg_id, gen_msg, SocialMessageHandler
from social.social_circle import SocialCircleHandler
from social.social_constants import MSG_TYPE_GOOD_BEGIN
import threading
from qfcommon.qfpay import defines
from qfcommon.thriftclient.audit import AuditServer
from qfcommon.server.client import ThriftClient

from qfcommon.thriftclient.weifutong import weifutong
from qfcommon.thriftclient.weifutong.ttypes import WechatConf,WechatConfUpdateItem,WechatConfUpdateArg,CHNLCODE

import uuid
import xlwt
import StringIO
import config



log = logging.getLogger()

unicode_to_utf8 = lambda s: s.encode('utf-8') if isinstance(s, unicode) else s


class mchntchangelog(core.Handler):
    @checkIsLogin
    def GET(self):
        uname = self.get_cookie('uname')
        data = {}
        data['uname'] = uname
        self.write(template.render('mchnt_change_log.html', data=data))


class BaseHandler(core.Handler):
    def __init__(self, app, req):
        super(BaseHandler, self).__init__(app, req)
        self.resp.mimetype = 'application/json'
        self.resp.headers['Content-Type'] = '%s; charset=%s' % (
            self.resp.mimetype, self.resp.charset)


#商户列表接口
class mchnt_change_log_list(BaseHandler):
    @with_database(["qf_solar"])
    def POST(self):

        try:
            params = self.req.inputjson()
            print params
            _sq = ' id != 0 '
            uid = params.get('uid')

            startdate = params.get('start_time')
            enddate = params.get('end_time')

            draw = params.get('draw')
            start = int(params.get('start'))
            length = int(params.get('length'))


            if startdate and enddate:
                _sq += " and ctime between '%s 00:00:00' and '%s 23:59:59'  " % (startdate,enddate)

            # if start_stime and end_stime:
            #     _sq += " and stime between  '%s %s' and '%s %s'  " % (start_stime,'00:00:00',end_stime,'23:59:59')

            if uid:
                uid = uid.split(",")
                if len(uid) > 0:
                    for xy in uid:
                        _sq += " and mchnt like '%%%s%%' " % str(xy)


            conn = self.db["qf_solar"]
            _sql = " select * from `mchnt_change` where  %s order by `ctime` desc limit %s,%s " % (_sq,start,length)
            print _sql
            log.debug(_sql)
            result = conn.query(_sql)
        except Exception, e:
            print e
            log.debug('mysql getdata error: %s' % traceback.format_exc())
            return json.dumps({'data': [],'code':'error'}, ensure_ascii=False)

        _sql_all = "select count(1) as count from `mchnt_change` where  %s " % _sq
        r_count = conn.query(_sql_all)

        try:
            recordsTotal = r_count[0]['count']
        except Exception, e:
            print e
            recordsTotal = 0
            pass



        # stime_list = []
        # with get_connection('qf_weifutong') as db:
        #     sql = "SELECT a.userid as uid,a.subscribe_appid as appid,a.ctime as stime FROM amchnl_bind a WHERE a.ctime in (SELECT MAX(`ctime`) FROM amchnl_bind where userid in (%s) and state = 1 GROUP BY userid) " % (uids_str)
        #     stime_list = db.query(sql)


        for d in result:


            try:
                _mchnt = d['mchnt'].split(',')
                d['mchnt'] = len(_mchnt)
            except Exception, e:
                print e
                d['mchnt'] = 0


            # 将mysql返回的日期数据类型转换成字符串
            try:
                #d['dtime'] = d['dtime'].strftime("%Y-%m-%d %H:%M:%S")
                d['ctime'] = d['ctime'].strftime("%Y-%m-%d %H:%M:%S")
            except Exception, e:
                print e
                d['ctime'] = ''

        return json.dumps({'draw': draw, 'recordsTotal': recordsTotal, 'recordsFiltered': recordsTotal, 'data': result,
                     'code': 200}, ensure_ascii=False)



#商户导出excel
class mchnt_log_tradeExcel(BaseHandler):
    def __init__(self, app, req):
        super(BaseHandler, self).__init__(app, req)
        self.resp.mimetype = 'application/vnd.ms-excel'
        self.resp.headers['Content-Type'] = '%s; charset=%s' % (
            self.resp.mimetype, self.resp.charset)

    @with_database(["qf_solar","qf_mis","qf_qudao","wxmp_customer","qf_weifutong","qf_fund2","qf_core"])
    def POST(self):
        params = self.req.input()
        id = params.get('id')

        conn = self.db["qf_solar"]
        _sql = " select * from `mchnt_change` where id = %s " % id
        result_u = conn.query(_sql)

        uuids = []

        uids = result_u[0]['mchnt']
        uid_list = uids.split(",")
        _len = len(uid_list)
        _appname = result_u[0]['appname']

        _ctime = str(result_u[0]['ctime'])
        _ctime = _ctime[0:10]

        _sname = '%s_%s_%s' % (_ctime,_appname,_len)

        self.resp.headers['Content-Disposition'] = 'attachment;filename="'+str(_sname)+'.xls"'

        _uidstr = ""
        for xy in uid_list:
            _uidstr += "%s," % int(xy)
            _zhi = {}
            _zhi['mchnt'] = xy
            uuids.append(_zhi)

        _uidstr = _uidstr.rstrip(",")

        _sql = "SELECT a.userid as uid, a.subscribe_appid as appid, a.ctime as stime,a.state,a.chnlcode,a.errmsg FROM amchnl_bind a WHERE a.ctime in (SELECT MAX(`ctime`) FROM amchnl_bind where userid in (%s) GROUP BY userid) " % _uidstr


        conn = self.db["qf_weifutong"]
        result_mc = conn.query(_sql)

        # 公众号
        results_mp_conf = self.db['wxmp_customer'].select(table='mp_conf', fields=['appid', 'nick_name'],
                                                          where={'status': 1})
        mp_conf = []
        wechat_id = []
        wechat_name = []
        for data in results_mp_conf:
            # if data.get('appid') and data.get('nick_name'):
            mp_conf.append(data)
            wechat_id.append(data.get('appid'))
            wechat_name.append(data.get('nick_name'))
        appIDtoNamedict = dict(zip(wechat_id, wechat_name))

        _group_type = {1: '白牌', 2: '联名', 3: '合伙人', 4: '直营', 5: '钱台', 6: '网络电销'}

        _chnlcode_type = {1: '中信普通', 2: '光大(已废弃)', 3: '富友', 4: '中信围餐', 5: '汇宜普通', 6: '汇宜快捷'

            , 7: '中信零费率', 8: '大则', 9: '网商', 10: '大则积分', 11: '收款宝', 12: '汇通', 13: '微信'

                          }
        _state_dic = {0:"未知",1:"成功",2:"失败"}

        for xy in uuids:
            chnlcode = ''
            appid = ""
            stime = ""
            state = 0
            errmsg = ''
            for jx in result_mc:
                if str(xy['mchnt']) == str(jx['uid']):
                    chnlcode = jx['chnlcode']
                    appid = jx['appid']
                    stime = str(jx['stime'])
                    state = jx['state']
                    errmsg = str(jx['errmsg'])
            xy['appid'] = appIDtoNamedict.get(appid)
            xy['chnlcode'] = _chnlcode_type.get(chnlcode)
            xy['stime'] = stime
            xy['state'] = _state_dic.get(state)
            xy['errmsg'] = errmsg






        header = ['商户ID','通道','关注公众号','结果','错误原因','时间']

        data_arr = []
        for i in uuids:
            info = {}
            info['mchnt'] = unicode_to_utf8(i.get('mchnt'))
            for (key, ve) in i.items():
                info[key] = unicode_to_utf8(str(ve))
            data_arr.append(info)

        # 创建一个workbook 设置编码
        workbook = xlwt.Workbook(encoding='utf-8')
        # 创建一个worksheet
        worksheet = workbook.add_sheet(_sname)
        i = 0
        for each_header in header:
            worksheet.write(0, i, each_header)
            i = i + 1
        j = 1
        for con in data_arr:
            worksheet.write(j, 0, con['mchnt'])
            worksheet.write(j, 1, con['chnlcode'])
            worksheet.write(j, 2, con['appid'])
            worksheet.write(j, 3, con['state'])
            worksheet.write(j, 4, con['errmsg'])
            worksheet.write(j, 5, con['stime'])
            j = j + 1
        # workbook.save('Excel_test.xls')
        sio = StringIO.StringIO()
        workbook.save(sio)  # 这点很重要，传给save函数的不是保存文件名，而是一个StringIO流

        return sio.getvalue()