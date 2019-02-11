# -*- coding: utf-8 -*-
import redis
import traceback
from honeycomb import Set, Dict, Counter, SortedSet

APP_PREF = "apppref"
APP_CUSTOM = "appcustom"


REDIS = {
    'app_config': {
        'use_class': 'Redis',
        'host': '192.20.20.8',
        'port': 6376,
        'db': 7
    },
    'social': {
        'use_class': 'Redis',
        'host': '192.20.20.8',
        'port': 6376,
        'db': 3
    },
    'temp': {
        'use_class': 'Redis',
        'host': '192.20.20.8',
        'port': 6376,
        'db': 2
    },
    'user': {
        'use_class': 'Redis',
        'host': '192.20.20.8',
        'port': 6376,
        'db': 4
    },
}

REDIS = {
    'app_config': {
        'use_class': 'Redis',
        'host': '172.100.102.101',
        'port': 6379,
        'db': 7
    },
    'social': {
        'use_class': 'Redis',
        'host': '172.100.102.101',
        'port': 6377,
        'db': 0
    },
    'temp': {
        'use_class': 'Redis',
        'host': '172.100.102.101',
        'port': 6379,
        'db': 1
    },
    'user': {
        'use_class': 'Redis',
        'host': '172.100.102.101',
        'port': 6379,
        'db': 1
    },
}


def get_app_conf_set(app_id, conf_id, app_conf=APP_PREF):
    my_redis = redis.Redis(host=REDIS["app_config"]["host"],
                           port=REDIS["app_config"]["port"],
                           db=REDIS["app_config"]["db"])
    key = "%s_appid%s_confid%s_userid" % (app_conf, app_id, conf_id)
    return Set(key=key, redis=my_redis)


def get_app_conf_dict(app_id, conf_id, prop_dict=None, app_conf=APP_PREF):
    my_redis = redis.Redis(host=REDIS["app_config"]["host"],
                           port=REDIS["app_config"]["port"],
                           db=REDIS["app_config"]["db"])
    key = "%s_appid%s_confid%s_dict" % (app_conf, app_id, conf_id)
    if prop_dict:
        return Dict(key=key, data=prop_dict, redis=my_redis)
    else:
        return Dict(key=key, redis=my_redis)


def get_honey_stat_count(honey_id):
    try:
        ret = {
            'collect': int(Counter(key='honey_collect_count').get(honey_id, default=0)),
            'like': len(SortedSet(key='_'.join(['honey', str(honey_id), 'likes']))),
            'share': int(Counter(key='honey_share_count').get(honey_id, default=0))
        }
        return ret
    except Exception, e:
        print e
        print traceback.format_exc()


def get_comb_stat_count(comb_id):
    try:
        ret = {
            'follow': len(SortedSet(key='_'.join(['comb', str(comb_id), 'followers']))),
            'share': int(Counter(key='comb_share_count').get(comb_id, default=0))
        }
        return ret
    except Exception, e:
            print e
            print traceback.format_exc()


temp_redis_client = redis.Redis(host=REDIS["temp"]["host"],
                     port=REDIS["temp"]["port"],
                     db=REDIS["temp"]["db"])

user_client = redis.Redis(host=REDIS["user"]["host"],
                     port=REDIS["user"]["port"],
                     db=REDIS["user"]["db"])



# redis 内部员工用户key
REDIS_QF_STAFF_USER_LIST = 'qf_staff_user_list'
