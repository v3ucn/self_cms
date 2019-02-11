# encoding:utf-8
import redis
from protobuf_to_dict import protobuf_to_dict

# from utils.utils import model2dict
from message_pb2 import Msg, User


if __name__ == '__main__':
    u = User(user_id=18, nickname='piggy',
             avatar="http://wx.qlogo.cn/mmopen/Q3auHgzwzM4dVYs8mZwibbCyuEDa2lZlYC1iaczEmetrjlSX4bYEoic5DLnrvVscD20R03eRlMJmGjfRNXfgJC3Sw/0")
    m = Msg(msg_id='1', type=0, content=u'您创建的话题有新内容', topic_id='1234', topic_name=u'望京soho拼车必杀技',
            post_id='123', post_img='http://www.baidu.jgp', timestamp="2015-05-28 22:57:39", users=[u, u])
    r = redis.Redis(host='172.100.102.101', port=6379, db=1)
    m_serialize = m.SerializeToString()
    # print len(m_serialize)
    # r.set('near_userid_10004_protobuf', m_serialize)

    # u1 = {"user_id":18, "nickname":'piggy', "avatar":"http://wx.qlogo.cn/mmopen/Q3auHgzwzM4dVYs8mZwibbCyuEDa2lZlYC1iaczEmetrjlSX4bYEoic5DLnrvVscD20R03eRlMJmGjfRNXfgJC3Sw/0"}
    # m1 = {"msg_id": '1',
    #       "type": 0,
    #       "content": u"您创建的话题有新内容",
    #       "topic_id": "1234",
    #       "topic_name": u"望京soho拼车必杀技",
    #       "post_id": "123",
    #       "post_img": "http://www.baidu.jpg",
    #       "timestamp": "2015-05-28 22:57:39",
    #       "users": [u1, u1]}
    # r.set('near_userid_10004_json', m)

    v = r.get('near_userid_10004_protobuf')
    out_m = Msg()
    out_m.ParseFromString(v)
    # print 'protobuf, v:', v, 'len:', len(v)
    # print 'out_m', out_m
    # print '__dict__', dir(out_m)
    # dict_m = model2dict(out_m)
    # print 'type:', type(dict_m)
    print 'dict:', protobuf_to_dict(out_m)


    # v1 = r.get('near_userid_10004_json')
    # print 'json, v:', v1, 'len:', len(v1)