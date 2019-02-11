#!/usr/bin/env python
# encoding: utf-8

import hashlib
import types
import time
import datetime
import json
import string
import traceback
import copy
import xlwt
import collections
import config
import StringIO
import logging
log = logging.getLogger()


from qfcommon.base.dbpool import get_connection, get_connection_exception
from qfcommon.library import createid
from qfcommon.library.excel import Cell, CellType
from qfcommon.web.core import Handler

from functools import partial
from utils.constants import TagDef
from .excepts import ParamError
from qfcommon.base.http_client import Urllib2Client

class MisHandler(Handler):

    def initial(self):
        self.set_headers({'Content-Type': 'application/json; charset=UTF-8'})

    def valid_args(self):
        d = self.req.input()
        d = {i:d[i].strip() for i in d}

        for i in d:
            if i.endswith('_time') or i.endswith('_datetime'):
                if not is_valid_datetime(d.get(i)) and not is_valid_date(d.get(i)):
                    raise ParamError('不是正确的日期时间')
            if 'start_time' in d and 'end_time' in d:
                st = datetime.datetime.strptime(d['start_time'], DATE_FMT)
                et = datetime.datetime.strptime(d['end_time'], DATE_FMT)
                if st > et:
                    raise ParamError('开始时间应该小于结束时间')

        # 手动验证的参数,不要求一定填写
        manual_list = []
        if hasattr(self, 'manual_list'):
            manual_list = [i[0] for i in self.manual_list]

        # 自动验证是否存在
        for i in self.valid_list:
            if i[0] in manual_list:
                continue
            if not d.get(i[0]):
                raise ParamError('请输入'+i[1])

    def build_lists(self):

        d = self.req.input()
        offset = int(d.get('offset', 0))
        limit = int(d.get('pageSize', 10))

        if 'table' not in self.list_args:
            raise ParamError('未知表')
        if 'db' not in self.list_args:
            raise ParamError('未知库')

        where = {}
        fuzzy_search = self.list_args.get('fuzzy', [])
        if 'limit' in self.list_args:
            for item in self.list_args['limit']:
                where.update(item)
        if 'where' in self.list_args:
            for item in self.list_args['where']:
                item_value = d.get(item)
                if item_value:
                    if item in fuzzy_search:
                        where[item] = ('like', '%{}%'.format(item_value))
                    else:
                        where[item] = item_value
        log.debug('where={}'.format(where))

        total = 0
        lists = []
        ret = {'total': total, 'list': lists}
        order_by = self.list_args.get('order_by') or ''
        group_by = self.list_args.get('group_by') or ''
        sort = self.list_args.get('sort') or 'desc'

        other = ''
        other_total = ''
        if group_by:
            other += 'group by {} '.format(group_by)
        if order_by:
            other += 'order by {} '.format(order_by)
        other_total = other
        other += sort
        if not (d.get('mode') == 'expo_excel'):
            other += ' limit {limit} offset {offset} '.format(
                limit = limit, offset = offset)
        log.debug('other_total={}|other={}'.format(other_total, other))

        # 返回值
        table = self.list_args['table']
        database = self.list_args['db']
        with get_connection(database) as db:
            lists = db.select(table,where=where,other=other)
            total = db.select(
                    table,fields='count(1) total',other=other_total,
                    where = where)
        # group by
        total = len(total) if group_by else total[0]['total']
        for li in lists:
            for k in li:
                if li[k] is None:
                    li[k] = ''
        ret['total'] = total
        ret['list'] = lists
        log.debug('source_list={}'.format(lists))

        return ret

    def build_excel(self, lists, excel_name='expo.xls'):
        if not self.head_list:
            raise ParamError('缺少excel列表头部')

        self.set_headers({'Content-Type': 'application/octet-stream'})
        self.set_headers(
            {'Content-disposition': 'attachment; filename={}'.format(excel_name)})

        return excel_data(self.head_list, lists)

def excel_data(head, data):
    if not head:
        raise ParamError('缺少excel列表头部')

    rows = []
    heads = []
    for head_data in head:
        arg_name = head_data[0]
        arg_str = head_data[1]
        heads.append(Cell(arg_str))
    rows.append(heads)

    max_item = getattr(config, 'MAX_EXCEL_ROWS', 5000)
    if len(data) > max_item:
        raise ParamError('导出数量太多,限制为{}条'.format(max_item))

    for item in data:
        row = []
        for head_data in head:
            arg_name = head_data[0]
            arg_str = head_data[1]
            tmp = Cell(str(item.get(arg_name, '')))
            row.append(tmp)
        rows.append(row)
    sio = StringIO.StringIO()
    create_xl(sio, rows)
    return sio.getvalue()

