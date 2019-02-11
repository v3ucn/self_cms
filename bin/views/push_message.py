# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import datetime
import time
import json
import traceback
from push_helper import push_msg2, set_custom, set_custom_dict, push_msg_v3
from push_helper import SEND_MODE_ALL, SEND_MODE_USERID, SEND_MODE_USERID
from qfcommon.base.dbpool import with_database, get_connection_exception, get_connection
from tools import checkIsLogin
from qfcommon.web import template
from qfcommon.web import core
import logging
from utils.misc import utf82unicode, now2str, unicode2utf8, convert_to_comma_delimited_string
from msg_center import MerchantMessageHandler, gen_mcht_msg
from social.social_message import gen_msg_id, gen_msg, SocialMessageHandler
from social.social_circle import SocialCircleHandler
from social.social_constants import MSG_TYPE_GOOD_BEGIN
import threading

log = logging.getLogger()
_data_name = 'honey_manage'
# _data_name = 'qmm_wx'

PLATEFORM_CHOICES = {
    "0": "IOS",
    "1": "Android"
}

APPTYPE_CHOICES = {
    "5", "应用市场版本",
    "6", "企业账号分发版",
    "7", "白牌V创宝",
    "8", "白牌达令",
    "9", "白牌金道池",
    "10", "白牌积积乐",
    "11", "白牌微云商户宝"
}

MODE_CHOICES = {"0": "全部推送",
                "2": "用户ID",
                "3": "渠道ID"
                }

MTYPE_CHOICES = {
    "1": "运营",
    "2": "通知",
    "3": "事件"
}

TAG_TYPE = {
    "0": "直营",
    "1": "渠道",
    "2": "白牌"
}

# 白牌渠道列表
BAIPAI_GROUPIDS = [1588076, 1645189, 1588158, 1634275, 1617325, 1659955, 1797730, 1869697, 1831630, 1935800, 1974299,
                   2011865, 2126041, 2199877, 2202844]

# 直营渠道列表# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import datetime
import time
import json
import traceback
from push_helper import push_msg2, set_custom, set_custom_dict, push_msg_v3
from push_helper import SEND_MODE_ALL, SEND_MODE_USERID, SEND_MODE_USERID
from qfcommon.base.dbpool import with_database, get_connection_exception, get_connection
from tools import checkIsLogin
from qfcommon.web import template
from qfcommon.web import core
import logging
from utils.misc import utf82unicode, now2str, unicode2utf8, convert_to_comma_delimited_string
from msg_center import MerchantMessageHandler, gen_mcht_msg
from social.social_message import gen_msg_id, gen_msg, SocialMessageHandler
from social.social_circle import SocialCircleHandler
from social.social_constants import MSG_TYPE_GOOD_BEGIN
import threading

log = logging.getLogger()
_data_name = 'honey_manage'
# _data_name = 'qmm_wx'

PLATEFORM_CHOICES = {
    "0": "IOS",
    "1": "Android"
}

APPTYPE_CHOICES = {
    "5", "应用市场版本",
    "6", "企业账号分发版",
    "7", "白牌V创宝",
    "8", "白牌达令",
    "9", "白牌金道池",
    "10", "白牌积积乐",
    "11", "白牌微云商户宝"
}

MODE_CHOICES = {"0": "全部推送",
                "2": "用户ID",
                "3": "渠道ID"
                }

MTYPE_CHOICES = {
    "1": "运营",
    "2": "通知",
    "3": "事件"
}

TAG_TYPE = {
    "0": "直营",
    "1": "渠道",
    "2": "白牌"
}

# 白牌渠道列表
BAIPAI_GROUPIDS = [1588076, 1645189, 1588158, 1634275, 1617325, 1659955, 1797730, 1869697, 1831630, 1935800, 1974299,
                   2011865, 2126041, 2199877, 2202844]

# 直营渠道列表
QF_GROUPIDS = [1694779, 20487, 20465, 1709635, 20485, 1725055, 20486, 1725049]


def div_list(ls, n):
    if not isinstance(ls, list) or not isinstance(n, int):
        return []
    ls_len = len(ls)
    if n <= 0 or 0 == ls_len:
        return []
    if n > ls_len:
        return []
    elif n == ls_len:
        return [[i] for i in ls]
    else:
        j = ls_len / n
        k = ls_len % n
        ### j,j,j,...(前面有n-1个j),j+k
        # 步长j,次数n-1
        ls_return = []
        for i in xrange(0, (n - 1) * j, j):
            ls_return.append(ls[i:i + j])
        # 算上末尾的j+k
        ls_return.append(ls[(n - 1) * j:])
        return ls_return


