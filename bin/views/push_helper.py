# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json
import random
import config
from msgpush import MsgPush
from qfcommon.base.tools import thrift_callex
from qfcommon.base.http_client import RequestsClient
from qfcommon.push.constants import Platform, MsgType
from utils.misc import utf82unicode,now2str,unicode2utf8,convert_to_comma_delimited_string

import logging

log = logging.getLogger()


# platform: 应用平台
(PLATFORM_IOS, PLATFORM_ANDROID, PLATFORM_WP) = (0, 1, 2)
APP_PLATFORM = {
    PLATFORM_IOS: 'ios',
    PLATFORM_ANDROID: 'android',
    PLATFORM_WP: 'wp'
}

# apptype
# 201(蜂蜜公司账号dev版),202（蜂蜜公司账号appstore版),211(蜂蜜企业账号dev版),212(蜂蜜企业账号分发版)
(APPTYPE_FM_DEV, APPTYPE_FM_DIS, APPTYPE_FM_ENT_DEV, APPTYPE_FM_ENT_DIS) = (201, 202, 211, 212)  # new
(APPTYPE_NEAR_DEV, APPTYPE_NEAR_DIS, APPTYPE_NEAR_ENT_DEV, APPTYPE_NEAR_ENT_DIS) = (301, 302, 311, 312)  # near

# mode
SEND_MODE_ALL = 0 #所有用户
SEND_MODE_GROUP = 1 #按groupid推送
SEND_MODE_MOBILE = 2 #按手机号推送
SEND_MODE_USERID = 3 #按用户id推送
SEND_MODE_OPENID = 100 #按用户OPENID推送（喵喵用户id）


MESSAGES_SERVER = config.MESSAGES_SERVER
MSGPUSH2_SERVER = config.MSGPUSH2_SERVER



SEND_MODE_ALL = 0       # 所有用户
SEND_MODE_GROUP = 1     # 按groupid推送
SEND_MODE_MOBILE = 2    # 按手机号推送
SEND_MODE_USERID = 3    # 按用户id推送



def set_custom(title='', link='', mtype=0, actiontype=0, act='', **kwargs):
    """
    生成自定义参数
    :param title: 标题，Android和WindowsPhone需要
    :param link: 跳转链接地址，如：http://www.baidu.com
    :param mtype: 消息类型
    :param actiontype:是否跳转,0不跳转至link，1跳转至link
    :param kwargs:每个app自定义需要的参数，(不可太多参数，因为有大小限制)
    :return: 字符串
    """
    extra = {"type": mtype, "title": title, "link": link, "actiontype": actiontype}
    extra.update(kwargs)
    extra["act"] = act
    extra["logo"] = ''
    extra["sound"] = ''
    str_extra = json.dumps(extra, separators=(',', ':'))
    return str_extra


def set_custom_dict(title='', link='', mtype=0, actiontype=0, act='', **kwargs):
    """
    生成自定义参数
    :param title: 标题，Android和WindowsPhone需要
    :param link: 跳转链接地址，如：http://www.baidu.com
    :param mtype: 消息类型
    :param actiontype:是否跳转,0不跳转至link，1跳转至link
    :param kwargs:每个app自定义需要的参数，(不可太多参数，因为有大小限制)
    :return: 字符串
    """
    extra = {"type": mtype, "title": title, "link": link, "actiontype": actiontype}
    extra.update(kwargs)
    extra["act"] = act
    extra["logo"] = ''
    extra["sound"] = ''
    return extra



def push_msg2(content, str_extra, to, apptypes=None, platforms=None, mode=3):
    """
    推送消息
    :param content: 消息内容
    :param str_extra: 消息自定义参数，由set_custom生成
    :param to: 用户ID(字符串类型)的列表
    :param apptypes: app类型
                301(好近公司账号dev版),
                302（好近公司账号appstore版),Android和wp为302
                311(好近企业账号dev版),
                312(好近企业账号分发版)。
    :param platforms: 平台，
                0:IOS
                1:Android
                2:Windows Phone
    :param mode: 推送模式，
                0: SEND_MODE_ALL, 所有用户
                1: SEND_MODE_GROUP, 按groupid推送
                2: SEND_MODE_MOBILE, 按手机号推送
                3: SEND_MODE_USERID, 按用户id推送
    :return:
    """
    if not apptypes:
        apptypes = [301, 302, 312, 311]
    if not platforms:
        platforms = [0, 1, 2]
    thrift_callex(MSGPUSH2_SERVER,
                  MsgPush, 'pushmsg2', apptypes, platforms, mode,content, str_extra, to)



