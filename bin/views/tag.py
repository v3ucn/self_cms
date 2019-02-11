#coding=utf8

import logging
import config
import datetime
import copy
import collections
import re
import uuid
import StringIO
log = logging.getLogger()

from qfcommon.web import core
from qfcommon.web import template
from qfcommon.base.qfresponse import success
from qfcommon.base.dbpool import get_connection, get_connection_exception
from qfcommon.library.excel import Cell, CellType
from qfcommon.base.tools import thrift_callex
from qfcommon.thriftclient.apollo import ApolloServer
from qfcommon.thriftclient.apollo.ttypes import UserCate
from qfcommon.server.client import ThriftClient

from tools import checkIsLogin, raise_excp
from utils.util import (
    MisHandler, create_xl, is_valid_int,
    just_letters_int, all_tags, get_str_len,
    get_tag_user, unicode_to_utf8
)
from utils.excepts import ParamError
from utils.constants import TagDef, DATETIME_FMT

class Index(core.Handler):
    @checkIsLogin
    def GET(self):
        data = {'uname': self.get_cookie('uname')}
        self.render('tag.html', data=data)

class List(MisHandler):

    def get_user_count(self, cate_codes):

        ret = {}
        if not cate_codes:
            return ret
        where = {}
        where['cate_code'] = ('in', cate_codes)
        where['status'] = TagDef.TAG_VALID
        where['userid'] = ('!=', TagDef.VIRTUAL_USER_ID)
        with get_connection('qf_user') as db:
            count = db.select(
                table = 'user_category',
                fields = 'cate_code, count(*) as count',
                where = where,
                other = 'group by cate_code'
            )
            log.debug('count={}'.format(count))
            if count:
                ret = {i['cate_code']: i['count'] for i in count}
        return ret

    @raise_excp('查看失败')
    @checkIsLogin
    def GET(self):
        d = self.req.input()
        self.list_args = {
            'db': 'qf_user',
            'table': 'user_category',
            'where': ['cate_code', 'status', 'remark', 'userid'],
            'order_by': 'ctime',
            'fuzzy': ['remark'],
            'group_by': 'cate_code',
            'limit': [
                {'userid': TagDef.VIRTUAL_USER_ID},
            ]
        }
        all_own_tags = all_tags('code_map')
        if all_own_tags:
            self.list_args['limit'].append(
                    {'cate_code': ('in', all_own_tags.keys())})
        ret = self.build_lists()
        lists = ret.get('list')

        # 其他操作
        exist_cate = [i['cate_code'] for i in lists]
        user_count = self.get_user_count(exist_cate)
        for i in ret.get('list'):
            cate_code = i.get('cate_code')
            remark = all_own_tags.get(cate_code).get('remark')
            cate_name = all_own_tags.get(cate_code).get('cate_name')
            i['user_count'] = user_count.get(i['cate_code'], 0)
            i['status_str'] = TagDef.TAG_STATUS_DICT.get(i['status'], '未知')
            i['cate_name'] = cate_name
            i['remark'] = remark
        self.head_list = [
            ('cate_name', '标签名称'), ('remark', '标签解释'),
            ('user_count', '商户数量'), ('ctime', '创建时间'),
            ('utime', '更新时间'), ('status_str', '状态')
        ]
        if d.get('mode') == 'expo_excel':
            excel_name = '标签管理_{}'.format(datetime.date.today())
            return self.build_excel(lists, excel_name=excel_name)

        return self.write(success(ret))


