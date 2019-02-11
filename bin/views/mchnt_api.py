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
from tools import checkIsLogin, raise_excp
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

from utils.util import (
    get_tag_user, all_tag_user, get_user_tags,
    is_valid_int,get_data_qudao
)
from utils.excepts import ParamError



log = logging.getLogger()

unicode_to_utf8 = lambda s: s.encode('utf-8') if isinstance(s, unicode) else s



class BaseHandler(core.Handler):
    def __init__(self, app, req):
        super(BaseHandler, self).__init__(app, req)
        self.resp.mimetype = 'application/json'
        self.resp.headers['Content-Type'] = '%s; charset=%s' % (
            self.resp.mimetype, self.resp.charset)


class ret2template(core.Handler):
    @checkIsLogin
    def GET(self):
        uname = self.get_cookie('uname')
        data = {}
        data['uname'] = uname
        self.write(template.render("push_message.html", data=data))

#商户列表接口
class mchnt_list(BaseHandler):
    @with_database(["qf_solar","qf_weifutong", 'qf_user'])
    def POST(self):

        try:
            params = self.req.inputjson()
            print params
            _sq = ' id != 0 '
            uid = params.get('uid')
            mcca = params.get('mcca')
            mcc = params.get('mcc')
            pro = params.get('pro')
            city = params.get('city')
            groupid = params.get('groupid')
            group_type = params.get('group_type')
            appid = params.get('appid')

            # start_dtime = params.get('start_dtime')
            # end_dtime = params.get('end_dtime')
            #
            # start_stime = params.get('start_stime')
            # end_stime = params.get('end_stime')

            startdate = params.get('startdate')
            enddate = params.get('enddate')
            draw = params.get('draw')
            start = int(params.get('start'))
            length = int(params.get('length'))

            cate_codes = params.get('cate_codes')
            cate_codes = [i.strip() for i in cate_codes.split(',')] if cate_codes else []
            if startdate == '' and enddate == '':
                today = datetime.date.today()
                yesterday = today - datetime.timedelta(days=1)
                startdate = str(yesterday).replace("-","")
                enddate = str(yesterday).replace("-", "")


            if startdate and enddate:
                _sq += " and ctime between %s and %s  " % (int(startdate.replace("-","")),int(enddate.replace("-","")))

            cate_userids = get_tag_user(cate_codes)
            uid = [int(i) for i in uid if is_valid_int(i)]
            if uid and cate_userids:
                uid = list(set(uid) & set(cate_userids))
            elif cate_userids:
                uid = cate_userids

            if uid:
                if len(uid) > 0:
                    _str = ''
                    for xy in uid:
                        _str += '%s,' % str(xy)
                    _str = _str.rstrip(",")
                    _sq += ' and uid in (%s) ' % _str
            elif cate_codes and params.get('uid'):
                _sq += ' and uid = "-1" '

            # 需要避免无意义的查询
            if 'untagged' in cate_codes:
                all_tag_userids = all_tag_user()
                all_tag_userids = set(all_tag_userids) - set(uid)
                all_tag_userids = [str(i) for i in all_tag_userids if i]
                if all_tag_userids:
                    _sq += ' and uid not in ({}) '.format(','.join(all_tag_userids))

            if appid:
                if len(appid) > 0:
                    _str = ''
                    for xy in appid:
                        _str += "'%s'," % str(xy)
                    _str = _str.rstrip(",")
                    _sq += ' and appid in (%s) ' % _str

            if mcca:
                _sq += " and mcc like '%s___'  " % str(mcca)

            if mcc:
                _sq += " and mcc = %s  " % str(mcc)

            if pro:
                _sq += " and pro = '%s'  " % str(pro)

            if city:
                _sq += " and city = '%s'  " % str(city)

            if groupid:
                _sq += " and groupid = %s  " % str(groupid)

            if group_type:
                _sq += " and group_type = %s  " % str(group_type)

            # 直营全部 = 直营 + 钱台 + 网络电销
            elif not getattr(config, 'IS_DIS_ALL', True):
                _sq += " and group_type in (4, 5, 6) "

            conn = self.db["qf_solar"]
            _sql = " select * from `mchnt_list` where  %s order by `ctime` desc limit %s,%s " % (_sq,start,length)
            #print _sql
            log.debug(_sql)
            result = conn.query(_sql)
        except Exception, e:
            print e
            log.debug('mysql getdata error: %s' % traceback.format_exc())
            return json.dumps({'data': [],'code':'error'}, ensure_ascii=False)

        _sql_all = "select count(1) as count from `mchnt_list` where  %s " % _sq
        r_count = conn.query(_sql_all)

        try:
            recordsTotal = r_count[0]['count']
        except Exception, e:
            print e
            recordsTotal = 0
            pass

        _sql_uids = "select `uid`,`id` from `mchnt_list` where  %s " % _sq
        r_uids = conn.query(_sql_uids)

        uids = []
        ids = []
        uids_str = ""
        for xy in r_uids:
            uids.append(int(xy['uid']))
            ids.append(int(xy['id']))

        for xy in result:
            uids_str += "%s," % int(xy['uid'])
        uids_str = uids_str.rstrip(",")

        # stime_list = []
        # with get_connection('qf_weifutong') as db:
        #     sql = "SELECT a.userid as uid,a.subscribe_appid as appid,a.ctime as stime FROM amchnl_bind a WHERE a.ctime in (SELECT MAX(`ctime`) FROM amchnl_bind where userid in (%s) and state = 1 GROUP BY userid) " % (uids_str)
        #     stime_list = db.query(sql)
        cate_codes = get_user_tags(uids, display='join_name')

        qd_dict = get_data_qudao()
        for d in result:
            # 将mysql返回的日期数据类型转换成字符串
            try:
                #d['dtime'] = d['dtime'].strftime("%Y-%m-%d %H:%M:%S")
                d['stime'] = d['stime'].strftime("%Y-%m-%d %H:%M:%S")
            except Exception, e:
                print e
                d['stime'] = ''

            try:
                d['fan'] = "%s%%" % str(round(  int(d['newfan']) / int(d['deal']) * 100 , 4))
            except Exception, e:
                d['fan'] = '0%'

            try:
                d['group_type'] = qd_dict.get(d['groupid'],'未知')
            except Exception, e:
                print e

            d['now_appid'] = ''
            d['now_stime'] = ''
            userid = d.get('uid')
            d['cate_name'] = cate_codes.get(userid, '无标签')

            # for jx in stime_list:
            #     if d['uid'] == jx['uid']:
            #         d['now_appid'] = jx['appid']
            #         d['now_stime'] = jx['stime'].strftime("%Y-%m-%d %H:%M:%S")

        return json.dumps({'draw': draw, 'recordsTotal': recordsTotal, 'recordsFiltered': recordsTotal, 'data': result,
                     'code': 200, 'uids': uids,'ids':ids}, ensure_ascii=False)



