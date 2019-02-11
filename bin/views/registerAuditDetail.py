import logging
import time
from qfcommon.web import core
from qfcommon.web import template
from tools import checkIsLogin

import config

log = logging.getLogger()


class Page(core.Handler):
    @checkIsLogin
    def GET(self):
        uname = self.get_cookie('uname')
        data = {}
        data['uname'] = uname
        params = self.req.input()
        userid = params.get('userid')
        aid = params.get('aid')
        data['userid'] = userid
        data['aid'] = aid

        self.write(template.render('register_audit_detail.html',data = data))