# vim: set ts=4 et sw=4 sts=4 fileencoding=utf-8 :

import os
import sys
import logging
import time
from qfcommon.web import core
from qfcommon.web import template
from qfcommon.base.dbpool import with_database
from tools import checkIsLogin

import config

log = logging.getLogger()


class Index(core.Handler):
    # @with_database('test')
    @checkIsLogin
    def GET(self):
        log.debug('headers %s', self.req.headers())
        log.debug('get cookie %s' % self.req.cookie)

        # data = self.db.query('show processlist')
        data = {}


        t = str(time.time())
        log.debug('set cookie time: %s', t)

        self.resp.set_cookie('time', t, expires=int(time.time()) + 20 )

        uname = self.get_cookie('uname')
        data['uname'] = uname
        return self.write(template.render('index.html', data=data))

    @checkIsLogin
    def POST(self):
        data = self.req.input()
        self.write(str(data))