class Manage(MisHandler):

    def build_args(self):
        d = self.req.input()
        self.valid_args()

        values = {}
        for i in self.valid_list:
            arg_name = i[0]
            arg_value = d[arg_name]
            if arg_name in self.valid_int_list:
                if not is_valid_int(arg_value):
                    raise ParamError('{}参数有误'.format(i[1]))
                arg_value = int(arg_value)
            if arg_name == 'status':
                if arg_value not in TagDef.TAG_STATUS:
                    raise ParamError('状态值不合法')
            if arg_name == 'cate_code':
                pass
            if arg_name == 'cate_name':
                with get_connection_exception('qf_user') as db:
                    where = {'cate_name': arg_value}
                    ret = db.select('user_category',where=where)
                    if ret:
                        raise ParamError('该标签已存在，请重新输入')
            if arg_name == 'cate_codes':
                arg_value = [i.strip() for i in arg_value.split(',')]
            if arg_name == 'userids':
                userids = arg_value.split(',')
                for userid in userids:
                    if not is_valid_int(userid):
                        raise ParamError('输入商户ID请使用英文分隔符')
                arg_value = [int(i) for i in userids]
                if not arg_value:
                    raise ParamError('未输入有效商户ID')
            values[arg_name] = arg_value
        for i in self.manual_list:
            arg_name = i[0]
            arg_value = d.get(arg_name)
            if not arg_value: continue
            if arg_name in self.valid_int_list:
                if not is_valid_int(arg_value):
                    raise ParamError('{}参数有误'.format(i[1]))
                arg_value = int(arg_value)
            if arg_name == 'remark':
                if get_str_len(arg_value) > getattr(config, 'REMARK_LEN', 100):
                    raise ParamError('标签解释长度不可超过100个字符')
            # code 放在valid_list中,已经存在
            if arg_name == 'cate_name':
                where = {'cate_name': arg_value}
                if values.get('cate_code'):
                    where['cate_code'] = ('!=', values.get('cate_code'))
                with get_connection_exception('qf_user') as db:
                    ret = db.select_one('user_category',
                            fields = 'count(*) as total',
                            where = where)
                    if ret and ret.get('total') != 0:
                        raise ParamError('名称重复')
            values[arg_name] = arg_value
        log.debug(values)
        return values

    def _gen_code(self, cate_name=None):
        code = '{}'.format(uuid.uuid4().hex[0:12])
        with get_connection('qf_user') as db:
            ret = db.select_one('user_category', where={'cate_code': code})
            while ret:
                code = '{}'.format(uuid.uuid4().hex[0:12])
                ret = db.select_one('user_category', where={'cate_code': code})
        return code



    def add_cate(self):
        self.valid_list = [
            ('cate_name', '标签名称'), ('status', '标签状态')
        ]
        self.manual_list = [('remark', '标签解释')]
        values = self.build_args()
        usercate = {}
        usercate['code'] = self._gen_code()
        usercate['name'] = values['cate_name']
        usercate['ctime'] = datetime.datetime.now().strftime(DATETIME_FMT)
        usercate['status'] = TagDef.TAG_VALID
        usercate['remark'] = values.get('remark', '')
        usercate = UserCate(**usercate)
        ret = thrift_callex(config.APOLLO_SERVERS, ApolloServer, 'setUsersCategory',
                [TagDef.VIRTUAL_USER_ID], [usercate])
        if ret != 0:
            raise ParamError('内部错误')
        return self.write(success({}))

    def get_cates(self):
        self.manual_list = [('status', '状态')]
        self.valid_list = []
        values = self.build_args()

        where = {
            'status': ('in', TagDef.TAG_STATUS),
            'userid': TagDef.VIRTUAL_USER_ID
        }
        if values.get('status'):
            where['status'] = values.get('status')


        cate_dict = {}
        with get_connection('qf_user') as db:
            ret = db.select(
                table = 'user_category',
                fields = 'cate_code, cate_name, status',
                where = where,
            )
            if ret:
                for i in ret:
                    cate_dict[i['cate_code']] = i['cate_name']
        return self.write(success({'cate_dict': cate_dict}))


    def tag_user(self):
        self.valid_list = [
            ('cate_codes', '标签'), ('userids' ,'商户ID'), ('status', '状态')
        ]
        values = self.build_args()
        with get_connection_exception('qf_user') as db:
            cate_map_list = db.select(
                fields = ['cate_code', 'cate_name', 'remark'],
                table = 'user_category',
                where = {'userid': TagDef.VIRTUAL_USER_ID}
            )
            cate_map = {i['cate_code']: (i['cate_name'], i['remark'])
                    for i in cate_map_list}
        categories = []
        for userid in values['userids']:
            for cate_code in values['cate_codes']:
                tmp = UserCate(
                    code = cate_code,
                    name = unicode_to_utf8(cate_map.get(cate_code, ('', ''))[0]),
                    status = values['status'],
                    ctime = datetime.datetime.now().strftime(DATETIME_FMT),
                    remark = unicode_to_utf8(cate_map.get(cate_code, ('', ''))[1]),
                )
                categories.append(tmp)
        ret = thrift_callex(config.APOLLO_SERVERS, ApolloServer, 'setUsersCategory',
                list(values['userids']), categories)
        if ret != 0:
            raise ParamError('内部错误')
        return self.write(success({}))

    def edit_cate(self):
        self.valid_list = [
            ('cate_code', '标签代码'),
        ]
        self.manual_list = [
            ('cate_name', '标签名称'), ('status', '状态'),
            ('remark', '标签解释'),
        ]
        values = self.build_args()
        where = {'cate_code': values['cate_code']}
        status_before = None
        remark_before = ''
        cate_name = ''

        cate_info_before_ret = {}
        with get_connection('qf_user') as db:
            cate_info_before_ret = db.select_one('user_category',
                where = {
                    'cate_code': values['cate_code'],
                    'userid': TagDef.VIRTUAL_USER_ID,
                },
                fields = 'status, cate_name, remark'
            )
        if not cate_info_before_ret:
            raise ParamError('当前修改标签不存在')
        status_before = cate_info_before_ret.get('status')
        remark_before = cate_info_before_ret.get('remark')
        cate_name_before = cate_info_before_ret.get('cate_name')

        # 原来的状态和更改的状态相同则不改状态
        if (values.get('remark') != remark_before or
                values.get('cate_name') != cate_name_before):
            tmp = {}
            tmp['code'] = values.get('cate_code')
            if values.get('cate_name'):
                tmp['name'] = values.get('cate_name')
            if values.get('remark'):
                tmp['remark'] = values.get('remark')
            update_cate = UserCate(**tmp)
            ret = thrift_callex(config.APOLLO_SERVERS, ApolloServer, 'setCategoryByCode', values.get('cate_code'), update_cate)
            if ret != 0:
                raise ParamError('error')
        if values.get('status') != status_before:
            update_cate = UserCate(
                code = values.get('cate_code'),
                name = values.get('cate_name'),
                status = values.get('status'),
                remark = values.get('remark')
            )
            ret = thrift_callex(config.APOLLO_SERVERS, ApolloServer, 'setUsersCategory', [TagDef.VIRTUAL_USER_ID], [update_cate])
            if ret != 0:
                raise ParamError('error')
        return self.write(success({}))

    @raise_excp('管理失败')
    @checkIsLogin
    def POST(self):
        d = self.req.input()
        self.valid_list = [
            ('cate_code', '标签'), ('userid' ,'商户ID'), ('status', '状态')
        ]
        self.manual_list = []
        self.valid_int_list = ['status', 'userid']
        allow_mode = ['add_cate', 'tag_user', 'get_cates', 'edit_cate']
        mode = d.get('mode', '')
        if mode in allow_mode:
            func = getattr(self, mode, None)
            if func:
                return func()

        raise ParamError('不合法的模式')

