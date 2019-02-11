# coding:utf-8

from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import config
import datetime
import json
import traceback
import logging
import xlwt
import StringIO

from tools import checkIsLogin

from qfcommon.web import template
from qfcommon.web import core
from qfcommon.base.dbpool import with_database
from qfcommon.qfpay.qfresponse import json_default_trans


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

# 消息列表接口
class app_rule_list(BaseHandler):
    @with_database(["qf_solar"])
    def POST(self):
        params = self.req.inputjson()

        where = {'id' : ('!=', 0)}
        if params.get('appname'):
            where['appname'] = ('like', '%%%s%%' % params['appname'])

        if params.get('chnlcode'):
            where['chnlcode'] = ('=', '"%s"' % params['chnlcode'])

        if params.get('state') != '':
            where['state'] = str(params['state'])

        if getattr(config, 'WX_MANAGE_APPIDS', None) is not None:
            where['appid'] = ('in', config.WX_MANAGE_APPIDS)

        try:
            result = self.db["qf_solar"].select(
                'app_rule', where = where,
                other = 'order by id desc'
            )
        except Exception, e:
            print e
            log.debug('mysql getdata error: %s' % traceback.format_exc())
            return json.dumps({'data': [],'code':'error'}, ensure_ascii=False)

        for item in result:
            chnlcode = unicode_to_utf8(item['chnlcode'])
            chnlcode = filter(str.isdigit, chnlcode or '')
            item['chnlcode_str'] = config.CHNLCODE_CONFIG.get(
                    chnlcode, '未知-{}'.format(chnlcode))

        return json.dumps(
            {'data': result,'code':'ok'}, ensure_ascii=False,
            default = json_default_trans
        )


class get_app_config(BaseHandler):
    @with_database(["qf_solar"])
    def POST(self):
        try:
            params = self.req.inputjson()
            _chnlcode = params.get('chnlcode')
            _chnlcode = json.loads(_chnlcode)

            _zh = ""
            ji = 1
            for xy in _chnlcode:
                if ji != 1:
                    _zh += " or chnlcode like '%%%s%%' " % str(xy)
                else:
                    _zh += " chnlcode like '%%%s%%' " % str(xy)
                ji += 1

            conn = self.db["qf_solar"]
            _sql = " select * from `app_conf` where (id != 0) and  (%s) " % _zh

            if getattr(config, 'WX_MANAGE_APPIDS', None):
                _sql += ' and appid in ({}) '.format(
                    ','.join("'%s'" % i for i in config.WX_MANAGE_APPIDS)
                )

            _sql += 'order by id desc'

            result = conn.query(_sql)
        except:
            log.debug(traceback.format_exc())
            return json.dumps({'data': [], 'code': 'error'}, ensure_ascii=False)

        return json.dumps({'data': result, 'code': 'ok'}, ensure_ascii=False)


# 消息拿一个
class app_rule_getone(BaseHandler):
    @with_database(["qf_solar"])
    def POST(self):

        try:
            params = self.req.inputjson()
            _id = params.get('id', '')

            _sql = " select * from `app_rule` where id = %s order by id desc " % str(_id)
            self.solar_ = self.db["qf_solar"]
            result = self.solar_.query(_sql)
        except Exception, e:
            print e
            log.debug('mysql getdata error: %s' % traceback.format_exc())
            return json.dumps({'data': [], 'code': 'error'}, ensure_ascii=False)

        for d in result:
            # 将mysql返回的日期数据类型转换成字符串
            try:
                d['ctime'] = d['ctime'].strftime("%Y-%m-%d %H:%M:%S")
                d['utime'] = d['utime'].strftime("%Y-%m-%d %H:%M:%S")
            except Exception, e:
                d['ctime'] = ''
                d['utime'] = ''

        return json.dumps({'data': result, 'code': 'ok'}, ensure_ascii=False)


