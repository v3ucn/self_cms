# vim: set ts=4 et sw=4 sts=4 fileencoding=utf-8 :

import os
import sys
import re
import logging
import time
import traceback
import datetime
import json
import urllib2
import urllib
from itertools import groupby
from qfcommon.web import core
from qfcommon.web import template
from qfcommon.base.dbpool import with_database, get_connection
from qfcommon.base.dbpool import DBFunc
from qfcommon.base.tools import thrift_callex
from qfcommon.base.http_client import RequestsClient
from qfcommon.server.selector import Selector
from qfcommon.thriftclient.apollo import ApolloServer
from qfcommon.thriftclient.apollo.ttypes import Permission
from qfcommon.thriftclient.apollo.ttypes import PermissionRole
from qfcommon.thriftclient.apollo.ttypes import ApolloException
from qfcommon.thriftclient.account2.ttypes import FeeQueryArgs
from qfcommon.thriftclient.account2.ttypes import RecordArgs
from qfcommon.thriftclient.account2.ttypes import AccountQueryArgs
from qfcommon.thriftclient.fund2 import Fund2
from qfcommon.thriftclient.fund2.ttypes import FundQueryParams
from qfcommon.qfpay.apollouser import ApolloUser
from qfcommon.thriftclient.qudao import QudaoServer
from qfcommon.thriftclient.spring import Spring
from qfcommon.thriftclient.account2 import Account2
from qfcommon.qfpay.defines import *
from tools import checkIsLogin
import config
from tools import thrift_callex_framed
from qfcommon.qfpay import defines
from qfcommon.globale import currency
from copy import deepcopy
import types
import xlwt
import StringIO
from hashids import Hashids
from qfcommon.thriftclient.weifutong import weifutong
from qfcommon.thriftclient.weifutong.ttypes import *
from qfcommon.server.client import ThriftClient

from qfcommon.thriftclient.audit import AuditServer
from qfcommon.thriftclient.audit.ttypes import Audit

from utils.util import (
    excel_data, get_tag_user, all_tag_user,
    all_tags, is_valid_int
)


log = logging.getLogger()
unicode_to_utf8 = lambda s: s.encode('utf-8') if isinstance(s, unicode) else s

merchant_server = Selector(config.MERCHANT_SERVER, 'round_robin')


class UserPermissionHelper:
    def __init__(self):
        pass

    # apollo接口
    # 添加新权限组, 成功返回0   失败返回其他值
    # i32 addPermissionRole(1:PermissionRole r) throws (1:ApolloException e);
    # 返回0代表添加角色成功
    def add_permission_role(self, name, code, group=''):
        name = unicode_to_utf8(name)
        code = unicode_to_utf8(code)
        group = unicode_to_utf8(group)
        r = -1
        try:
            r = thrift_callex(config.APOLLO_SERVERS, ApolloServer,
                                 'addPermissionRole',
                                 PermissionRole(name=name, code=code,
                                                group=group))
            msg = '添加成功' if not r else '添加失败'
        except ApolloException, e:
            log.debug('apollo error:%s' % e)
            msg = '添加失败'
        except:
            log.error('apollo error:%s' % traceback.format_exc())
            msg = '添加失败'

        return r, msg

    # 绑定权限到组, 只取其中的code,成功返回0   失败返回其他值
    # i32 bindPermissionToRole(1:Permission p, 2:PermissionRole r) throws (1:ApolloException e);
    # 返回元组，元组中第一个元素为0则成功
    def bind_permission_to_role(self, pname, pcode, rname, rcode, pgroup='',
                             rgroup=''):
        pname = unicode_to_utf8(pname)
        pcode = unicode_to_utf8(pcode)
        pgroup = unicode_to_utf8(pgroup)
        rname = unicode_to_utf8(rname)
        rcode = unicode_to_utf8(rcode)
        rgroup = unicode_to_utf8(rgroup)
        r = -1
        try:
            r = thrift_callex(config.APOLLO_SERVERS, ApolloServer,
                              'bindPermissionToRole',
                              Permission(name=pname, code=pcode, group=pgroup),
                              PermissionRole(name=rname, code=rcode,
                                             group=rgroup))
            msg = '成功' if not r else '失败'
        except ApolloException, e:
            log.debug('apollo error:%s' % e)
            msg = '失败'
        except:
            log.error('apollo error:%s' % traceback.format_exc())
            msg = '失败'
        return r, msg

    # 解绑权限到组, 只取其中的code,成功返回0   失败返回其他值
    # i32 unbindPermissionToRole(1:Permission p, 2:PermissionRole r) throws (1:ApolloException e);
    # 返回元组，元组中第一个元素为0则成功
    def unbind_permission_to_role(self, pname, pcode, rname, rcode, pgroup='',
                                rgroup=''):
        pname = unicode_to_utf8(pname)
        pcode = unicode_to_utf8(pcode)
        pgroup = unicode_to_utf8(pgroup)
        rname = unicode_to_utf8(rname)
        rcode = unicode_to_utf8(rcode)
        rgroup = unicode_to_utf8(rgroup)
        r = -1
        try:
            r = thrift_callex(config.APOLLO_SERVERS, ApolloServer,
                              'unbindPermissionToRole',
                              Permission(name=pname, code=pcode,
                                         group=pgroup),
                              PermissionRole(name=rname, code=rcode,
                                             group=rgroup))
            msg = '成功' if not r else '失败'
        except ApolloException, e:
            log.debug('apollo error:%s' % e)
            msg = '失败'
        except:
            log.error('apollo error:%s' % traceback.format_exc())
            msg = '失败'
        return r, msg

    def create_role_permissions(self, params=None):
        role = params.get('role')

        # 新建的 role，code 和 name 一样
        r, msg = self.add_permission_role(name=role['name'], code=role['name'])
        if r == -1:
            return -1  # 添加失败

        perm_add = params.get('permissionsBind')
        if perm_add and len(perm_add):
            for p in perm_add:
                r, msg = self.bind_permission_to_role(
                    pname=p.get('name'),
                    pcode=p.get('code'),
                    pgroup=p.get('group'),
                    rname=role.get('name'),
                    rcode=role.get('name'),  # 新建的 role，code 和 name 一样
                    rgroup=role.get('group'),
                )
                if r == -1:
                    return -2  # 添加成功，绑定过程失败

        return 0  # 成功

    def update_role_permissions(self, params=None):
        perm_add = params.get('permissionsBind')
        perm_del = params.get('permissionsUnbind')
        role = params.get('role')
        if perm_add and len(perm_add):
            for p in perm_add:
                r, msg = self.bind_permission_to_role(
                    pname=p.get('name'),
                    pcode=p.get('code'),
                    pgroup=p.get('group'),
                    rname=role.get('name'),
                    rcode=role.get('code'),
                    rgroup=role.get('group'),
                )
                if r == -1:
                    return False

        if perm_del and len(perm_del):
            for p in perm_del:
                r, msg = self.unbind_permission_to_role(
                    pname=p.get('name'),
                    pcode=p.get('code'),
                    pgroup=p.get('group'),
                    rname=role.get('name'),
                    rcode=role.get('code'),
                    rgroup=role.get('group'),
                )
                if r == -1:
                    return False
        return True

    # 绑定用户到组, 只取其中的code,成功返回0   失败返回其他值
    # i32 bindUserToRole(1:i64 uid, 2:PermissionRole r) throws (1:ApolloException e);
    # 返回元组，元组中第一个元素为0则成功
    def bind_user_to_role(self, uid, name, code, group=''):
        name = unicode_to_utf8(name)
        code = unicode_to_utf8(code)
        group = unicode_to_utf8(group)
        r = -1
        try:
            r = thrift_callex(config.APOLLO_SERVERS, ApolloServer,
                              'bindUserToRole', uid,
                              PermissionRole(name=name, code=code, group=group))
            msg = '成功' if not r else '失败'
        except ApolloException, e:
            log.debug('apollo error:%s' % e)
            msg = '失败'
        except:
            log.error('apollo error:%s' % traceback.format_exc())
            msg = '失败'
        return r, msg

    # 解绑用户到组, 只取其中的code,成功返回0   失败返回其他值
    # i32 unbindUserToRole(1:i64 uid, 2:PermissionRole r) throws (1:ApolloException e);
    # 返回元组，元组中第一个元素为0则成功
    def unbind_user_to_role(self, uid, name, code, group=''):
        name = unicode_to_utf8(name)
        code = unicode_to_utf8(code)
        group = unicode_to_utf8(group)
        r = -1
        try:
            r = thrift_callex(config.APOLLO_SERVERS, ApolloServer,
                              'unbindUserToRole', uid,
                              PermissionRole(name=name, code=code,
                                             group=group))
            msg = '成功' if not r else '失败'
        except ApolloException, e:
            log.debug('apollo error:%s' % e)
            msg = '失败'
        except:
            log.error('apollo error:%s' % traceback.format_exc())
            msg = '失败'
        return r, msg

    def update_user_roles(self, params=None):
        roles_add = params.get('rolesBind')
        roles_del = params.get('rolesUnbind')
        uid = params.get('uid')
        uid = int(uid)
        if roles_add and len(roles_add):
            for role in roles_add:
                r, msg = self.bind_user_to_role(
                    uid=uid,
                    name=role.get('name'),
                    code=role.get('code'),
                    group=role.get('group'))
                if r == -1:
                    return False

        if roles_del and len(roles_del):
            for role in roles_del:
                r, msg = self.unbind_user_to_role(
                    uid=uid,
                    name=role.get('name'),
                    code=role.get('code'),
                    group=role.get('group'))
                if r == -1:
                    return False
        return True

    @with_database(['qf_core', 'qf_user'])
    def get_users(self, params=None):
        qf_core_conn = self.db['qf_core']
        qf_user_conn = self.db['qf_user']

        uids_has_role = None
        # check if need query user_role_map first
        if params.get('role'):
            where = {
                'urm.status': 1,
                'urm.role_code': DBFunc('pr.code'),
            }
            like = ' and pr.name like "%' + params['role'] + '%"'
            # get user_role_map for role name
            ur_map = qf_user_conn.select_join(
                table1='user_role_map as urm',
                table2='permission_role as pr',
                fields=['urm.userid', 'pr.code', 'pr.name', 'urm.status'],
                where=where,
                other=like,
            )
            uids_has_role = set([m['userid'] for m in ur_map])
            # return [] if no role name found
            if len(uids_has_role) == 0:
                return []

        # get users
        where = {
            'p.userid': DBFunc('a.id'),
            # 'p.groupid': ('in', config.GROUPID_IN)
        }
        if params.get('mobile'):
            where.update({'a.mobile': params['mobile']})
        if params.get('fullname'):
            where.update({'p.name': params['fullname']})
        if params.get('isActive'):
            where.update({'a.is_active': params['isActive']})
        # filter no role users
        limit = ' limit 100'
        if uids_has_role:
            where.update({'a.id': ('in', uids_has_role)})
            limit = ''

        users = qf_core_conn.select_join(
            table1='profile as p',
            table2='auth_user as a',
            fields=['a.id as uid', 'a.username', 'a.mobile', 'a.is_active',
                    'a.last_login', 'a.date_joined', 'p.name'],
            where=where,
            other=limit,
        )

        if len(users) == 0:
            return []

        uids = [row['uid'] for row in users]
        where = {
            'urm.userid': ('in', uids),
            'urm.status': 1,
            'urm.role_code': DBFunc('pr.code'),
        }
        # get user_role_map in user ids
        ur_map = qf_user_conn.select_join(
            table1='user_role_map as urm',
            table2='permission_role as pr',
            fields=['urm.userid', 'pr.code', 'pr.name', 'urm.status'],
            where=where,
            other='order by urm.userid'
        )

        # group user_role_map by key='userid'
        ur_group = {}
        for k, group in groupby(ur_map, lambda x: x['userid']):
            ur_group[k] = {
                'roles': [{'code': v['code'], 'name': v['name']} for v in group]
            }

        # post process users result
        for u in users:
            uid = u['uid']
            if u['date_joined'] is not None:
                u['date_joined'] = u['date_joined'].date().isoformat()
            if u['last_login'] is not None:
                u['last_login'] = u['last_login'].date().isoformat()
            u['roles'] = [] if ur_group.get(uid) is None else \
                ur_group.get(uid)['roles']
        return users

    @with_database('qf_user')
    def get_roles(self, params=None):
        where = {'status': 1}
        if params.get('role'):
            where.update({'name': ('like', '%' + params['role'] + '%')})
        roles = self.db.select(table='permission_role', where=where)

        for r in roles:
            if r['ctime'] is not None:
                r['ctime'] = r['ctime'].date().isoformat()
            if r['utime'] is not None:
                r['utime'] = r['utime'].date().isoformat()

        return roles

    @with_database('qf_user')
    def get_permissions(self, params=None):
        permissions = self.db.select(table='permission', where={'status': 1})
        # post process permissions result
        for p in permissions:
            if p['ctime'] is not None:
                p['ctime'] = p['ctime'].date().isoformat()
            if p['utime'] is not None:
                p['utime'] = p['utime'].date().isoformat()
        # group permissions by key='group'
        p_group = []
        for k, group in groupby(permissions, lambda x: x['group']):
            p_group.append({
                    'group': k,
                    'permissions': [v for v in group]})
        return p_group

    @with_database('qf_user')
    def get_permission_role_map(self, params=None):
        role_code = params.get('role')
        where = {'status': 1}
        if role_code:
            where.update({'role_code': role_code})
        permission_codes = self.db.select(
            fields=['permission_code', 'role_code'],
            table='permission_role_map',
            where=where)
        return permission_codes


class BaseHandler(core.Handler):
    def __init__(self, app, req):
        super(BaseHandler, self).__init__(app, req)
        self.resp.mimetype = 'application/json'
        self.resp.headers['Content-Type'] = '%s; charset=%s' % (
            self.resp.mimetype, self.resp.charset)

    # values {'username':value2,'operation_type':value3,'operation_code':value4,'description':value5}
    @with_database('qf_solar')
    def record(self, values):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        values['ctime'] = now_time
        sesid = self.get_cookie('sessionid')
        user = ApolloUser(sessionid=sesid)
        values['operator'] = user.ses['username']
        try:
            self.db.insert(table='operation_table', values=values)
        except Exception, e:
            log.debug('mysql insert error: %s' % traceback.format_exc())


class Users(BaseHandler):
    # query
    def GET(self):
        params = self.req.input()
        data = UserPermissionHelper().get_users(params)
        return json.dumps({'data': data}, ensure_ascii=False)

    # create
    def POST(self):
        return "not implement"

    # update
    def PUT(self):
        if self.req.environ.get('CONTENT_TYPE', '').lower().startswith(
                'application/json'):
            try:
                params = self.req.inputjson()
                ret = UserPermissionHelper().update_user_roles(params)
                if not ret:
                    return json.dumps({'ok': False, 'msg': '保存失败'},
                                  ensure_ascii=False)
                # 记录操作日志
                # values {'username':value2,'operation_type':value3,'operation_code':value4,'description':value5}
                roles_add = params.get('rolesBind')
                roles_del = params.get('rolesUnbind')
                mobile = params.get('mobile')
                uid = params.get('uid')
                vals = {}
                vals['username'] = mobile
                vals['operation_type'] = 'update_user'
                vals['operation_code'] = 1001
                vals['description'] = ''
                if len(roles_add):
                    vals['description'] += ' Bind:' + ','.join(
                        [r['name'] for r in roles_add])
                if len(roles_del):
                    vals['description'] += ' UnBind:' + ','.join(
                        [r['name'] for r in roles_del])
                self.record(vals)
                return json.dumps({'ok': True, 'msg': '修改成功'},
                                  ensure_ascii=False)
            except ValueError:
                return json.dumps({'ok': False, 'msg': 'Bad request'},
                                  ensure_ascii=False)
        return json.dumps({'ok': False, 'msg': 'Need json input format'},
                          ensure_ascii=False)


class Roles(BaseHandler):
    # query
    def GET(self):
        params = self.req.input()
        data = UserPermissionHelper().get_roles(params)
        return json.dumps({'data': data}, ensure_ascii=False)

    # create
    def POST(self):
        if self.req.environ.get('CONTENT_TYPE', '').lower().startswith(
                'application/json'):
            try:
                params = self.req.inputjson()
                ret = UserPermissionHelper().create_role_permissions(params)
                if ret == -1:
                    return json.dumps({'ok': False, 'msg': '角色添加失败'},
                                  ensure_ascii=False)
                elif ret == -2:
                    return json.dumps({'ok': False, 'msg': '角色添加成功，但权限绑定过程失败'},
                                      ensure_ascii=False)
                # 记录操作日志
                # values {'username':value2,'operation_type':value3,'operation_code':value4,'description':value5}
                role = params.get('role')
                perm_add = params.get('permissionsBind')
                vals = {}
                vals['username'] = role.get('name')
                vals['operation_type'] = 'create_role'
                vals['operation_code'] = 2001
                vals['description'] = ''
                if len(perm_add):
                    vals['description'] += ' Bind:' + ','.join(
                        [r['name'] for r in perm_add])
                self.record(vals)
                return json.dumps({'ok': True, 'msg': '角色添加成功'},
                                  ensure_ascii=False)
            except ValueError:
                return json.dumps({'ok': False, 'msg': 'Bad request'},
                                  ensure_ascii=False)
        return json.dumps({'ok': False, 'msg': 'Need json input format'},
                          ensure_ascii=False)

    # update
    def PUT(self):
        if self.req.environ.get('CONTENT_TYPE', '').lower().startswith(
                'application/json'):
            try:
                params = self.req.inputjson()
                ret = UserPermissionHelper().update_role_permissions(params)
                if not ret:
                    return json.dumps({'ok': False, 'msg': '保存失败'},
                                  ensure_ascii=False)
                # 记录操作日志
                # values {'username':value2,'operation_type':value3,'operation_code':value4,'description':value5}
                perm_add = params.get('permissionsBind')
                perm_del = params.get('permissionsUnbind')
                role = params.get('role')
                vals = {}
                vals['username'] = role.get('name')
                vals['operation_type'] = 'update_role'
                vals['operation_code'] = 2002
                vals['description'] = ''
                if len(perm_add):
                    vals['description'] += ' Bind:' + ','.join(
                        [r['name'] for r in perm_add])
                if len(perm_del):
                    vals['description'] += ' UnBind:' + ','.join(
                        [r['name'] for r in perm_del])
                self.record(vals)
                return json.dumps({'ok': True, 'msg': '修改成功'},
                                  ensure_ascii=False)
            except ValueError:
                return json.dumps({'ok': False, 'msg': 'Bad request'},
                                  ensure_ascii=False)
        return json.dumps({'ok': False, 'msg': 'Need json input format'},
                          ensure_ascii=False)


