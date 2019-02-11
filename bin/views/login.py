# vim: set ts=4 et sw=4 sts=4 fileencoding=utf-8 :

import os
import sys
import logging
import time
import traceback
import datetime
from qfcommon.web import core
from qfcommon.web import template
from qfcommon.base.dbpool import with_database
from qfcommon.base.tools import thrift_callex
from qfcommon.thriftclient.apollo import ApolloServer
from qfcommon.qfpay.apollouser import ApolloUser
# from qfcommon.base.qfresponse import QFRET,error,success
from tools import redis_pool,checkPassword,operationRecord
import config

unicode_to_utf8 = lambda s: s.encode('utf-8') if isinstance(s, unicode) else s
log = logging.getLogger()

class Pub_Method(object):
    # 验证登录是否成功，返回元组，成功返回商户userid， 不成功抛出相应错误
    @classmethod
    def get_login_status(cls, username, password):
        r = None
        try:
            r = thrift_callex(config.APOLLO_SERVERS, ApolloServer, 'checkUsername',
                              username, password)
            msg = '糟糕，密码错误！' if not r else '登录成功！'
        except:
            log.debug('apollo error:%s' % traceback.format_exc())
            msg = '糟糕，密码错误！'

        return r, msg

    # 获取用户信息，判断是否有该用户,返回元组，第一个为user对象，第二个为msg
    @classmethod
    def get_user_info(cls, username):
        user = None
        try:
            user = thrift_callex(config.APOLLO_SERVERS, ApolloServer, 'findUserByMobile',
                                 username)
            msg = '账号未注册，请注册钱方好近商户' if not user else '已注册！'
        except:
            log.debug('apollo error:%s' % traceback.format_exc())
            msg = '账号未注册，请注册钱方好近商户'

        return user, msg

    # 获取该手机号的权限，返回的元组，元组中第一个元素为列表，第二个为msg
    @classmethod
    def get_userpermissionrole(cls, uid):
        roles = []
        try:
            roles = thrift_callex(config.APOLLO_SERVERS, ApolloServer, 'getUserPermissionRole',
                                  uid)
            msg = '账号未开通权限，请联系管理员！' if not roles else '已开通！'
        except:
            log.debug('apollo error:%s' % traceback.format_exc())
            msg = '账号未开通权限，请联系管理员！'

        return roles, msg

    #根据uid获取用户信息
    @classmethod
    def get_username(self,uid):
        user = None
        try:
            user = thrift_callex(config.APOLLO_SERVERS, ApolloServer, 'findUserByid',
                                  uid)
            msg = '用户信息获取失败！' if not user else '用户信息获取成功！'
        except:
            log.debug('apollo error:%s' % traceback.format_exc())
            msg = '用户信息获取失败！'

        return user, msg


class Login_safe(core.Handler):
    # 设置session
    def _set_session(self, uid, username, expire):
        user = ApolloUser(uid, expire=expire)
        user.ses['username'] = username
        log.debug('user_info[0].name:%s', username)
        user.ses['uid'] = uid
        user.login(uid)
        user.ses.save()
        return user.ses._sesid
    def GET(self):
        sesid = self._set_session(uid=11754, username='李巍', expire=86400 * 10)
        self.set_cookie(config.sesskey, sesid, **config.COOKIE_CONFIG)
        user = ApolloUser(sessionid=sesid)
        uname = '李巍'
        self.set_cookie('uname', unicode_to_utf8(uname), **config.COOKIE_CONFIG)
        self.set_cookie('uid', 11754, **config.COOKIE_CONFIG)
        ret = {'success': 1, 'msg': uname}
        return self.redirect('/index')

