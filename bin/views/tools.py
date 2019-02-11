#coding=utf-8
import redis
import config
import re
import datetime
import traceback
import logging

from qfcommon.base.dbpool import with_database
from qfcommon.qfpay.apollouser import ApolloUser
from qfcommon.server.client import ThriftClient
from qfcommon.base.qfresponse import success, error, QFRET

from utils.excepts import SLAException

log = logging.getLogger()

USER_DB = ['qf_solar', 'qf_user']

#建立redis连接
redis_conf = config.CACHE_CONF['redis_conf']
redis_pool = redis.Redis(host=redis_conf['host'],port=redis_conf['port'],password=redis_conf['password'])

#检查长度
def checklen(pwd):
    return len(pwd) >= 8

#检查大写
def checkContainUpper(pwd):
    pattern = re.compile('[A-Z]+')
    match = pattern.findall(pwd)

    if match:
        return True
    else:
        return False

#检查数字
def checkContainNum(pwd):
    pattern = re.compile('[0-9]+')
    match = pattern.findall(pwd)

    if match:
        return True
    else:
        return False

#检查小写
def checkContainLower(pwd):
    pattern = re.compile('[a-z]+')
    match = pattern.findall(pwd)

    if match:
        return True
    else:
        return False

#检查符号
def checkSymbol(pwd):
    pattern = re.compile('([^a-z0-9A-Z])+')
    match = pattern.findall(pwd)

    if match:
        return True
    else:
        return False

#综合调用
def checkPassword(pwd):
    # 判断密码长度是否合法
    lenOK = checklen(pwd)
    # 判断是否包含大写字母
    upperOK = checkContainUpper(pwd)
    # 判断是否包含小写字母
    lowerOK = checkContainLower(pwd)
    # 判断是否包含数字
    numOK = checkContainNum(pwd)
    # 判断是否包含符号
    symbolOK = checkSymbol(pwd)

    if not lenOK:
        return False
    result = int(upperOK) + int(lowerOK) + int(numOK) + int(symbolOK)
    if result >= 2:
        return True
    else:
        return False

#values {'username':value2,'operation_type':value3,'operation_code':value4,'description':value5}
#操作日志的装饰器
def operationRecord(func):
    def record(self,values):
        if func:
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            values['ctime'] = now_time
            sesid = self.get_cookie('sessionid')
            user = ApolloUser(sessionid=sesid)
            values['operator'] = user.ses['username']
            try:
                self.db['qf_solar'].insert(table='operation_table',values=values)
            except Exception,e:
                log.debug('mysql insert error: %s' % traceback.format_exc())
        return func
    return record

#验证是否登录的装饰器
def checkIsLogin(func):
    def isLogin(self):
        sesid = self.get_cookie(config.sesskey)
        user = ApolloUser(sessionid=sesid)
        if user.is_login():
            log.debug('已登录')
            return func(self)
        else:
            log.debug('未登录')
            return self.redirect('/login')
    return isLogin

def raise_excp(info='参数错误'):
    def _(func):
        def __(self, *args, **kwargs):
            try:
                # 错误信息
                module_name = getattr(self, '__module__', '')
                class_name  = getattr(getattr(self, '__class__', ''), '__name__', '')
                func_name   = getattr(func, '__name__', '')
                errinfo = '%s %s %s' % (module_name, class_name, func_name)

                return func(self, *args, **kwargs)
            except SLAException, e:
                log.warn('[%s] error: %s' % (errinfo, e))
                return self.write(error(e.errcode, respmsg=e.errmsg))
            except:
                log.warn('[%s] error:%s' % (errinfo, traceback.format_exc()))
                return self.write(error(QFRET.PARAMERR, respmsg=info))
        return __
    return _

def thrift_callex_framed(server_config, mod, func, *args, **kwargs):
    client = ThriftClient(server_config, mod, framed=True)
    client.raise_except = True
    return client.call(func, *args, **kwargs)