# 过滤id函数
def id_filter(_tag_type, _mode, _to):
    _tolist = _to.split(",")
    for index, item in enumerate(_tolist):
        _tolist[index] = int(item)

    retD = []

    # 渠道列表
    with get_connection('qf_core') as db:
        profiles = db.select(
            table='profile',
            fields='distinct groupid',
            where={'groupid': ('not in', QF_GROUPIDS + BAIPAI_GROUPIDS)}
        )
        QD_GROUPIDS = [i['groupid'] for i in profiles or []]

    # 过滤渠道id
    if (_mode == '3'):
        if _tag_type == '0':
            retD = list(set(_tolist).difference(set(QF_GROUPIDS)))
        elif _tag_type == '1':
            retD = list(set(_tolist).difference(set(QD_GROUPIDS)))
        elif _tag_type == '2':
            retD = list(set(_tolist).difference(set(BAIPAI_GROUPIDS)))
        elif _tag_type == '0,1':
            retD = list(set(_tolist).difference(set(QF_GROUPIDS + QD_GROUPIDS)))
        elif _tag_type == '0,2':
            retD = list(set(_tolist).difference(set(QF_GROUPIDS + BAIPAI_GROUPIDS)))
        elif _tag_type == '1,2':
            retD = list(set(_tolist).difference(set(QD_GROUPIDS + BAIPAI_GROUPIDS)))
    # 过滤商户id
    elif (_mode == '2'):
        if _tag_type == '0':
            with get_connection('qf_core') as db:
                profiles = db.select(
                    table='profile',
                    fields='userid',
                    where={'groupid': ('in', QF_GROUPIDS)}
                )
                userids = [i['userid'] for i in profiles or []]

            retD = list(set(_tolist).difference(set(userids)))
        elif _tag_type == '1':
            with get_connection('qf_core') as db:
                profiles = db.select(
                    table='profile',
                    fields='userid',
                    where={'groupid': ('in', QD_GROUPIDS)}
                )
                userids = [i['userid'] for i in profiles or []]

            retD = list(set(_tolist).difference(set(userids)))
        elif _tag_type == '2':
            with get_connection('qf_core') as db:
                profiles = db.select(
                    table='profile',
                    fields='userid',
                    where={'groupid': ('in', BAIPAI_GROUPIDS)}
                )
                userids = [i['userid'] for i in profiles or []]

            retD = list(set(_tolist).difference(set(userids)))
        elif _tag_type == '0,1':
            with get_connection('qf_core') as db:
                profiles = db.select(
                    table='profile',
                    fields='userid',
                    where={'groupid': ('in', QF_GROUPIDS + QD_GROUPIDS)}
                )
                userids = [i['userid'] for i in profiles or []]

            retD = list(set(_tolist).difference(set(userids)))
        elif _tag_type == '0,2':
            with get_connection('qf_core') as db:
                profiles = db.select(
                    table='profile',
                    fields='userid',
                    where={'groupid': ('in', QF_GROUPIDS + BAIPAI_GROUPIDS)}
                )
                userids = [i['userid'] for i in profiles or []]

            retD = list(set(_tolist).difference(set(userids)))
        elif _tag_type == '1,2':
            with get_connection('qf_core') as db:
                profiles = db.select(
                    table='profile',
                    fields='userid',
                    where={'groupid': ('in', QD_GROUPIDS + BAIPAI_GROUPIDS)}
                )
                userids = [i['userid'] for i in profiles or []]

            retD = list(set(_tolist).difference(set(userids)))

    if _tag_type != '0,1,2':

        for i in retD:
            _tolist.remove(i)

        for index, item in enumerate(_tolist):
            _tolist[index] = str(item)

    _tolist = ','.join(_tolist)

    return _tolist


class BaseHandler(core.Handler):
    def __init__(self, app, req):
        super(BaseHandler, self).__init__(app, req)
        self.resp.mimetype = 'application/json'
        self.resp.headers['Content-Type'] = '%s; charset=%s' % (
            self.resp.mimetype, self.resp.charset)


class ret2template(core.Handler):
    @checkIsLogin
    def GET(self):
        uname = self.get_cookie('uname')
        data = {}
        data['uname'] = uname
        self.write(template.render("push_message.html", data=data))


# 消息列表页面
class push_list(core.Handler):
    @checkIsLogin
    def GET(self):
        uname = self.get_cookie('uname')
        data = {}
        data['uname'] = uname
        self.write(template.render("push_list.html", data=data))


# 推送到消息中心
def add_merchant_message(mcht_msg, to=None):
    """好近专用:添加好近商户版消息至Redis"""
    if to is not None:
        user_ids = to
    else:
        user_ids = [int(uid) for uid in mcht_msg.get('to').split(',')]

    # 添加至消息中心
    handler = MerchantMessageHandler()
    for user_id in user_ids:
        msg_id = gen_msg_id()
        msg = gen_mcht_msg(msg_id, int(mcht_msg.get('mtype')), str(mcht_msg.get('title')), str(mcht_msg.get('content')),
                           str(mcht_msg.get('ref_id')),
                           int(mcht_msg.get('ref_type')), str(mcht_msg.get('ref_title')),
                           int(mcht_msg.get('actiontype')), str(mcht_msg.get('link')), now2str())
        handler.add_message(0, int(user_id), msg_id, msg)


