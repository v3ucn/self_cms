# vim: set ts=4 et sw=4 sts=4 fileencoding=utf-8 :

import logging
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
        self.write(template.render('audit_black.html', data=data))
