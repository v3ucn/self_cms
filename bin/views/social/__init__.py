# -*- coding: utf-8 -*-
from .social_para import validParam, nullOk, multiType


@validParam(str, multiType(int, long, basestring), nullOk(str))
def gen_key(obj, obj_id, op=None, op_id='', op_type=''):
    """设置Redis SortedSet 的 key
    user_1124_followers    用户1124的粉丝

    :param obj: 对象 user topic posts comments circle
    :param obj_id: 对象ID
    :param op: 动作,
    :param op_type: 操作对象类型
    :return:
    """
    prefix = 'near'
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