class Permissions(BaseHandler):
    # query
    def GET(self):
        params = self.req.input()
        data = UserPermissionHelper().get_permissions(params)
        return json.dumps({'data': data}, ensure_ascii=False)


class PermissionRoleMap(BaseHandler):
    # query
    def GET(self):
        params = self.req.input()
        data = UserPermissionHelper().get_permission_role_map(params)
        return json.dumps({'data': data}, ensure_ascii=False)


class Rate(BaseHandler):
    def get_rate_id(self):
        r = None
        try:
            r = thrift_callex(config.SPRING_SERVERS , Spring, 'getid')
            msg = 'rate_id获取失败！' if not r else 'rate_id获取成功！'
        except:
            log.debug('apollo error:%s' % traceback.format_exc())
            msg = 'rate_id获取error！'
        return r, msg

    @with_database('qf_core')
    def GET(self):
        #假数据
        # data = [{'id':'1','base_currency':'USD','foreign_currency':'OPPD','rate':'367.22','unit':'100',
        #          'utime': '2016-07-27 10:10:23','rate_resources':'中国银行','comments':'测试1','operator':'测试员1'},
        #         {'id':'2','base_currency': 'ABC', 'foreign_currency': 'DFGH', 'rate': '1000.22', 'unit': '100',
        #          'utime': '2016-07-27 10:10:23', 'rate_resources': '中国银行', 'comments': '测试2', 'operator': '测试员2'},
        #         {'id':'3','base_currency': 'MKID', 'foreign_currency': 'IDR', 'rate': '20000', 'unit': '100',
        #          'utime': '2016-07-27 10:10:23', 'rate_resources': '中国银行', 'comments': '测试3', 'operator': '测试员3'},
        #         {'id':'4','base_currency': 'DPP', 'foreign_currency': 'CCVVVV', 'rate': '390987.22', 'unit': '100',
        #          'utime': '2016-07-27 10:10:23', 'rate_resources': '中国银行', 'comments': '测试4电话噶看过后会感到恐惧火锅', 'operator': '测试员4'}]
        try:
            data = self.db.select(table='rate_table')
        except Exception, e:
            log.debug('mysql getdata error: %s' % traceback.format_exc())
            return json.dumps({'data': []}, ensure_ascii=False)
        for d in data:
            #将mysql返回的日期数据类型转换成字符串
            d['utime'] = d['utime'].strftime("%Y-%m-%d %H:%M:%S")
            d['ctime'] = d['ctime'].strftime('%Y-%m-%d %H:%M:%S')
            d['id'] = str(d['id'])

        return json.dumps({'data': data}, ensure_ascii=False)

    @with_database('qf_core')
    def POST(self):
        if self.req.environ.get('CONTENT_TYPE', '').lower().startswith(
                'application/json'):
            try:
                params = self.req.inputjson()
                #转utf8
                base_currency = unicode_to_utf8(params.get('base_currency'))
                foreign_currency = unicode_to_utf8(params.get('foreign_currency'))
                rate = unicode_to_utf8(params.get('rate'))
                unit = int(unicode_to_utf8(params.get('unit')))
                rate_resources = unicode_to_utf8(params.get('rate_resources'))
                comments = unicode_to_utf8(params.get('comments'))

                #构造新建的入库的数据
                values = {}
                values['base_currency'] = base_currency
                values['foreign_currency'] = foreign_currency
                values['rate'] = rate
                values['unit'] = unit
                values['src'] = rate_resources
                values['comments'] = comments

                rate_id = self.get_rate_id()[0]

                if rate_id:
                    values['id'] = rate_id
                else:
                    return json.dumps({'ok': False, 'msg': 'Bad request'},
                                      ensure_ascii=False)

                #获取当前的时间
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                #创建的时间
                values['ctime'] = now_time
                #更新的时间
                values['utime'] = now_time
                #获取当前操作人的name，即当前的登录用户的name
                sesid = self.get_cookie('sessionid')
                user = ApolloUser(sessionid=sesid)
                values['operator'] = user.ses['username']
                # values['operator'] = '张三'
                result = self.db.select(table='rate_table',where={'base_currency':base_currency,'foreign_currency':foreign_currency})
                # 判断该换算组合是否存在
                if len(result) > 0:
                    return json.dumps({'ok': False, 'msg': '该汇率换算已存在，无法新建 ！'},
                                      ensure_ascii=False)
                # 入库操作
                try:
                    self.db.insert(table='rate_table', values=values)
                except Exception, e:
                    log.debug('mysql insert error: %s' % traceback.format_exc())
                    return json.dumps({'ok': False, 'msg': '新建失败'},
                                      ensure_ascii=False)
                #构造需要插入历史表的数据，历史表中有rid，rid为rate_table中的id
                values['rid'] = rate_id
                del values['id']
                # 插入数据到历史记录表
                try:
                    self.db.insert(table='rate_history_table', values=values)
                except Exception, e:
                    log.debug('mysql insert error: %s' % traceback.format_exc())

                return json.dumps({'ok': True, 'msg': '新建成功'},
                                  ensure_ascii=False)

            except ValueError:
                return json.dumps({'ok': False, 'msg': 'Bad request'},
                                  ensure_ascii=False)
        return json.dumps({'ok': False, 'msg': 'Need json input format'},
                          ensure_ascii=False)

    @with_database('qf_core')
    def PUT(self):
        if self.req.environ.get('CONTENT_TYPE', '').lower().startswith(
                'application/json'):
            try:
                params = self.req.inputjson()
                #转utf8
                ori_base_currency = unicode_to_utf8(params.get('ori_base_currency'))
                ori_foreign_currency = unicode_to_utf8(params.get('ori_foreign_currency'))
                rate_id = unicode_to_utf8(params.get('rate_id'))
                base_currency = unicode_to_utf8(params.get('base_currency'))
                foreign_currency = unicode_to_utf8(params.get('foreign_currency'))
                rate = unicode_to_utf8(params.get('rate'))
                unit = int(unicode_to_utf8(params.get('unit')))
                rate_resources = unicode_to_utf8(params.get('rate_resources'))
                comments = unicode_to_utf8(params.get('comments'))
                #构造更新的数据
                values = {}
                values['base_currency'] = base_currency
                values['foreign_currency'] = foreign_currency
                values['rate'] = rate
                values['unit'] = unit
                values['src'] = rate_resources
                values['comments'] = comments
                #获取当前的时间
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                #更新的时间
                values['utime'] = now_time
                #获取当前操作人的name，即当前的登录用户的name
                sesid = self.get_cookie(config.sesskey)
                user = ApolloUser(sessionid=sesid)
                values['operator'] = user.ses['username']

                if ori_base_currency == base_currency and ori_foreign_currency == foreign_currency:
                    pass
                else:
                    result = self.db.select(table='rate_table',where={'base_currency':base_currency,'foreign_currency':foreign_currency})
                    # 判断该换算组合是否存在
                    if len(result) > 0:
                        return json.dumps({'ok': False, 'msg': '该汇率换算已存在，无法修改 ！'},
                                          ensure_ascii=False)
                # 更新操作
                try:
                    self.db.update(table='rate_table', values=values, where={'id':int(rate_id)})
                except Exception, e:
                    log.debug('mysql update error: %s' % traceback.format_exc())
                    return json.dumps({'ok': False, 'msg': '修改失败'},
                                      ensure_ascii=False)
                #插入到历史表
                values['rid'] = int(rate_id)
                try:
                    ret = self.db.insert(table='rate_history_table', values=values)

                except Exception, e:
                    log.debug('mysql insert_history error: %s' % traceback.format_exc())
                    return json.dumps({'ok': True, 'msg': '修改成功'},
                                      ensure_ascii=False)

                return json.dumps({'ok': True, 'msg': '修改成功'},
                                  ensure_ascii=False)

            except ValueError:
                return json.dumps({'ok': False, 'msg': 'Bad request'},
                                  ensure_ascii=False)
        return json.dumps({'ok': False, 'msg': 'Need json input format'},
                          ensure_ascii=False)


class RateHistory(BaseHandler):
    @with_database('qf_core')
    def GET(self):
        params = self.req.input()
        bid = params.get('bid')
        bid = 0 if len(bid) == 0 else int(bid)
        try:
            data = self.db.select(table='rate_history_table',fields=['base_currency','foreign_currency','unit','rate','src','comments','operator','utime'],where={'rid':bid},other='order by utime desc')
        except Exception, e:
            log.debug('mysql getdata error: %s' % traceback.format_exc())
            return json.dumps({'data': []}, ensure_ascii=False)
        for d in data:
            #将mysql返回的日期数据类型转换成字符串
            d['utime'] = d['utime'].strftime("%Y-%m-%d %H:%M:%S")
            # d['ctime'] = d['ctime'].strftime('%Y-%m-%d %H:%M:%S')

        return json.dumps({'data': data}, ensure_ascii=False)


class Merchants(BaseHandler):
    @with_database(['qf_core', 'qf_mis', 'qf_user'])
    def GET(self):
        qf_core_conn = self.db['qf_core']
        qf_mis_conn = self.db['qf_mis']
        qf_user_conn = self.db['qf_user']

        where = {}
        params = self.req.input()
        uid = params.get('uid')
        mobile = params.get('mobile')
        gid = params.get('gid')
        gname = params.get('gname')
        fullname = params.get('fullname')
        nickname = params.get('nickname')
        state = params.get('state')
        cate_codes = params.get('cate_codes')
        cate_codes = [i.strip() for i in cate_codes.split(',')] if cate_codes else []
        limit = params.get('length', 10)
        offset = params.get('start', 0)
        userids_in = []
        if not uid:
            uid = []
        elif ',' in uid:
            uid = uid.split(',')
        else:
            uid = [uid]

        userids_in.extend(uid)
        if mobile:
            if ',' in mobile:
                mobile = mobile.split(',')
                where.update({'auth_user.mobile': ('in', mobile)})
            else:
                where.update({'auth_user.mobile': mobile})
        if gid:
            where.update({'profile.groupid': gid})
        if gname:
            where.update({'groupname': ('like', '%' + gname + '%')})
        if fullname:
            where.update({'profile.name': fullname})
        if nickname:
            where.update({'profile.nickname': ('like', '%' + nickname + '%')})
        if state:
            where.update({'auth_user.state': state})

        # 搜索框userid和cate_code 合并
        cate_userids = get_tag_user(cate_codes)
        userids_in = [int(i) for i in userids_in if is_valid_int(i)]
        if userids_in and cate_userids:
            userids_in = list(set(userids_in) & set(cate_userids))
        elif cate_userids:
            userids_in = cate_userids

        if userids_in:
            where['profile.userid'] = ('in', userids_in)
        elif cate_codes and uid:
            where['profile.userid'] = '-1'


        # 需要避免无意义的查询
        if 'untagged' in cate_codes:
            all_tag_userids = all_tag_user()
            all_tag_userids = set(all_tag_userids) - set(userids_in)
            if all_tag_userids:
                where['auth_user.id'] = ('not in', all_tag_userids)

        other = 'order by profile.utime'
        excel_limit = getattr(config, 'MAX_EXCEL_ROWS', 5000)
        if params.get('mode') == 'expo_excel':
            other += ' limit {}'.format(excel_limit)
        else:
            other += ' limit {} offset {}'.format(limit, offset)

        data = qf_core_conn.select_join(
            table1='profile',
            table2='auth_user',
            join_type='left',
            on={'profile.userid': 'auth_user.id'},
            fields=[
                'profile.userid', 'profile.name', 'auth_user.username',
                'auth_user.mobile', 'profile.nickname', 'profile.groupid',
                '(SELECT auth_user.username FROM auth_user WHERE profile.groupid = auth_user.id) AS groupname',
                'auth_user.state',
            ],
            where=where,
            other=other
        )
        total = qf_core_conn.select_join(
            table1='profile',
            table2='auth_user',
            join_type='left',
            on={'profile.userid': 'auth_user.id'},
            fields = 'count(1) as total',
            where=where,
            other='order by profile.utime limit 1'
        )
        if total:
            total = total[0].get('total')

        if len(data) == 0:
            return json.dumps({'data': []}, ensure_ascii=False)

        uids = [x.get('userid') for x in data]
        # 获取新渠道
        mchnts = thrift_callex_framed(config.QUDAO_API_SERVERS, QudaoServer,
                                      'mchnt_get', uids)
        mchnt_qd_map = {m.mchnt_uid: m.qd_uid for m in mchnts}
        qd_ids = set(m.qd_uid for m in mchnts)
        qds = thrift_callex_framed(config.QUDAO_API_SERVERS, QudaoServer,
                                     'qd_get', qd_ids)
        for x in mchnt_qd_map:
            for q in qds:
                if mchnt_qd_map[x] == q.uid:
                    mchnt_qd_map[x] = {'qid': q.profile.qd_uid, 'qname': q.profile.name}
        # 新渠道覆盖老渠道
        for d in data:
            if d['userid'] in mchnt_qd_map:
                d['groupid'] = mchnt_qd_map[d['userid']]['qid']
                d['groupname'] = mchnt_qd_map[d['userid']]['qname']

        where = {
            'user': ('in', uids),
        }
        audit = qf_mis_conn.select(
            table='apply',
            fields=['user', 'lastaudittime', 'state'],
            where=where
        )

        audit_dict = {}
        for x in audit:
            audit_dict[x['user']] = x

        USER_STATES = {
            1: u'新建',
            2: u'通过审核, 未设备激活',
            3: u'已设备激活，未业务激活',
            4: u'已业务激活，正常',
            5: u'呆户',
            6: u'临时封禁，黑名单',
            7: u'永久封禁',
            8: u'用户主动注销',
            9: u'临时停用',
        }

        APPLY_STATE_CHOICES = (
            (0, u'等待基本信息'),
            (1, u'等待上传凭证'),
            (2, u'--'),
            (3, u'审核中'),
            (4, u'等待审核'),
            (5, u'审核通过'),
            (6, u'自动审核失败，待人工审核'),
            (7, u'审核拒绝'),
            (8, u'审核失败'),
            (9, u'等待复审'),
            (10, u'自动审核成功'),
        )

        # post process results
        for row in data:
            audit = audit_dict.get(row['userid'])
            lastaudittime = audit.get('lastaudittime') if audit is not None else None
            state = audit.get('state')if audit is not None else None
            row['lastaudittime'] = lastaudittime.strftime('%Y-%m-%d %H:%M:%S') if lastaudittime else u'--'
            row['auditstate'] = APPLY_STATE_CHOICES[state][1] if state in range(0, 11) else u'--'
            row['state'] = USER_STATES.get(row['state'], '无')

        if params.get('mode') == 'expo_excel':
            excel_name = '商户信息_{}.xls'.format(datetime.date.today())
            self.set_headers({'Content-Type': 'application/octet-stream'})
            self.set_headers(
                {'Content-disposition': 'attachment; filename={}'.format(excel_name)})
            head_list = [
                ('userid', '用户ID'), ('name', '签约实体'), ('mobile', '手机号码'),
                ('nickname', '收据名称'), ('groupid', '渠道ID'),
                ('groupname', '渠道名称'), ('lastaudittime', '审核时间'),
                ('auditstate', '审核状态'), ('state', '用户状态'),
            ]
            try:
                excel_file = excel_data(head_list, data)
            except:
                raise ValueError('错误')
            return excel_file

        return json.dumps({'data': data, 'total': total}, ensure_ascii=False)

get_imgurl = lambda userid, out_name: os.path.join('http://pic.qfpay.com/userprofile', os.path.join(str(userid/10000), str(userid)), out_name)


