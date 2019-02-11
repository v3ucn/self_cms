# -*- coding: utf-8 -*-
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
import xlwt,xlrd
import StringIO
import config
import os
import zipfile
import urllib


log = logging.getLogger()

unicode_to_utf8 = lambda s: s.encode('utf-8') if isinstance(s, unicode) else s


class Sales_Audit(core.Handler):
    @checkIsLogin
    def GET(self):
        uname = self.get_cookie('uname')
        data = {}
        data['uname'] = uname
        data['uid'] = self.get_cookie('uid')
        self.write(template.render('sales_audit_list.html', data=data))


class BaseHandler(core.Handler):
    def __init__(self, app, req):
        super(BaseHandler, self).__init__(app, req)
        self.resp.mimetype = 'application/json'
        self.resp.headers['Content-Type'] = '%s; charset=%s' % (
            self.resp.mimetype, self.resp.charset)


#商户列表接口
class Sales_Audit_List(BaseHandler):
    @with_database(["qf_audit"])
    def POST(self):

        try:
            params = self.req.inputjson()
            print params
            _sq = ' id != 0 '
            uid = params.get('uid')

            startdate = params.get('start_time')
            enddate = params.get('end_time')

            if startdate is None and enddate is None:
                today = datetime.date.today()
                yesterday = today
                startdate = str(yesterday)
                enddate = str(yesterday)

            type = params.get('type')
            state = params.get('state')

            draw = params.get('draw')
            start = int(params.get('start'))
            length = int(params.get('length'))

            if type:
                _sq += " and type = %s " % str(type)

            if state:
                _sq += " and state = %s " % str(state)


            if startdate and enddate:
                _sq += " and ctime between '%s' and '%s'  " % (startdate,enddate)


            # if uid:
            #     # uid = uid.split(",")
            #     # if len(uid) > 0:
            #     #     for xy in uid:
            #     #         _sq += " and mchnt like '%%%s%%' " % str(xy)
            #     _sq += " and userid = %s " % str(uid)

            if uid:
                uid = uid.split(',')
                if len(uid) > 0:
                    _str = ''
                    for xy in uid:
                        _str += '%s,' % str(xy)
                    _str = _str.rstrip(",")
                    _sq += ' and userid in (%s) ' % _str


            conn = self.db["qf_audit"]
            _sql = " select * from `salesman_event` where  %s order by `ctime` desc limit %s,%s " % (_sq,start,length)
            print _sql
            log.debug(_sql)
            result = conn.query(_sql)
        except Exception, e:
            print e
            log.debug('mysql getdata error: %s' % traceback.format_exc())
            return json.dumps({'data': [],'code':'error'}, ensure_ascii=False)

        _sql_all = "select count(1) as count from `salesman_event` where  %s " % _sq
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


        dict_type = {1:'微信绿洲',2:'支付宝蓝海'}
        dict_state = {1:'审核通过',2:'审核失败',3:'待审'}
        for d in result:


            # 将mysql返回的日期数据类型转换成字符串
            try:
                #d['dtime'] = d['dtime'].strftime("%Y-%m-%d %H:%M:%S")
                d['ctime'] = d['ctime'].strftime("%Y-%m-%d %H:%M:%S")
            except Exception, e:
                print e
                d['ctime'] = ''

            try:
                #d['dtime'] = d['dtime'].strftime("%Y-%m-%d %H:%M:%S")
                d['atime'] = d['atime'].strftime("%Y-%m-%d %H:%M:%S")
            except Exception, e:
                print e
                d['atime'] = ''

            try:
                d['type'] = dict_type[d['type']]
            except Exception, e:
                print e
                d['type'] = ''

            try:
                d['state'] = dict_state[d['state']]
            except Exception, e:
                print e
                d['state'] = ''

        return json.dumps({'draw': draw, 'recordsTotal': recordsTotal, 'recordsFiltered': recordsTotal, 'data': result,
                     'code': 200}, ensure_ascii=False)

class Sales_Do_Audit(BaseHandler):
    @with_database(["qf_audit","qf_settle"])
    def POST(self):

        params = self.req.inputjson()
        print params

        uid = params.get('uids').strip()

        memo = params.get('memo')

        state = int(params.get('type'))

        stype = int(params.get('stype'))

        now = time.strftime('%Y-%m-%d %H:%M:%S')


        if uid:
            uid = uid.split(",")

        uids = ""
        for xy in uid:
            uids += "%s," % int(xy)
        uids = uids.rstrip(",")

        print uids


        conn = self.db["qf_audit"]
        conn_settle = self.db["qf_settle"]
        _sql = " select `userid`,`type` from `salesman_event` where  userid in (%s) and type = %s " % (uids,stype)
        log.debug(_sql)
        result = conn.query(_sql)


        for xy in result:

            if state == 1:

                try:
                    if xy['type'] == 1:
                        _sql = "update account set tenpay_ratio = 0 where userid = %s " % xy['userid']
                    else:
                        _sql = "update account set alipay_ratio = 0 where userid = %s " % xy['userid']

                    conn_settle.query(_sql)
                except Exception, e:
                    print e
                    pass




            sql = "update `salesman_event` set state = %s,memo = '%s',atime = '%s',admin_userid = %s where userid = %s and type = %s " % (state,memo,now,self.get_cookie('uid'),xy['userid'],xy['type'])
            print sql
            conn.query(sql)


        return json.dumps(
            {'code': 200}, ensure_ascii=False)