# 消息推送动作
class push_act(BaseHandler):
    @with_database(_data_name)
    def POST(self):
        if self.req.environ.get('CONTENT_TYPE', '').lower().startswith(
                'application/json'):
            try:
                params = self.req.inputjson()

                push_msg = {}
                push_msg['title'] = params.get('title')
                push_msg['content'] = params.get('content')
                push_msg['mode'] = params.get('mode')
                push_msg['to'] = params.get('to')
                push_msg['platforms'] = params.get('platforms')
                push_msg['apptypes'] = params.get('apptypes')
                push_msg['mtype'] = int(params.get('mtype'))
                push_msg['link'] = params.get('link')
                push_msg['actiontype'] = int(params.get('actiontype'))
                push_msg['id'] = int(params.get('push_id'))

                push_msg['ref_id'] = 0
                push_msg['ref_type'] = 0
                push_msg['ref_title'] = params.get('ref_title')

                title = push_msg.get('title')
                content = push_msg.get('content')
                ref_id = push_msg.get('ref_id')
                _tag_type = str(params.get('tag_type'))

                apptypes = [int(item) for item in push_msg.get('apptypes').split(',')]
                platforms = [int(item) for item in push_msg.get('platforms').split(',')]
                for index, item in enumerate(apptypes):
                    if item == 5:
                        apptypes[index] = 402
                    elif item == 6:
                        apptypes[index] = 401
                    elif item == 7:
                        apptypes[index] = 412
                    elif item == 8:
                        apptypes[index] = 411
                    elif item == 9:
                        apptypes[index] = 9010
                    elif item == 10:
                        apptypes[index] = 9011
                    elif item == 12:
                        apptypes[index] = 9012
                    elif item == 13:
                        apptypes[index] = 9013
                    elif item == 14:
                        apptypes[index] = 9014
                mode = int(push_msg.get('mode'))

                to = [str(item) for item in push_msg.get('to').split(',')]
                # ------ 提出的处理方式  -------#
                topic_type = 0
                msg_type = 3  # 0 运营小 1 买单 2 外卖订单 3 消息中心
                # actiontype 0 不跳转 1 跳转
                if push_msg.get('actiontype') == 1 and push_msg.get('mtype') == 1:
                    msg_actiontype = 1
                else:
                    msg_actiontype = 0

                userids = None
                # 如果按照渠道推送需要通过profile查出userid
                try:
                    if mode == 3:
                        with get_connection('qf_core') as db:
                            groupids = map(int, to)
                            profiles = db.select(
                                table='profile',
                                fields='userid',
                                where={'groupid': ('in', groupids)}
                            )
                            userids = [i['userid'] for i in profiles or []]

                    if mode == 0:

                        # 渠道列表
                        with get_connection('qf_core') as db:
                            profiles = db.select(
                                table='profile',
                                fields='distinct groupid',
                                where={'groupid': ('not in', QF_GROUPIDS + BAIPAI_GROUPIDS)}
                            )
                            QD_GROUPIDS = [i['groupid'] for i in profiles or []]

                        log.debug('全渠道列表长度: %s' % str(len(QD_GROUPIDS)))

                        if _tag_type == '0':
                            _aqd_list = QF_GROUPIDS
                        elif _tag_type == '1':
                            _aqd_list = QD_GROUPIDS
                        elif _tag_type == '2':
                            _aqd_list = BAIPAI_GROUPIDS
                        elif _tag_type == '0,1':
                            _aqd_list = QF_GROUPIDS + QD_GROUPIDS
                        elif _tag_type == '0,2':
                            _aqd_list = QF_GROUPIDS + BAIPAI_GROUPIDS
                        elif _tag_type == '1,2':
                            _aqd_list = QD_GROUPIDS + BAIPAI_GROUPIDS
                        elif _tag_type == '0,1,2':
                            _aqd_list = QF_GROUPIDS + QD_GROUPIDS + BAIPAI_GROUPIDS

                        with get_connection('qf_core') as db:
                            profiles = db.select(
                                table='profile',
                                fields='distinct userid',
                                where={'groupid': ('in', _aqd_list)}
                            )
                            userids = [i['userid'] for i in profiles or []]
                except Exception, e:
                    log.debug('读取mysql过滤报错')
                    log.debug(e)
                    return json.dumps({'ok': False, 'msg': '读取mysql过滤报错'},
                                      ensure_ascii=False)

                try:
                    log.debug('全用户列表长度: %s' % str(len(userids)))
                except Exception, e:
                    print e
                    pass

                try:
                    if userids and len(userids) > 10:
                        dlist = div_list(userids, 10)
                        threads = []
                        t1 = threading.Thread(target=add_merchant_message, args=(push_msg, dlist[0]))
                        threads.append(t1)
                        t2 = threading.Thread(target=add_merchant_message, args=(push_msg, dlist[1]))
                        threads.append(t2)
                        t3 = threading.Thread(target=add_merchant_message, args=(push_msg, dlist[2]))
                        threads.append(t3)
                        t4 = threading.Thread(target=add_merchant_message, args=(push_msg, dlist[3]))
                        threads.append(t4)
                        t5 = threading.Thread(target=add_merchant_message, args=(push_msg, dlist[4]))
                        threads.append(t5)

                        t6 = threading.Thread(target=add_merchant_message, args=(push_msg, dlist[5]))
                        threads.append(t6)
                        t7 = threading.Thread(target=add_merchant_message, args=(push_msg, dlist[6]))
                        threads.append(t7)
                        t8 = threading.Thread(target=add_merchant_message, args=(push_msg, dlist[7]))
                        threads.append(t8)
                        t9 = threading.Thread(target=add_merchant_message, args=(push_msg, dlist[8]))
                        threads.append(t9)
                        t10 = threading.Thread(target=add_merchant_message, args=(push_msg, dlist[9]))
                        threads.append(t10)

                        for t in threads:
                            t.setDaemon(True)
                            t.start()
                    else:

                        add_merchant_message(push_msg, userids)
                except Exception, e:
                    log.debug('同步redis出错')
                    log.debug(e)
                    return json.dumps({'ok': False, 'msg': '同步redis出错'},
                                      ensure_ascii=False)

                # 设置推送参数
                extra = set_custom(title=title, actiontype=0, mtype=msg_type, link=push_msg.get('link'),
                                   ref_id=str(push_msg.get('ref_id')),
                                   topic_type=topic_type, post_id='', act=1,
                                   comment_id='', comment_content='', msgid='notice_%d' % push_msg.get('id'))

                extra_dict = set_custom_dict(title=title, actiontype=0, mtype=msg_type, link=push_msg.get('link'),
                                             ref_id=str(push_msg.get('ref_id')),
                                             topic_type=topic_type, post_id='', act=1,
                                             comment_id='', comment_content='', msgid='notice_%d' % push_msg.get('id'))

                if mode == 3 or mode == 0:
                    to = map(str, userids or [])

                log.debug(
                    '一级标签 :%s ,推送方式 %s , 推送标题 %s  推送内容 %s ' % (str(_tag_type), str(mode), str(title), str(content)))
                # log.debug('to_list: %s' % str(to))

                log.debug('推送消息开始....................:')

                # try:
                #
                #     if to and len(to) > 5:
                #
                #         dlist = div_list(to, 5)
                #         threads = []
                #         t1 = threading.Thread(target=push_msg2, args=(unicode2utf8(content), extra,dlist[0],apptypes,platforms,SEND_MODE_USERID))
                #         threads.append(t1)
                #         t2 = threading.Thread(target=push_msg2, args=(unicode2utf8(content), extra,dlist[1],apptypes,platforms,SEND_MODE_USERID))
                #         threads.append(t2)
                #         t3 = threading.Thread(target=push_msg2, args=(unicode2utf8(content), extra,dlist[2],apptypes,platforms,SEND_MODE_USERID))
                #         threads.append(t3)
                #         t4 = threading.Thread(target=push_msg2, args=(unicode2utf8(content), extra,dlist[3],apptypes,platforms,SEND_MODE_USERID))
                #         threads.append(t4)
                #         t5 = threading.Thread(target=push_msg2, args=(unicode2utf8(content), extra,dlist[4],apptypes,platforms,SEND_MODE_USERID))
                #         threads.append(t5)
                #
                #         for t in threads:
                #             t.setDaemon(True)
                #             t.start()
                #
                #     else:
                #         push_msg2(unicode2utf8(content),extra,to,apptypes=apptypes,platforms=platforms,mode=SEND_MODE_USERID)
                # except Exception, e:
                #     log.debug('推送消息出错')
                #     log.debug('thrift_callex pushmsg2 error')
                #     log.debug(e)
                #     return json.dumps({'ok': False, 'msg': '推送消息出错'},
                #                   ensure_ascii=False)

                try:
                    push_msg2(unicode2utf8(content), extra, to, apptypes=apptypes, platforms=platforms,
                              mode=SEND_MODE_USERID)
                except Exception, e:
                    log.debug('推送消息出错')
                    log.debug('thrift_callex pushmsg2 error')
                    log.debug(e)
                    return json.dumps({'ok': False, 'msg': '推送消息出错'},
                                      ensure_ascii=False)

                log.debug('推送消息结束....................:')

                msg = u'消息推送成功'

                # 修改操作
                try:
                    values = {}
                    values['status'] = 1
                    self.db.update(table='mcht_push_message', values=values, where={'id': int(push_msg.get('id'))})
                except Exception, e:
                    log.debug('mysql insert error: %s' % traceback.format_exc())
                    return json.dumps({'ok': False, 'msg': '消息推送失败'},
                                      ensure_ascii=False)

                return json.dumps({'ok': True, 'msg': '消息推送成功'},
                                  ensure_ascii=False)

            except ValueError:
                return json.dumps({'ok': False, 'msg': 'Bad request'},
                                  ensure_ascii=False)
        return json.dumps({'ok': False, 'msg': 'Need json input format'},
                          ensure_ascii=False)


