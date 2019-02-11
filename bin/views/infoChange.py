import logging
from qfcommon.web import core
from qfcommon.web import template
from tools import checkIsLogin


class Page(core.Handler):
    @checkIsLogin
    def GET(self):
        uname = self.get_cookie('uname')
        data = {}
        data['uname'] = uname
        self.write(template.render('infoChange.html',data = data))