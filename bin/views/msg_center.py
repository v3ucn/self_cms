# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
import types

import redis
from honeycomb import SortedSet, Dict
from protobuf_to_dict import protobuf_to_dict

from protobuf.msg_pb2 import Msg
from .social_base import SOCIAL_REDIS


class SocialObj:
    MESSAGE_CENTER = 'msg'
    NEWS = 'news'
    ME = 'me'
    DETAIL = 'detail'
    HISTORY = 'history'


def avg_get_message(user_id, offset, pagesize):

    handler = SocialMessageHandler()
    msgs = handler.get_messages(user_id, offset, pagesize)
    ret = {"messages": msgs}
    return ret


class MerchantMessageHandler():
    def __init__(self, host=None, port=None, db=None):
        self.host = host if host else SOCIAL_REDIS['host']
        self.port = port if port else SOCIAL_REDIS['port']
        self.db = db if db else SOCIAL_REDIS['db']
        self.redis_object = redis.StrictRedis(host=self.host,
                                              port=self.port,
                                              db=self.db)

    def get_messages(self, user_id, offset, limit):
        """
        获取消息列表
        :param user_id: 用户ID
        :param offset: 偏移量
        :param pagesize: 数量
        :return:
        """
        mc_me = SortedSet(redis=self.redis_object, key=gen_key(SocialObj.MESSAGE_CENTER, user_id, SocialObj.ME))
        mc_detail = Dict(redis=self.redis_object, key=gen_key(SocialObj.MESSAGE_CENTER, user_id, SocialObj.DETAIL))

        msgs = []
        for msg_id, timestamp in mc_me.rchunk(limit=limit, offset=offset):
            msg = Msg()
            msg.ParseFromString(mc_detail[msg_id])
            msg_dict = protobuf_to_dict(msg)
            msgs.append(msg_dict)
        return msgs

    def add_message(self, user_id, owner_id, msg_id, msg):
        """
        添加消息到消息中心
        :param user_id: 消息触发者ID
        :param owner_id: 用户ID
        :param msg_id: 消息ID
        :param msg: 消息内容
        :return:
        """
        timestamp = int(time.time())
        # if owner_id != user_id:
        mc_me = SortedSet(redis=self.redis_object, key=gen_key(SocialObj.MESSAGE_CENTER, owner_id, SocialObj.ME))
        mc_detail = Dict(redis=self.redis_object, key=gen_key(SocialObj.MESSAGE_CENTER, owner_id, SocialObj.DETAIL))
        mc_me.add(msg_id, timestamp)
        mc_detail[msg_id] = msg

def gen_mcht_msg(msg_id, msg_type, title, content, ref_id, ref_type, ref_title, actiontype, url, timestamp):
    """
    生成一个msg对象
    :param msg_id:
    :param type:
    :param title:
    :param content:
    :param ref_id:
    :param ref_type:
    :param ref_title:
    :param timestamp:
    :return:
    """

    msg = Msg(msg_id=msg_id,
              msg_type=msg_type,
              title=utf82unicode(title),
              content=utf82unicode(content),
              ref_id=ref_id,
              ref_type=ref_type,
              ref_title=utf82unicode(ref_title),
              timestamp=timestamp,
              actiontype=actiontype,
              url=url)
    msg_str = msg.SerializeToString()
    return msg_str


def gen_key(obj, obj_id, op=None, op_id='', op_type=''):
    """设置Redis SortedSet 的 key
    user_1124_followers    用户1124的粉丝

    :param obj: 对象 user topic posts comments circle
    :param obj_id: 对象ID
    :param op: 动作,
    :param op_type: 操作对象类型
    :return:
    """
    prefix = 'merch'
    if op_type != '':
        key_str = '_'.join([prefix, obj, str(obj_id), op, op_type])
    elif op_id != '':
        key_str = '_'.join([prefix, obj, str(obj_id), op, str(op_id)])
    elif op:
        key_str = '_'.join([prefix, obj, str(obj_id), op])
    else:
        key_str = '_'.join([prefix, obj, str(obj_id)])
    return key_str


def parse_key(key, idx=None):
    """
    gen_key 的逆过程，返回类似 [type, id, op] 的多元列表, 如果传入了 idx 参数, 则只返回 idx 位置的单个元素 。支持批量参数
    """
    if isinstance(key, str):
        assert '_' in key
        pair = key.split('_')
        if isinstance(idx, int):
            return pair[idx]
        return pair
    else:  # 这里没做 集合类型 判断是因为validParam已经做过了
        return [parse_key(k, idx) for k in key]


def unicode2utf8(text):
    if isinstance(text, types.UnicodeType):
        return text.encode('utf-8')
    else:
        return text


def utf82unicode(text):
    if isinstance(text, types.StringType):
        return text.decode('utf-8')
    else:
        return text