def create_xl(sio, rows = None):
    '''
    根据rows[[], [], []]完成表格
    '''
    # 创建excel文件
    table = xlwt.Workbook()             # 创建一个工作簿
    sheet = table.add_sheet('Sheet1')       # 创建一个工作表
    if rows:
        # rows存在，将rows添加到excel中
        # 不存在，直接保存excel
        for rownum in xrange(0, len(rows)):
            for colnum in xrange(0, len(rows[rownum])):
                #在rownum行rolnum列写入cell
                cell = rows[rownum][colnum]
                sheet.write(rownum, colnum, cell.value)    # 保存单元格式数据
    table.save(sio)     # 保存


# 判断是否合法
def is_valid(s, func):
    try:
        func(s)
        return True
    except:
        return False

# 判断是否是日期
is_valid_date = partial(is_valid, func=lambda s: time.strptime(s, '%Y-%m-%d'))
# 判断是否是日期
is_valid_datetime = partial(is_valid, func=lambda s: time.strptime(s, '%Y-%m-%d %H:%M:%S'))

# 判断是否是数字
is_valid_num= partial(is_valid, func=float)

# 判断是否是整形
is_valid_int= partial(is_valid, func=int)

# 转化
unicode_to_utf8 = lambda s: s.encode('utf-8') if isinstance(s, unicode) else s

# 判断只有字母数字
def just_letters_int_func(s):
    range_in = string.digits + string.ascii_letters
    for i in s:
        if i not in range_in:
            raise ValueError
just_letters_int = partial(is_valid, func=just_letters_int_func)


# 先暂时放一些业务逻辑相关的代码在这里
# 整体封装的都乱

def get_tag_user(cate_codes):
    '''根据传来的cate code 列表返回相关的userid'''

    cate_userids = []
    if not cate_codes:
        return cate_userids
    where_cate = {
        'status': 1,
        'cate_code': ('in', cate_codes)
    }
    cate_userid_list = []
    with get_connection('qf_user') as db:
        cate_userid_list = db.select(
            table = 'user_category',
            where = where_cate,
            fields = ['userid']
        )
    if cate_userid_list:
        cate_userids = [int(i['userid']) for i in cate_userid_list]

    return cate_userids


def all_tag_user():

    # 先拿到所有的catecode，包括失效的
    all_codes = all_tags()
    userids = get_tag_user(all_codes)
    return set(userids)

def all_tags(display='code_list'):
    '''取出所有的标签'''

    all_codes = [] if display == 'code_list' else {}
    where = {'userid': TagDef.VIRTUAL_USER_ID}
    with get_connection('qf_user') as db:
        all_codes = db.select(
            table = 'user_category',
            fields = 'cate_code, cate_name, remark',
            where = where
        )
        if all_codes:
            if display == 'code_list':
                all_codes = [i['cate_code'] for i in all_codes]
            elif display == 'code_map':
                all_codes_map = {}
                for i in all_codes:
                    all_codes_map[i['cate_code']] = {
                        'cate_name': i['cate_name'],
                        'remark': i['remark']
                    }
                all_codes = all_codes_map
    return all_codes

def get_user_tags(userids, display='list_code', seq=','):
    '''根据userid获取这些用户的标签'''

    ret = collections.defaultdict(list)
    if not userids:
        return ret
    all_own_tags = all_tags()
    if isinstance(userids, str):
        if ',' in userids:
            userids = userids.split(',')
    where = {
        'status': TagDef.TAG_VALID,
        'userid': ('in', userids),
    }
    code_name_map = all_tags(display='code_map')

    # 防止拿到其他tag
    if all_own_tags:
        where['cate_code'] = ('in', all_own_tags)
    else:
        where['cate_code'] = ''

    # 内容展示解析
    display_type = display.split('_')[0] if '_' in display else 'default'
    display_content = display.split('_')[1] if '_' in display else 'default'
    with get_connection('qf_user') as db:
        ret_db = db.select('user_category',
            fields = 'cate_code, userid',
            where = where,
        )
        if ret_db:
            for tmp in ret_db:
                userid = tmp['userid']
                cate_code = tmp['cate_code']
                if display_content == 'code':
                    ret[userid].append(cate_code)
                elif display_content == 'name':
                    cate_name = code_name_map.get(cate_code, {}).get('cate_name')
                    ret[userid].append(cate_name)
                else:
                    ret[userid].append(cate_code)
    if display_type == 'join':
        for k,v in ret.items():
            ret[k] = ','.join(v)
    log.debug('get_user_tags result is {}'.format(ret))
    return ret


def get_str_len(name, cn=1, en=1):
    len_of_name = 0
    try:
        if not isinstance(name, unicode):
            name = str(name).decode('utf8')
        for i in name:
            if u'\u4e00' <= i <= u'\u9fff':
                len_of_name += cn
            else:
                len_of_name += en
    except:
        log.warn(traceback.format_exc())
        return 0 # 字符串长度设置为0
    return len_of_name


def get_data_qudao():

    try:
        r = Urllib2Client().get("http://192.20.20.12:8097/findChnlInfo")
        r_j = json.loads(r)
        qudao_list = r_j['data']
        qdict = {}
        for xy in qudao_list:
            qdict[xy['chnlId']] = xy['chnlTypeName']
        return qdict
    except Exception, e:
        log.warn(e)
        return {}