class SalesExcel(BaseHandler):
    def __init__(self, app, req):
        super(BaseHandler, self).__init__(app, req)

        self.set_headers({'Content-Type': 'application/octet-stream'})
        self.set_headers(
            {'Content-disposition': 'attachment; filename={}'.format('sales.xls')})

    @with_database(["qf_solar","qf_audit","qf_mis","qf_qudao","wxmp_customer","qf_weifutong","qf_fund2","qf_core"])
    def POST(self):
        params = self.req.input()

        _sq = " id != 0 "

        log.debug(str(params))

        startdate = params.get('startdate')
        enddate = params.get('enddate')

        type = params.get('type')
        state = params.get('state')

        mchntid = params.get('mchntid')


        # if mchntid:
        #     _sq += " and userid = %s " % mchntid

        if mchntid:
            uid = mchntid.split(',')
            if len(uid) > 0:
                _str = ''
                for xy in uid:
                    _str += '%s,' % str(xy)
                _str = _str.rstrip(",")
                _sq += ' and userid in (%s) ' % _str


        if type:
            _sq += " and type = %s " % str(type)

        if state:
            _sq += " and state = %s " % str(state)

        if startdate and enddate:
            _sq += " and ctime between '%s' and '%s'  " % (startdate, enddate)

        conn = self.db["qf_audit"]
        _sql = " select `userid`,`type`,`state`,`ctime`,`sls_uid`,`atime`,`memo` from `salesman_event` where %s order by ctime desc " % _sq
        uuids = conn.query(_sql)
        uids = ''

        for xy in uuids:
            try:
                uids += "%s," % int(xy['userid'])
            except Exception, e:
                print e
                log.debug(str(e))
                pass

        uids = uids.rstrip(",")

        conn = self.db["qf_core"]
        _sql = " select `userid`,`name`,`nickname`,`province`,`city`,`businessaddr` from `profile` where userid in (%s) " % uids
        result_f = conn.query(_sql)

        for xy in uuids:
            name = ''
            nickname = ''
            province = ''
            city = ''
            businessaddr = ''
            for jx in result_f:
                if xy['userid'] == jx['userid']:
                    name = jx['name']
                    nickname = jx['nickname']
                    province = jx['province']
                    city = jx['city']
                    businessaddr = jx['businessaddr']
            xy['name'] = name
            xy['nickname'] = nickname
            xy['province'] = province
            xy['city'] = city
            xy['businessaddr'] = businessaddr

        dict_state = {1:'审核成功',2:'审核失败',3:'待审'}
        dict_type = {1: '微信绿洲', 2: '支付宝蓝海'}


        header = ['商户ID','企业名称','店铺门头名称','经营省份','经营城市','店铺经营地址','活动类型','创建时间','创建人','审核状态','备注','审核时间']

        data_arr = []

        for i in uuids:
            info = {}
            try:
                i['state'] = dict_state[i.get('state')]
                i['type'] = dict_type[i.get('type')]
            except Exception, e:
                print e
                log.debug(str(e))
                pass
            for (key, ve) in i.items():
                info[key] = unicode_to_utf8(str(ve))
            data_arr.append(info)

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
            worksheet.write(j, 0, con['userid'])
            worksheet.write(j, 1, con['name'])
            worksheet.write(j, 2, con['nickname'])
            worksheet.write(j, 3, con['province'])
            worksheet.write(j, 4, con['city'])
            worksheet.write(j, 5, con['businessaddr'])
            worksheet.write(j, 6, con['type'])
            worksheet.write(j, 7, con['ctime'])
            worksheet.write(j, 8, con['sls_uid'])
            worksheet.write(j, 9, con['state'])
            worksheet.write(j, 10, con['memo'])
            worksheet.write(j, 11, con['atime'])
            j = j + 1
        # workbook.save('Excel_test.xls')
        sio = StringIO.StringIO()
        workbook.save(sio)  # 这点很重要，传给save函数的不是保存文件名，而是一个StringIO流

        return sio.getvalue()