#商户关注历史
class mchnt_history(BaseHandler):
    @with_database(["qf_weifutong"])
    def POST(self):

        try:
            params = self.req.inputjson()
            uid = params.get('uid')

            # with get_connection('qf_weifutong') as db:
            #     userids = db.select(
            #         table='amchnl_bind',
            #         where={'state':1, 'userid':uid},
            #         fields='subscribe_appid,ctime')

            conn = self.db["qf_weifutong"]
            _sql = " select `subscribe_appid`,`ctime`,`mchnt_id`,`chnlcode` from `amchnl_bind` where `state` = 1 and userid = %s order by ctime desc " % str(uid)
            result = conn.query(_sql)
        except Exception, e:
            print e
            log.debug('mysql getdata error: %s' % traceback.format_exc())
            return json.dumps({'data': [],'code':'error'}, ensure_ascii=False)

        _re = []

        for d in result:
            # 将mysql返回的日期数据类型转换成字符串
            try:
                d['ctime'] = d['ctime'].strftime("%Y-%m-%d %H:%M:%S")
            except Exception, e:
                d['ctime'] = ''

            _re.append({'uid':uid,'subscribe_appid':d['subscribe_appid'],'ctime':d['ctime'],'mchnt_id':d['mchnt_id'],'chnlcode':d['chnlcode']})

        return json.dumps({ 'data': _re,'code': 200}, ensure_ascii=False)

