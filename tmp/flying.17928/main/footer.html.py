# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1529461547.431107
_enable_loop = True
_template_filename = u'templates/main/footer.html'
_template_uri = u'main/footer.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n<div class="container">\n  <small>\n    Copyright \xa9 2018 \u5317\u4eac\u94b1\u65b9\u94f6\u901a\u79d1\u6280\u6709\u9650\u516c\u53f8\n\n')
        __M_writer(u'  </small>\n</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"16": 0, "28": 22, "21": 2, "22": 13}, "uri": "main/footer.html", "filename": "templates/main/footer.html"}
__M_END_METADATA
"""
