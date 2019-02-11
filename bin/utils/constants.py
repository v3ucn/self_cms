#coding=utf8

DATE_FMT     = '%Y-%m-%d'          # 日期格式
DATETIME_FMT = '%Y-%m-%d %H:%M:%S' # 日期时间格式

class MpconfDef(object):
    CHNLCODE = FUIOU, MY = (3, 9)
    CHNLCODE_STR = {
        FUIOU:'fuiou',
        MY:'my'
    }
    CHNLCODE_DICT = {
        FUIOU: '富友',
        MY: '网商'
    }

class TagDef(object):
    TAG_STATUS = (TAG_VALID, TAG_INVALID) = (1, 0)
    TAG_STATUS_DICT = {
        TAG_VALID: '有效',
        TAG_INVALID: '无效',
    }
    VIRTUAL_USER_ID = 1
