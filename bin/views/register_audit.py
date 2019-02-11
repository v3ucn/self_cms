import logging
import time
from qfcommon.web import core
from qfcommon.web import template
from tools import checkIsLogin
import config
from qfcommon.base.dbpool import with_database
import json

log = logging.getLogger()
unicode_to_utf8 = lambda s: s.encode('utf-8') if isinstance(s, unicode) else s

class Page(core.Handler):
    @checkIsLogin
    def GET(self):
        uname = self.get_cookie('uname')
        data = {}
        data['uname'] = uname
        self.write(template.render('register_audit.html',data = data))


class GetGroups(core.Handler):
    @with_database(['qf_qudao'])
    def POST(self):
        params = self.req.input()
        result = self.db['qf_qudao'].select(table='qd_profile',fields=['qd_uid','name'])
        return json.dumps({'code':200,'msg':'success','data':result},ensure_ascii=False)