# 消息列表接口
class push_list_api(BaseHandler):
    @with_database([_data_name])
    # def GET(self):
    #     try:
    #         data = self.db.select(table='mcht_push_message',other='order by id desc')
    #     except Exception, e:
    #         log.debug('mysql getdata error: %s' % traceback.format_exc())
    #         return json.dumps({'data': []}, ensure_ascii=False)
    #     for d in data:
    #         #将mysql返回的日期数据类型转换成字符串
    #         d['create_time'] = d['create_time'].strftime("%Y-%m-%d %H:%M:%S")
    #         d['update_time'] = d['update_time'].strftime('%Y-%m-%d %H:%M:%S')
    #         d['send_time'] = d['send_time'].strftime('%Y-%m-%d %H:%M:%S')
    #         d['id'] = str(d['id'])
    #
    #     return json.dumps({'data': data}, ensure_ascii=False)
    def GET(self):
        try:
            conn = self.db[_data_name]
            result = conn.query(
                "select `id`,`title`,`content`,`mtype`,`mode`,`platforms`,`apptypes`,`to`,`actiontype`,`link`,`status`,`ref_title`,`create_time`,`tag_type` from `mcht_push_message` where `create_time` >= '2018-01-01'   order by id desc")
        except Exception, e:
            print e
            log.debug('mysql getdata error: %s' % traceback.format_exc())
            return json.dumps({'data': []}, ensure_ascii=False)
        for d in result:
            # 将mysql返回的日期数据类型转换成字符串
            try:
                d['create_time'] = d['create_time'].strftime("%Y-%m-%d %H:%M:%S")
            except Exception, e:
                d['create_time'] = ''

            d['id'] = str(d['id'])
            d['mtype_str'] = MTYPE_CHOICES[str(d['mtype'])]
            d['mode_str'] = MODE_CHOICES[str(d['mode'])]
            d['tag_type_str'] = d['tag_type'].replace("0", u"直营").replace("1", u"渠道").replace("2", u"白牌")

        return json.dumps({'data': result}, ensure_ascii=False)

    @with_database(_data_name)
    def POST(self):
        if self.req.environ.get('CONTENT_TYPE', '').lower().startswith(
                'application/json'):
            try:
                params = self.req.inputjson()

                # 构造新建的入库的数据
                values = {}
                values['title'] = params.get('title')
                values['content'] = params.get('content')
                values['mode'] = params.get('mode')
                values['to'] = convert_to_comma_delimited_string(params.get('to'))
                values['platforms'] = params.get('platforms')
                values['apptypes'] = params.get('apptypes')
                values['mtype'] = params.get('mtype')
                values['link'] = params.get('link').strip()
                values['actiontype'] = params.get('actiontype')

                values['ref_id'] = 0
                values['ref_type'] = 0
                values['ref_title'] = params.get('ref_title')
                values['tag_type'] = params.get('tag_type')

                # 获取当前的时间
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # 创建的时间
                values['create_time'] = now_time

                # 过滤非法id
                try:
                    values['to'] = id_filter(values['tag_type'], values['mode'], values['to'])
                except Exception, e:
                    print e
                    log.debug('过滤id错误')
                    pass

                # 入库操作
                try:
                    self.db.insert(table='mcht_push_message', values=values)
                except Exception, e:
                    log.debug('mysql insert error: %s' % traceback.format_exc())
                    return json.dumps({'ok': False, 'msg': '新建失败'},
                                      ensure_ascii=False)

                return json.dumps({'ok': True, 'msg': '新建成功'},
                                  ensure_ascii=False)

            except ValueError:
                return json.dumps({'ok': False, 'msg': 'Bad request'},
                                  ensure_ascii=False)
        return json.dumps({'ok': False, 'msg': 'Need json input format'},
                          ensure_ascii=False)

    @with_database(_data_name)
    def PUT(self):
        if self.req.environ.get('CONTENT_TYPE', '').lower().startswith(
                'application/json'):
            try:
                params = self.req.inputjson()

                print params

                # 构造新建的入库的数据
                values = {}
                values['title'] = params.get('title')
                values['content'] = params.get('content')
                values['mode'] = params.get('mode')
                values['to'] = convert_to_comma_delimited_string(params.get('to'))
                values['platforms'] = params.get('platforms')
                values['apptypes'] = params.get('apptypes')
                values['mtype'] = params.get('mtype')
                values['link'] = params.get('link').strip()
                values['actiontype'] = params.get('actiontype')
                values['ref_title'] = params.get('ref_title')
                values['tag_type'] = params.get('tag_type')

                # 过滤非法id
                try:
                    values['to'] = id_filter(values['tag_type'], values['mode'], values['to'])
                except Exception, e:
                    print e
                    log.debug('过滤id错误')
                    pass

                # 获取当前的时间
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # 更新操作
                try:
                    self.db.update(table='mcht_push_message', values=values, where={'id': int(params.get('id'))})
                except Exception, e:
                    print e
                    log.debug('mysql update error: %s' % traceback.format_exc())
                    return json.dumps({'ok': False, 'msg': '修改失败'},
                                      ensure_ascii=False)
                return json.dumps({'ok': True, 'msg': '修改成功'},
                                  ensure_ascii=False)

            except ValueError:
                return json.dumps({'ok': False, 'msg': 'Bad request'},
                                  ensure_ascii=False)
        return json.dumps({'ok': False, 'msg': 'Need json input format'},
                          ensure_ascii=False)


