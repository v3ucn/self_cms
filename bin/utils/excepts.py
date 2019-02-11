# encoding:utf-8

from qfcommon.qfpay.qfresponse import QFRET

class SLAException(Exception):

    def __init__(self, errmsg, errcode=QFRET.PARAMERR):
        self.errmsg  = errmsg
        self.errcode = errcode

    def __str__(self):
        return '[code:%s] errormsg:%s' % (self.errcode, self.errmsg)


class SessionError(SLAException):

    def __init(self, errmsg):
        super(SessionError, self).__init__(QFRET.SESSIONERR, errmsg)

class ParamError(SLAException):

    def __init(self, errmsg):
        super(ParamError, self).__init__(QFRET.PARAMERR, errmsg)

class ThirdError(SLAException):

    def __init(self, errmsg):
        super(ThirdError, self).__init__(QFRET.THIRDERR, errmsg)

class DBError(SLAException):

    def __init(self, errmsg):
        super(DBError, self).__init__(QFRET.DBError, errmsg)
