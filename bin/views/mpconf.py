#coding=utf8

import logging
import config
import datetime
import StringIO
log = logging.getLogger()

from qfcommon.web import core
from qfcommon.web import template
from qfcommon.base.qfresponse import success
from qfcommon.base.dbpool import (
    get_connection, get_connection_exception
)
from qfcommon.library.excel import Cell, CellType

from tools import checkIsLogin, raise_excp
from utils.util import (
        MisHandler, create_xl, is_valid_int,
        just_letters_int, get_str_len
)
from utils.excepts import ParamError
from utils.constants import MpconfDef

class Index(core.Handler):
    @checkIsLogin
    def GET(self):
        data = {'uname': self.get_cookie('uname')}
        where = None
        if getattr(config, 'WX_MANAGE_APPIDS', None):
            where = {'appid' : ('in', config.WX_MANAGE_APPIDS)}
        with get_connection('qf_solar') as db:
            appname_ret = db.select(
                table = 'app_conf',
                fields = 'appname, appid',
                where = where
            )
            appnames = {i['appname']: i['appid'] for i in appname_ret}
        data['appname'] = appnames
        data['chnlcode_config'] = config.CHNLCODE_CONFIG
        self.render('mpconf.html', data=data)

class List(MisHandler):
    @checkIsLogin
    def GET(self):

        limit = []
        if getattr(config, 'WX_MANAGE_APPIDS', None):
            limit.append({'appid' : ('in', config.WX_MANAGE_APPIDS)})

        self.list_args = {
            'db': 'qf_solar',
            'table': 'app_conf',
            'where': ['appname', 'appid', 'main', 'cid', 'id'],
            'fuzzy': ['appname', 'main'],
            'order_by': 'appid',
            'limit': limit
        }
        ret = self.build_lists()

        lists = ret.get('list')
        for item in lists:
            chnlcode_list = []
            if item['chnlcode']:
                chnlcode_list = item['chnlcode'].split(',')
            item['chnlcode_str'] = [
                config.CHNLCODE_CONFIG.get(str(i), '未配置')
                for i in chnlcode_list
            ]
            item['chnlcode_display'] = ','.join(item['chnlcode_str'])
        # 添加通道配置
        ret['chnlcode_config'] = config.CHNLCODE_CONFIG

        self.head_list =  [
            ('main', '主体名称'), ('cid', '微信渠道号'),
            ('pay_appid', '支付APPID'), ('menu', '支付目录'),
            ('appname', '公众号名称'), ('appid', '公众号APPID'),
            ('uid', '商户ID'), ('chnlcode_display', '支持通道')
        ]

        if self.req.input().get('mode') == 'expo_excel':
            excel_name = '公众号配置_{}.xls'.format(datetime.date.today())
            return self.build_excel(lists, excel_name=excel_name)

        return self.write(success(ret))

class Manage(MisHandler):

    def build_args(self):
        d = self.req.input()
        self.valid_args()

        values = {}
        main_len = getattr(config, 'MAIN_LEN', 100)
        chnlcode_len = getattr(config, 'CHNLCODE_LEN', 1)
        for i in self.valid_list:
            arg_name = i[0]
            arg_value = d[arg_name]
            if arg_name == 'main':
                if get_str_len(arg_value) > main_len:
                    raise ParamError('主体名称需少于{}个字符'.format(main_len))
            if arg_name == 'cid':
                arg_value = arg_value.strip()
                if not just_letters_int(arg_value):
                    raise ParamError('微信渠道号不要输入字母数字以外的字符')
            if arg_name == 'pay_appid':
                arg_value = arg_value.strip()
                if not just_letters_int(arg_value):
                    raise ParamError('支付APPID请输入数字字母组合')
            if arg_name == 'menu':
                if get_str_len(arg_value) > main_len:
                    raise ParamError('支付目录需少于{}个字符'.format(main_len))
            if arg_name == 'chnlcode':
                chnlcode_list = arg_value.split(',')
                if len(chnlcode_list) > chnlcode_len:
                    raise ParamError('支持通道仅限{}个'.format(chnlcode_len))
                if chnlcode_list[0] not in config.CHNLCODE_CONFIG.keys():
                    raise ParamError('支持通道不在允许范围之内')
            values[arg_name] = arg_value
        for i in self.manual_list:
            arg_name = i[0]
            arg_value = d[arg_name]
            values[arg_name] = arg_value
            if not arg_value: continue
            if arg_name == 'uid':
                userids = arg_value.split(',')
                for userid in userids:
                    if not is_valid_int(userid):
                        raise ParamError('输入商户ID请使用英文分隔符')
        log.debug(values)
        return values


    def edit_mpconf(self):
        '''修改配置'''
        values = self.build_args()
        where = {'id': values.pop('id')}
        try:
            with get_connection_exception('qf_solar') as db:
                db.update('app_conf', values=values, where=where)
        except:
            raise ParamError('保存失败，该配置已存在')
        return self.write(success({}))

    def add_mpconf(self):

        self.valid_list.remove(('id', '公众号配置ID'))
        self.valid_list.extend([
            ('appname', '公众号名称'),('appid', '公众号APPID')
        ])

        values = self.build_args()

        try:
            with get_connection_exception('qf_solar') as db:
                db.insert('app_conf', values=values)
        except:
            raise ParamError('保存失败，该配置已存在')
        return self.write(success({}))


    @checkIsLogin
    @raise_excp('参数错误')
    def POST(self):
        d = self.req.input()
        self.valid_list = [
            ('main', '主体名称'), ('cid', '微信渠道号'),
            ('pay_appid', '支付APPID'),
            ('menu', '支付目录'), ('id', '公众号配置ID'),
            ('chnlcode', '通道')
        ]
        self.manual_list = [('uid', '商户ID'), ]

        allow_mode = ['edit_mpconf', 'add_mpconf']
        mode = d.get('mode', '')
        if mode in allow_mode:
            func = getattr(self, mode, None)
            if func:
                return func()

        raise ParamError('不合法的模式')