class Sales_Download(core.Handler):
    @with_database(["qf_mis","qf_audit"])
    def POST(self):
        params = self.req.inputjson()

        _sq = " id != 0 "

        startdate = params.get('startdate')
        enddate = params.get('enddate')

        type = params.get('type')
        state = params.get('state')

        mchntid = params.get('mchntid')

        if mchntid:
            uid = mchntid.split(',')
            if len(uid) > 0:
                _str = ''
                for xy in uid:
                    _str += '%s,' % str(xy)
                _str = _str.rstrip(",")
                _sq += ' and userid in (%s) ' % _str

        if type:
            _sq += " and type = %s " % str(type)

        if state:
            _sq += " and state = %s " % str(state)

        if startdate and enddate:
            _sq += " and ctime between '%s' and '%s'  " % (startdate, enddate)


        dict_img = {'checkstand_alipay':'收银台照片_支付宝蓝海','checkstand_weixin':'收银台照片_微信绿洲'
        ,'checkin_weixin':'餐饮平台入驻照_微信绿洲','checkin_alipay':'餐饮平台入驻照_支付宝蓝海','goodsphoto':'店铺内景照片'
        ,'shopphoto':'店铺外景照片','licensephoto':'营业执照'}


        CUR_PATH = './static/common/zip'

        os.system('mkdir ./static/common/zip/zip_%s' % str(self.get_cookie('uid')))

        def del_file(path):
            ls = os.listdir(path)
            for i in ls:
                c_path = os.path.join(path, i)
                if os.path.isdir(c_path):
                    del_file(c_path)
                else:
                    os.remove(c_path)

        del_file(CUR_PATH)

        #下载文件
        conn = self.db["qf_audit"]
        sql = " select DISTINCT `userid` from `salesman_event` where %s " % _sq
        userids = conn.query(sql)
        uidstr = ''
        for xy in userids:
            try:
                uidstr += "%s," % int(xy['userid'])
            except Exception, e:
                print e
                log.debug(str(e))
                pass
        uidstr = uidstr.rstrip(",")

        conn = self.db["qf_mis"]
        sql = " select user_id,`name`,imgname from  `mis_upgrade_voucher` where user_id in (%s) and name in ('checkstand_alipay','checkstand_weixin','checkin_weixin','checkin_alipay','licensephoto','goodsphoto','shopphoto') " % uidstr
        img_list = conn.query(sql)

        for xy in img_list:
            img_path = "%s%s/%s/%s" % ("/home/qfpay/mfs/userprofile/", str(xy['user_id'] / 10000), str(xy['user_id']), 'middle_' + xy['imgname'])
            log.debug(str(img_path))
            os.system('cp %s ./static/common/zip/zip_%s/%s_%s.jpg' % (img_path,str(self.get_cookie('uid')),str(xy['user_id']),dict_img[xy['name']]))

        startdir = "./static/common/zip/zip_%s" % str(self.get_cookie('uid'))  # 要压缩的文件夹路径
        file_news = startdir + '.zip'  # 压缩后文件夹的名字
        z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(startdir):
            fpath = dirpath.replace(startdir, '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath + filename)
                print ('压缩成功')
        z.close()

        return json.dumps({'code':200,'msg':'success','data':{}})


class Upload_Ajax(core.Handler):
    @with_database(["qf_audit", "qf_settle"])
    def POST(self):
        def print_all(module_):
            modulelist = dir(module_)
            length = len(modulelist)
            for i in range(0, length, 1):
                print getattr(module_, modulelist[i])
        file_obj = self.req.storage.list[0]
        fileitem = file_obj.file
        now = time.strftime('%Y-%m-%d %H:%M:%S')

        open('./static/common/zip/excel_%s.xls' % str(self.get_cookie('uid')), 'wb').write(fileitem.read())

        myWorkbook = xlrd.open_workbook('./static/common/zip/excel_%s.xls' % str(self.get_cookie('uid')))

        sh = myWorkbook.sheet_by_name("Sheet1")

        nrows = sh.nrows
        conn = self.db["qf_audit"]

        try:

            for i in range(1, nrows):
                row_data = sh.row_values(i)

                excel_uid = row_data[0]
                excel_type = row_data[1]
                excel_state = row_data[2]
                excel_memo = row_data[3]

                excel_type = excel_type.strip().replace(u"微信绿洲",'1').replace(u"支付宝蓝海",'2')
                excel_state = excel_state.strip().replace(u"审核成功", '1').replace(u"审核失败", '2')

                sql = "update `salesman_event` set state = %s,memo = '%s',atime = '%s',admin_userid = %s where userid = %s and type = %s " % (
                    excel_state, excel_memo, now, self.get_cookie('uid'), excel_uid, excel_type)
                conn.query(sql)
        except Exception, e:
            print e
            return json.dumps({'code': 201, 'msg':u'文件格式有误', 'data': {}})



        return json.dumps({'code':200,'msg':'success','data':{}})
