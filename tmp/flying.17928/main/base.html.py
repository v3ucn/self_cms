# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1529461547.402074
_enable_loop = True
_template_filename = u'templates/main/base.html'
_template_uri = u'main/base.html'
_source_encoding = 'utf-8'
_exports = [u'base_body_media', u'base_addition_header', u'base_body_main', u'title']


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        def base_body_media():
            return render_base_body_media(context._locals(__M_locals))
        def base_addition_header():
            return render_base_addition_header(context._locals(__M_locals))
        def base_body_main():
            return render_base_body_main(context._locals(__M_locals))
        def title():
            return render_title(context._locals(__M_locals))
        __M_writer = context.writer()
        __M_writer(u'\n<!DOCTYPE html>\n<html>\n<head>\n  <title>\n      ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'title'):
            context['self'].title(**pageargs)
        

        __M_writer(u'\n  </title>\n  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n  <meta name="viewport"\n        content="width=device-width, initial-scale=1, shrink-to-fit=no">\n  <link rel="shortcut icon" href="/static/common/img/favicon.ico">\n  <link rel="stylesheet" href="/static/common/css/bootstrap-3.3.7.min.css">\n  <link rel="stylesheet" href="/static/common/css/font-awesome-4.7.0.min.css">\n  <link rel="stylesheet" href="/static/common/css/toastr.css">\n  <script type="text/javascript" src="/static/common/js/jquery-3.2.1.min.js"></script>\n  <script type="text/javascript" src="/static/common/js/bootstrap-3.3.7.min.js"></script>\n  <script type="text/javascript" src="/static/common/js/toastr.js"></script>\n  ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'base_addition_header'):
            context['self'].base_addition_header(**pageargs)
        

        __M_writer(u'\n</head>\n<body>\n  ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'base_body_main'):
            context['self'].base_body_main(**pageargs)
        

        __M_writer(u'\n  ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'base_body_media'):
            context['self'].base_body_media(**pageargs)
        

        __M_writer(u'\n</body>\n</html>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_base_body_media(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def base_body_media():
            return render_base_body_media(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_base_addition_header(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def base_addition_header():
            return render_base_addition_header(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_base_body_main(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def base_body_main():
            return render_base_body_main(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def title():
            return render_title(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"34": 7, "99": 88, "39": 19, "44": 22, "66": 19, "77": 22, "16": 0, "49": 23, "55": 23, "88": 7, "29": 2}, "uri": "main/base.html", "filename": "templates/main/base.html"}
__M_END_METADATA
"""