QF_GROUPIDS = [1694779, 20487, 20465, 1709635, 20485, 1725055, 20486, 1725049]


def div_list(ls, n):
    if not isinstance(ls, list) or not isinstance(n, int):
        return []
    ls_len = len(ls)
    if n <= 0 or 0 == ls_len:
        return []
    if n > ls_len:
        return []
    elif n == ls_len:
        return [[i] for i in ls]
    else:
        j = ls_len / n
        k = ls_len % n
        ### j,j,j,...(前面有n-1个j),j+k
        # 步长j,次数n-1
        ls_return = []
        for i in xrange(0, (n - 1) * j, j):
            ls_return.append(ls[i:i + j])
        # 算上末尾的j+k
        ls_return.append(ls[(n - 1) * j:])
        return ls_return


# 过滤id函数
def id_filter(_tag_type, _mode, _to):
    _tolist = _to.split(",")
    for index, item in enumerate(_tolist):
        _tolist[index] = int(item)

    retD = []

    # 渠道列表
    with get_connection('qf_core') as db:
        profiles = db.select(
            table='profile',
            fields='distinct groupid',
            where={'groupid': ('not in', QF_GROUPIDS + BAIPAI_GROUPIDS)}
        )
        QD_GROUPIDS = [i['groupid'] for i in profiles or []]

    # 过滤渠道id
    if (_mode == '3'):
        if _tag_type == '0':
            retD = list(set(_tolist).difference(set(QF_GROUPIDS)))
        elif _tag_type == '1':
            retD = list(set(_tolist).difference(set(QD_GROUPIDS)))
        elif _tag_type == '2':
            retD = list(set(_tolist).difference(set(BAIPAI_GROUPIDS)))
        elif _tag_type == '0,1':
            retD = list(set(_tolist).difference(set(QF_GROUPIDS + QD_GROUPIDS)))
        elif _tag_type == '0,2':
            retD = list(set(_tolist).difference(set(QF_GROUPIDS + BAIPAI_GROUPIDS)))
        elif _tag_type == '1,2':
            retD = list(set(_tolist).difference(set(QD_GROUPIDS + BAIPAI_GROUPIDS)))
    # 过滤商户id
    elif (_mode == '2'):
        if _tag_type == '0':
            with get_connection('qf_core') as db:
                profiles = db.select(
                    table='profile',
                    fields='userid',
                    where={'groupid': ('in', QF_GROUPIDS)}
                )
                userids = [i['userid'] for i in profiles or []]

            retD = list(set(_tolist).difference(set(userids)))
        elif _tag_type == '1':
            with get_connection('qf_core') as db:
                profiles = db.select(
                    table='profile',
                    fields='userid',
                    where={'groupid': ('in', QD_GROUPIDS)}
                )
                userids = [i['userid'] for i in profiles or []]

            retD = list(set(_tolist).difference(set(userids)))
        elif _tag_type == '2':
            with get_connection('qf_core') as db:
                profiles = db.select(
                    table='profile',
                    fields='userid',
                    where={'groupid': ('in', BAIPAI_GROUPIDS)}
                )
                userids = [i['userid'] for i in profiles or []]

            retD = list(set(_tolist).difference(set(userids)))
        elif _tag_type == '0,1':
            with get_connection('qf_core') as db:
                profiles = db.select(
                    table='profile',
                    fields='userid',
                    where={'groupid': ('in', QF_GROUPIDS + QD_GROUPIDS)}
                )
                userids = [i['userid'] for i in profiles or []]

            retD = list(set(_tolist).difference(set(userids)))
        elif _tag_type == '0,2':
            with get_connection('qf_core') as db:
                profiles = db.select(
                    table='profile',
                    fields='userid',
                    where={'groupid': ('in', QF_GROUPIDS + BAIPAI_GROUPIDS)}
                )
                userids = [i['userid'] for i in profiles or []]

            retD = list(set(_tolist).difference(set(userids)))
        elif _tag_type == '1,2':
            with get_connection('qf_core') as db:
                profiles = db.select(
                    table='profile',
                    fields='userid',
                    where={'groupid': ('in', QD_GROUPIDS + BAIPAI_GROUPIDS)}
                )
                userids = [i['userid'] for i in profiles or []]

            retD = list(set(_tolist).difference(set(userids)))

    if _tag_type != '0,1,2':

        for i in retD:
            _tolist.remove(i)

        for index, item in enumerate(_tolist):
            _tolist[index] = str(item)

    _tolist = ','.join(_tolist)

    return _tolist


