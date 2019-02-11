import logging
import time
from qfcommon.web import core
from qfcommon.web import template
from tools import checkIsLogin
from qfcommon.base.dbpool import with_database
import json
import config

log = logging.getLogger()


class Page(core.Handler):
    @checkIsLogin
    def GET(self):
        data = {}
        uname = self.get_cookie('uname')
        data['uname'] = uname
        self.write(template.render('trade.html',data=data))


class GetData(core.Handler):
    @checkIsLogin
    @with_database(['qf_fund2'])
    def POST(self):
        try:
            fund2_result = self.db['qf_fund2'].select(table='channel', fields=['id', 'name'])
        except Exception, e:
            return json.dumps({'code': 0, 'msg': 'fail', 'data': []})
        return json.dumps({'code': 200, 'msg': 'success', 'data': fund2_result})