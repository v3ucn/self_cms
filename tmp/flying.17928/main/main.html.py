# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1529461547.380696
_enable_loop = True
_template_filename = u'templates/main/main.html'
_template_uri = u'main/main.html'
_source_encoding = 'utf-8'
_exports = [u'body_media', u'addition_header', u'base_body_main', u'base_addition_header', u'base_body_media', u'page']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'base.html', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        def body_media():
            return render_body_media(context._locals(__M_locals))
        def addition_header():
            return render_addition_header(context._locals(__M_locals))
        def base_body_main():
            return render_base_body_main(context._locals(__M_locals))
        def base_addition_header():
            return render_base_addition_header(context._locals(__M_locals))
        def base_body_media():
            return render_base_body_media(context._locals(__M_locals))
        def page():
            return render_page(context._locals(__M_locals))
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'base_addition_header'):
            context['self'].base_addition_header(**pageargs)
        

        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'base_body_main'):
            context['self'].base_body_main(**pageargs)
        

        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'base_body_media'):
            context['self'].base_body_media(**pageargs)
        

        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_body_media(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def body_media():
            return render_body_media(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_addition_header(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def addition_header():
            return render_addition_header(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_base_body_main(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def base_body_main():
            return render_base_body_main(context)
        def page():
            return render_page(context)
        __M_writer = context.writer()
        __M_writer(u'\n  <header>\n    <nav class="navbar navbar-default navbar-fixed-top" role="navigation">\n        ')
        runtime._include_file(context, u'header.html', _template_uri)
        __M_writer(u'\n    </nav>\n  </header>\n\n  <div class="body slide">\n    <aside class="sidebar show perfectScrollbar">\n      <div id="solso-sidebar">\n          ')
        runtime._include_file(context, u'menu.html', _template_uri)
        __M_writer(u'\n      </div>\n    </aside>\n    <div class="container-fluid">\n      <div class="row">\n        <div class="col-md-12 col-lg-12 bottom40 top40">\n            ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'page'):
            context['self'].page(**pageargs)
        

        __M_writer(u'\n        </div>\n        <div class="footer">\n            ')
        runtime._include_file(context, u'footer.html', _template_uri)
        __M_writer(u'\n        </div>\n      </div>\n    </div>\n  </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_base_addition_header(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def base_addition_header():
            return render_base_addition_header(context)
        def addition_header():
            return render_addition_header(context)
        __M_writer = context.writer()
        __M_writer(u'\n  <link rel="stylesheet" href="/static/main/css/main.css">\n  <script src="/static/main/js/main.js?v=0.0.1"></script>\n  ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'addition_header'):
            context['self'].addition_header(**pageargs)
        

        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_base_body_media(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def base_body_media():
            return render_base_body_media(context)
        def body_media():
            return render_body_media(context)
        __M_writer = context.writer()
        __M_writer(u'\n  ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'body_media'):
            context['self'].body_media(**pageargs)
        

        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_page(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def page():
            return render_page(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"132": 37, "140": 37, "145": 38, "151": 27, "27": 0, "162": 151, "44": 2, "45": 3, "50": 9, "55": 35, "60": 39, "66": 38, "77": 8, "88": 11, "96": 11, "97": 14, "98": 14, "99": 21, "100": 21, "105": 27, "106": 30, "107": 30, "113": 5, "121": 5, "126": 8}, "uri": "main/main.html", "filename": "templates/main/main.html"}
__M_END_METADATA
"""