class BaseHandler(core.Handler):
    def __init__(self, app, req):
        super(BaseHandler, self).__init__(app, req)
        self.resp.mimetype = 'application/json'
        self.resp.headers['Content-Type'] = '%s; charset=%s' % (
            self.resp.mimetype, self.resp.charset)


class ret2template(core.Handler):
    @checkIsLogin
    def GET(self):
        uname = self.get_cookie('uname')
        data = {}
        data['uname'] = uname
        self.write(template.render("push_message.html", data=data))


# 消息列表页面
class push_list(core.Handler):
    @checkIsLogin
    def GET(self):
        uname = self.get_cookie('uname')
        data = {}
        data['uname'] = uname
        self.write(template.render("push_list.html", data=data))


# 推送到消息中心
def add_merchant_message(mcht_msg, to=None):
    """好近专用:添加好近商户版消息至Redis"""
    if to is not None:
        user_ids = to
    else:
        user_ids = [int(uid) for uid in mcht_msg.get('to').split(',')]

    # 添加至消息中心
    handler = MerchantMessageHandler()
    for user_id in user_ids:
        msg_id = gen_msg_id()
        msg = gen_mcht_msg(msg_id, int(mcht_msg.get('mtype')), str(mcht_msg.get('title')), str(mcht_msg.get('content')),
                           str(mcht_msg.get('ref_id')),
                           int(mcht_msg.get('ref_type')), str(mcht_msg.get('ref_title')),
                           int(mcht_msg.get('actiontype')), str(mcht_msg.get('link')), now2str())
        handler.add_message(0, int(user_id), msg_id, msg)


