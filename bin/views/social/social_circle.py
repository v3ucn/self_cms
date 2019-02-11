# -*- coding:utf-8 -*-
import time
import redis
import logging

from honeycomb import SortedSet

from . import gen_key
from .social_base import SOCIAL_REDIS
from .social_constants import SocialObj
from .social_constants import SocialAction

from .social_para import validParam
log = logging.getLogger()


class SocialCircleHandler():
    def __init__(self, host=None, port=None, db=None):
        self.host = host if host else SOCIAL_REDIS['host']
        self.port = port if port else SOCIAL_REDIS['port']
        self.db = db if db else SOCIAL_REDIS['db']
        self.redis_object = redis.StrictRedis(host=self.host,
                                              port=self.port,
                                              db=self.db)

    def op_join_circle(self, user_id, circle_id):
        """加入商圈"""

        timestamp = int(time.time())
        s1 = SortedSet(redis=self.redis_object, key=gen_key(SocialObj.CIRCLE, circle_id, SocialAction.JOIN))    # near_circle_12345_joined
        s2 = SortedSet(redis=self.redis_object, key=gen_key(SocialObj.USER, user_id, SocialAction.JOIN, op_type=SocialObj.CIRCLE))  # user_12345_joined_circle
        s1.add(user_id, timestamp)      # 商圈加入的用户集合
        s2.add(circle_id, timestamp)     # 用户加入的商圈集合

        log.info("SocialInfo: user-{0} join circle-{1}.".format(user_id, circle_id))

    def get_user_join_circles(self, user_id):
        """
        获取用户加入的商圈ID列表
        """
        ss = SortedSet(redis=self.redis_object, key=gen_key(SocialObj.USER, user_id, SocialAction.JOIN, op_type=SocialObj.CIRCLE))
        return list(ss.chunk(withscore=False, offset=0, limit=len(ss)))

    def get_circle_joined_users(self, circle_id):
        """
        获取该商圈加入的用户ID列表
        """
        ss = SortedSet(redis=self.redis_object, key=gen_key(SocialObj.CIRCLE, circle_id, SocialAction.JOIN))
        return list(ss.chunk(withscore=False, offset=0, limit=len(ss)))