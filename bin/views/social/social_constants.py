
# -*- coding:utf-8 -*-

MSG_TYPE_SYSTEM = 0                 # 系统
MSG_TYPE_AUDIT_PASS = 21            # 审核通过
MSG_TYPE_AUDIT_NOPASS = 22          # 审核失败
MSG_TYPE_POST_UP = 23               # 顶贴
MSG_TYPE_POST_REPLY = 24            # 回帖
MSG_TYPE_GOOD_BEGIN = 25            # 特卖开始
MSG_TYPE_COMMENT_REPLY = 26         # 评论

MSG_CONTENT = {
    MSG_TYPE_AUDIT_PASS: u'您创建的话题已审核通过',
    MSG_TYPE_AUDIT_NOPASS: u'您创建的话题审核失败',
    MSG_TYPE_POST_UP: u'赞同了你',
    MSG_TYPE_POST_REPLY: u'评论了你',
    MSG_TYPE_GOOD_BEGIN: u'',
    MSG_TYPE_COMMENT_REPLY: u'回复了你的评论'
}


class SocialAction:
    CREATE = 'create'       # 创建
    SHARE = 'share'         # 分享

    FOLLOW = 'follow'       # 关注
    UNFOLLOW = 'unfollow'   # 取消关注

    LIKE = 'like'           # 点赞
    UNLIKE = 'unlike'       # 取消点赞

    # near
    UP = 'up'               # 顶
    DOWN = 'down'           # 踩,暂时未用
    AUDIT_PASS = 'audit_pass'       # 审核通过
    AUDIT_NOPASS = 'audit_nopass'   # 审核不通过
    BEGIN = 'begin'         # 开始
    DISCUSS = 'discuss'     # 评论（帖子）
    REPLY = 'reply'         # 回复（评论）
    JOIN = 'joined'           # 加入


    action_chinese = {
        CREATE: '创建',
        SHARE: '分享',
        FOLLOW: '关注',
        UNFOLLOW: '取消关注',
        LIKE: '点赞',
        UNLIKE: '取消点赞',
        UP: '顶',
        DOWN: '踩',          # 暂时未用
    }


class SocialObj:
    USER = 'user'
    TOPIC = 'topic'
    POSTS = 'posts'
    COMMENTS = 'comments'
    GOOD = 'good'
    CIRCLE = 'circle'

    obj_chinese = {
        USER: '用户',
        TOPIC: '话题',
        POSTS: '帖子',
        GOOD: '特卖',
        CIRCLE: '商圈',
    }

    MESSAGE_CENTER = 'msg'
    NEWS = 'news'
    ME = 'me'
    DETAIL = 'detail'
    HISTORY = 'history'

    FOLLOWERS = 'followers'
    FOLLOWINGS = 'followings'
    LIKES = 'likes'


class SocialCounter:
    USER_SHARE = 'user_share_count'