# 消息推送动作
class push_act(BaseHandler):
    @with_database(_data_name)
    def POST(self):
        if self.req.environ.get('CONTENT_TYPE', '').lower().startswith(
                'application/json'):
            try:
                params = self.req.inputjson()

                push_msg = {}
                push_msg['title'] = params.get('title')
                push_msg['content'] = params.get('content')
                push_msg['mode'] = params.get('mode')
                push_msg['to'] = params.get('to')
                push_msg['platforms'] = params.get('platforms')
                push_msg['apptypes'] = params.get('apptypes')
                push_msg['mtype'] = int(params.get('mtype'))
                push_msg['link'] = params.get('link')
                push_msg['actiontype'] = int(params.get('actiontype'))
                push_msg['id'] = int(params.get('push_id'))

                push_msg['ref_id'] = 0
                push_msg['ref_type'] = 0
                push_msg['ref_title'] = params.get('ref_title')

                title = push_msg.get('title')
                content = push_msg.get('content')
                ref_id = push_msg.get('ref_id')
                _tag_type = str(params.get('tag_type'))

                apptypes = [int(item) for item in push_msg.get('apptypes').split(',')]
                platforms = [int(item) for item in push_msg.get('platforms').split(',')]
                for index, item in enumerate(apptypes):
                    if item == 5:
                        apptypes[index] = 402
                    elif item == 6:
                        apptypes[index] = 401
                    elif item == 7:
                        apptypes[index] = 412
                    elif item == 8:
                        apptypes[index] = 411
                    elif item == 9:
                        apptypes[index] = 9010
                    elif item == 10:
                        apptypes[index] = 9011
                    elif item == 12:
                        apptypes[index] = 9012
                    elif item == 13:
                        apptypes[index] = 9013
                    elif item == 14:
                        apptypes[index] = 9014
                mode = int(push_msg.get('mode'))

                to = [str(item) for item in push_msg.get('to').split(',')]
                # ------ 提出的处理方式  -------#
                topic_type = 0
                msg_type = 3  # 0 运营小 1 买单 2 外卖订单 3 消息中心
                # actiontype 0 不跳转 1 跳转
                if push_msg.get('actiontype') == 1 and push_msg.get('mtype') == 1:
                    msg_actiontype = 1
                else:
                    msg_actiontype = 0

                userids = None
                # 如果按照渠道推送需要通过profile查出userid
                try:
                    if mode == 3:
                        with get_connection('qf_core') as db:
                            groupids = map(int, to)
                            profiles = db.select(
                                table='profile',
                                fields='userid',
                                where={'groupid': ('in', groupids)}
                            )
                            userids = [i['userid'] for i in profiles or []]

                    if mode == 0:

                        # 渠道列表
                        with get_connection('qf_core') as db:
                            profiles = db.select(
                                table='profile',
                                fields='distinct groupid',
                                where={'groupid': ('not in', QF_GROUPIDS + BAIPAI_GROUPIDS)}
                            )
                            QD_GROUPIDS = [i['groupid'] for i in profiles or []]

                        log.debug('全渠道列表长度: %s' % str(len(QD_GROUPIDS)))

                        if _tag_type == '0':
                            _aqd_list = QF_GROUPIDS
                        elif _tag_type == '1':
                            _aqd_list = QD_GROUPIDS
                        elif _tag_type == '2':
                            _aqd_list = BAIPAI_GROUPIDS
                        elif _tag_type == '0,1':
                            _aqd_list = QF_GROUPIDS + QD_GROUPIDS
                        elif _tag_type == '0,2':
                            _aqd_list = QF_GROUPIDS + BAIPAI_GROUPIDS
                        elif _tag_type == '1,2':
                            _aqd_list = QD_GROUPIDS + BAIPAI_GROUPIDS
                        elif _tag_type == '0,1,2':
                            _aqd_list = QF_GROUPIDS + QD_GROUPIDS + BAIPAI_GROUPIDS

                        with get_connection('qf_core') as db:
                            profiles = db.select(
                                table='profile',
                                fields='distinct userid',
                                where={'groupid': ('in', _aqd_list)}
                            )
                            userids = [i['userid'] for i in profiles or []]
                except Exception, e:
                    log.debug('读取mysql过滤报错')
                    log.debug(e)
                    return json.dumps({'ok': False, 'msg': '读取mysql过滤报错'},
                                      ensure_ascii=False)

                try:
                    log.debug('全用户列表长度: %s' % str(len(userids)))
                except Exception, e:
                    print e
                    pass

                try:
                    if userids and len(userids) > 10:
                        dlist = div_list(userids, 10)
                        threads = []
                        t1 = threading.Thread(target=add_merchant_message, args=(push_msg, dlist[0]))
                        threads.append(t1)
                        t2 = threading.Thread(target=add_merchant_message, args=(push_msg, dlist[1]))
                        threads.append(t2)
                        t3 = threading.Thread(target=add_merchant_message, args=(push_msg, dlist[2]))
                        threads.append(t3)
                        t4 = threading.Thread(target=add_merchant_message, args=(push_msg, dlist[3]))
                        threads.append(t4)
                        t5 = threading.Thread(target=add_merchant_message, args=(push_msg, dlist[4]))
                        threads.append(t5)

                        t6 = threading.Thread(target=add_merchant_message, args=(push_msg, dlist[5]))
                        threads.append(t6)
                        t7 = threading.Thread(target=add_merchant_message, args=(push_msg, dlist[6]))
                        threads.append(t7)
                        t8 = threading.Thread(target=add_merchant_message, args=(push_msg, dlist[7]))
                        threads.append(t8)
                        t9 = threading.Thread(target=add_merchant_message, args=(push_msg, dlist[8]))
                        threads.append(t9)
                        t10 = threading.Thread(target=add_merchant_message, args=(push_msg, dlist[9]))
                        threads.append(t10)

                        for t in threads:
                            t.setDaemon(True)
                            t.start()
                    else:

                        add_merchant_message(push_msg, userids)
                except Exception, e:
                    log.debug('同步redis出错')
                    log.debug(e)
                    return json.dumps({'ok': False, 'msg': '同步redis出错'},
                                      ensure_ascii=False)

                # 设置推送参数
                extra = set_custom(title=title, actiontype=0, mtype=msg_type, link=push_msg.get('link'),
                                   ref_id=str(push_msg.get('ref_id')),
                                   topic_type=topic_type, post_id='', act=1,
                                   comment_id='', comment_content='', msgid='notice_%d' % push_msg.get('id'))

                extra_dict = set_custom_dict(title=title, actiontype=0, mtype=msg_type, link=push_msg.get('link'),
                                             ref_id=str(push_msg.get('ref_id')),
                                             topic_type=topic_type, post_id='', act=1,
                                             comment_id='', comment_content='', msgid='notice_%d' % push_msg.get('id'))

                if mode == 3 or mode == 0:
                    to = map(str, userids or [])

                log.debug(
                    '一级标签 :%s ,推送方式 %s , 推送标题 %s  推送内容 %s ' % (str(_tag_type), str(mode), str(title), str(content)))
                # log.debug('to_list: %s' % str(to))

                log.debug('推送消息开始....................:')

                # try:
                #
                #     if to and len(to) > 5:
                #
                #         dlist = div_list(to, 5)
                #         threads = []
                #         t1 = threading.Thread(target=push_msg2, args=(unicode2utf8(content), extra,dlist[0],apptypes,platforms,SEND_MODE_USERID))
                #         threads.append(t1)
                #         t2 = threading.Thread(target=push_msg2, args=(unicode2utf8(content), extra,dlist[1],apptypes,platforms,SEND_MODE_USERID))
                #         threads.append(t2)
                #         t3 = threading.Thread(target=push_msg2, args=(unicode2utf8(content), extra,dlist[2],apptypes,platforms,SEND_MODE_USERID))
                #         threads.append(t3)
                #         t4 = threading.Thread(target=push_msg2, args=(unicode2utf8(content), extra,dlist[3],apptypes,platforms,SEND_MODE_USERID))
                #         threads.append(t4)
                #         t5 = threading.Thread(target=push_msg2, args=(unicode2utf8(content), extra,dlist[4],apptypes,platforms,SEND_MODE_USERID))
                #         threads.append(t5)
                #
                #         for t in threads:
                #             t.setDaemon(True)
                #             t.start()
                #
                #     else:
                #         push_msg2(unicode2utf8(content),extra,to,apptypes=apptypes,platforms=platforms,mode=SEND_MODE_USERID)
                # except Exception, e:
                #     log.debug('推送消息出错')
                #     log.debug('thrift_callex pushmsg2 error')
                #     log.debug(e)
                #     return json.dumps({'ok': False, 'msg': '推送消息出错'},
                #                   ensure_ascii=False)

                try:
                    push_msg2(unicode2utf8(content), extra, to, apptypes=apptypes, platforms=platforms,
                              mode=SEND_MODE_USERID)
                except Exception, e:
                    log.debug('推送消息出错')
                    log.debug('thrift_callex pushmsg2 error')
                    log.debug(e)
                    return json.dumps({'ok': False, 'msg': '推送消息出错'},
                                      ensure_ascii=False)

                log.debug('推送消息结束....................:')

                msg = u'消息推送成功'

                # 修改操作
                try:
                    values = {}
                    values['status'] = 1
                    self.db.update(table='mcht_push_message', values=values, where={'id': int(push_msg.get('id'))})
                except Exception, e:
                    log.debug('mysql insert error: %s' % traceback.format_exc())
                    return json.dumps({'ok': False, 'msg': '消息推送失败'},
                                      ensure_ascii=False)

                return json.dumps({'ok': True, 'msg': '消息推送成功'},
                                  ensure_ascii=False)

            except ValueError:
                return json.dumps({'ok': False, 'msg': 'Bad request'},
                                  ensure_ascii=False)
        return json.dumps({'ok': False, 'msg': 'Need json input format'},
                          ensure_ascii=False)