class Voucher(BaseHandler):
    @with_database(['qf_mis'])
    def GET(self):
        # 获取凭证图片信息
        params = self.req.input()
        uid = params.get('uid')
        CERT_NAME = {
            'idcardfront': '身份证正面',
            'idcardback': '身份证背面',
            'licensephoto': '营业执照',
            'livingphoto': '近期生活照',
            'groupphoto': '业务员与申请人在收银台合影',
            'goodsphoto': '店铺内景照片',
            'shopphoto': '店铺外景照片',
            'authcertphoto': '授权书照片',
            'idcardinhand': '手持身份证合照',
            'signphoto': '手写签名照',
            'otherphoto': '其他凭证照片',
            'otherphoto1': '其他凭证照片',
            'otherphoto2': '其他凭证照片',
            'otherphoto3': '其他凭证照片',
            'authidcardfront': '授权法人身份证正面',
            'authidcardback': '授权法人身份证背面',
            'authedcardfront': '被授权人身份证正面',
            'authedcardback': '被授权人身份证背面',
            'invoicephoto': '发票',
            'purchaselist': '进货单',
            'taxphoto': '税务登记证',
            'taxproof': '完税证明',
            'paypoint': '收银台照',
            'lobbyphoto': '财务室或者大堂照',
            'authbankcardfront': '银行卡正面',  # 授权法人银行卡正面
            'authbankcardback': '银行卡背面',  # 授权法人银行卡背面
            'rentalagreement': '店铺租赁合同',
            'orgphoto': '组织机构代码证',
            'openlicense': '开户许可证',
            'delegateagreement': '业务代理合同或者协议',
            'iatacert': '航协证',
            'insurancecert': '经营保险代理业务许可证，保险兼业',
            'licensephoto1': '营业执照照片',
            'foodcirculationpermit': '食品流通许可证',
            'foodhygienelicense': '食品卫生许可证',
            'foodservicelicense': '餐饮服务许可证',
        }
        cert_names_list = CERT_NAME.keys()
        voucher_dic = {}
        voucher_dic['data'] = {}
        voucher_dic['data']['identity'] = []
        voucher_dic['data']['account'] = []
        voucher_dic['data']['shop'] = []
        voucher_dic['data']['other'] = []

        vouchers = self.db['qf_mis'].select("mis_upgrade_voucher",
                                  fields="cert_type, name, imgname, submit_time",
                                  where={"user_id": uid})
        identity_list = ['idcardfront','idcardback','licensephoto','openlicense','orgphoto','taxphoto']
        account_list = ['authbankcardfront','authbankcardback','authcertphoto','authedcardfront','authedcardback']
        shop_list = ['shopphoto','goodsphoto','paypoint','lobbyphoto','idcardinhand','groupphoto']
        other_list = ['otherphoto','otherphoto1','otherphoto2','otherphoto3']
        voucher_dic['success'] = 1
        pattern = re.compile(r'otherphoto')

        for v in vouchers:
            if v['imgname'] == '' or v['imgname'] == None:
                voucher_dic['data']['identity'].append({
                    'cert_type': v['cert_type'],
                    'name': '凭证图片',
                    # 'imgurl': self.makeImgurl(uid,v['name'],v['imgname'],'middle'),
                    'imgurl': self.display_image(int(uid), v['name'], v['imgname'], 'large'),
                    # 'imgurl': 'http://easyread.ph.126.net/5s-Byepk6uzaA5WBv0j6-g==/7916558486779044144.jpg',
                    'submit_time': v['submit_time'].strftime("%Y-%m-%d"),
                })

            if v['name'] in identity_list:
                voucher_dic['data']['identity'].append({
                    'cert_type': v['cert_type'],
                    'name': CERT_NAME[v['name']],
                    # 'imgurl': self.makeImgurl(uid,v['name'],v['imgname'],'middle'),
                    'imgurl': self.display_image(int(uid), v['name'], v['imgname'], 'large'),
                    # 'imgurl': 'http://easyread.ph.126.net/5s-Byepk6uzaA5WBv0j6-g==/7916558486779044144.jpg',
                    'submit_time': v['submit_time'].strftime("%Y-%m-%d"),
                })
            elif v['name'] in  account_list:
                voucher_dic['data']['account'].append({
                    'cert_type': v['cert_type'],
                    'name': CERT_NAME[v['name']],
                    # 'imgurl': self.makeImgurl(uid, v['name'], v['imgname'], 'middle'),
                    'imgurl': self.display_image(int(uid), v['name'], v['imgname'], 'large'),
                    # 'imgurl': 'http://img5.imgtn.bdimg.com/it/u=4085853809,2185421038&fm=11&gp=0.jpg',
                    'submit_time': v['submit_time'].strftime("%Y-%m-%d"),
                })
            elif v['name'] in  shop_list:
                voucher_dic['data']['shop'].append({
                    'cert_type': v['cert_type'],
                    'name': CERT_NAME[v['name']],
                    # 'imgurl': self.makeImgurl(uid, v['name'], v['imgname'], 'middle'),
                    'imgurl': self.display_image(int(uid), v['name'], v['imgname'], 'large'),
                    # 'imgurl': 'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=743164759,2092542896&fm=11&gp=0.jpg',
                    'submit_time': v['submit_time'].strftime("%Y-%m-%d"),
                })
            elif re.match(pattern,v['name']):
                voucher_dic['data']['other'].append({
                    'cert_type': v['cert_type'],
                    'name': '其他凭证照片',
                    # 'imgurl': self.makeImgurl(uid, v['name'], v['imgname'], 'middle'),
                    'imgurl': self.display_image(int(uid), v['name'], v['imgname'], 'large'),
                    # 'imgurl': 'https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=402760109,117089075&fm=27&gp=0.jpg',
                    'submit_time': v['submit_time'].strftime("%Y-%m-%d"),
                })

        return  json.dumps(voucher_dic)

    def makeImgurl(self,userid, oldimgname, newimgname, size):
        '''
        生成图片get_imgurl(11111098, v['imgname']),
        '''
        sizesuffix = ""
        imgnamesuffix = newimgname
        if newimgname:
            sizesuffix = ""
            if size != 'original':
                sizesuffix = size + '_'
        else:
            sizesuffix = size + '_'
            imgnamesuffix = oldimgname

        return 'http://pic.qfpay.com/userprofile/%d/%d/%s%s' % (userid / 10000, userid, sizesuffix, imgnamesuffix)

    def display_image(self, user_id, name, imagename, size):
        '''
        显示图片
        传入Voucher 或 UpgradeVoucher 实例，分析新名称如果没有，使用旧名称
        参看pic.qfpay.com配置
        size = [middle, large] 不知道有没有 small
        '''
        # 如果是新图片
        if imagename:
            if size == 'original':
                size = ''
            else:
                size = size + '_'
            return 'http://pic.qfpay.com/userprofile/%d/%d/%s%s' % (
            user_id / 10000, user_id, size, imagename),
        # 如果是旧图片
        else:
            size = size + '_'
            return 'http://pic.qfpay.com/userprofile/%d/%d/%s%s' % (
            user_id / 10000, user_id, size, name)

class Channel(BaseHandler):
    @with_database(['qf_qudao'])
    def GET(self):
        params = self.req.input()
        uid = params.get('uid')
        result = self.db['qf_qudao'].select_join(
            table1='qd_profile as p',
            table2='qd_user as u',
            fields=['u.type as type', 'u.qd_uid as uid', 'p.name as name', 'u.status as status',
                    'p.business_mobile as business_mobile', 'p.business_name as business_name', 'p.auth_areas as auth_areas', 'p.manager_name as manager_name','p.service_manager_name as service_manager_name','u.memo as memo'],
            on={'p.qd_uid':DBFunc('u.qd_uid')},
            where={'u.qd_uid':uid},
        )
        return json.dumps(result[0])

