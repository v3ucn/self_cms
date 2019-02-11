# -*- coding:utf-8 -*-
import time
import redis
import logging

from honeycomb import SortedSet

from . import gen_key
from .social_base import SOCIAL_REDIS
from .social_constants import SocialObj
from .social_constants import SocialAction
from .social_message import SocialMessageHandler

from .social_para import validParam
log = logging.getLogger()


class SocialTopicHandler():
    def __init__(self, host=None, port=None, db=None):
        self.host = host if host else SOCIAL_REDIS['host']
        self.port = port if port else SOCIAL_REDIS['port']
        self.db = db if db else SOCIAL_REDIS['db']
        self.redis_object = redis.StrictRedis(host=self.host,
                                              port=self.port,
                                              db=self.db)

    def is_needed_pushed(self, user_id, posts_id):
        key = gen_key(SocialObj.POSTS, posts_id, SocialAction.UP, op_type=SocialObj.HISTORY)
        up_history = SortedSet(redis=self.redis_object, key=key)  # post_12345_up_history
        if user_id in up_history:
            return False
        return True

    @validParam(user_id=int, posts_id=basestring, owner_id=int)
    def op_up_posts(self, user_id, posts_id, owner_id, msg_id, msg):
        """顶帖子"""

        timestamp = int(time.time())
        s1 = SortedSet(redis=self.redis_object, key=gen_key(SocialObj.POSTS, posts_id, SocialAction.UP))    # posts_12345_up
        s2 = SortedSet(redis=self.redis_object, key=gen_key(SocialObj.USER, user_id, SocialAction.UP, op_type=SocialObj.POSTS))  # user_12345_up_posts
        s1.add(user_id, timestamp)      # 话题的被点赞信息
        s2.add(posts_id, timestamp)     # 用户的点赞信息

        key = gen_key(SocialObj.POSTS, posts_id, SocialAction.UP, op_type=SocialObj.HISTORY)
        up_history = SortedSet(redis=self.redis_object, key=key)  # post_12345_up_history
        if user_id not in up_history:    # 重复点赞，只会记录一条消息
            up_history.add(user_id, timestamp)
            handler = SocialMessageHandler()
            handler.add_message(user_id=user_id, owner_id=owner_id, msg_id=msg_id, msg=msg)

        log.info("SocialInfo: user-{0} up posts-{1}.".format(user_id, posts_id))
        return

    @validParam(user_id=int, posts_id=basestring)
    def op_unup_posts(self, user_id, posts_id):
        """取消顶帖子"""

        # 话题的被点赞信息, key: posts_12345_up
        s1 = SortedSet(redis=self.redis_object, key=gen_key(SocialObj.POSTS, posts_id, SocialAction.UP))
        # 用户的点赞信息, key: user_12345_up_posts
        s2 = SortedSet(redis=self.redis_object, key=gen_key(SocialObj.USER, user_id, SocialAction.UP, op_type=SocialObj.POSTS))
        s1.discard(user_id)
        s2.discard(posts_id)

        log.info("SocialInfo: user-{0} unup posts-{1}.".format(user_id, posts_id))
        return

    @validParam(posts_id=basestring)
    def get_posts_up_count(self, posts_id):
        """获取帖子被顶数"""
        s = SortedSet(redis=self.redis_object, key=gen_key(SocialObj.POSTS, posts_id, SocialAction.UP))
        return len(s)

    def get_user_up_posts(self, user_id):
        """
        获取赞过的 post 列表
        """
        ss = SortedSet(redis=self.redis_object, key=gen_key(SocialObj.USER, user_id, SocialAction.UP, op_type=SocialObj.POSTS))
        return list(ss.chunk(withscore=False, offset=0, limit=len(ss)))

    def get_user_up_post_count(self, user_id):
        """
        获取用户赞过的帖子数
        """
        ss = SortedSet(redis=self.redis_object, key=gen_key(SocialObj.USER, user_id, SocialAction.UP, op_type=SocialObj.POSTS))
        return len(ss)