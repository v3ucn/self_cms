# vim: set ts=4 et sw=4 sts=4 fileencoding=utf-8 :

import os
import sys
from webconfig import *

# 服务地址
HOST = '0.0.0.0'

# 服务端口
PORT = 6200

# 调试模式: True/False
# 生产环境必须为False
DEBUG = False

# 日志文件配置
LOGFILE = os.path.join(HOME, '../log/solar.log')

# 数据库配置
DATABASE = {
    'qf_core': {
        'engine': 'mysql',
        'db': 'qf_core',
        'host': '172.100.101.107',
        'port': 3306,
        'user': 'qf',
        'passwd': '123456',
        'charset': 'utf8',
        'conn': 16,
    },
    'qf_user': {
        'engine': 'mysql',
        'db': 'qf_user',
        'host': '172.100.101.107',
        'port': 3306,
        'user': 'qf',
        'passwd': '123456',
        'charset': 'utf8',
        'conn': 16,
    },
    'qf_solar': {
        'engine': 'mysql',
        'db': 'qf_solar',
        'host': '172.100.101.107',
        'port': 3306,
        'user': 'qf',
        'passwd': '123456',
        'charset': 'utf8',
        'conn': 16,
    },
    'qf_mis': {
        'engine': 'mysql',
        'db': 'qf_mis',
        'host': '172.100.101.107',
        'port': 3306,
        'user': 'qf',
        'passwd': '123456',
        'charset': 'utf8',
        'conn': 16,
    },
    'qf_qudao': {
        'engine': 'mysql',
        'db': 'qf_qudao',
        'host': '172.100.101.107',
        'port': 3306,
        'user': 'qf',
        'passwd': '123456',
        'charset': 'utf8',
        'conn': 16,
    },
    'qmm_wx': {
        'engine': 'mysql',
        'db': 'qmm_wx',
        'host': '172.100.101.107',
        'port': 3306,
        'user': 'qf',
        'passwd': '123456',
        'charset': 'utf8',
        'conn': 16,
    },
    'honey_manage': {
        'engine': 'mysql',
        'db': 'qmm_wx',
        'host': '172.100.101.107',
        'port': 3306,
        'user': 'qf',
        'passwd': '123456',
        'charset': 'utf8',
        'conn': 16,
    },
    'qf_risk_2': {
        'engine': 'mysql',
        'db': 'qf_risk_2',
        'host': '172.100.101.107',
        'port': 3306,
        'user': 'qf',
        'passwd': '123456',
        'charset': 'utf8',
        'conn': 16,
    },
    'qf_trade': {
        'engine': 'mysql',
        'db': 'qf_trade',
        'host': '172.100.101.156',
        'port': 3306,
        'user': 'qf',
        'passwd': '123456',
        'charset': 'utf8',
        'conn': 16,
    },
    'qf_audit': {
        'engine': 'mysql',
        'db': 'qf_audit',
        'host': '172.100.101.156',
        'port': 3306,
        'user': 'qf',
        'passwd': '123456',
        'charset': 'utf8',
        'conn': 16,
    },
    'qf_sms': {
        'engine': 'mysql',
        'db': 'qf_sms',
        'host': '172.100.101.107',
        'port': 3306,
        'user': 'qf',
        'passwd': '123456',
        'charset': 'utf8',
        'conn': 16,
    },
    'wxmp_customer': {
        'engine': 'mysql',
        'db': 'wxmp_customer',
        'host': '172.100.101.107',
        'port': 3306,
        'user': 'qf',
        'passwd': '123456',
        'charset': 'utf8',
        'conn': 16,
    },
    'qf_weifutong': {
        'engine': 'mysql',
        'db': 'qf_weifutong',
        'host': '172.100.101.107',
        'port': 3306,
        'user': 'qf',
        'passwd': '123456',
        'charset': 'utf8',
        'conn': 16,
    },
    'open_user': {
        'engine': 'mysql',
        'db': 'open_user',
        'host': '172.100.101.107',
        'port': 3306,
        'user': 'qf',
        'passwd': '123456',
        'charset': 'utf8',
        'conn': 16,
    },

    'qf_settle': {
        'engine': 'mysql',
        'db': 'qf_settle',
        'host': '172.100.101.107',
        'port': 3306,
        'user': 'qf',
        'passwd': '123456',
        'charset': 'utf8',
        'conn': 16,
    },

}

APOLLO_SERVERS = [{'addr': ('172.100.101.107', 6900), 'timeout': 2000}, ]
# APOLLO_SERVERS = [{'addr': ('172.100.111.45', 6900), 'timeout': 2000}, ]

# 生成id
SPRING_SERVERS = [{'addr': ('172.100.101.106', 4590), 'timeout': 2000}, ]

#渠道信息
QUDAO_API_SERVERS = [{'addr': ('172.100.101.107', 8000), 'timeout': 2000}, ]

# 费率服务
ACCOUNT2_SERVERS = [{'addr': ('172.100.101.107', 2013), 'timeout': 2000}, ]

#获取商户的结算类型
MERCHANT_SERVER = [{'addr': 'http://172.100.101.107:6310', 'timeout': 60000}]

# FUND2 服务
FUND2_SERVERS = [{'addr': ('172.100.116.238', 8009), 'timeout': 2000}, ]

# redis  cache 缓存的配置
CACHE_CONF = {
    'redis_cache_name': 'permission_cache',
    'redis_conf': {
        'host': '127.0.0.1',
        'port': 6379,
        'password': ''
    }
}

# 二维码url
code = {
    'jh':'https://o2.qfpay.com/q/pay?h=%s'
}

# cookie配置
COOKIE_CONFIG = {
     'max_age': 86400*1,
     'domain': None,
}

sesskey = 'sessidsolar'

# 渠道ID限定
GROUPID_IN = [10016, 10017]


#消息推送服务地址
MESSAGES_SERVER = [{'addr': ('192.20.10.6', 5800), 'timeout': 2000},
                       {'addr': ('192.20.10.7', 5800), 'timeout': 2000}]
MSGPUSH2_SERVER = [{'addr': ('192.20.10.6', 6001), 'timeout': 2000},
                   {'addr': ('192.20.10.7', 6001), 'timeout': 2000}]

AUDIT_SERVER = [{'addr': ('172.100.101.110', 7100), 'timeout': 2000}, ]

#获取微信token
WX_SERVER = [{'addr': ('172.100.101.107', 6120), 'timeout': 8000},]