def push_msg_v3(content, custom, to, apptypes=None, platforms=None, mode=3):
    """
    使用push_entry服务推送消息
    :param content: 消息内容
    :param str_extra: 消息自定义参数，由set_custom生成
    :param to: 用户ID(字符串类型)的列表
    :param apptypes: app类型
                301(好近公司账号dev版),
                302（好近公司账号appstore版),Android和wp为302
                311(好近企业账号dev版),
                312(好近企业账号分发版)。
                401(好近商户 AppStore Dev)
                402(好近商户 AppStore Release)
                411(好近商户 Ent Dev)
                412(好近商户 Ent Release)

    :param platforms: 平台，
                0:IOS
                1:Android
                2:Windows Phone
    :param mode: 推送模式，
                0: SEND_MODE_ALL, 所有用户
                1: SEND_MODE_GROUP, 按groupid推送
                2: SEND_MODE_MOBILE, 按手机号推送
                3: SEND_MODE_USERID, 按用户id推送
    :return:
    """

    # FIXBY YYK, 运营消息只给msgpush推送, 不再给push_entry推送。
    return

#    android_content = {
#        "title": "标题",  # 标题
#        "content": "内容",  # 内容
#        "type": 3,  # 消息类型，0为运营消息, 1为专享卡消费，2为外卖订单,3为消息中心
#        "actiontype": 0,  # 是否跳转, 0为不跳转, 1为跳转至 link.
#        "link": "http://www.baidu.com",  # 跳转链接.
#        "act": "",  # 预留字段.
#        "logo": "",  # 提示图标.
#        "sound": "",  # 提示声音. "takeout_order"为外卖订单语音, "discount_order"为买单付款语音, "pay_success"(新增)为收款成功.
#        "notice": ""  # 字符串, 客户端会将其转为语音播放.
#    }

    if not apptypes or not platforms:
        log.debug('miss apptype')
        return

    params = {
        'apptype_list': [],
        'platform_list': [Platform.Android, Platform.IOS],
        'msgtype': MsgType.Multi,
        'userid_list': [10512],
        'ttl': 600,
        'body': '',
    }
    #MsgType (1)按UserID推送 (2)通过DeviceID推送 (3)通过分组推送 (4)全量推送

    if PLATFORM_IOS in platforms:
        # 需要推送IOS设备
        body = {
                "aps": {
                    "alert": "内容",
                    "badge": 1,
                    "sound": "default"
                }
        }

        sound = custom.pop("sound") if "sound" in custom and custom['sound'] else "default"
        aps = {}
        aps['alert'] = content
        aps['badge'] = 1
        aps['sound'] = sound
        body['aps'] = aps

        params['apptype_list'] = apptypes
        params['platform_list'] = [Platform.IOS]
        params['userid_list'] = to

        body.update(custom)
        params['body'] = json.dumps(body)
        try:
            RequestsClient().post_json('http://192.10.21.152:8002/v1/push2app', params)
        #try:
        #    thrift_callex(MSGPUSH2_SERVER,
        #                  MsgPush, 'pushmsg2', apptypes, platforms, mode, content, str_extra, to)
        except Exception, e:
            log.debug(e)
            log.debug('push_entry error')


    if PLATFORM_ANDROID in platforms:
        # 需要推送Android设备
        #custom['msgid'] ='notice_%d' % random.randint(100000, 999999)
        custom['content'] = content

#        body = {
#            'content' : content,
#            'title' : '标题',
#            'type' : 0,
#            'actiontype' : 0,
#            'link': 'https://www.baidu.com',
#            'act' : '',
#            'logo' : '',
#            'sound' : 'pay_success',
#            'notice' : 'pay success',
#            'msgid' :  'notice_%d' % random.randint(100000, 999999)
#        }

        params['apptype_list'] = apptypes
        params['platform_list'] = [Platform.Android]
        params['userid_list'] = to
        params['body'] = json.dumps(custom)

        try:
            RequestsClient().post_json('http://192.10.21.152:8002/v1/push2app', params)
        #try:
        #    thrift_callex(MSGPUSH2_SERVER,
        #                  MsgPush, 'pushmsg2', apptypes, platforms, mode, content, str_extra, to)
        except Exception, e:
            log.debug(e)
            log.debug('push_entry error')