# 商户切换公众号
class mchnt_change(BaseHandler):
    @with_database(["qf_weifutong","qf_solar","wxmp_customer"])
    def POST(self):

        def byteify(input):
            if isinstance(input, dict):
                return {byteify(key): byteify(value) for key, value in input.iteritems()}
            elif isinstance(input, list):
                return [byteify(element) for element in input]
            elif isinstance(input, unicode):
                return input.encode('utf-8')
            else:
                return input

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

        try:
            params = self.req.inputjson()
            uids = params.get('uids')
            appid = params.get('appid')
            pay_appid = params.get('pay_appid')
            menu = params.get('menu')
            cid = params.get('cid')
            chnlcode = params.get('chnlcode')
            memo = params.get('memo')

            list = uids
            s_list = []
            relationship = getattr(config, 'RELATIONSHIP', 1)
            for xy in list:
                _wc = WechatConf(jsapipath=json.dumps(menu,ensure_ascii=False),sub_appid=str(pay_appid),
                                 subscribe_appid=str(appid),cid=str(cid),relationship=relationship)
                _va = WechatConfUpdateItem(userid=xy,wechat_conf=_wc,chnlcode=int(chnlcode))
                s_list.append(_va)

            log.debug("weifutong args: %s" % s_list)

            client = ThriftClient(config.WEIFUTONG_SERVER,weifutong, framed=True)
            client.raise_except = True
            _batch_id = str(uuid.uuid1())
            client.call('wechatconf_update',arg=WechatConfUpdateArg(batch_id=_batch_id, src='audit.1',wechatconf_list=s_list))

            #插入记录表
            values = {}
            values['mchnt'] = ','.join('%s' % id for id in uids)
            values['menu'] = ','.join('%s' % id for id in menu)
            values['appid'] = appid
            values['d_appid'] = pay_appid
            values['cid'] = cid
            values['memo'] = memo
            values['user'] = self.get_cookie('uname')
            values['ctime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            values['appname'] = appIDtoNamedict[appid]

            with get_connection('qf_solar') as db:
                db.insert(table='mchnt_change', values=values)

        except Exception, e:
            print e
            log.debug('error: %s' % traceback.format_exc())
            return json.dumps({'data': [], 'code': 'error'}, ensure_ascii=False)


        return json.dumps({'data': 'ok', 'code': 200}, ensure_ascii=False)




#商户导出excel
class tradeExcel(BaseHandler):
    def __init__(self, app, req):
        super(BaseHandler, self).__init__(app, req)
        self.resp.mimetype = 'application/vnd.ms-excel'
        self.resp.headers['Content-Type'] = '%s; charset=%s' % (
            self.resp.mimetype, self.resp.charset)

    @with_database(["qf_solar","qf_mis","qf_qudao","wxmp_customer","qf_weifutong","qf_fund2","qf_core"])
    def POST(self):
        params = self.req.input()
        uids = params.get('uids')
        uids_l = uids.split(",")

        _sq = ' uid != 0 '

        mcca = params.get('mcca')
        mcc = params.get('mcc')
        pro = params.get('pro')
        city = params.get('city')
        groupid = params.get('groupid')
        group_type = params.get('group_type')
        appid = params.get('appid')

        startdate = params.get('startdate')
        enddate = params.get('enddate')
        log.debug('params={}'.format(params))

        if startdate and enddate:
            _sq += " and ctime between %s and %s  " % (int(startdate.replace("-", "")), int(enddate.replace("-", "")))

        # if start_stime and end_stime:
        #     _sq += " and stime between  '%s %s' and '%s %s'  " % (start_stime,'00:00:00',end_stime,'23:59:59')

        cate_codes = params.get('cate_code')
        cate_codes = [i.strip() for i in cate_codes.split(',')] if cate_codes else []
        cate_userids = get_tag_user(cate_codes)

        # 需要避免无意义的查询
        if 'untagged' in cate_codes:
            all_tag_userids = all_tag_user()
            all_tag_userids = set(all_tag_userids) - set(uids_l)
            all_tag_userids = [str(i) for i in all_tag_userids if i]
            if all_tag_userids:
                _sq += ' and uid not in ({}) '.format(','.join(all_tag_userids))

        if cate_userids:
            cate_userids = [str(i) for i in cate_userids]
            _sq += ' and uid in ({}) '.format(','.join(cate_userids))

        if appid:
            if len(appid) > 0:
                _str = ''
                appid = appid.split(",")
                for xy in appid:
                    _str += "'%s'," % str(xy)
                _str = _str.rstrip(",")
                _sq += ' and appid in (%s) ' % _str


        if mcca:
            _sq += " and mcc like '%s___'  " % str(mcca)

        if mcc:
            _sq += " and mcc = %s  " % str(mcc)

        if pro:
            _sq += " and pro = '%s'  " % str(pro)

        if city:
            _sq += " and city = '%s'  " % str(city)

        if groupid:
            _sq += " and groupid = %s  " % str(groupid)

        if group_type:
            _sq += " and group_type = %s  " % str(group_type)

        #行业
        result_mccs = self.db['qf_mis'].select(table='tools_mcc', fields=['id', 'mcc_name'])
        mcc_idArr = []
        mcc_nameArr = []
        for result in result_mccs:
            mcc_idArr.append(result.get('id'))
            mcc_nameArr.append(result.get('mcc_name'))
        # 封装成ID为key name为value的字典格式
        id_mcc = dict(zip(mcc_idArr, mcc_nameArr))

        #渠道
        result_groupids = self.db['qf_qudao'].select(table='qd_profile', fields=['qd_uid', 'name'])
        old = self.db['qf_mis'].select(table='channel_crm', fields=['channelid', 'channelname'])
        for v in old:
            result_groupids.append({'qd_uid': v['channelid'], 'name': v['channelname']})
        groupid = []
        groupname = []
        for result in result_groupids:
            groupid.append(int(result.get('qd_uid')))
            groupname.append(result.get('name'))
        groupIDtoName = dict(zip(groupid, groupname))

        #公众号
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
        appIDtoNamedict= dict(zip(wechat_id, wechat_name))

        _chnlcode_type = {1: '中信普通', 2: '光大(已废弃)', 3: '富友', 4: '中信围餐', 5: '汇宜普通', 6: '汇宜快捷'

            ,7: '中信零费率',8: '大则',9: '网商',10: '大则积分',11: '收款宝',12: '汇通',13: '微信'

                          }

        fund2_result = self.db['qf_core'].select(table='channel', fields=['code', 'name'])
        _chnlcode_type = {}
        for i in fund2_result:
            try:
                keystr = int(i.get('code', 0))
                _chnlcode_type[keystr] = i['name']
            except Exception, e:
                pass

        _ids = ''

        for xy in uids_l:
            _ids += "%s," % str(xy)
        _ids = _ids.rstrip(",")

        conn = self.db["qf_solar"]
        #_sql = " select * from `mchnt_list` where id in (%s) and %s order by `ctime` desc " % (_ids,_sq)
        _sql = " select `uid`,`nickname`,`mcc`,`pro`,`city`,`groupid`,`group_type`,`appid`,`stime`,`mchnt_id`,sum(fan) as fan,sum(newfan) as newfan,sum(deal) as deal,`chnlcode` from `mchnt_list` where id in (%s) and %s group by `uid`,`mchnt_id`  order by `ctime` desc " % (_ids, _sq)
        result = conn.query(_sql)

        # stime_list = []
        # with get_connection('qf_weifutong') as db:
        #     sql = "SELECT a.userid as uid,a.subscribe_appid as appid,a.ctime as stime FROM amchnl_bind a WHERE a.ctime in (SELECT MAX(`ctime`) FROM amchnl_bind where userid in (%s) and state = 1 GROUP BY userid) " % (
        #     _ids)
        #     stime_list = db.query(sql)
        userids_in = [i['uid'] for i in result]
        code_name = get_user_tags(userids_in, display='join_name')
        log.debug('code_name={}'.format(code_name))

        qd_dict = get_data_qudao()
        for d in result:
            # 将mysql返回的日期数据类型转换成字符串
            try:
                d['mcc'] = id_mcc[d['mcc']]
            except Exception, e:
                pass


            try:
                d['group_type'] = qd_dict.get(d['groupid'],'未知')
            except Exception, e:
                print e
                pass


            try:
                d['groupid'] = groupIDtoName[d['groupid']]
            except Exception, e:
                log.debug(e)
                pass

            try:
                d['appid'] = appIDtoNamedict[d['appid']]
            except Exception, e:
                pass


            try:
                d['chnlcode'] = _chnlcode_type[int(d['chnlcode'])]
            except Exception, e:
                pass
            try:
                d['stime'] = d['stime'].strftime("%Y-%m-%d %H:%M:%S")
            except Exception, e:
                pass
            try:
                d['fan'] = "%s%%" % str(round(  int(d['newfan']) / int(d['deal']) * 100 , 4))
            except Exception, e:
                d['fan'] = '0%'

            d['now_appid'] = ''
            d['now_stime'] = ''
            userid = d.get('uid')
            d['cate_name'] = code_name.get(userid, '无标签')

            # for jx in stime_list:
            #     if d['uid'] == jx['uid']:
            #         try:
            #             d['now_appid'] = appIDtoNamedict[jx['appid']]
            #             d['now_stime'] = jx['stime'].strftime("%Y-%m-%d %H:%M:%S")
            #         except Exception, e:
            #             pass
        data_arr = []
        for i in result:
            info = {}
            info['userid'] = unicode_to_utf8(i.get('userid'))
            for (key, ve) in i.items():
                info[key] = unicode_to_utf8(str(ve))
            data_arr.append(info)

        #header = ['商户id','商户名称','交易日期','支付通道','通道商户号','关注公众号','关注时间','新增粉丝数','微信交易笔数','吸粉率','行业','省份','城市','所属渠道','渠道类型', '标签']
        header = ['商户id', '商户名称','支付通道', '通道商户号', '关注公众号', '关注时间', '新增粉丝数', '微信交易笔数', '吸粉率', '行业', '省份', '城市',
                  '所属渠道', '渠道类型', '标签']

        # 创建一个workbook 设置编码
        workbook = xlwt.Workbook(encoding='utf-8')
        # 创建一个worksheet
        worksheet = workbook.add_sheet('My Worksheet')
        i = 0
        for each_header in header:
            worksheet.write(0, i, each_header)
            i = i + 1
        j = 1
        for con in data_arr:
            worksheet.write(j, 0, con['uid'])
            worksheet.write(j, 1, con['nickname'])
            #worksheet.write(j, 2, con['ctime'])
            worksheet.write(j, 2, con['chnlcode'])
            worksheet.write(j, 3, con['mchnt_id'])
            worksheet.write(j, 4, con['appid'])
            worksheet.write(j, 5, con['stime'])
            worksheet.write(j, 6, con['newfan'])
            worksheet.write(j, 7, con['deal'])
            worksheet.write(j, 8, con['fan'])
            worksheet.write(j, 9, con['mcc'])
            worksheet.write(j, 10, con['pro'])
            worksheet.write(j, 11, con['city'])
            worksheet.write(j, 12, con['groupid'])
            worksheet.write(j, 13, con['group_type'])
            worksheet.write(j, 14, con['cate_name'])
            j = j + 1
        # workbook.save('Excel_test.xls')
        sio = StringIO.StringIO()
        workbook.save(sio)  # 这点很重要，传给save函数的不是保存文件名，而是一个StringIO流

        return sio.getvalue()



