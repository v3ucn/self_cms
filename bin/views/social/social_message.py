# -*- coding:utf-8 -*-
import time
import uuid
import redis
import logging
from honeycomb import SortedSet, Dict
from protobuf_to_dict import protobuf_to_dict
from protocbuf.message_pb2 import User, Msg

from . import gen_key
from .social_base import SOCIAL_REDIS
from .social_constants import SocialObj
from .social_para import validParam
from .social_helper import utf82unicode

log = logging.getLogger()


class SocialMessageHandler():
    def __init__(self, host=None, port=None, db=None):
        self.host = host if host else SOCIAL_REDIS['host']
        self.port = port if port else SOCIAL_REDIS['port']
        self.db = db if db else SOCIAL_REDIS['db']
        self.redis_object = redis.StrictRedis(host=self.host,
                                              port=self.port,
                                              db=self.db)

    @validParam(user_id=int, offset=int, limit=int)
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


def gen_user(user_id, nickname, avatar):
    """
    生成一个user对象
    :param user_id:
    :param nickname:
    :param avatar:
    :return:
    """
    return User(user_id=user_id, nickname=utf82unicode(nickname), avatar=avatar)


def gen_msg_id():
    """
    生成一个msg_id
    :return:
    """
    return utf82unicode(uuid.uuid4().get_hex())


def gen_msg(msg_id, type, content, topic_id, topic_name, topic_type, post_id, post_img, comment_id, comment_content,
            actiontype, url, timestamp, users, activity_id):
    """
    生成一个msg对象
    :param msg_id:
    :param type:
    :param content:
    :param topic_id:
    :param topic_name:
    :param post_id:
    :param post_img:
    :param timestamp:
    :param users:
    :return:
    """
    msg = Msg(msg_id=msg_id,
              type=type,
              content=utf82unicode(content),
              topic_id=topic_id,
              topic_name=utf82unicode(topic_name),
              topic_type=topic_type,
              post_id=post_id,
              post_img=post_img,
              timestamp=timestamp,
              actiontype=actiontype,
              url=url,
              users=users,
              comment_id=comment_id,
              comment_content=utf82unicode(comment_content),
              activity_id=activity_id)
    msg_str = msg.SerializeToString()
    return msg_str