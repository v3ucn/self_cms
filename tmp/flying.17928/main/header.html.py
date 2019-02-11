# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1529461547.417461
_enable_loop = True
_template_filename = u'templates/main/header.html'
_template_uri = u'main/header.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        data = context.get('data', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n<div class="container-fluid">\n  <div class="navbar-header">\n    <div class="brand">\n      <a class="navbar-brand"\n         href="/index"><span>\u94b1\u65b9\u8fd0\u8425\u7ba1\u7406\u7cfb\u7edf</span></a>\n    </div>\n  </div>\n  <div class="login">\n     \u6b22\u8fce\uff1a<em>')
        __M_writer(filters.decode.utf8(data.get('uname')))
        __M_writer(u'</em>\n     <span>|</span>\n     <a href="/exit">\u9000\u51fa</a>\n  </div>\n</div>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"16": 0, "24": 11, "30": 24, "22": 2, "23": 11}, "uri": "main/header.html", "filename": "templates/main/header.html"}
__M_END_METADATA
"""
