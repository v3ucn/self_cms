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
        data = {}
        uname = self.get_cookie('uname')
        data['uname'] = uname
        self.write(template.render('tradeCode.html',data=data))