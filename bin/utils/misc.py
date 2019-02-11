# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
"""
日期
"""
import re
import json
import types
import time
import datetime
import random
import unittest

# 日期格式
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
TIME_ONLY_FORMAT = '%H:%M:%S'

date_pattern = re.compile("\d+\-\d+\-\d+")
time_pattern = re.compile("\d+-\d+-\d+ \d+:\d+:\d+")


def time2date(timestamp):
    """
    将时间戳转换成日期
    :param timestamp: 时间戳 eg:1426231925.17
    :return: datetime eg: 2015-03-13 15:33:00.598979
    """
    return datetime.datetime.fromtimestamp(time.time())


def get_match_pattern(dstr):
    fm = TIME_FORMAT
    if time_pattern.search(dstr):
        fm = TIME_FORMAT
    elif date_pattern.search(dstr):
        fm = DATE_FORMAT
    return fm


def now2str(ftype=TIME_FORMAT):
    return datetime2str(datetime.datetime.now(), ftype)


def datetime2str(t, ftype=TIME_FORMAT):
    return t.strftime(ftype)


def timestamp2str(ts):
    return datetime2str(datetime.datetime.fromtimestamp(ts))


def timestamp2datestr(ts):
    return datetime2str(datetime.datetime.fromtimestamp(ts), ftype=DATE_FORMAT)


def str2datetime(dstr, fm=None):
    if not fm:
        fm = get_match_pattern(dstr.strip())
    return datetime.datetime.strptime(dstr, fm)


def date2timestamp(t):
    dstr = datetime2str(t, TIME_FORMAT)
    return time.mktime(time.strptime(dstr, TIME_FORMAT))


def str2timestamp(dstr):
    return time.mktime(time.strptime(dstr, TIME_FORMAT))


def minus_seconds(d1, d2):
    minus = d1 - d2
    days = minus.days
    seconds = (days * 3600 * 12) + minus.seconds
    return seconds


def get_day_begin(ts=time.time()):
    """
    获取时间戳ts当天的起始时间戳
    """
    return int(time.mktime(time.strptime(time.strftime('%Y-%m-%d', time.localtime(ts)), '%Y-%m-%d')))


def get_day_begin_datetime(offset=0):
    """
    获取当天起始时间字符串
    offset: int 日期偏移量
    """
    time_begin = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(offset), datetime.time.min)
    return time_begin


def yuan2cent(value):
    return int(round(value * 100))


def cent2yuan(value):
    val = int(value)
    return float(str(val / 100) + '.' + ('%02d' % (val % 100)))

def randomStr(n=16):
    '''generate a SHORT random string include digits and letters.
    '''
    SAMPLE = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join([random.choice(SAMPLE) for _i in xrange(n)])


"""
编码处理
"""


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


def seconds2timestr(seconds):
    """
    秒 数 转换 时间字符串
    :param seconds:
    :return:
    """
    seconds = int(seconds)
    left, sec = divmod(seconds, 60)
    hour, min = divmod(left, 60)
    tm = datetime.time(hour, min, sec)
    timestr = datetime2str(tm, TIME_ONLY_FORMAT)
    return timestr


def timestr2seconds(timestr):
    """
    时间字符串 转变为 总 秒数
    :param timestr:
    :return:
    """
    ft = time.strptime(timestr, '%H:%M:%S')
    return datetime.timedelta(hours=ft.tm_hour, minutes=ft.tm_min, seconds=ft.tm_sec).seconds


def datetime2seconds(ft):
    """
    时间 datetime 转变为 总 秒数
    :param timestr:
    :return:
    """
    return datetime.timedelta(hours=ft.hour, minutes=ft.minute, seconds=ft.second).seconds


def convert_to_comma_delimited_string(input_string):
    """
    接受以逗号， 换行， 空格分割的字符串，统一装换成逗号分割的字符串
    """
    # convert to utf8
    if isinstance(input_string, types.UnicodeType):
        input_string = input_string.encode('utf8')
        pass

    if not input_string:
        return ''

    # conver comman to blank
    s = input_string.replace(',', ' ')
    
    # split by blank
    s = s.strip().split()

    # exclude empty
    s = filter(None, s)

    # join by ,
    s = ','.join(s)

    return s.decode('utf8')

class TestMisc(unittest.TestCase):
    def test_to_convert_to_comma_delimited_string(self):
        a = ''
        self.assertTrue(a == convert_to_comma_delimited_string(a))

        a = u''
        self.assertTrue(a == convert_to_comma_delimited_string(a))

        a = u'a,b,'

        retval = convert_to_comma_delimited_string(a)
        self.assertTrue(u'a,b' == retval)

        #
        a = u'哈哈,a'
        retval = convert_to_comma_delimited_string(a)
        self.assertTrue(a == retval)

        #
        a = '1, 2,, b ,, '
        retval = convert_to_comma_delimited_string(a)
        self.assertTrue('1,2,b' == retval)