#规则入库接口
class app_rule_insert(core.Handler):
    @with_database("qf_solar")
    def POST(self):
        if self.req.environ.get('CONTENT_TYPE', '').lower().startswith(
                'application/json'):
            try:
                params = self.req.inputjson()

                # 构造新建的入库的数据
                values = {}
                values['appname'] = params.get('appname')
                values['appid'] = params.get('appid')
                values['pay_appid'] = params.get('pay_appid')
                values['area'] = json.dumps(params.get('area'),ensure_ascii=False)
                values['trade'] = json.dumps(params.get('trade'), ensure_ascii=False)
                values['group'] = json.dumps(params.get('group'), ensure_ascii=False)
                values['menu'] = json.dumps(params.get('menu'), ensure_ascii=False)
                values['chnlcode'] = json.dumps(params.get('chnlcode'), ensure_ascii=False)
                values['state'] = int(params.get('state'))
                values['level'] = int(params.get('level'))
                values['cid'] = params.get('cid')
                try:
                    results = self.db.select(table='app_rule',fields=['level'])
                    levels = []
                    for result in results:
                        levels.append(result.get('level'))
                    if values['level'] in levels:
                         return json.dumps({'ok': False, 'msg': '该优先级已存在，请输入其他优先级'},
                                          ensure_ascii=False)
                except Exception, e:
                     log.debug('mysql get level error: %s' % traceback.format_exc())
                     return json.dumps({'ok': False, 'msg': '校验优先级失败'},
                                       ensure_ascii=False)

                # 获取当前的时间
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # 创建的时间
                values['ctime'] = now_time


                # 入库操作
                try:
                    self.db.insert(table='app_rule', values=values)
                except Exception, e:
                    log.debug('mysql insert error: %s' % traceback.format_exc())
                    return json.dumps({'ok': False, 'msg': '新建失败'},
                                      ensure_ascii=False)

                return json.dumps({'ok': True, 'msg': '新建成功'},
                                  ensure_ascii=False)

            except ValueError:
                return json.dumps({'ok': False, 'msg': 'Bad request'},
                                  ensure_ascii=False)
        return json.dumps({'ok': False, 'msg': 'Need json input format'},
                          ensure_ascii=False)


#规则更新接口
class app_rule_update(core.Handler):
    @with_database("qf_solar")
    def POST(self):
        if self.req.environ.get('CONTENT_TYPE', '').lower().startswith(
                'application/json'):
            try:
                params = self.req.inputjson()
                results = self.db.select(table='app_rule', fields=['level'])
                where = {'id': int(params.get('id'))}
                myLevelResult = self.db.select(table='app_rule', fields=['level'], where=where)
                myLevel = myLevelResult[0].get('level')
                if int(params.get('level')) != myLevel:
                    levels = []
                    for result in results:
                        levels.append(result.get('level'))
                    if int(params.get('level')) in levels:
                        return json.dumps({'ok': False, 'msg': '该优先级已存在，请输入其他优先级'},
                                          ensure_ascii=False)
                # 构造新建的入库的数据
                values = {}
                msg = {}

                for (key,ve) in params.items():
                    if key in ['area','trade','group','menu','chnlcode']:
                        values[key] = json.dumps(ve, ensure_ascii=False)
                    elif key in ['state','level']:
                        values[key] = int(ve)
                    else:
                        values[key] = ve

                msg['id'] = params.get('id')


                # 获取当前的时间
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # 创建的时间
                values['utime'] = now_time

                # 入库操作
                try:
                    self.db.update(table='app_rule',values=values, where={'id':int(msg.get('id'))})
                except Exception, e:
                    log.debug('mysql insert error: %s' % traceback.format_exc())
                    return json.dumps({'ok': False, 'msg': '更新失败'},
                                      ensure_ascii=False)

                return json.dumps({'ok': True, 'msg': '更新成功'},
                                  ensure_ascii=False)

            except ValueError:
                return json.dumps({'ok': False, 'msg': 'Bad request'},
                                  ensure_ascii=False)
        return json.dumps({'ok': False, 'msg': 'Need json input format'},
                          ensure_ascii=False)