# 消息列表接口
class push_list_api(BaseHandler):
    @with_database([_data_name])
    # def GET(self):
    #     try:
    #         data = self.db.select(table='mcht_push_message',other='order by id desc')
    #     except Exception, e:
    #         log.debug('mysql getdata error: %s' % traceback.format_exc())
    #         return json.dumps({'data': []}, ensure_ascii=False)
    #     for d in data:
    #         #将mysql返回的日期数据类型转换成字符串
    #         d['create_time'] = d['create_time'].strftime("%Y-%m-%d %H:%M:%S")
    #         d['update_time'] = d['update_time'].strftime('%Y-%m-%d %H:%M:%S')
    #         d['send_time'] = d['send_time'].strftime('%Y-%m-%d %H:%M:%S')
    #         d['id'] = str(d['id'])
    #
    #     return json.dumps({'data': data}, ensure_ascii=False)
    def GET(self):
        try:
            conn = self.db[_data_name]
            result = conn.query(
                "select `id`,`title`,`content`,`mtype`,`mode`,`platforms`,`apptypes`,`to`,`actiontype`,`link`,`status`,`ref_title`,`create_time`,`tag_type` from `mcht_push_message` where `create_time` >= '2018-01-01'   order by id desc")
        except Exception, e:
            print e
            log.debug('mysql getdata error: %s' % traceback.format_exc())
            return json.dumps({'data': []}, ensure_ascii=False)
        for d in result:
            # 将mysql返回的日期数据类型转换成字符串
            try:
                d['create_time'] = d['create_time'].strftime("%Y-%m-%d %H:%M:%S")
            except Exception, e:
                d['create_time'] = ''

            d['id'] = str(d['id'])
            d['mtype_str'] = MTYPE_CHOICES[str(d['mtype'])]
            d['mode_str'] = MODE_CHOICES[str(d['mode'])]
            d['tag_type_str'] = d['tag_type'].replace("0", u"直营").replace("1", u"渠道").replace("2", u"白牌")

        return json.dumps({'data': result}, ensure_ascii=False)

    @with_database(_data_name)
    def POST(self):
        if self.req.environ.get('CONTENT_TYPE', '').lower().startswith(
                'application/json'):
            try:
                params = self.req.inputjson()

                # 构造新建的入库的数据
                values = {}
                values['title'] = params.get('title')
                values['content'] = params.get('content')
                values['mode'] = params.get('mode')
                values['to'] = convert_to_comma_delimited_string(params.get('to'))
                values['platforms'] = params.get('platforms')
                values['apptypes'] = params.get('apptypes')
                values['mtype'] = params.get('mtype')
                values['link'] = params.get('link').strip()
                values['actiontype'] = params.get('actiontype')

                values['ref_id'] = 0
                values['ref_type'] = 0
                values['ref_title'] = params.get('ref_title')
                values['tag_type'] = params.get('tag_type')

                # 获取当前的时间
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # 创建的时间
                values['create_time'] = now_time

                # 过滤非法id
                try:
                    values['to'] = id_filter(values['tag_type'], values['mode'], values['to'])
                except Exception, e:
                    print e
                    log.debug('过滤id错误')
                    pass

                # 入库操作
                try:
                    self.db.insert(table='mcht_push_message', values=values)
                except Exception, e:
                    log.debug('mysql insert error: %s' % traceback.format_exc())
                    return json.dumps({'ok': False, 'msg': '新建失败'},
                                      ensure_ascii=False)

                return json.dumps({'ok': True, 'msg': '新建成功'},
                                  ensure_ascii=False)

            except ValueError:
                return json.dumps({'ok': False, 'msg': 'Bad request'},
                                  ensure_ascii=False)
        return json.dumps({'ok': False, 'msg': 'Need json input format'},
                          ensure_ascii=False)

    @with_database(_data_name)
    def PUT(self):
        if self.req.environ.get('CONTENT_TYPE', '').lower().startswith(
                'application/json'):
            try:
                params = self.req.inputjson()

                print params

                # 构造新建的入库的数据
                values = {}
                values['title'] = params.get('title')
                values['content'] = params.get('content')
                values['mode'] = params.get('mode')
                values['to'] = convert_to_comma_delimited_string(params.get('to'))
                values['platforms'] = params.get('platforms')
                values['apptypes'] = params.get('apptypes')
                values['mtype'] = params.get('mtype')
                values['link'] = params.get('link').strip()
                values['actiontype'] = params.get('actiontype')
                values['ref_title'] = params.get('ref_title')
                values['tag_type'] = params.get('tag_type')

                # 过滤非法id
                try:
                    values['to'] = id_filter(values['tag_type'], values['mode'], values['to'])
                except Exception, e:
                    print e
                    log.debug('过滤id错误')
                    pass

                # 获取当前的时间
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # 更新操作
                try:
                    self.db.update(table='mcht_push_message', values=values, where={'id': int(params.get('id'))})
                except Exception, e:
                    print e
                    log.debug('mysql update error: %s' % traceback.format_exc())
                    return json.dumps({'ok': False, 'msg': '修改失败'},
                                      ensure_ascii=False)
                return json.dumps({'ok': True, 'msg': '修改成功'},
                                  ensure_ascii=False)

            except ValueError:
                return json.dumps({'ok': False, 'msg': 'Bad request'},
                                  ensure_ascii=False)
        return json.dumps({'ok': False, 'msg': 'Need json input format'},
                          ensure_ascii=False)
