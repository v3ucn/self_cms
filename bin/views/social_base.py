# -*- coding:utf-8 -*-
import redis
from honeycomb import Dict

SOCIAL_REDIS_ONLINE = \
    {
        'host': '192.20.20.8',
        'port': 6376,
        'db': 3
    }

SOCIAL_REDIS_LOCAL = \
    {
        'host': '172.100.102.101',
        'port': 6379,
        'db': 0
    }

try:
    init_conf = Dict(key='project_honey_init')
    environ = init_conf['environ']
    SOCIAL_REDIS = SOCIAL_REDIS_LOCAL if environ == 'local_debug' else SOCIAL_REDIS_ONLINE
except Exception:
    SOCIAL_REDIS = SOCIAL_REDIS_ONLINE


class MessageBean(object):
    def __init__(self, msg):
        info_list = msg[0].split('_')
        timestamp = msg[1]
        self.executor_id = info_list[0]
        self.action = info_list[1]
        self.obj = info_list[2]
        self.obj_id = info_list[3]
        self.timestamp = int(timestamp)


def get_production_redis_object():
    redis_object = redis.StrictRedis(host=SOCIAL_REDIS['host'],
                                     port=SOCIAL_REDIS['port'],
                                     db=SOCIAL_REDIS['db'])
    return redis_object