#app查询接口
class app_list(BaseHandler):
    @with_database(["qf_solar"])
    def POST(self):
        try:
            params = self.req.inputjson()
            print params
            _sq = ' id != 0 '
            appid = params.get('appid')
            start_time = params.get('start_time').replace("-","")
            end_time = params.get('end_time').replace("-","")

            if start_time == '' and end_time == '':
                today = datetime.date.today()
                yesterday = today - datetime.timedelta(days=1)
                start_time = str(yesterday).replace("-","")
                end_time = str(yesterday).replace("-", "")

            draw = params.get('draw')
            start = int(params.get('start'))
            length = int(params.get('length'))

            if start_time and end_time:
                _sq += " and ctime between  %s and %s  " % (start_time,end_time)

            if appid:
                _sq += " and appid = '%s'  " % str(appid)

            elif getattr(config, 'WX_MANAGE_APPIDS', None) is not None:
                _sq += " and appid in ({}) ".format(','.join("'%s'" % i for i in config.WX_MANAGE_APPIDS))


            conn = self.db["qf_solar"]
            _sql = " select * from `app_list` where  %s order by ctime desc limit %s,%s " % (_sq,start,length)
            print _sql
            result = conn.query(_sql)
        except Exception, e:
            print e
            log.debug('mysql getdata error: %s' % traceback.format_exc())
            return json.dumps({'data': [],'code':'error'}, ensure_ascii=False)

        _sql_all = "select count(1) as count from `app_list` where  %s " % _sq
        r_count = conn.query(_sql_all)

        try:
            recordsTotal = r_count[0]['count']
        except Exception, e:
            print e
            recordsTotal = 0
            pass

        _sql_uids = "select `id` from `app_list` where  %s " % _sq
        r_uids = conn.query(_sql_uids)

        uids = []
        for xy in r_uids:
            uids.append(int(xy['id']))

        for d in result:
            # 将mysql返回的日期数据类型转换成字符串
            try:
                d['fan'] = "%s%%" % str(round(  (int(d['newfan']) / int(d['deal'])) * 100 , 4))
            except Exception, e:
                print e
                d['fan'] = '0%'

        return json.dumps({'draw': draw, 'recordsTotal': recordsTotal, 'recordsFiltered': recordsTotal, 'data': result,
                     'code': 200,"id":uids}, ensure_ascii=False)



#app导出excel
class appExcel(BaseHandler):
    def __init__(self, app, req):
        super(BaseHandler, self).__init__(app, req)
        self.resp.mimetype = 'application/vnd.ms-excel'
        self.resp.headers['Content-Type'] = '%s; charset=%s' % (
            self.resp.mimetype, self.resp.charset)

    @with_database(["qf_solar"])
    def POST(self):
        params = self.req.input()
        uids = params.get('ids')
        uids_l = uids.split(",")

        _ids = ''

        for xy in uids_l:
            _ids += "%s," % str(xy)
        _ids = _ids.rstrip(",")

        conn = self.db["qf_solar"]
        _sql = " select * from `app_list` where id in (%s) order by ctime desc " % _ids
        result = conn.query(_sql)

        data_arr = []

        for d in result:
            try:
                d['fan'] = "%s%%" % str(round(  int(d['newfan']) / int(d['deal']) * 100 , 4))
            except Exception, e:
                d['fan'] = '0%'


        for i in result:
            info = {}
            for (key, ve) in i.items():
                info[key] = unicode_to_utf8(str(ve))
            data_arr.append(info)

        header = ['日期','公众号名称','公众号APPID','所属主体','商户数','微信交易笔数','新增粉丝数','吸粉率','总粉丝数','净增用户','取关用户']

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
            worksheet.write(j, 0, con['ctime'])
            worksheet.write(j, 1, con['appname'])
            worksheet.write(j, 2, con['appid'])
            worksheet.write(j, 3, con['belong'])
            worksheet.write(j, 4, con['shop'])
            worksheet.write(j, 5, con['deal'])
            worksheet.write(j, 6, con['newfan'])
            worksheet.write(j, 7, con['fan'])
            worksheet.write(j, 8, con['allfan'])
            worksheet.write(j, 9, con['auser'])
            worksheet.write(j, 10, con['cuser'])
            j = j + 1
        # workbook.save('Excel_test.xls')
        sio = StringIO.StringIO()
        workbook.save(sio)  # 这点很重要，传给save函数的不是保存文件名，而是一个StringIO流

        return sio.getvalue()