#登录
class Login(core.Handler):
    @with_database(['qf_solar'])
    def GET(self):
        ret = {}
        # operate_dict = {'username':None, 'operation_type':'删除', 'operation_code':'ADD_SING', 'description':None}
        # self.operate(operate_dict)
        self.write(template.render('user_login.html',data=ret))

    @operationRecord
    @with_database(['qf_solar'])
    def operate(self,values):
        return True

    def POST(self):
        data = self.req.input()
        username = data['username']
        password = data['password']
        # 获取用户，user[0]有数据则有该用户
        # user = self._get_user_info(username)
        user = Pub_Method.get_user_info(username)
        if not user[0]:
            ret = {'success': 0, 'username': username, 'msg': user[1]}
            return self.write(template.render('user_login.html',data=ret))

        count = 0 if not redis_pool.get(username) else int(redis_pool.get(username))
        if count >= 5:
            ret = {'success': 0, 'username': username, 'msg': '抱歉，您输入的密码错误已达到5次，账号处于锁定状态，请联系管理员！'}
            return self.write(template.render('user_login.html', data=ret))

        # 验证登录是否成功，result[0]为0的话，登录失败，否则登录成功
        # result = self._get_login_status(username,password)
        result = Pub_Method.get_login_status(username, password)

        if not result[0]:
            count = redis_pool.get(username)
            # 获取当前时间，仅仅获取到年月日
            now_time = datetime.datetime.now().strftime('%Y-%m-%d')
            # 得到次日凌晨时间
            when = datetime.datetime.strptime(now_time, '%Y-%m-%d') + datetime.timedelta(days=1)
            if not count:
                count = 1
                redis_pool.set(username, count)
                redis_pool.expireat(username, when)
            else:
                count = int(count) + 1
                redis_pool.set(username, count)
                redis_pool.expireat(username, when)
            ret = {}
            if count >= 5:
                ret = {'success': 0, 'username': username, 'msg': '抱歉，您输入的密码错误已达到5次，账号处于锁定状态，请联系管理员！'}
            else:
                ret = {'success': 0, 'username': username, 'msg': result[1]+'还有'+str(5-count)+'次机会！'}
            return self.write(template.render('user_login.html', data=ret))

        else:
            # 获取该手机号用户的权限，通过uid，有权限方可继续登录，返回的元组，元组中第一个元素为列表，第二个为msg
            # roles = self._get_userpermissionrole(result[0])
            roles = Pub_Method.get_userpermissionrole(result[0])
            if len(roles[0]) == 0:
                ret = {'success':0,'username':username,'msg':roles[1]}
                return self.write(template.render('user_login.html',data=ret))

            # 登录成功后验证密码
            pwd_ok = checkPassword(password)

            if pwd_ok:
                user_info = Pub_Method.get_username(result[0])
                if not user_info[0]:
                    ret = {'success': 0, 'username': username, 'msg': '用户信息获取失败'}
                    return self.write(template.render('user_login.html', data=ret))
                #86400*30

                sesid = self._set_session(uid=result[0],username=user_info[0].name,expire=86400*1)
                self.set_cookie(config.sesskey, sesid, **config.COOKIE_CONFIG)
                user = ApolloUser(sessionid=sesid)
                uname = user.ses['username']
                self.set_cookie('uname', unicode_to_utf8(uname), **config.COOKIE_CONFIG)
                self.set_cookie('uid', result[0], **config.COOKIE_CONFIG)
                ret = {'success': 1, 'msg': result[1]}
                return self.redirect('/index')
            else:
                ret = {'success': 0, 'username': username, 'msg': '您的密码存在风险，请通过"钱方好近商户app"修改', 'tourl': '/reset_pwd',
                       'toword': '点击此处去修改'}
                return self.write(template.render('user_login.html', data=ret))

    # 设置session
    def _set_session(self,uid,username,expire):
        user = ApolloUser(uid, expire=expire)
        user.ses['username'] = username
        log.debug('user_info[0].name:%s', username)
        user.ses['uid'] = uid
        user.login(uid)
        user.ses.save()
        return user.ses._sesid



#重置密码
class Reset_PWD(core.Handler):

    def GET(self):
        ret = {}
        return self.write(template.render('reset_pwd.html', data=ret))

    def POST(self):
        data = self.req.input()
        username = data['username']
        password_old = data['password_old']
        password_new = data['password_new']
        # 获取用户，user[0]有数据则有该用户
        user = Pub_Method.get_user_info(username)
        if not user[0]:
            ret = {'success': 0, 'username': username, 'msg': user[1]}
            return self.write(template.render('reset_pwd.html', data=ret))

        # 验证登录是否成功，result[0]为0的话，登录失败，否则登录成功,重置密码需要先验证登录名和之前的密码是否相等
        result = Pub_Method.get_login_status(username, password_old)
        if not result[0]:
            ret = {'success': 0, 'username': username, 'msg': '原始密码输入错误'}
            return self.write(template.render('reset_pwd.html', data=ret))
        else:
            # 用户名和原密码验证
            pwd_ok = checkPassword(password_new)
            if pwd_ok:
                # 用户名和原密码验证成功后判断新老密码是否相等
                if password_new == password_old:
                    ret = {'success': 0, 'username': username, 'msg': '您的密码与原密码相同，请设置新的密码！'}
                    return self.write(template.render('reset_pwd.html', data=ret))
                else:
                    #pass
                    #调用apollo更改密码
                    userid = result[0]
                    result_reset = self._reset_password(userid,password_new)
                    if result_reset[0] == 0:
                        ret = {'success': 0, 'username': username, 'msg': '您的密码修改成功','tourl':'/login','toword':'点击此处返回登录页'}
                        return self.write(template.render('reset_pwd.html', data=ret))
                    else:
                        ret = {'success': 0, 'username': username, 'msg': '您的密码修改失败'}
                        return self.write(template.render('reset_pwd.html', data=ret))
            else:
                ret = {'success': 0, 'username': username, 'msg': '抱歉，您的密码不符合平台要求，请设置8位包含大小写字母，数字，字符中任意两种组合的密码！'}
                return self.write(template.render('reset_pwd.html', data=ret))

    # 重置密码函数
    def _reset_password(self,userid,password):
        r = -1
        try:
            r = thrift_callex(config.APOLLO_SERVERS, ApolloServer, 'changePwd',
                              userid, password)
            msg = '糟糕，密码错误！' if not r else '登录成功！'
        except:
            log.debug('apollo error:%s' % traceback.format_exc())
            msg = '糟糕，密码错误！'

        return r, msg

class LoginOut(core.Handler):
    def GET(self):
        uid = self.get_cookie('uid')
        sessionid = self.get_cookie(config.sesskey)
        user = ApolloUser(uid,sessionid)
        user.logout()
        self.resp.del_cookie(config.sesskey)
        self.resp.del_cookie('uname')
        self.resp.del_cookie('uid')
        return self.redirect('/login')