#基本信息
class BaseInfo(BaseHandler):
    @with_database(['qf_core','qf_mis','qf_user'])
    def GET(self):
        params = self.req.input()
        uid = params.get('uid')
        data = {}
        try:
            info = self.db['qf_core'].select_one(table='profile',fields=['user_type','bankmobile','user_state','applytime','name','legalperson','mobile','nickname','businessaddr','address','longitude','latitude','mcc','email','telephone','province','city',
                                                                         'brchbank_code','bankaccount','bankProvince','bankname','headbankname','bankCity','banktype','bankuser'], where={'userid':uid})
            # 申请时间
            info['applytime'] = info.get('applytime').strftime("%Y-%m-%d %H:%M:%S") if info['applytime'] else ''

            info_mis = self.db['qf_mis'].select_one(table='apply',fields=['state','src','idstatdate','idenddate','lastaudittime','idnumber'] , where={'user': uid})
            info_mcc = self.db['qf_mis'].select_one(table='tools_mcc',fields=['mcc_name'],where={'id':info['mcc']})
            # info['latitude'] = 39.9525548169708
            # info['longitude'] = 116.451341231353
            info['idnumber'] = info_mis.get('idnumber','--') if info_mis else '--'
            info['mcc_name'] = info_mcc.get('mcc_name','--') if info_mcc else '--'
            info['state'] = info_mis.get('state','--') if info_mis else '--'
            info['src'] = info_mis.get('src','--') if info_mis else '--'
            # 审核时间
            info['lastaudittime'] = info_mis.get('lastaudittime').strftime("%Y-%m-%d %H:%M:%S") if info_mis and info_mis.get('lastaudittime') else '--'
            info['idstatdate'] = info_mis.get('idstatdate').strftime("%Y-%m-%d") if info_mis and info_mis.get('idstatdate') else '--'
            info['idenddate'] = info_mis.get('idenddate').strftime("%Y-%m-%d") if info_mis and info_mis.get('idenddate') else '--'
            info['dishonestyinfo'] = '否' if len(self.getDishonestyInfo(info.get('legalperson',''),info.get('idnumber','')))==0 else '是'

            info['user_state_name'] = self.get_user_state_name(info.get('user_state',''))
            info['apply_state_name'] = self.get_apply_state_name(info.get('state',''))
            info['user_type_name'] = self.get_user_type_name(info.get('user_type',''))
            info['bank_type_name'] = self.get_bank_type_name(info.get('banktype',''))

            #获取用户标签
            user_tag = self.db['qf_user'].select(table='user_tag',fields=['tag_name'],where={'userid':uid,'status':1})
            tag_arr = []
            for i in user_tag:
                tag_arr.append(i['tag_name'])
            info['user_tag'] = '|'.join(tag_arr) if len(tag_arr) else '无'
            #获取用户身份
            user_cate = self.db['qf_user'].select(
                table='user_category',
                fields=['cate_name','cate_code'],
                where={
                    'userid': uid,
                    'status': 1,
                    'cate_code': ('not in', all_tags())
                }
            )
            cate_arr = []
            for i in user_cate:
                cate_arr.append(i['cate_name'])
            info['cates'] = '|'.join(cate_arr) if len(cate_arr) else '无'

            isbigmerchant = False
            for i in user_cate:
                if i['cate_code'] == 'bigmerchant':
                    #大商户，总店
                    isbigmerchant = True

            if isbigmerchant:
                #是大商户则是总店，然后查询其他分店
                info['shop_type'] = '总店'
                relation = thrift_callex(config.APOLLO_SERVERS, ApolloServer,'getUserRelation', int(uid),'merchant')

            else:
                #不是大商户，则反查是否有总店，有总店则是分店，没有总店则是门店
                relation = thrift_callex(config.APOLLO_SERVERS, ApolloServer, 'getUserReverseRelation', int(uid),'merchant')

                if len(relation):
                    info['shop_type'] = '分店'
                else:
                    info['shop_type'] = '门店'

            data['success'] = 1
            data['msg'] = '成功'
            data['info'] = info
        except :
            log.error("baseinfo %s" % (traceback.format_exc()))
            data['success'] = 0
            data['msg'] = '失败'

        return json.dumps({'data':data})

    def get_bank_type_name(self,type):
        if type == 1:
            return '对私'
        elif type == 2:
            return '对公'
        else:
            return '无'

    #获取是否失信被执行人
    def getDishonestyInfo(self, name, idnumber):
        result = []
        if name and idnumber:
            urldata = {
                'resource_id': '6899',
                'query': '失信被执行人名单',
                'cardNum': idnumber,
                'iname': name,
                'areaName': '',
                'ie': 'utf-8',
                'oe': 'utf-8',
                'format': 'json',
                't': int(time.time()),
            }
            try:
                uri = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php'
                request = urllib2.Request(uri)
                request.add_header('Host', 'sp0.baidu.com')
                request.add_header('Referer', 'https://www.baidu.com/')
                request.add_header('User-Agent',
                                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36')
                res = urllib2.urlopen(request, urllib.urlencode(urldata), timeout=5).read()
                retjson = json.loads(res)
                result = retjson.get("data")[0].get("result") if retjson.get("data", None) else []
            except:
                log.info("获取数据异常 %s" % (traceback.format_exc()))
        return result

    #获取用户类型名称
    def get_user_type_name(self,type):
        if type == 1:
            return '小微'
        if type == 2:
            return '个体商户'
        if type == 3:
            return '企业'

    #获取用户状态名称
    def get_user_state_name(self,state):
        if state == 1:
            return '新建'
        elif state == 2:
            return '通过审核, 未设备激活'
        elif state == 3:
            return '已设备激活，未业务激活'
        elif state == 4:
            return '已业务激活，正常'
        elif state == 5:
            return '呆户'
        elif state == 6:
            return '临时封禁，黑名单'
        elif state == 7:
            return '永久封禁'
        elif state == 8:
            return '用户主动注销'
        elif state == 9:
            return '临时停用'
        else:
            return '无'

    #获取审核状态名称
    def get_apply_state_name(self,state):
        if state == 0:
            return '等待基本信息'
        if state == 1:
            return '等待上传凭证'
        elif state == 3:
            return '审核中'
        elif state == 4:
            return '等待审核'
        elif state == 5:
            return '审核通过'
        elif state == 6:
            return '自动审核失败，待人工审核'
        elif state == 7:
            return '审核拒绝'
        elif state == 8:
            return '审核失败'
        elif state == 9:
            return '等待复审'
        elif state == 10:
            return '自动审核成功'
        else:
            return '无'

#关联店铺
class Relation(BaseHandler):
    @checkIsLogin
    @with_database(['qf_core', 'qf_user','qf_mis'])
    def GET(self):
        qf_core_conn = self.db['qf_core']
        qf_core_user = self.db['qf_user']

        params = self.req.input()
        uid = params.get('uid',0)
        user_cate = self.db['qf_user'].select(table='user_category', fields=['cate_name', 'cate_code'],
                                              where={'userid': uid, 'status': 1})

        isbigmerchant = False
        for i in user_cate:
            if i['cate_code'] == 'bigmerchant':
                # 大商户，总店
                isbigmerchant = True
        uids = [0]
        if isbigmerchant:
            # 是大商户则是总店，然后查询其他分店
            relation = thrift_callex(config.APOLLO_SERVERS, ApolloServer, 'getUserRelation', int(uid), 'merchant')
            if len(relation):
                for i in relation:
                    if int(uid) != i.userid:
                        uids.append(i.userid)
        else:
            # 不是大商户，则反查是否有总店，有总店则是分店，没有总店则是门店
            relation = thrift_callex(config.APOLLO_SERVERS, ApolloServer, 'getUserReverseRelation', int(uid),
                                     'merchant')
            if len(relation):
                # 分店
                for i in relation:
                    if int(uid) != i.userid:
                        uids.append(i.userid)
                    # 查询到是总店，再获取总店下的分店
                    relation2 = thrift_callex(config.APOLLO_SERVERS, ApolloServer, 'getUserRelation', int(i.userid),
                                             'merchant')
                    if len(relation2):
                        for i in relation2:
                            if int(uid) != i.userid:
                                uids.append(i.userid)
            else:
                # 门店
                pass

        uids = list(set(uids))
        where = {
            'auth_user.id': ('in', uids),
        }

        data = qf_core_conn.select_join(
            table1='profile',
            table2='auth_user',
            join_type='left',
            on={'profile.userid': 'auth_user.id'},
            fields=[
                'profile.userid', 'profile.name', 'auth_user.username',
                'auth_user.mobile', 'profile.nickname', 'profile.groupid',
                '(SELECT auth_user.username FROM auth_user WHERE profile.groupid = auth_user.id) AS groupname',
            ],
            where=where,
        )
        uids2 = [x.get('userid') for x in data] if data else [0]
        where1 = {
            'user': ('in', uids2),
        }
        qf_mis_conn = self.db['qf_mis']
        audit = qf_mis_conn.select(
            table='apply',
            fields=['user', 'lastaudittime', 'state'],
            where=where1,
        )

        audit_dict = {}
        for x in audit:
            audit_dict[x['user']] = x

        STATE_CHOICES = (
            (0, u'等待基本信息'),
            (1, u'等待上传凭证'),
            (2, u'--'),
            (3, u'审核中'),
            (4, u'等待审核'),
            (5, u'审核通过'),
            (6, u'自动审核失败，待人工审核'),
            (7, u'审核拒绝'),
            (8, u'审核失败'),
            (9, u'等待复审'),
            (10, u'自动审核成功'),
        )
        # post process results
        for row in data:

            audit = audit_dict.get(row['userid'])
            lastaudittime = audit.get('lastaudittime') if audit is not None else None
            state = audit.get('state') if audit is not None else None
            row['lastaudittime'] = lastaudittime.strftime('%Y-%m-%d %H:%M:%S') if lastaudittime else u'--'
            row['auditstate'] = STATE_CHOICES[state][1] if state in range(0, 11) else u'--'

            # user_cate = self.db['qf_user'].select(table='user_category', fields=['cate_name', 'cate_code'],
            #                                       where={'userid': row['userid'], 'status': 1})
            # isbigmerchant = False
            # for i in user_cate:
            #     if i['cate_code'] == 'bigmerchant':
            #         # 大商户，总店
            #         isbigmerchant = True
            #
            # if isbigmerchant:
            #     # 是大商户则是总店，然后查询其他分店
            #     row['shop_type'] = '总店'
            # else:
            #     # 不是大商户，则反查是否有总店，有总店则是分店，没有总店则是门店
            #     relation = thrift_callex(config.APOLLO_SERVERS, ApolloServer, 'getUserReverseRelation', int(row['userid']),
            #                              'merchant')
            #     if len(relation):
            #         # 分店
            #         row['shop_type'] = '分店'
            #     else:
            #         # 门店
            #         row['shop_type'] = '门店'

        return json.dumps({'data': data})

#身份证关联
class IDRelation(BaseHandler):
    @with_database(['qf_mis','qf_core','qf_user'])
    def GET(self):
        params = self.req.input()
        uid = params['uid']
        id_number = params['idnumber']
        result = self.db['qf_mis'].select(table='apply',fields=['user','idnumber'],where={'idnumber':id_number,'user':('<>',int(uid)),})
        uids = [0]

        for i in result:
            if i['user'] != uid:
                uids.append(i['user'])

        where = {
            'auth_user.id': ('in', uids),
        }
        qf_core_conn = self.db['qf_core']
        data = qf_core_conn.select_join(
            table1='profile',
            table2='auth_user',
            join_type='left',
            on={'profile.userid': 'auth_user.id'},
            fields=[
                'profile.userid', 'profile.name', 'auth_user.username',
                'auth_user.mobile', 'profile.nickname', 'profile.groupid',
                '(SELECT auth_user.username FROM auth_user WHERE profile.groupid = auth_user.id) AS groupname',
            ],
            where=where,
        )

        uids2 = [x.get('userid') for x in data] if data else [0]

        where1 = {
            'user': ('in', uids2),
        }
        qf_mis_conn = self.db['qf_mis']
        audit = qf_mis_conn.select(
            table='apply',
            fields=['user', 'lastaudittime', 'state'],
            where=where1,
        )

        audit_dict = {}
        for x in audit:
            audit_dict[x['user']] = x

        STATE_CHOICES = (
            (0, u'等待基本信息'),
            (1, u'等待上传凭证'),
            (2, u'--'),
            (3, u'审核中'),
            (4, u'等待审核'),
            (5, u'审核通过'),
            (6, u'自动审核失败，待人工审核'),
            (7, u'审核拒绝'),
            (8, u'审核失败'),
            (9, u'等待复审'),
            (10, u'自动审核成功'),
        )

        # post process results
        for row in data:

            audit = audit_dict.get(row['userid'])
            lastaudittime = audit.get('lastaudittime') if audit is not None else None
            state = audit.get('state') if audit is not None else None
            row['lastaudittime'] = lastaudittime.strftime('%Y-%m-%d %H:%M:%S') if lastaudittime else u'--'
            row['auditstate'] = STATE_CHOICES[state][1] if state in range(0, 11) else u'--'

            # user_cate = self.db['qf_user'].select(table='user_category', fields=['cate_name', 'cate_code'],
            #                                       where={'userid': row['userid'], 'status': 1})
            # isbigmerchant = False
            # for i in user_cate:
            #     if i['cate_code'] == 'bigmerchant':
            #         # 大商户，总店
            #         isbigmerchant = True
            #
            # if isbigmerchant:
            #     # 是大商户则是总店，然后查询其他分店
            #     row['shop_type'] = '总店'
            # else:
            #     # 不是大商户，则反查是否有总店，有总店则是分店，没有总店则是门店
            #     relation = thrift_callex(config.APOLLO_SERVERS, ApolloServer, 'getUserReverseRelation',
            #                              int(row['userid']),
            #                              'merchant')
            #     if len(relation):
            #         # 分店
            #         row['shop_type'] = '分店'
            #     else:
            #         # 门店
            #         row['shop_type'] = '门店'

        return json.dumps({'data': data})

#渠道信息
class qudaoInfo(BaseHandler):
    @with_database(["qf_solar","qf_mis","qf_core"])
    def GET(self):
        params = self.req.input()
        uid = params.get('uid',0)
        qudaoid = params.get('qudaoid', 0)
        data = {}
        info = {}
        try:
            result = thrift_callex_framed(config.QUDAO_API_SERVERS , QudaoServer, 'mchnt_get',[int(uid)])
            qudao_id =  result[0].qd_uid if result else 0
            memo = result[0].memo if len(result) else ''
            try:
                qudao = thrift_callex_framed(config.QUDAO_API_SERVERS , QudaoServer, 'qd_get', [int(qudaoid)])
            except Exception, e:
                qudao = []

            if len(qudao):
                qudao_info = qudao[0]
                status = qudao_info.base_info.status if qudao_info else ''
                type = qudao_info.base_info.type if qudao_info else ''

                name = qudao_info.profile.name if qudao_info else ''
                business_mobile = qudao_info.profile.business_mobile if qudao_info else ''  #业务员手机
                business_name = qudao_info.profile.business_name if qudao_info else ''  #业务员姓名
                manager_name = qudao_info.profile.manager_name if qudao_info else '' #渠道经理
                service_manager_name = qudao_info.profile.service_manager_name if qudao_info else '' #渠道服务
                areas = []
                for a in qudao_info.auth_areas:
                    areas.append({'province':a.province,'city':a.city,'county':a.county})

                info['type'] = type
                info['type_name'] = self.get_type_name(type)
                info['qudao_id'] = qudao_id
                info['name'] = name
                info['status'] = status
                info['business_mobile'] = business_mobile
                info['business_name'] = business_name
                info['manager_name'] = manager_name
                info['service_manager_name'] = service_manager_name
                info['memo'] = memo
                info['area'] = areas
            else:
                print '老渠道逻辑'
                conn = self.db["qf_mis"]
                _sql = " select `channelid`,`channelname`,`area`,`status`,`companyname` from channel_crm where channelid = %s  " % (qudaoid)
                result = conn.query(_sql)

                conn = self.db["qf_mis"]
                _sql = " select `code_id`,`user` from audit_applycoderecord where `user` = %s  " % (
                uid)
                audit = conn.query(_sql)

                salesmanid = 0

                if audit:
                    salesmanid = audit[0]['user']

                conn = self.db["qf_core"]
                _sql = " select `name`,`mobile` from `profile` where `userid` = %s  " % (salesmanid)
                sales = conn.query(_sql)

                if result and sales:

                    info['type'] = '无'
                    info['type_name'] = '无'
                    info['qudao_id'] = result[0]['channelid']
                    info['name'] = result[0]['channelname']
                    info['status'] = result[0]['status']
                    info['business_mobile'] = sales[0]['mobile']
                    info['business_name'] = sales[0]['name']
                    info['manager_name'] = '无'
                    info['service_manager_name'] = '无'
                    info['memo'] = '无'
                    info['area'] = result[0]['area']

                else:

                    info['type'] = '无'
                    info['type_name'] = '无'
                    info['qudao_id'] = '无'
                    info['name'] = '无'
                    info['status'] = '无'
                    info['business_mobile'] = '无'
                    info['business_name'] = '无'
                    info['manager_name'] = '无'
                    info['service_manager_name'] = '无'
                    info['memo'] = '无'
                    info['area'] = '无'

            data['info'] = info
            data['success'] = 1
            data['msg'] = '成功'
        except ApolloException, e:
            log.debug('apollo error:%s' % e)
            data['success'] = 0
            data['msg'] = '失败'
        except Exception, e:
            print e
            log.error('apollo error:%s' % traceback.format_exc())
            data['success'] = 0
            data['msg'] = '失败'

        return json.dumps(data)

    def get_type_name(self,type):
        if type == 1:
            return '白牌'
        elif type == 2:
            return '联名'
        elif type == 3:
            return '合伙人'
        elif type == 4:
            return '直营'
        elif type == 5:
            return '钱台'


class FeeRatio(BaseHandler):
    @with_database('qf_risk_2')
    def GET(self):
        params = self.req.input()
        uid = params.get('uid', 0)
        uid = int(uid)
        busicd = {
            # QF_BUSICD_PAYMENT: u'刷卡消费',
            QF_BUSICD_WEIXIN_PRECREATE: u'微信正扫',
            QF_BUSICD_WEIXIN_SWIPE: u'微信反扫',
            QF_BUSICD_WEIXIN_PRECREATE_H5: u'微信H5',
            QF_BUSICD_ALIPAY_PRECREATE: u'支付宝正扫',
            QF_BUSICD_ALIPAY_SWIPE: u'支付宝反扫',
            QF_BUSICD_ALIPAY_H5: u'支付宝H5',
            QF_BUSICD_QQPAY_QRCODE: u'QQ钱包正扫',
            QF_BUSICD_QQPAY_SWIPE: u'QQ钱包反扫',
            QF_BUSICD_QQPAY_H5: u'QQ钱包H5',
            QF_BUSICD_JDPAY_PRECREATE: u'京东正扫',
            QF_BUSICD_JDPAY_SWIPE: u'京东反扫',
            QF_BUSICD_JDPAY_H5: u'京东H5',
        }

        data = {}
        # 借记卡
        data['debit_card'] = {
            'trade_type': u'借记卡',
            'available': u'否',
            'deduct_type': u'--',
            'ratio': u'--',
            'max_fee': u'--',
            'risk_level': u'--',
            'amt_per': u'--',
            'settle_cycle': u'--',
            'settle_mode': u'--',
        }
        # 信用卡
        data['credit_card'] = {
            'trade_type': u'信用卡',
            'available': u'否',
            'deduct_type': u'--',
            'ratio': u'--',
            'max_fee': u'--',
            'risk_level': u'--',
            'amt_per': u'--',
            'settle_cycle': u'--',
            'settle_mode': u'--',
        }
        # 无卡
        for k in busicd:
            data[k] = {
                'trade_type': u'--',
                'available': u'否',
                'deduct_type': u'--',
                'ratio': u'--',
                'max_fee': u'--',
                'risk_level': u'--',
                'amt_per': u'--',
                'settle_cycle': u'--',
                'settle_mode': u'--',
            }

        fee_query = FeeQueryArgs()
        fee_query.userid = [uid]
        fee_query.trade_type = [QF_BUSICD_PAYMENT]
        fee_query.card_type = 1  # 卡类型   1.借记卡 2.信用卡 3.准贷记卡 4.储值卡 5.无卡
        fee_ratios = thrift_callex(config.ACCOUNT2_SERVERS, Account2,
                                   'fee_ratio_query', fee_query)
        user_info = thrift_callex(config.APOLLO_SERVERS, ApolloServer,
                                  'findUserByid', uid)
        where = {'userid': uid}
        fields = [
            'amt_per_debit',
            'amt_per_credit',
            'amt_per_wxpay',
            'amt_per_alipay',
            'amt_per_jd',
        ]
        ret = self.db.select(table='risk_restrict', fields=fields, where=where)
        risk_ret = None if len(ret) == 0 else ret[0]
        settle_cycle = self.get_settle_cycle(uid)

        for r in fee_ratios:
            data['debit_card'] = {
                'trade_type': u'借记卡',
                'available': u'是',
                'deduct_type': u'固定费率',
                'ratio': str(r.ratio*100)+'%',
                'max_fee': r.max_fee if r.max_fee != -1 else u'无',
                'risk_level': user_info.risklevel,
                'amt_per': risk_ret['amt_per_debit']/100 if risk_ret else u'--',
                'settle_cycle': u'--',
                'settle_mode': u'自动结算',
            }

        fee_query.card_type = 2  # 卡类型   1.借记卡 2.信用卡 3.准贷记卡 4.储值卡 5.无卡
        fee_ratios = thrift_callex(config.ACCOUNT2_SERVERS, Account2,
                                   'fee_ratio_query', fee_query)
        for r in fee_ratios:
            data['credit_card'] = {
                'trade_type': u'信用卡',
                'available': u'是',
                'deduct_type': u'固定费率',
                'ratio': str(r.ratio * 100) + '%',
                'max_fee': r.max_fee if r.max_fee != -1 else u'无',
                'risk_level': user_info.risklevel,
                'amt_per': risk_ret['amt_per_credit']/100 if risk_ret else u'--',
                'settle_cycle': u'--',
                'settle_mode': u'自动结算',
            }

        fee_query.trade_type = [t for t in busicd]
        fee_query.card_type = 5  # 卡类型   1.借记卡 2.信用卡 3.准贷记卡 4.储值卡 5.无卡
        fee_ratios = thrift_callex(config.ACCOUNT2_SERVERS, Account2,
                                   'fee_ratio_query', fee_query)
        for r in fee_ratios:
            data[r.trade_type] = {
                'trade_type': busicd.get(r.trade_type, u'无'),
                'available': u'是',
                'deduct_type': u'固定费率',
                'ratio': str(r.ratio * 100) + '%',
                'max_fee': r.max_fee if r.max_fee != -1 else u'无',
                'risk_level': user_info.risklevel,
                'amt_per': self.get_risk(r.trade_type, risk_ret),
                'settle_cycle': settle_cycle if r.trade_type.startswith('8002') else u'--',
                'settle_mode': u'自动结算',
            }

        return json.dumps({'data': data}, ensure_ascii=False)

    def get_risk(self, trade_type, risk_ret):
        if risk_ret is None:
            return u'--'
        if trade_type.startswith('8002'):
            return risk_ret['amt_per_wxpay']/100
        if trade_type.startswith('8001'):
            return risk_ret['amt_per_alipay']/100
        if trade_type.startswith('8005'):
            return risk_ret['amt_per_jd']/100
        return u'--'

    def get_settle_cycle(self, uid):
        server = merchant_server.next()
        url = server['server']['addr'] + '/mchnt/qd/settle_type'
        client = RequestsClient(timeout=server['server']['timeout'] / 1000)
        content, status_code, headers = client.request(
            'GET', url, headers={}, params={'userids': uid})
        if status_code == 200:
            data = json.loads(content)['data']
            for key in data:
                if data[key] == 1:
                    return "T+1"
                elif data[key] == 2:
                    return "D+1"
                elif data[key] == 3:
                    return "D+0"
        return u'--'


class PayInfo(BaseHandler):
    @with_database('qf_user')
    def GET(self):
        params = self.req.input()
        uid = params.get('uid', 0)
        uid = int(uid)

        ret = {}

        data = self.get_pay_info(key='card', uid=uid)
        ret.update(data)
        data = self.get_pay_info(key='diancan', uid=uid)
        ret.update(data)
        data = self.get_pay_info(key='prepaid', uid=uid)
        ret.update(data)

        # 提现开通状态
        ret.update({'balance': {'status': '否'}})
        where = {
            'userid': uid,
            'service_code': 'balance',
            'status': 1,
        }
        data = self.db.select(table='user_service', where=where)
        if len(data):
            ret.update({'balance': {'status': '是'}})

        return json.dumps({'data': ret}, ensure_ascii=False)

    def get_pay_info(self, key, uid):
        server = merchant_server.next()
        url = server['server']['addr'] + '/mchnt/user/v1/pay_info'
        client = RequestsClient(timeout=server['server']['timeout'] / 1000)
        code_type = 'goods_code'
        if key == 'prepaid':
            code_type = 'service_code'
        content, status_code, headers = client.request(
            'GET', url, headers={},
            params={code_type: key, 'userid': uid})

        ret = {key: {
            'status': '--',
            'free': '--',
            'left_day': '--',
            'is_qfgroup': '--',
            'left_warn': '--',
            'expire_time': '--',
            'overdue': '--',
        }}
        data = json.loads(content)
        if status_code == 200 and data.get('respcd') == '0000':
            ret[key]['free'] = str(data['data'].get('free', '--')) + u'天'
            ret[key]['left_day'] = str(data['data'].get('left_day', ' --')) + u'天'
            ret[key]['expire_time'] = data['data'].get('expire_time', '--')

            if data['data'].get('status') == 0:
                ret[key]['status'] = u'未开通'
            elif data['data'].get('status') == 1:
                ret[key]['status'] = u'免费体验'
            elif data['data'].get('status') == 2:
                ret[key]['status'] = u'付费'

            if data['data'].get('is_qfgroup') == 0:
                ret[key]['is_qfgroup'] = u'否'
            elif data['data'].get('is_qfgroup') == 1:
                ret[key]['is_qfgroup'] = u'是'

            if data['data'].get('left_warn') == 0:
                ret[key]['left_warn'] = u'否'
            elif data['data'].get('left_warn') == 1:
                ret[key]['left_warn'] = u'是'

            if data['data'].get('overdue') == 0:
                ret[key]['overdue'] = u'未过期'
            elif data['data'].get('overdue') == 1:
                ret[key]['overdue'] = u'过期'

        return ret


class Termbind(BaseHandler):
    @with_database(['qf_core', 'qf_mis'])
    def GET(self):
        params = self.req.input()
        uid = params.get('uid', 0)
        uid = int(uid)

        core_conn = self.db['qf_core']
        mis_conn = self.db['qf_mis']
        where = {'userid': uid}
        fields = ['terminalid', 'state', 'active_date']
        other = 'order by terminalid'
        data = core_conn.select(
            table='termbind',
            fields=fields,
            where=where,
            other=other,
        )
        if len(data) == 0:
            return json.dumps({'data': []}, ensure_ascii=False)

        # tids = [t['terminalid'] for t in data]
        # where = {'terminalid': ('in', tids)}
        # fields = ['terminalid', 'model']
        # res = mis_conn.select(table='terminal', fields=fields, where=where)
        # term_map = {t['terminalid']: t['model'] for t in res}
        # TERMINAL_MODELS = {
        #     '0001': u'qpos',
        #     '0002': u'ipos',
        #     '0003': u'qpos2.0',
        # }
        TERMINAL_MODELS = {
            '0001000100': 'QPOS 1.0',
            '0002000200': 'QPOS 2.0',
            '0002000300': 'QPOS 2.0',
            '0003000300': 'QPOS 3.0',
            '0003000500': '刷卡头',
            '0104000300': '联迪M35',
            '0104000500': '联迪M35非接',
            '0204000300': '联迪M15',
            '0504000300': '联迪M18',
            '1006000100': '钱好近一代',
            '0305000300': '安卓POS(W790)',
            '0003000301': '白牌QPOS',
            '0403000300': '鼎合刷卡头A19',
            '0607000400': '商米V1',
            '0704000600': '联迪A8',
            '0708000600': '富友A8',
            '0809000700': '好近快盒',
            '0909000700': '好近快盒无线版',
        }
        TERMINAL_STATES = {
            1: u'未绑定',
            2: u'正常',
            3: u'激活未成功',
            4: u'失效',
        }
        for t in data:
            t['state'] = TERMINAL_STATES.get(t['state'], u'--')
            model = u'--'
            if len(t['terminalid']) > 14:
                model = TERMINAL_MODELS.get(t['terminalid'][4:14], u'--')
            t['model'] = model
            t['active_date'] = t['active_date'].strftime("%Y-%m-%d %H:%M:%S") if t['active_date'] else u'--'

        return json.dumps({'data': data}, ensure_ascii=False)


class Trade(BaseHandler):
    @with_database(['qf_trade','qf_fund2','qf_core'])
    def GET(self):
        try:
            # 获取支付通道name
            fund2_result = self.db['qf_core'].select(table='channel',fields=['code','name'])
            fund2_dic = {}
            for i in fund2_result:
                try:
                    keystr = int(i.get('code',0))
                    fund2_dic[keystr] = i['name']
                except Exception, e:
                    pass


            params = self.req.input()
            uid = params.get('uid')
            chnlid = params.get('chnlid')
            syssn = params.get('syssn')
            groupid = params.get('groupid')
            chnluserid = params.get('chnluserid')
            startdate = params.get('startdate')
            enddate = params.get('enddate')
            starttxamt = params.get('starttxamt')
            endtxamt = params.get('endtxamt')
            status = params.get('status')
            txcurrcd = params.get('txcurrcd')
            busicd = params.get('busicd')
            chnlsn = params.get('chnlsn')
            print startdate
            print enddate
            where = []
            if uid:
                str = "userid=%s" % uid
                where.append(str)
            if chnlid:
                str = "chnlid='%s'" % chnlid
                where.append(str)
            if syssn:
                str = "syssn='%s'" % syssn
                where.append(str)
            if groupid:
                str = "groupid=%s" % groupid
                where.append(str)
            if chnluserid:
                str = "chnluserid='%s'" % chnluserid
                where.append(str)
            if starttxamt and endtxamt:
                str = "txamt between %.2f and %.2f" % (float(starttxamt) * 100.00, float(endtxamt) * 100.00)
                where.append(str)
            if txcurrcd:
                str = "txcurrcd='%s'" % txcurrcd
                where.append(str)
            if status:
                str = "status='%s'" % status
                where.append(str)
            if busicd:
                str = "busicd='%s'" % busicd
                where.append(str)
            if chnlsn:
                str = "chnlsn='%s'" % chnlsn
                where.append(str)
            table_name1 = ''
            table_name2 = ''
            if startdate and enddate:
                str = "sysdtm between '%s' and '%s'" % (startdate, enddate)
                where.append(str)
                table_name1 = "record_" + startdate.split('-')[0] + startdate.split('-')[1]
                table_name2 = "record_" + enddate.split('-')[0] + enddate.split('-')[1]
            other = 'limit 100'
            result = []

            if table_name1 == table_name2:
                t = ''
                if len(where) > 1:
                    t = ' and '.join(where)
                else:
                    t = where[0]
                sqlstr = "select '%s' as 'table_name',sysdtm,userid,syssn,status,chnlid,chnluserid,txamt,txcurrcd,busicd,cancel,retcd,origssn,groupid,chnlsn from %s where %s limit 100 " % (table_name1,table_name1,t)
                result = self.db['qf_trade'].query(sqlstr)
            else:
                t = ''
                if len(where) > 1:
                    t = ' and '.join(where)
                else:
                    t = where[0]
                sqlstr = "select * from (select '%s' as 'table_name',sysdtm,userid,syssn,status,chnlid,chnluserid,txamt,txcurrcd,busicd,cancel,retcd,origssn,groupid,chnlsn from %s where %s union all select '%s' as 'table_name',sysdtm,userid,syssn,status,chnlid,chnluserid,txamt,txcurrcd,busicd,cancel,retcd,origssn,groupid,chnlsn from %s where %s) as t_table limit 100 " % (table_name1,table_name1, t,table_name2,table_name2,t)

                result = self.db['qf_trade'].query(sqlstr)
            print sqlstr
            data_arr = []
            for i in result:
                info = {}
                info['userid'] = unicode_to_utf8(i.get('userid'))
                info['chnlid'] = unicode_to_utf8(i.get('chnlid'))
                info['chnlname'] = unicode_to_utf8(fund2_dic.get(int(i.get('chnlid'))))
                info['chnluserid'] = unicode_to_utf8(i.get('chnluserid'))
                info['txamt'] = unicode_to_utf8(i.get('txamt'))
                info['txcurrcd'] = unicode_to_utf8(currency.Currency.get(i.get('txcurrcd')))
                info['busicd'] = unicode_to_utf8(defines.busicd.get(i.get('busicd')))
                info['cancel'] = unicode_to_utf8(defines.cancel_state.get(i.get('cancel')))
                info['retcd'] = unicode_to_utf8(i.get('retcd'))
                info['retcd_name'] = unicode_to_utf8(self.get_retcd_name(i.get('retcd')))
                info['syssn'] = unicode_to_utf8(i.get('syssn'))
                info['origssn'] = unicode_to_utf8(i.get('origssn'))
                info['txdtm'] = unicode_to_utf8(i.get('sysdtm').strftime("%Y-%m-%d %H:%M:%S"))
                info['groupid'] = unicode_to_utf8(i.get('groupid'))
                info['trade_status'] = self.get_trade_status(unicode_to_utf8(i.get('status')))
                info['table_name'] = unicode_to_utf8(i.get('table_name'))
                info['chnlsn'] = unicode_to_utf8(i.get('chnlsn'))
                data_arr.append(info)
            # defines.busicd.get('600002')
            ret = {'code': 200, 'msg': '成功', 'data': data_arr}
        except:
            log.info("交易列表获取数据异常 %s" % (traceback.format_exc()))
            ret = {'code': 0, 'msg': '失败', 'data': []}

        return json.dumps(ret)

    def get_trade_status(self,status):
        if status == 0:
            return '交易中'
        elif status == 1:
            return '交易成功'
        elif status == 2:
            return '交易失败'
        elif status == 3:
            return '交易超时'
        else:
            return '未知'

    def get_retcd_name(self,retcd):
        return defines.err_state.get(retcd,'无')


class tradeTotal(BaseHandler):
    @with_database(['qf_trade'])
    def GET(self):
        # pass
        params = self.req.input()
        uid = params.get('uid')
        chnlid = params.get('chnlid')
        syssn = params.get('syssn')
        groupid = params.get('groupid')
        chnluserid = params.get('chnluserid')
        startdate = params.get('startdate')
        enddate = params.get('enddate')
        starttxamt = params.get('starttxamt')
        endtxamt = params.get('endtxamt')
        status = params.get('status')
        txcurrcd = params.get('txcurrcd')
        busicd = params.get('busicd')
        chnlsn = params.get('chnlsn')
        where = []
        if uid:
            str = "userid=%s" % uid
            where.append(str)
        if chnlid:
            str = "chnlid='%s'" % chnlid
            where.append(str)
        if syssn:
            str = "syssn='%s'" % syssn
            where.append(str)
        if groupid:
            str = "groupid=%s" % groupid
            where.append(str)
        if chnluserid:
            str = "chnluserid='%s'" % chnluserid
            where.append(str)
        if starttxamt and endtxamt:
            str = "txamt between %.2f and %.2f" % (float(starttxamt) * 100.00, float(endtxamt) * 100.00)
            where.append(str)
        if txcurrcd:
            str = "txcurrcd='%s'" % txcurrcd
            where.append(str)
        if status:
            str = "status='%s'" % status
            where.append(str)
        if busicd:
            str = "busicd='%s'" % busicd
            where.append(str)
        if chnlsn:
            str = "chnlsn='%s'" % chnlsn
            where.append(str)
        table_name1 = ''
        table_name2 = ''
        if startdate and enddate:
            str = "sysdtm between '%s' and '%s'" % (startdate, enddate)
            where.append(str)
            table_name1 = "record_" + startdate.split('-')[0] + startdate.split('-')[1]
            table_name2 = "record_" + enddate.split('-')[0] + enddate.split('-')[1]
        # result = {}
        if table_name1 == table_name2:
            t = ''
            if len(where) > 1:
                t = ' and '.join(where)
            else:
                t = where[0]
            # t_success = ''
            # if not status:
            t_success = t + ' and status=%d' % 1
            # else:
            #     t_success = t
            t_refund = t + " and cancel<>%d and retcd='0000'" % 0
            sqlstr_succ = "select count(*) as num,sum(txamt) as total from %s where %s" % (table_name1,t_success)
            # print 'succ :%s' % sqlstr_succ
            # result = self.db['qf_trade'].query(sqlstr_succ)
            sqlstr_refund = "select count(*) as re_num,sum(txamt) as re_total from %s where %s" % (table_name1, t_refund)
            # print 'refund :%s' % sqlstr_refund
            # result1 = self.db['qf_trade'].query(sqlstr_succ)
            sql =  "select * from (%s) as t1,(%s) as t2" % (sqlstr_succ,sqlstr_refund)
            # print sql
            try:
                result = self.db['qf_trade'].query(sql)
                data = {}
                if len(result):
                    data['total'] = int(result[0].get('total')) if result[0].get('total') else 0
                    data['re_total'] = int(result[0].get('re_total')) if result[0].get('re_total') else 0
                    data['num'] = int(result[0].get('num')) if result[0].get('num') else 0
                    data['re_num'] = int(result[0].get('re_num')) if result[0].get('re_num') else 0
                    # if type(data['total']) is types.IntType and type(data['re_total']) is types.IntType:
                    data['final_total'] = data['total'] - data['re_total']
                    # else:
                    #     data['final_total'] = '无'
                    # if type(data['num']) is types.LongType and type(data['re_num']) is types.LongType:
                    data['final_num'] = data['num'] - data['re_num']

                    # else:
                    #     data['final_num'] = '无'

                return json.dumps({'code':200,'msg':'成功','data':data})
            except:
                log.error('交易统计 db error:%s' % traceback.format_exc())
                return json.dumps({'code': 500, 'msg': '查询失败'})
        else:
            t = ''
            if len(where) > 1:
                t = ' and '.join(where)
            else:
                t = where[0]
            # t_success = ''
            # if not status:
            t_success = t + ' and status=%d' % 1
            # else:
            #     t_success = t
            t_refund = t + " and cancel<>%d  and retcd='0000'" % 0
            sqlstr_succ = "select sum(t1.num) as num,sum(t1.total) as total from (select count(*) as num,sum(table1.txamt) as total from %s as table1 where %s union all select count(*) as num,sum(table2.txamt) as total from %s as table2 where %s) as t1" % (table_name1, t_success, table_name2, t_success)
            sqlstr_refund = "select sum(t2.re_num) as re_num,sum(t2.re_total) as re_total from (select count(*) as re_num,sum(table3.txamt) as re_total from %s as table3 where %s union all select count(*) as re_num,sum(table4.txamt) as re_total from %s as table4 where %s) as t2" % (table_name1, t_refund, table_name2, t_refund)

            # sqlstr_succ = "select count(*) as num,sum(txamt) as total from %s where %s union all select count(*) as num,sum(txamt) as total from %s where %s" % (table_name1, t_success, table_name2, t_success)
            # sqlstr_refund = "select count(*) as re_num,sum(txamt) as re_total from %s where %s union all select count(*) as re_num,sum(txamt) as re_total from %s where %s" % (table_name1, t_refund, table_name2, t_refund)
            sql = "select * from (%s) as s1,(%s) as r1" % (sqlstr_succ, sqlstr_refund)

            try:
                result = self.db['qf_trade'].query(sql)
                # print result
                data = {}
                if len(result):
                    data['total'] = int(result[0].get('total')) if result[0].get('total') else 0
                    data['re_total'] = int(result[0].get('re_total')) if result[0].get('re_total') else 0
                    data['num'] = int(result[0].get('num')) if result[0].get('num') else 0
                    data['re_num'] = int(result[0].get('re_num')) if result[0].get('re_num') else 0
                    data['final_total'] = data['total'] - data['re_total']
                    data['final_num'] = data['num'] - data['re_num']

                return json.dumps({'code':200,'msg':'成功','data':data})
            except:
                log.error('交易统计 db error:%s' % traceback.format_exc())
                return json.dumps({'code': 500, 'msg': '查询失败'})


class tradeDetail(BaseHandler):
    @with_database(['qf_trade','qf_core'])
    def GET(self):
        params = self.req.input()
        syssn = params.get('syssn')
        table_name = params.get('table_name')
        sql = "select sysdtm,userid,groupid,out_trade_no,syssn,orderno,txamt,txcurrcd,coupon_amt,paydtm,status,retcd,busicd,cancel,origssn,chnlsn,haspwd,sign,chnlid,chnluserid,chnltermid,cardtp,cardcd,issuerbank,os,phonemodel,appver,terminalid,psamid from %s where syssn='%s'" % (table_name,syssn)
        result = self.db['qf_trade'].query(sql)

        data = {}
        if len(result):
            data['userid'] = result[0].get('userid','无')
            data['groupid'] = result[0].get('groupid','无')
            data['syssn'] = result[0].get('syssn','无')
            data['orderno'] = result[0].get('orderno','无')
            data['txamt'] = result[0].get('txamt','无')
            data['out_trade_no'] = result[0].get('out_trade_no', '无')
            data['txcurrcd'] = unicode_to_utf8(currency.Currency.get(result[0].get('txcurrcd')))
            data['coupon_amt'] = result[0].get('coupon_amt','无')
            if result[0].get('sysdtm'):
                data['txdtm'] = result[0].get('sysdtm').strftime("%Y-%m-%d %H:%M:%S")
            else:
                data['txdtm'] = '无'

            if result[0].get('paydtm'):
                data['paydtm'] = result[0].get('paydtm').strftime("%Y-%m-%d %H:%M:%S")
            else:
                data['paydtm'] = '无'
            data['status'] = self.get_trade_status(result[0].get('status','--'))
            data['retcd'] = result[0].get('retcd','无')
            data['busicd_name'] = unicode_to_utf8(defines.busicd.get(result[0].get('busicd')))
            data['busicd'] = result[0].get('busicd','无')
            data['cancel'] = unicode_to_utf8(defines.cancel_state.get(result[0].get('cancel')))
            data['origssn'] = result[0].get('origssn','无')
            data['chnlsn'] = result[0].get('chnlsn','无')
            data['haspwd'] = result[0].get('haspwd','无')
            data['sign'] = result[0].get('sign','无')
            data['chnlid'] = result[0].get('chnlid','无')
            data['chnluserid'] = result[0].get('chnluserid', '无')
            data['chnltermid'] = result[0].get('chnltermid','无')
            data['cardtp'] = defines.card_type.get(int(unicode_to_utf8(result[0].get('cardtp'))) if result[0].get('cardtp') else '--')
            data['cardcd'] = unicode_to_utf8(result[0].get('cardcd','无'))
            data['issuerbank'] = result[0].get('issuerbank','无')
            data['os'] = result[0].get('os','无')
            data['phonemodel'] = result[0].get('phonemodel','无')
            data['appver'] = result[0].get('appver')
            data['terminalid'] = result[0].get('terminalid')
            data['psamid'] = result[0].get('psamid','无')
            # data[''] = result[0].get('')
            # 退款金额部分
            # origssn = result[0].get('origssn')
            # if origssn:
            #     refund_sql = "select txamt from %s where syssn='%s' and busicd in ('%s','%s','%s','%s','%s','%s')" % (table_name,origssn,defines.QF_BUSICD_QUICK_REFUND,defines.QF_BUSICD_QQPAY_REFUND,defines.QF_BUSICD_JDPAY_REFUND,defines.QF_BUSICD_BAIFUBAO_REFUND_QUERY,defines.QF_BUSICD_WEIXIN_REFUND,defines.QF_BUSICD_ALIPAY_REFUND)
            #     refund = self.db['qf_trade'].query(sql)
            #     if len(refund):
            #         data['refund'] = refund[0]['txamt']
            #     else:
            #         data['refund'] = 0
            # else:
            #     data['refund'] = 0

            try:
                qudao = thrift_callex_framed(config.QUDAO_API_SERVERS, QudaoServer, 'qd_get', [int(data['groupid'])])
                qudao_info = qudao[0]
                type = qudao_info.base_info.type if qudao_info else ''
                data['qudaoname'] = self.get_type_name(type)
            except:
                log.error('qudao error:%s' % traceback.format_exc())
                data['qudaoname'] = '--'


            info = self.db['qf_core'].select_one(table='profile',fields=['nickname'],where={'userid':data['userid']})
            data['nick_name'] = info['nickname']

        return json.dumps({'code':200,'msg':'成功','data':data})

    def get_trade_status(self,status):
        if status == 0:
            return '交易中'
        elif status == 1:
            return '交易成功'
        elif status == 2:
            return '交易失败'
        elif status == 3:
            return '交易超时'
        else:
            return '未知'

    def get_retcd_name(self,retcd):
        return defines.err_state.get(retcd,'无')

    def get_type_name(self,type):
        if type == 1:
            return '白牌'
        elif type == 2:
            return '联名'
        elif type == 3:
            return '合伙人'
        elif type == 4:
            return '直营'
        elif type == 5:
            return '钱台'


class tradeExcel(BaseHandler):
    def __init__(self, app, req):
        super(BaseHandler, self).__init__(app, req)
        self.resp.mimetype = 'application/vnd.ms-excel'
        self.resp.headers['Content-Type'] = '%s; charset=%s' % (
            self.resp.mimetype, self.resp.charset)

    @with_database(['qf_trade'])
    def POST(self):
        params = self.req.input()
        uid = params.get('uid')
        chnlid = params.get('chnlid')
        syssn = params.get('syssn')
        groupid = params.get('groupid')
        chnluserid = params.get('chnluserid')
        startdate = params.get('startdate')
        enddate = params.get('enddate')
        starttxamt = params.get('starttxamt')
        endtxamt = params.get('endtxamt')
        status = params.get('status')
        txcurrcd = params.get('txcurrcd')
        busicd = params.get('busicd')
        chnlsn = params.get('chnlsn')
        where = []
        if uid:
            str = "userid=%s" % uid
            where.append(str)
        if chnlid:
            str = "chnlid='%s'" % chnlid
            where.append(str)
        if syssn:
            str = "syssn='%s'" % syssn
            where.append(str)
        if groupid:
            str = "groupid=%s" % groupid
            where.append(str)
        if chnluserid:
            str = "chnluserid='%s'" % chnluserid
            where.append(str)
        if starttxamt and endtxamt:
            str = "txamt between %.2f and %.2f" % (float(starttxamt) * 100.00, float(endtxamt) * 100.00)
            where.append(str)
        if txcurrcd:
            str = "txcurrcd='%s'" % txcurrcd
            where.append(str)
        if status:
            str = "status='%s'" % status
            where.append(str)
        if busicd:
            str = "busicd='%s'" % busicd
            where.append(str)
        if chnlsn:
            str = "chnlsn='%s'" % chnlsn
            where.append(str)
        table_name1 = ''
        table_name2 = ''
        if startdate and enddate:
            str = "sysdtm between '%s' and '%s'" % (startdate, enddate)
            where.append(str)
            table_name1 = "record_" + startdate.split('-')[0] + startdate.split('-')[1]
            table_name2 = "record_" + enddate.split('-')[0] + enddate.split('-')[1]
        other = 'limit 100'
        result = []

        if table_name1 == table_name2:
            t = ''
            if len(where) > 1:
                t = ' and '.join(where)
            else:
                t = where[0]
            sqlstr = "select '%s' as 'table_name',sysdtm,userid,status,chnlid,chnluserid,txamt,txcurrcd,busicd,cancel,retcd,syssn,origssn,groupid from %s where %s order by 'txdtm' desc limit 5000" % (
            table_name1, table_name1, t)
            result = self.db['qf_trade'].query(sqlstr)
        else:
            t = ''
            if len(where) > 1:
                t = ' and '.join(where)
            else:
                t = where[0]
            sqlstr = "select * from (select '%s' as 'table_name',sysdtm,userid,status,chnlid,chnluserid,txamt,txcurrcd,busicd,cancel,retcd,syssn,origssn,groupid from %s where %s union all select '%s' as 'table_name',sysdtm,userid,status,chnlid,chnluserid,txamt,txcurrcd,busicd,cancel,retcd,syssn,origssn,groupid from %s where %s) as t_table order by 'txdtm' desc limit 5000 " % (
            table_name1, table_name1, t, table_name2, table_name2, t)

            result = self.db['qf_trade'].query(sqlstr)
        data_arr = []
        for i in result:
            info = {}
            info['userid'] = unicode_to_utf8(i.get('userid'))
            info['chnlid'] = unicode_to_utf8(i.get('chnlid'))
            info['chnluserid'] = unicode_to_utf8(i.get('chnluserid'))
            info['txamt'] = unicode_to_utf8(i.get('txamt'))
            info['txcurrcd'] = unicode_to_utf8(currency.Currency.get(i.get('txcurrcd')))
            info['busicd'] = unicode_to_utf8(defines.busicd.get(i.get('busicd')))
            info['cancel'] = unicode_to_utf8(defines.cancel_state.get(i.get('cancel')))
            # info['retcd'] = unicode_to_utf8(i.get('retcd'))
            # info['retcd_name'] = unicode_to_utf8(self.get_retcd_name(i.get('retcd')))
            info['syssn'] = unicode_to_utf8(i.get('syssn'))
            # info['origssn'] = unicode_to_utf8(i.get('origssn'))
            info['txdtm'] = unicode_to_utf8(i.get('sysdtm').strftime("%Y-%m-%d %H:%M:%S"))
            info['groupid'] = unicode_to_utf8(i.get('groupid'))
            info['trade_status'] = self.get_trade_status(unicode_to_utf8(i.get('status')))
            info['table_name'] = unicode_to_utf8(i.get('table_name'))
            data_arr.append(info)
        # defines.busicd.get('600002')
        # ret = {'code': 200, 'msg': '成功', 'data': data_arr}
        header = ['用户ID','支付通道','通道商户号','交易金额','币种','支付类型','交易状态','取消状态','钱方流水号','创建时间','渠道ID']
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
            worksheet.write(j, 1, con['chnlid'])
            worksheet.write(j, 2, con['chnluserid'])
            worksheet.write(j, 3, con['txamt']/100.0)
            worksheet.write(j, 4, con['txcurrcd'])
            worksheet.write(j, 5, con['busicd'])
            worksheet.write(j, 6, con['trade_status'])
            worksheet.write(j, 7, con['cancel'])
            worksheet.write(j, 8, con['syssn'])
            worksheet.write(j, 9, con['txdtm'])
            worksheet.write(j, 10, con['groupid'])
            j = j + 1
        # workbook.save('Excel_test.xls')
        sio = StringIO.StringIO()
        workbook.save(sio)  # 这点很重要，传给save函数的不是保存文件名，而是一个StringIO流

        return sio.getvalue()

    def get_trade_status(self,status):
        if status == 0:
            return '交易中'
        elif status == 1:
            return '交易成功'
        elif status == 2:
            return '交易失败'
        elif status == 3:
            return '交易超时'
        else:
            return '未知'

    def get_retcd_name(self,retcd):
        return defines.err_state.get(retcd,'无')


class QRCode(BaseHandler):
    def POST(self):
        params = self.req.input()
        userid = params.get('userid')

        jhhs = Hashids(salt='qfpay').encode(int(userid))
        jhcode = config.code['jh'] % jhhs

        dchs = Hashids().encode(int(userid))
        czcode = "https://o2.qfpay.com/prepaid/v1/page/c/recharge/index.html?h=%s" % dchs

        dccode = "https://o.qfpay.com/dc/index.html?/#/merchant/%s" % userid

        ret = {'code':200,'msg':'成功','data':{'jhcode':jhcode,'dccode':dccode,'czcode':czcode}}

        return json.dumps(ret)


class Fund(BaseHandler):
    def GET(self):
        params = self.req.input()
        # 用户ID、手机号
        mobile = params.get('uid')
        if len(mobile) >= 11:
            users = UserPermissionHelper().get_users({'mobile': mobile})
            uid = users[0].get('uid') if len(users) > 0 else 0
        else:
            uid = int(mobile)
        # 起止时间
        start_date = params.get('start_date')
        end_date = params.get('end_date')
        start_time = start_date + ' 00:00:00'
        end_time = end_date + ' 23:59:59'
        # 账户名称
        account_type = params.get('account_type')
        account_type_ids = [
            2000, 2001, 2002, 2003, 2004, 2005,
            2006, 2007, 2008, 2009, 2100, 2010,
            2011, 2012, 2014, 2015, 2016, 2017, 
            2018,
        ]
        if account_type:
            account_type_ids = [int(account_type)]
        # 余额详情
        action_type = params.get('action_type')
        action_types = []
        if action_type:
            action_types = [int(action_type)]
        else:
            action_types = [2, 3, 4, 6, 7]

        # record 接口
        record_args = RecordArgs()
        record_args.userid = uid
        record_args.action_types = action_types
        record_args.pos = 0
        record_args.count = 100000
        record_args.start_time = start_time
        record_args.end_time = end_time
        record_args.account_type_ids = account_type_ids
        try:
            record = thrift_callex(config.ACCOUNT2_SERVERS, Account2,
                                   'account_record', record_args)
            records = [r.__dict__ for r in record]
            # print json.dumps({'data': records}, ensure_ascii=False)
        except Exception, e:
            log.error('record error: %s' % e)
            return json.dumps({'data': [], 'msg': e.msg}, ensure_ascii=False)

        if 3 in action_types:
            # fund 接口
            fund_args = FundQueryParams()
            fund_args.userid = uid
            fund_args.start_date = start_date
            fund_args.end_date = end_date
            try:
                remit = thrift_callex(config.FUND2_SERVERS, Fund2, 'remit_query', fund_args)
                remits = [r.__dict__ for r in remit]
                # print json.dumps({'data': remits}, ensure_ascii=False)
            except Exception, e:
                log.error('remit error: %s' % e)
                return json.dumps({'data': [], 'msg': e.msg}, ensure_ascii=False)

            remits_map = {r.get('id'): r for r in remits}
            for record in records:
                if record['action_type'] == 3:
                    remit = remits_map.get(int(record.get('biz_sn', 0)), None)
                    record['bank_name'] = '--'
                    record['name'] = '--'
                    record['remitback_id'] = '--'
                    record['bank_brch'] = '--'
                    record['cardno'] = '--'
                    record['bank_code'] = '--'
                    if remit:
                        record['bank_name'] = remit.get('bank_name')
                        record['name'] = remit.get('name')
                        record['remitback_id'] = remit.get('remitback_id')
                        record['bank_brch'] = remit.get('bank_brch')
                        record['cardno'] = remit.get('cardno')
                        record['bank_code'] = remit.get('bank_code')
                        record['remitback_memo'] = remit.get('remitback_memo')

        records.sort(key=lambda t: t['biz_time'], reverse=True)
        return json.dumps({'data': records}, ensure_ascii=False)


class Account(BaseHandler):
    def GET(self):
        params = self.req.input()
        # 用户ID、手机号
        mobile = params.get('uid')
        if len(mobile) >= 11:
            users = UserPermissionHelper().get_users({'mobile': mobile})
            uid = users[0].get('uid') if len(users) > 0 else 0
        else:
            uid = int(mobile)

        # account 接口
        account_args = AccountQueryArgs()
        account_args.userids = [uid]
        try:
            account = thrift_callex(config.ACCOUNT2_SERVERS, Account2, 'account_query', account_args)
        except Exception, e:
            log.error('account error: %s' % e)

        accounts = [a.__dict__ for a in account]
        total = dict();
        total['account_type_id'] = 0  # 账户余额
        total['amt'] = sum([a.get('amt', 0) for a in accounts])
        total['frozen_amt'] = sum([a.get('frozen_amt', 0) for a in accounts])
        accounts.append(total)
        return json.dumps({'data': accounts}, ensure_ascii=False)


class AuditBlack(BaseHandler):
    # 读取列表
    @with_database('qf_mis')
    def GET(self):
        params = self.req.input()
        value = params.get('value')
        type = params.get('type')
        state = params.get('state')

        where = {}
        if value:
            where.update({'value': value})
        if type:
            where.update({'type': type})
        if state:
            where.update({'state': state})

        data = self.db.select(
            table='audit_black',
            fields=['id', 'type', 'value', 'state', 'utime'],
            where=where,
            other='order by utime desc limit 1000'
        )
        for d in data:
            if d['utime'] is not None:
                d['utime'] = d['utime'].strftime('%Y-%m-%d %H:%M:%S')

        return json.dumps({'data': data}, ensure_ascii=False)

    # 新增
    @with_database('qf_mis')
    def POST(self):
        json_format = self.req.environ.get('CONTENT_TYPE', '').lower().startswith('application/json')
        if not json_format:
            return json.dumps({'ok': False, 'msg': 'Need json input format'}, ensure_ascii=False)
        params = self.req.inputjson()
        type = params.get('type')
        state = params.get('state')
        values = params.get('values')

        duplicated = 0  # 重复未更新数量
        updated = 0  # 更新成功数量
        update_failed = 0  # 更新失败数量
        created = 0  # 新增数量

        insert_list = []

        # 类型为用户ID时，先取用户信息
        if int(type) == 99:
            for uid in values:
                try:
                    user = thrift_callex(config.APOLLO_SERVERS, ApolloServer,
                                         'findUserByid', int(uid))
                    profile = thrift_callex(config.APOLLO_SERVERS, ApolloServer,
                                            'findUserProfileByid', int(uid))
                except ApolloException, e:
                    error_msg = e.respmsg + '<br>' + 'ID：' + str(uid);
                    return json.dumps({'ok': False, 'msg': error_msg}, ensure_ascii=False)
                # 身份证
                insert_list.append({
                    'type': 2,
                    'state': state,
                    'value': user.idnumber
                })
                # 手机号
                insert_list.append({
                    'type': 3,
                    'state': state,
                    'value': user.mobile
                })
                # 银行卡
                insert_list.append({
                    'type': 4,
                    'state': state,
                    'value': profile.bankInfo.bankaccount
                })
        else:
            insert_list = [{'type': type, 'state': state, 'value': v}
                           for v in values]

        for x in insert_list:
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            x.update({'ctime': now_time})
            try:
                self.db.insert(table='audit_black', values=x)
                created += 1
            except Exception, e:  # insert 失败
                where = {'type': x['type'], 'value': x['value']}
                rows = self.db.select(table='audit_black',
                                      fields=['id', 'state'], where=where)
                old_state = rows[0]['state']
                old_id = rows[0]['id']
                if int(old_state) == int(x['state']):
                    duplicated += 1
                else:
                    try:
                        now_time = datetime.datetime.now().strftime(
                            '%Y-%m-%d %H:%M:%S')
                        self.db.update(
                            table='audit_black',
                            values={'state': x['state'], 'utime': now_time},
                            where={'id': old_id},
                        )
                        updated += 1
                    except Exception, e:
                        update_failed += 1

        ###########  create data test  ###########
        # re = 0
        # for i in range(3100, 7100):
        #     now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #     values = {'type': 3, 'value': str(i), 'state': 1, 'ctime': now_time}
        #     try:
        #         re = self.db.insert(table='audit_black', values=values)
        #     except:
        #         re += 1
        ###########  create data test  ###########

        msg = u'保存成功！\n\n'
        msg += '新增：' + str(created) + ' 条\n'
        msg += '忽略重复：' + str(duplicated) + ' 条\n'
        msg += '更新成功：' + str(updated) + ' 条\n'
        msg += '更新失败：' + str(update_failed) + ' 条\n'

        return json.dumps({'ok': True, 'msg': msg}, ensure_ascii=False)

    # 修改
    @with_database('qf_mis')
    def PUT(self):
        json_format = self.req.environ.get('CONTENT_TYPE', '').lower().startswith('application/json')
        if not json_format:
            return json.dumps({'ok': False, 'msg': 'Need json input format'}, ensure_ascii=False)
        params = self.req.inputjson()
        type = params.get('type')
        state = params.get('state')
        value = params.get('value')
        id = params.get('id')
        if not id:
            # error
            return json.dumps({'ok': False, 'msg': 'Need id'}, ensure_ascii=False)
        id = int(id)
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        where = {'id': id}
        values = {'type': type, 'value': value, 'state': state, 'utime': now_time}
        try:
            self.db.update(table='audit_black', values=values, where=where)
        except Exception, e:
            msg = '保存失败，已有相同数据！<br/><br/>' + str(e)
            return json.dumps({'ok': False, 'msg': msg}, ensure_ascii=False)

        return json.dumps({'ok': True, 'msg': '保存成功！'}, ensure_ascii=False)

    # 删除
    @with_database('qf_mis')
    def DELETE(self):
        params = self.req.input()
        id = params.get('id')
        if len(id) == 0:
            return json.dumps({'msg': '删除失败!'}, ensure_ascii=False)
        self.db.delete(table='audit_black', where={'id': id})
        return json.dumps({'ok': True, 'msg': '删除成功!'}, ensure_ascii=False)


class RegisterAuditList(BaseHandler):
    @with_database(['qf_audit','qf_mis'])
    def POST(self):
        params = self.req.input()
        draw = params.get('draw')
        start = params.get('start')
        length = params.get('length')

        manual_status = json.loads(params.get('manual_status'))
        uid_mobile = params.get('uid_mobile')
        groupid = params.get('gid')
        src = params.get('src')

        where = ['status=2']

        if uid_mobile:
            if len(uid_mobile) >= 11:
                users = UserPermissionHelper().get_users({'mobile': uid_mobile})
                uid = users[0].get('uid') if len(users) > 0 else 0
                w_str = "userid=%d" % uid
                where.append(w_str)
            else:
                uid = int(uid_mobile)
                w_str = "userid=%d" % uid
                where.append(w_str)
        if groupid != '-1':
            w_str = "groupid=%s" % groupid
            where.append(w_str)

        if manual_status[0] != '0':
            manual_status_arr = []
            for status in manual_status:
                manual_status_arr.append("manual_status=%s"%status)
            if len(manual_status_arr) > 1:
                manual_status_str = ' or '.join(manual_status_arr)
            else:
                manual_status_str = manual_status_arr[0]
            where.append(manual_status_str)
        where_str = ''
        if len(where) > 1:
            where_str = ' and '.join(where)
        else:
            where_str = where[0]
        try:
            sql = "select id,audit_uid,userid,groupid,src,status,manual_status,info,display from audit where %s order by id desc limit %s,%s"% (where_str,start,length)
            result = self.db['qf_audit'].query(sql)
            count_sql = "select count(*) as 'total' from audit where %s order by 'utime'" % (where_str)
            count = self.db['qf_audit'].query(count_sql)
            ret_arr = []
            recordsFiltered = count[0].get('total')
            recordsTotal = count[0].get('total')
            if len(result):
                for temp in result:
                    data = {}
                    info = json.loads(temp.get('info')) #info字段
                    aid = temp.get('id')
                    aid_str = str(aid)
                    data['id'] = aid_str
                    data['userid'] = temp.get('userid') #用户id
                    data['name'] = info.get('name') #签约实体
                    data['usertype'] = info.get('usertype') #商户类型
                    data['nickname'] = info.get('nickname') #收据名称
                    info_mcc = self.db['qf_mis'].select_one(table='tools_mcc', fields=['mcc_name'], where={'id':info.get('mcc',0)})
                    if info_mcc:
                        data['mcc'] = info_mcc.get('mcc_name','--')
                    else:
                        data['mcc'] = '--'
                    # data['mcc'] = info.get('mcc') #MCC
                    data['channel_name'] = info.get('channel_name') #渠道
                    data['salesmanname'] = info.get('salesmanname') #业务员
                    data['src'] = temp.get('src') #用户来源
                    data['manual_status'] = temp.get('manual_status') #审核状态
                    data['shoptype'] = info.get('shoptype') #门店类型
                    ret_arr.append(data)
        except Exception,e:
            log.error("audit_list_error %s" % (traceback.format_exc()))
            return json.dumps({'draw':draw,'recordsTotal':0,'recordsFiltered':0,'data':[],'error':'加载失败，请重试！'})
        ret = {'draw': draw, 'recordsTotal': recordsTotal, 'recordsFiltered': recordsFiltered, 'data': ret_arr}
        return json.dumps(ret)


class RegisterAuditDetail(BaseHandler):
    @with_database(['qf_audit','qf_mis','qf_user'])
    def GET(self):
        params = self.req.input()
        userid = params.get('userid','')
        aid = params.get('aid','')
        try:
            sql = ''
            if aid:
                sql = "select audit_uid,userid,groupid,src,status,manual_status,info,display,ctime,utime from audit where audit.id=%s" % (aid)
            else:
                # print userid
                sql = "select audit_uid,userid,groupid,src,status,manual_status,info,display,ctime,utime from audit where userid=%s order by utime desc limit 0,1" % (userid)
            result = self.db['qf_audit'].query(sql)
            data = {}
            if len(result):
                info = json.loads(result[0].get('info'))  # info字段
                if aid and result[0].get('manual_status') == 1:
                    self.db['qf_audit'].update(table='audit',values={'manual_status':2},where={'id':aid})
                # data['src'] = result[0].get('src')  # 用户来源
                # 基本信息
                data['usertype'] = info.get('usertype')  # 商户类型
                data['manual_status'] = result[0].get('manual_status')  # 审核状态
                data['ctime'] = result[0].get('ctime').strftime("%Y-%m-%d %H:%M:%S")
                data['utime'] = result[0].get('utime').strftime("%Y-%m-%d %H:%M:%S")
                data['name'] = info.get('name')  # 签约实体
                data['licensenumber'] = info.get('licensenumber') #营业执照号
                data['legalperson'] = info.get('legalperson') #法人代表
                data['idnumber'] = info.get('idnumber')  #身份证号
                # data['idnumbertime'] = info.get('idnumbertime')  # 身份证有效期
                data['cardstart'] = info.get('cardstart')
                data['cardend'] = info.get('cardend')
                data['piclist'] = info.get('piclist',[])
                # 是否失信被执行人
                data['dishonestyinfo'] = '否' if len(self.getDishonestyInfo(data.get('legalperson', ''), data.get('idnumber', ''))) == 0 else '是'
                data[''] = info.get('')  # 被授权人身份证号
                # 店铺信息
                data['src'] = info.get('src')  #用户来源
                # 店铺类型判断
                user_cate = self.db['qf_user'].select(table='user_category', fields=['cate_name', 'cate_code'],
                                                      where={'userid': userid, 'status': 1})
                isbigmerchant = False
                for i in user_cate:
                    if i['cate_code'] == 'bigmerchant':
                        # 大商户，总店
                        isbigmerchant = True
                if isbigmerchant:
                    # 是大商户则是总店，然后查询其他分店
                    data['shop_type'] = '总店'
                else:
                    # 不是大商户，则反查是否有总店，有总店则是分店，没有总店则是门店
                    relation = thrift_callex(config.APOLLO_SERVERS, ApolloServer, 'getUserReverseRelation',
                                             int(userid),
                                             'merchant')
                    if len(relation):
                        # 分店
                        data['shop_type'] = '分店'
                    else:
                        # 门店
                        data['shop_type'] = '门店'
                # data[''] = info.get('')  #门店类型
                data['otherid'] = info.get('otherid')  #其他身份
                data['mobile'] = info.get('mobile')  #手机号
                data['nickname'] = info.get('nickname')  #收据名称
                data['mcc'] = info.get('mcc')  # MCC
                data['shop_province'] = info.get('shop_province')  #经营所属省份
                data['shop_city'] = info.get('shop_city')  # 经营所属城市
                data['shop_address'] = info.get('shop_address')  #经营地址
                data['telephone'] = info.get('telephone')  #固定联系电话
                data['email'] = info.get('email')  #email
                # 收款账户信息
                data['banktype'] = info.get('banktype')  #清算银行类型
                data['bankuser'] = info.get('bankuser')  #银行账户名称
                data['account_province'] = info.get('account_province')  #开户行省份
                data['account_city'] = info.get('account_city')  #城市
                data['headbankname'] = info.get('headbankname')  #开户银行
                data['bankaccount'] = info.get('bankaccount')   #银行账号
                data['bankname'] = info.get('bankname')  #开户支行
                data['bankcode'] = info.get('bankcode')  #开户网点联行号
                data[''] = info.get('')  #银行预留手机号
                # 渠道信息
                data['channel_type'] = info.get('channel_type')  #渠道类型
                data['salesmanname'] = info.get('salesmanname')  #业务员姓名
                data['channel_name'] = info.get('channel_name')  #渠道名称
                data['channel_province'] = info.get('channel_province')  #渠道授权区域
                data['channel_city'] = info.get('channel_city')  #备注
                data['memo'] = info.get('memo')  #
                # 费率
                data['risk_level'] = info.get('risk_level')  # 用户风控等级
                data['fee_ratio'] = info.get('fee_ratio')  #借记卡费率
                data['credit_ratio'] = info.get('credit_ratio')  #信用卡费率
                data['tenpay_ratio'] = info.get('tenpay_ratio')  #微信费率
                data['alipay_ratio'] = info.get('alipay_ratio')  #支付宝费率
                data['qqpay_ratio'] = info.get('qqpay_ratio')  #QQ费率
                data['jdpay_ratio'] = info.get('jdpay_ratio')  #京东费率
                # data['usertags'] = json.loads(info.get('usertags'))
                data['usertags'] = info.get('usertags')
                # data['usertags'] = ['1','2']
                data['audit_record'] = info.get('audit_record')
                # MCC对应关系
                info_mcc = self.db['qf_mis'].select(table='tools_mcc', fields=['id','mcc_name'])
                data['mccs'] = info_mcc

                risklevel = self.getRiskLevel()

                data['risklevel'] = risklevel

                TONGDAOS = [CHNLCODE.CITIC,CHNLCODE.ZXWC,CHNLCODE.FUIOU,CHNLCODE.HUIYI,CHNLCODE.HYQK,CHNLCODE.WANGSHANG]

                client = ThriftClient(config.WEIFUTONG_SERVER, weifutong, framed=True)
                client.raise_except = True
                merchant_arr = []
                for tongdao in TONGDAOS:
                    merchant_dic = {}
                    merchant_number_d = client.call('query_mchntid_by_uids', [int(userid)], tongdao)

                    if merchant_number_d:
                        queryMeta = QueryMeta()
                        queryMeta.offset = 0
                        queryMeta.count = 1
                        queryMeta.orderby = 'utime desc'

                        addMchntQueryArg = AddMchntQueryArg()
                        addMchntQueryArg.query_meta = queryMeta
                        addMchntQueryArg.mchnt_id_list = merchant_number_d.values()[0] if merchant_number_d else []
                        record_ids_l = client.call('addmchnt_query', addMchntQueryArg)

                        addMchntRecord_d = client.call('addmchnt_get', record_ids_l)

                        merchant_dic['merchant_type'] = tongdao
                        merchant_dic['result'] = addMchntRecord_d.values()[0].state
                        merchant_dic['msg'] = addMchntRecord_d.values()[0].errmsg
                        merchant_arr.append(merchant_dic)

                data['merchant_results'] = merchant_arr
        except WeifutongError, e:
            log.error('WeifutongError error: %s' % e)
            return json.dumps({'code': 200, 'msg': '威富通失败', 'data': data})
        except Exception, e:
            log.error('audit_detail error: %s' % e)
            return json.dumps({'code': 0, 'msg': '收据获取失败', 'data': {}})

        return json.dumps({'code':200,'msg':'成功','data':data})

    def getRiskLevel(self):
        risklevel = [
                        {
                            'paychannel': 55,
                            'risklevel': 118,
                            'debitfee': 0.5,
                            'creditfee': 0.6,
                            'feelimit': 26,
                            'creditfeelimit': -1
                        },
                        {
                            'paychannel': 55,
                            'risklevel': 116,
                            'debitfee': 0.5,
                            'creditfee': 0.6,
                            'feelimit': 26,
                            'creditfeelimit': -1
                        },
                        {
                            'paychannel': 55,
                            'risklevel': 121,
                            'debitfee': 0.5,
                            'creditfee': 0.6,
                            'feelimit': 26,
                            'creditfeelimit': -1
                        },
                        {
                            'paychannel': 55,
                            'risklevel': 124,
                            'debitfee': 0.5,
                            'creditfee': 0.6,
                            'feelimit': 26,
                            'creditfeelimit': -1
                        },
                        {
                            'paychannel': 55,
                            'risklevel': 123,
                            'debitfee': 0.5,
                            'creditfee': 0.6,
                            'feelimit': 26,
                            'creditfeelimit': -1
                        },
                        {
                            'paychannel': 55,
                            'risklevel': 125,
                            'debitfee': 0.5,
                            'creditfee': 0.6,
                            'feelimit': 26,
                            'creditfeelimit': -1
                        },
                        {
                            'paychannel': 55,
                            'risklevel': 126,
                            'debitfee': 0.5,
                            'creditfee': 0.6,
                            'feelimit': 26,
                            'creditfeelimit': -1
                        },
                        {
                            'paychannel': 55,
                            'risklevel': 127,
                            'debitfee': 0.5,
                            'creditfee': 0.6,
                            'feelimit': 26,
                            'creditfeelimit': -1
                        },
                        {
                            'paychannel': 55,
                            'risklevel': 120,
                            'debitfee': 0.5,
                            'creditfee': 0.6,
                            'feelimit': 26,
                            'creditfeelimit': -1
                        },
                        {
                            'paychannel': 55,
                            'risklevel': 11,
                            'debitfee': 0.6,
                            'creditfee': 0.7,
                            'feelimit': 26,
                            'creditfeelimit': -1
                        },
                        {
                            'paychannel': 55,
                            'risklevel': 13,
                            'debitfee': 0.5,
                            'creditfee': 0.6,
                            'feelimit': 26,
                            'creditfeelimit': -1
                        }
                    ]
        return risklevel

    # 获取是否失信被执行人
    def getDishonestyInfo(self, name, idnumber):
        result = []
        if name and idnumber:
            urldata = {
                'resource_id': '6899',
                'query': '失信被执行人名单',
                'cardNum': idnumber,
                'iname': name,
                'areaName': '',
                'ie': 'utf-8',
                'oe': 'utf-8',
                'format': 'json',
                't': int(time.time()),
            }
            try:
                uri = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php'
                request = urllib2.Request(uri)
                request.add_header('Host', 'sp0.baidu.com')
                request.add_header('Referer', 'https://www.baidu.com/')
                request.add_header('User-Agent',
                                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36')
                res = urllib2.urlopen(request, urllib.urlencode(urldata), timeout=5).read()
                retjson = json.loads(res)
                result = retjson.get("data")[0].get("result") if retjson.get("data", None) else []
            except:
                log.info("获取数据异常 %s" % (traceback.format_exc()))
        return result


class auditDetailMore(BaseHandler):
    @with_database(['qf_mis','qf_core','qf_user','qf_risk_2','qf_audit'])
    def POST(self):
        params = self.req.input()
        draw = params.get('draw')
        start = params.get('start')
        length = params.get('length')

        recordsTotal = 0
        recordsFiltered = 0
        button_type = params.get('button_type')
        data_arr = []
        if button_type == '1':
            uid = params.get('uid',0)
            # uid = '11599'
            idnumber = params.get('other',0)
            # idnumber = '110101199009091550'
            # idnumber = '411421198710192105'
            # profile中获取到所有的userid
            # p_where = {'idnumber': idnumber,'user': ('<>', int(uid))}#apply表
            p_where = {'profile.idnumber': idnumber, 'profile.userid': ('<>', int(uid))}  # profile表
            # p_datas = self.db['qf_mis'].select(table='apply',fields=['user','state'],where=p_where)
            #
            # p_uids = []
            # p_userstates = []
            # for p_data in p_datas:
            #     p_uids.append(int(p_data['user']))
            #     p_userstates.append(p_data['state'])
            # p_idState_dic = dict(zip(p_uids,p_userstates))
            # if not len(p_uids):
            #     return json.dumps({'code':200,'msg':'成功','draw': draw, 'recordsTotal': 0, 'recordsFiltered': 0, 'data':data_arr})
            # a_where = {'userid':('in',p_uids)}

            datas = self.db['qf_core'].select_join(
                table1='profile',
                table2='auth_user',
                join_type='left',
                on={'profile.userid': 'auth_user.id'},
                fields=[
                    'profile.userid', 'profile.nickname', 'profile.mcc',
                    'profile.groupid', 'profile.user_state', 'profile.province', 'profile.city', 'auth_user.username',
                    '(SELECT auth_user.username FROM auth_user WHERE profile.groupid = auth_user.id) AS groupname',
                ],
                # where=a_where,
                where=p_where,
                other='order by profile.userid limit %s,%s' % (start,length)
            )
            #获取userid 通过userid到audit中查询其审核状态
            uidAuditStatusArr = []
            for d in datas:
                uidAuditStatusArr.append(int(d.get('userid',0)))
            #  audit中查询审核状态
            uidStatusData = []
            if len(uidAuditStatusArr) != 0:
                uidStatusData = self.db['qf_audit'].select(table='audit',fields=['userid','manual_status'],where={'userid':('in',uidAuditStatusArr)},other='order by utime desc')
            useridsArr = []
            statusArr = []
            # 将userid和manual_status整理成字典格式
            for data in uidStatusData:
                useridsArr.append(int(data.get('userid',0)))
                statusArr.append(data.get('manual_status',-1))
            useridStatusDic = dict(zip(useridsArr,statusArr))
            #获取MCC对应关系
            info_mcc = self.db['qf_mis'].select(table='tools_mcc', fields=['id','mcc_name'])
            keys_arr = []
            vals_arr = []
            for mcc in info_mcc:
                keys_arr.append(int(mcc['id']))
                vals_arr.append(mcc['mcc_name'])
            #生成MCC ID和name的对应字典
            mcc_dic = dict(zip(keys_arr,vals_arr))

            for d in datas:
                info = {}
                info['user'] = d.get('userid',0)
                info['nickname'] = d.get('nickname','--')
                info['mcc_name'] = mcc_dic.get(int(d.get('mcc','0') if d.get('mcc').isdigit() else 0),'--') if mcc_dic else '--'
                # 费率部分代码
                info['groupid'] = d.get('groupname','--')
                info['user_state'] = self.get_user_state_name(d.get('user_state','--'))
                # info['state'] = self.get_apply_state_name(p_idState_dic.get(int(d.get('userid',0)),'--'))
                info['state'] = useridStatusDic.get(int(d.get('userid',0)),-1)
                info['province'] = d.get('province','--') if d.get('province') else '--'
                info['city'] = d.get('city','--') if d.get('city') else '--'

                fee_query = FeeQueryArgs()
                fee_query.userid = [int(uid)]
                fee_query.trade_type = ['QF_BUSICD_WEIXIN_PRECREATE_H5', 'QF_BUSICD_ALIPAY_H5']
                fee_query.card_type = 5  # 卡类型   1.借记卡 2.信用卡 3.准贷记卡 4.储值卡 5.无卡
                fee_ratios = thrift_callex(config.ACCOUNT2_SERVERS, Account2,
                                           'fee_ratio_query', fee_query)
                for f in fee_ratios:
                    info[f.trade_type] = f.ratio

                data_arr.append(info)

                # 店铺类型判断
                # user_cate = self.db['qf_user'].select(table='user_category', fields=['cate_name', 'cate_code'],
                #                                       where={'userid': d.get('userid',0), 'status': 1})
                # isbigmerchant = False
                # for i in user_cate:
                #     if i['cate_code'] == 'bigmerchant':
                #         # 大商户，总店
                #         isbigmerchant = True
                #
                # if isbigmerchant:
                #     # 是大商户则是总店，然后查询其他分店
                #     info['shop_type'] = '总店'
                # else:
                #     # 不是大商户，则反查是否有总店，有总店则是分店，没有总店则是门店
                #     relation = thrift_callex(config.APOLLO_SERVERS, ApolloServer, 'getUserReverseRelation',
                #                              int(d.get('userid',0)),
                #                              'merchant')
                #     if len(relation):
                #         # 分店
                #         info['shop_type'] = '分店'
                #     else:
                #         # 门店
                #         info['shop_type'] = '门店'
            count = self.db['qf_core'].select_join(
                table1='profile',
                table2='auth_user',
                join_type='left',
                on={'profile.userid': 'auth_user.id'},
                fields=[
                    'count(*) as total'
                ],
                # where=a_where,
                where=p_where,
                other='order by profile.userid'
            )
            recordsTotal = count[0].get('total',0)
            recordsFiltered = count[0].get('total',0)
        if button_type == '2':
            uid = params.get('uid', 0)
            # uid = '11751'
            data_arr = []
            user_cate = self.db['qf_user'].select(table='user_category', fields=['cate_name', 'cate_code'],
                                                  where={'userid': uid, 'status': 1})
            isbigmerchant = False
            for i in user_cate:
                if i['cate_code'] == 'bigmerchant':
                    # 大商户，总店
                    isbigmerchant = True
            uids = []
            if isbigmerchant:
                # 是大商户则是总店，然后查询其他分店
                relation = thrift_callex(config.APOLLO_SERVERS, ApolloServer, 'getUserRelation', int(uid), 'merchant')
                if len(relation):
                    for i in relation:
                        if int(uid) != i.userid:
                            uids.append(i.userid)
            else:
                # 不是大商户，则反查是否有总店，有总店则是分店，没有总店则是门店
                relation = thrift_callex(config.APOLLO_SERVERS, ApolloServer, 'getUserReverseRelation', int(uid),
                                         'merchant')
                if len(relation):
                    # 分店
                    for i in relation:
                        if int(uid) != i.userid:
                            uids.append(i.userid)
                        # 查询到是总店，再获取总店下的分店
                        relation2 = thrift_callex(config.APOLLO_SERVERS, ApolloServer, 'getUserRelation', int(i.userid),
                                                  'merchant')
                        if len(relation2):
                            for i in relation2:
                                if int(uid) != i.userid:
                                    uids.append(i.userid)
                else:
                    # 门店
                    pass
            if not len(uids):
                return json.dumps({'code': 200, 'msg': '成功', 'draw': draw, 'recordsTotal': 0, 'recordsFiltered': 0, 'data': data_arr})
            uids = list(set(uids))
            # a_datas = self.db['qf_mis'].select(table='apply',fields=['user', 'state'],where={'user':('in',uids)})
            # a_uids = []
            # a_userstates = []
            # for a_data in a_datas:
            #     a_uids.append(int(a_data['user']))
            #     a_userstates.append(a_data['state'])
            # a_idstate_dic = dict(zip(a_uids,a_userstates))
            # if not len(a_uids):
            #     return json.dumps(
            #         {'code': 200, 'msg': '成功', 'draw': draw, 'recordsTotal': 0, 'recordsFiltered': 0, 'data': data_arr})
            #
            # where = {'userid': ('in', a_uids)}
            where = {'userid': ('in', uids)}
            datas = self.db['qf_core'].select_join(
                table1='profile',
                table2='auth_user',
                join_type='left',
                on={'profile.userid': 'auth_user.id'},
                fields=[
                    'profile.userid', 'profile.nickname', 'profile.mcc',
                    'profile.groupid', 'profile.user_state', 'profile.province', 'profile.city', 'auth_user.username',
                    '(SELECT auth_user.username FROM auth_user WHERE profile.groupid = auth_user.id) AS groupname',
                ],
                where=where,
                other='order by profile.userid limit %s,%s' % (start, length)
            )

            # 获取userid 通过userid到audit中查询其审核状态
            uidAuditStatusArr = []
            for d in datas:
                uidAuditStatusArr.append(int(d.get('userid', 0)))
            # audit中查询审核状态
            uidStatusData = []
            if len(uidAuditStatusArr) != 0:
                uidStatusData = self.db['qf_audit'].select(table='audit', fields=['userid', 'manual_status'],
                                                       where={'userid': ('in', uidAuditStatusArr)},
                                                       other='order by utime desc')
            useridsArr = []
            statusArr = []
            # 将userid和manual_status整理成字典格式
            for data in uidStatusData:
                useridsArr.append(int(data.get('userid', 0)))
                statusArr.append(data.get('manual_status', -1))
            useridStatusDic = dict(zip(useridsArr, statusArr))
            # 获取MCC对应关系
            info_mcc = self.db['qf_mis'].select(table='tools_mcc', fields=['id', 'mcc_name'])
            keys_arr = []
            vals_arr = []
            for mcc in info_mcc:
                keys_arr.append(int(mcc['id']))
                vals_arr.append(mcc['mcc_name'])
            # 生成MCC ID和name的对应字典
            mcc_dic = dict(zip(keys_arr, vals_arr))

            for d in datas:
                info = {}
                info['user'] = d.get('userid', 0)
                info['nickname'] = d.get('nickname', '--')

                info['mcc_name'] = mcc_dic.get(int(d.get('mcc','0') if d.get('mcc').isdigit() else 0),'--') if mcc_dic else '--'

                info['groupid'] = d.get('groupname', '--')
                info['user_state'] = self.get_user_state_name(d.get('user_state', '--'))
                # info['state'] = self.get_apply_state_name(a_idstate_dic.get(int(d.get('userid', 0)), '--'))
                info['state'] = useridStatusDic.get(int(d.get('userid', 0)), -1)
                info['province'] = d.get('province', '--') if d.get('province') else '--'
                info['city'] = d.get('city', '--') if d.get('city') else '--'

                fee_query = FeeQueryArgs()
                fee_query.userid = [int(uid)]
                fee_query.trade_type = ['QF_BUSICD_WEIXIN_PRECREATE_H5', 'QF_BUSICD_ALIPAY_H5']
                fee_query.card_type = 5  # 卡类型   1.借记卡 2.信用卡 3.准贷记卡 4.储值卡 5.无卡
                fee_ratios = thrift_callex(config.ACCOUNT2_SERVERS, Account2,
                                           'fee_ratio_query', fee_query)
                for f in fee_ratios:
                    info[f.trade_type] = f.ratio

                data_arr.append(info)

                # 店铺类型判断
                # user_cate = self.db['qf_user'].select(table='user_category', fields=['cate_name', 'cate_code'],
                #                                       where={'userid': d.get('userid', 0), 'status': 1})
                # isbigmerchant = False
                # for i in user_cate:
                #     if i['cate_code'] == 'bigmerchant':
                #         # 大商户，总店
                #         isbigmerchant = True
                #
                # if isbigmerchant:
                #     # 是大商户则是总店，然后查询其他分店
                #     info['shop_type'] = '总店'
                # else:
                #     # 不是大商户，则反查是否有总店，有总店则是分店，没有总店则是门店
                #     relation = thrift_callex(config.APOLLO_SERVERS, ApolloServer, 'getUserReverseRelation',
                #                              int(d.get('userid', 0)),
                #                              'merchant')
                #     if len(relation):
                #         # 分店
                #         info['shop_type'] = '分店'
                #     else:
                #         # 门店
                #         info['shop_type'] = '门店'
            count = self.db['qf_core'].select_join(
                table1='profile',
                table2='auth_user',
                join_type='left',
                on={'profile.userid': 'auth_user.id'},
                fields=[
                    'count(*) as total'
                ],
                where=where,
                other='order by profile.userid'
            )
            recordsTotal = count[0].get('total', 0)
            recordsFiltered = count[0].get('total', 0)

        if button_type == '3':
            uid = params.get('uid', 0)
            # uid = '11599'
            bankaccount = params.get('other')
            # bankaccount = '6212260200010534424'
            # apply中获取到所有的userid
            # p_where = {'bankaccount': bankaccount, 'user': ('<>', int(uid))}
            # p_datas = self.db['qf_mis'].select(table='apply', fields=['user', 'state'], where=p_where)
            p_where = {'profile.bankaccount': bankaccount, 'profile.userid': ('<>', int(uid))}  # profile表
            # p_uids = []
            # p_userstates = []
            # for p_data in p_datas:
            #     p_uids.append(int(p_data['user']))
            #     p_userstates.append(p_data['state'])
            # p_idState_dic = dict(zip(p_uids, p_userstates))
            # if not len(p_uids):
            #     return json.dumps({'code':200,'msg':'成功','draw': draw, 'recordsTotal': 0, 'recordsFiltered': 0, 'data':data_arr})
            # a_where = {'userid': ('in', p_uids)}

            datas = self.db['qf_core'].select_join(
                table1='profile',
                table2='auth_user',
                join_type='left',
                on={'profile.userid': 'auth_user.id'},
                fields=[
                    'profile.userid', 'profile.nickname', 'profile.mcc',
                    'profile.groupid', 'profile.user_state', 'profile.province', 'profile.city', 'auth_user.username',
                    '(SELECT auth_user.username FROM auth_user WHERE profile.groupid = auth_user.id) AS groupname',
                ],
                # where=a_where,
                where=p_where,
                other='order by profile.userid limit %s,%s' % (start, length)
            )

            # 获取userid 通过userid到audit中查询其审核状态
            uidAuditStatusArr = []
            for d in datas:
                uidAuditStatusArr.append(int(d.get('userid', 0)))
            # audit中查询审核状态
            uidStatusData = []
            if len(uidAuditStatusArr) != 0:
                uidStatusData = self.db['qf_audit'].select(table='audit', fields=['userid', 'manual_status'],
                                                       where={'userid': ('in', uidAuditStatusArr)},
                                                       other='order by utime desc')
            useridsArr = []
            statusArr = []
            # 将userid和manual_status整理成字典格式
            for data in uidStatusData:
                useridsArr.append(int(data.get('userid', 0)))
                statusArr.append(data.get('manual_status', -1))
            useridStatusDic = dict(zip(useridsArr, statusArr))
            # 获取MCC对应关系
            info_mcc = self.db['qf_mis'].select(table='tools_mcc', fields=['id', 'mcc_name'])
            keys_arr = []
            vals_arr = []
            for mcc in info_mcc:
                keys_arr.append(int(mcc['id']))
                vals_arr.append(mcc['mcc_name'])
            # 生成MCC ID和name的对应字典
            mcc_dic = dict(zip(keys_arr, vals_arr))

            for d in datas:
                info = {}
                info['user'] = d.get('userid', 0)
                info['nickname'] = d.get('nickname', '--')
                print d.get('mcc','')
                print '^^^^^^'
                print d
                info['mcc_name'] = mcc_dic.get(int(d.get('mcc','0') if (d.get('mcc','').isdigit() if d.get('mcc')!=None else 0) else 0),'--') if mcc_dic else '--'
                # 费率部分代码，后续补上
                info['groupid'] = d.get('groupname', '--')
                info['user_state'] = self.get_user_state_name(d.get('user_state', '--'))
                # info['state'] = self.get_apply_state_name(p_idState_dic.get(int(d.get('userid', 0)), '--'))
                info['state'] = useridStatusDic.get(int(d.get('userid', 0)), -1)
                info['province'] = d.get('province', '--') if d.get('province') else '--'
                info['city'] = d.get('city', '--') if d.get('city') else '--'

                fee_query = FeeQueryArgs()
                fee_query.userid = [int(uid)]
                fee_query.trade_type = ['QF_BUSICD_WEIXIN_PRECREATE_H5', 'QF_BUSICD_ALIPAY_H5']
                fee_query.card_type = 5  # 卡类型   1.借记卡 2.信用卡 3.准贷记卡 4.储值卡 5.无卡
                fee_ratios = thrift_callex(config.ACCOUNT2_SERVERS, Account2,
                                           'fee_ratio_query', fee_query)
                for f in fee_ratios:
                    info[f.trade_type] = f.ratio

                data_arr.append(info)

                # 店铺类型判断
                # user_cate = self.db['qf_user'].select(table='user_category', fields=['cate_name', 'cate_code'],
                #                                       where={'userid': d.get('userid', 0), 'status': 1})
                # isbigmerchant = False
                # for i in user_cate:
                #     if i['cate_code'] == 'bigmerchant':
                #         # 大商户，总店
                #         isbigmerchant = True
                #
                # if isbigmerchant:
                #     # 是大商户则是总店，然后查询其他分店
                #     info['shop_type'] = '总店'
                # else:
                #     # 不是大商户，则反查是否有总店，有总店则是分店，没有总店则是门店
                #     relation = thrift_callex(config.APOLLO_SERVERS, ApolloServer, 'getUserReverseRelation',
                #                              int(d.get('userid', 0)),
                #                              'merchant')
                #     if len(relation):
                #         # 分店
                #         info['shop_type'] = '分店'
                #     else:
                #         # 门店
                #         info['shop_type'] = '门店'
            count = self.db['qf_core'].select_join(
                table1='profile',
                table2='auth_user',
                join_type='left',
                on={'profile.userid': 'auth_user.id'},
                fields=[
                    'count(*) as total'
                ],
                where=p_where,
                other='order by profile.userid'
            )
            recordsTotal = count[0].get('total', 0)
            recordsFiltered = count[0].get('total', 0)
        return json.dumps({'code':200,'msg':'成功','draw': draw, 'recordsTotal': recordsTotal, 'recordsFiltered': recordsFiltered, 'data':data_arr})

    # 获取用户状态名称
    def get_user_state_name(self, state):
        if state == 1:
            return '新建'
        elif state == 2:
            return '通过审核, 未设备激活'
        elif state == 3:
            return '已设备激活，未业务激活'
        elif state == 4:
            return '已业务激活，正常'
        elif state == 5:
            return '呆户'
        elif state == 6:
            return '临时封禁，黑名单'
        elif state == 7:
            return '永久封禁'
        elif state == 8:
            return '用户主动注销'
        elif state == 9:
            return '临时停用'
        else:
            return '无'

    # 获取审核状态名称
    def get_apply_state_name(self, state):
        if state == 0:
            return '等待基本信息'
        if state == 1:
            return '等待上传凭证'
        elif state == 3:
            return '审核中'
        elif state == 4:
            return '等待审核'
        elif state == 5:
            return '审核通过'
        elif state == 6:
            return '自动审核失败，待人工审核'
        elif state == 7:
            return '审核拒绝'
        elif state == 8:
            return '审核失败'
        elif state == 9:
            return '等待复审'
        elif state == 10:
            return '自动审核成功'
        else:
            return '无'


class auditResult(BaseHandler):
    @with_database(['qf_audit'])
    def POST(self):
        params = self.req.input()
        userid = params.get('userid')
        aid = params.get('aid')
        result_type = params.get('result_type')
        usertype = params.get('usertype')
        name = params.get('name')
        licensenumber = params.get('licensenumber')
        legalperson = params.get('legalperson')
        idnumber = params.get('idnumber')
        cardstart = params.get('cardstart')
        cardend = params.get('cardend')
        mobile = params.get('mobile')
        nickname = params.get('nickname')
        mcc = params.get('mcc')
        shop_province = params.get('shop_province')
        shop_city = params.get('shop_city')
        shop_address = params.get('shop_address')
        telephone = params.get('telephone')
        email = params.get('email')
        banktype = params.get('banktype')
        bankuser = params.get('bankuser')
        account_province = params.get('account_province')
        account_city = params.get('account_city')
        headbankname = params.get('headbankname')
        bankaccount = params.get('bankaccount')
        bankname = params.get('bankname')
        bankcode = params.get('bankcode')
        risk_level = params.get('risk_level')
        audit_memo = params.get('audit_memo')
        usertags = params.get('usertags')

        try:
            sql = "select audit_uid,userid,groupid,src,manual_status,status,manual_status,info,display from audit where id=%s" % (aid)
            result = self.db['qf_audit'].query(sql)
            ori_usertype = ''
            ori_name = ''
            ori_licensenumber = ''
            ori_legalperson = ''
            ori_idnumber = ''
            ori_cardstart = ''#身份证开始日期
            ori_cardend = ''#身份证结束日期
            ori_mobile = ''
            ori_nickname = ''
            ori_mcc = ''
            ori_shop_province = ''
            ori_shop_city = ''
            ori_shop_address = ''
            ori_telephone = ''
            ori_email = ''
            ori_banktype = ''
            ori_bankuser = ''
            ori_account_province = ''
            ori_account_city = ''
            ori_headbankname = ''
            ori_bankaccount = ''
            ori_bankname = ''
            ori_bankcode = ''
            ori_select_risk_level = ''
            # ori_usertags = ''
            if len(result):
                if result[0].get('manual_status') == 4:
                    return json.dumps({'code': 0, 'msg': '该用户已经通过审核', 'data': {}})
                info = json.loads(result[0].get('info'))  # info字段
                ori_usertype = info.get('usertype')
                ori_name = info.get('name')
                ori_licensenumber = info.get('licensenumber')
                ori_legalperson = info.get('legalperson')
                ori_idnumber = info.get('idnumber')
                ori_cardstart = info.get('cardstart')
                ori_cardend = info.get('cardend')

                ori_mobile = info.get('mobile')
                ori_nickname = info.get('nickname')
                ori_mcc = info.get('mcc')
                ori_shop_province = info.get('shop_province')
                ori_shop_city = info.get('shop_city')
                ori_shop_address = info.get('shop_address')
                ori_telephone = info.get('telephone')
                ori_email = info.get('email')
                ori_banktype = info.get('banktype')
                ori_bankuser = info.get('bankuser')
                ori_account_province = info.get('account_province')
                ori_account_city = info.get('account_city')
                ori_headbankname = info.get('headbankname')
                ori_bankaccount = info.get('bankaccount')
                ori_bankname = info.get('bankname')
                ori_bankcode = info.get('bankcode')
                ori_risk_level = info.get('risk_level')

            modify = {}
            if usertype != ori_usertype:
                modify["usertype"] = usertype
            if name != ori_name:
                modify["name"] = name
            if licensenumber != ori_licensenumber:
                modify["licensenumber"] = licensenumber
            if legalperson != ori_legalperson:
                modify["legalperson"] = legalperson
            if idnumber != ori_idnumber:
                modify["idnumber"] = idnumber
            if cardstart != ori_cardstart:
                modify["cardstart"] = cardstart
            if cardend != ori_cardend:
                modify["cardend"] = cardend
            if mobile != ori_mobile:
                modify["mobile"] = mobile
            if nickname != ori_nickname:
                modify["nickname"] = nickname
            if mcc != ori_mcc:
                modify["mcc"] = mcc
            if shop_province != ori_shop_province:
                modify["shop_province"] = shop_province
            if shop_city != ori_shop_city:
                modify["shop_city"] = shop_city
            if shop_address != ori_shop_address:
                modify["shop_address"] = shop_address
            if telephone != ori_telephone:
                modify["telephone"] = telephone
            if email != ori_email:
                modify["email"] = email
            if banktype != ori_banktype:
                modify["banktype"] = banktype
            if bankuser != ori_bankuser:
                modify["bankuser"] = bankuser
            if account_province != ori_account_province:
                modify["account_province"] = account_province
            if account_city != ori_account_city:
                modify["account_city"] = account_city
            if headbankname != ori_headbankname:
                modify["headbankname"] = headbankname
            if bankaccount != ori_bankaccount:
                modify["bankaccount"] = bankaccount
            if bankname != ori_bankname:
                modify["bankname"] = bankname
            if bankcode != ori_bankcode:
                modify["bankcode"] = bankcode
            # if audit_memo != ori_audit_memo:
            #     modify["audit_memo"] = audit_memo
            if risk_level != ori_risk_level:
                modify["risk_level"] = risk_level
            modify["usertags"] = usertags
            modify["audit_record"] = {"operator":self.get_cookie('uname'),"audit_result":result_type,"audit_time":time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),"audit_memo":audit_memo}

        except:
            log.error("audit_data_get_error %s" % (traceback.format_exc()))
            return json.dumps({'code': 0, 'msg': '获取数据失败', 'data': {}})

        try:
            client = ThriftClient(config.AUDIT_SERVER, AuditServer,framed=False)
            client.raise_except = True
            re = client.call('audit_api', id=str(aid), type=str(result_type), modify=str(json.dumps(modify,ensure_ascii=False)))
        except:
            log.error("audit_error %s" % (traceback.format_exc()))
            return json.dumps({'code': 0, 'msg': '操作失败', 'data': {}})
        return json.dumps({'code':200,'msg':'操作成功','data':{}})


class SMSRecord(BaseHandler):
    @with_database('qf_sms')
    def GET(self):
        params = self.req.input()

        draw = params.get('draw')
        start = params.get('start')
        length = params.get('length')

        month = params.get('month')
        phone = params.get('phone')
        sms_type = params.get('sms_type')
        where = {}
        if phone:
            where.update({'phone': phone})
        if sms_type:
            where.update({'sms_type': sms_type})
        try:
            table = 'sms_record_' + month
            sql = 'select count(id) from ' + table
            count = self.db.query(sql=sql)
            records_total = records_filtered = count[0]['count(id)']
            other = 'order by add_time desc limit %s,%s' % (start, length)
            data = self.db.select(
                table=table,
                where=where,
                other=other,
            )
        except Exception, e:
            log.error('record error: %s' % e)
            return json.dumps({'data': [], 'msg': str(e)}, ensure_ascii=False)
        for x in data:
            x['add_time'] = x['add_time'].strftime('%Y-%m-%d %H:%M:%S')

        return json.dumps({
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }, ensure_ascii=False)


class SMSTemplate(BaseHandler):
    @with_database('qf_mis')
    def GET(self):
        params = self.req.input()

        id = params.get('id')
        if id:
            data = self.db.select_one(
                table='sms_sms_template',
                where={'id': id},
            )
            return json.dumps({'data': data}, ensure_ascii=False)

        draw = params.get('draw')
        start = params.get('start')
        length = params.get('length')

        name = params.get('name')
        state = params.get('state')
        where = {}
        if name:
            where.update({'name': ('like', '%' + name + '%')})
        if state:
            where.update({'state': state})

        table = 'sms_sms_template'
        sql = 'select count(id) from ' + table
        count = self.db.query(sql=sql)
        records_total = records_filtered = count[0]['count(id)']
        other = 'order by id desc limit %s,%s' % (start, length)
        data = self.db.select(
            table=table,
            where=where,
            other=other,
        )

        return json.dumps({
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }, ensure_ascii=False)

    @with_database('qf_mis')
    def POST(self):
        json_format = self.req.environ.get('CONTENT_TYPE', '').lower().startswith('application/json')
        if not json_format:
            return json.dumps({'ok': False, 'msg': 'Need json input format'}, ensure_ascii=False)
        params = self.req.inputjson()
        type = params.get('type')
        state = params.get('state')
        name = params.get('name')
        content = params.get('content')

        values = {'type': type, 'content': content, 'state': state,
                  'name': name}
        try:
            self.db.insert(table='sms_sms_template', values=values)
        except Exception, e:
            msg = '保存失败，请检查输入！<br/><br/>' + str(e)
            return json.dumps({'ok': False, 'msg': msg}, ensure_ascii=False)

        return json.dumps({'ok': True, 'msg': '保存成功！'}, ensure_ascii=False)

    @with_database('qf_mis')
    def PUT(self):
        json_format = self.req.environ.get('CONTENT_TYPE', '').lower().startswith('application/json')
        if not json_format:
            return json.dumps({'ok': False, 'msg': 'Need json input format'}, ensure_ascii=False)
        params = self.req.inputjson()
        type = params.get('type')
        state = params.get('state')
        name = params.get('name')
        content = params.get('content')
        id = params.get('id')
        if not id:
            # error
            return json.dumps({'ok': False, 'msg': 'Need id'},
                              ensure_ascii=False)
        id = int(id)
        where = {'id': id}
        values = {'type': type, 'content': content, 'state': state, 'name': name}
        try:
            self.db.update(table='sms_sms_template', values=values, where=where)
        except Exception, e:
            msg = '保存失败，请检查输入！<br/><br/>' + str(e)
            return json.dumps({'ok': False, 'msg': msg}, ensure_ascii=False)

        return json.dumps({'ok': True, 'msg': '保存成功！'}, ensure_ascii=False)
