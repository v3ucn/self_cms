# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1529461547.425457
_enable_loop = True
_template_filename = u'templates/main/menu.html'
_template_uri = u'main/menu.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n<div class="panel-group" id="accordion" role="tablist">\n\n  <div class="panel panel-default">\n    <div class="panel panel-default">\n      <div class="panel-heading" role="tab">\n        <h4 class="panel-title">\n          <a href="/index" class="single-item">\n            <i class="fa fa-dashboard"></i>\n            Dashboard\n          </a>\n        </h4>\n      </div>\n    </div>\n  </div>\n\n  <div class="panel panel-default">\n    <div class="panel-heading" role="tab">\n      <h4 class="panel-title">\n        <a href="#collapse1" data-toggle="collapse" data-parent="#accordion"\n           class="collapsed">\n          <i class="fa fa-shield"></i>\n          \u6743\u9650\u7ba1\u7406\n          <i class="pull-right fa fa-caret-down"></i>\n        </a>\n      </h4>\n    </div>\n    <div id="collapse1" class="panel-collapse collapse" role="tabpanel">\n      <div>\n        <a href="/users" class="list-group-item">\u7528\u6237\u7ba1\u7406</a>\n        <a href="/roles" class="list-group-item">\u89d2\u8272\u7ba1\u7406</a>\n      </div>\n    </div>\n  </div>\n\n  <div class="panel panel-default">\n    <div class="panel-heading" role="tab">\n      <h4 class="panel-title">\n        <a href="#collapse2" data-toggle="collapse" data-parent="#accordion"\n           class="collapsed">\n          <i class="fa fa-money"></i>\n          \u6c47\u7387\u7ba1\u7406\n          <i class="pull-right fa fa-caret-down"></i>\n        </a>\n      </h4>\n    </div>\n    <div id="collapse2" class="panel-collapse collapse" role="tabpanel">\n      <div>\n        <a href="/rate" class="list-group-item">\u6c47\u7387\u7ba1\u7406</a>\n\n      </div>\n    </div>\n  </div>\n\n  <div class="panel panel-default">\n    <div class="panel-heading" role="tab">\n      <h4 class="panel-title">\n        <a href="#collapse3" data-toggle="collapse" data-parent="#accordion"\n           class="collapsed">\n          <i class="fa fa-address-book"></i>\n          \u5546\u6237\u7ba1\u7406\n          <i class="pull-right fa fa-caret-down"></i>\n        </a>\n      </h4>\n    </div>\n    <div id="collapse3" class="panel-collapse collapse" role="tabpanel">\n      <div>\n        <a href="/merchants" class="list-group-item">\u5546\u6237\u4fe1\u606f</a>\n        <a href="/trade" class="list-group-item">\u4ea4\u6613\u4fe1\u606f</a>\n        <a href="/fund" class="list-group-item">\u6536\u652f\u8bb0\u5f55</a>\n        <a href="/trade_code" class="list-group-item">\u5546\u6237\u4e8c\u7ef4\u7801</a>\n        <a href="/audit_black" class="list-group-item">\u5ba1\u6838\u9ed1\u540d\u5355</a>\n        <a href="/register_audit" class="list-group-item">\u5165\u7f51\u5ba1\u6838</a>\n        <a href="/info_change" class="list-group-item">\u4fe1\u606f\u53d8\u66f4</a>\n          <a href="/sales_audit" class="list-group-item">\u7b7e\u7ea6\u5b9d\u5ba1\u6838</a>\n      </div>\n    </div>\n  </div>\n\n  <div class="panel panel-default">\n    <div class="panel-heading" role="tab">\n      <h4 class="panel-title">\n        <a href="#collapse4" data-toggle="collapse" data-parent="#accordion"\n           class="collapsed">\n          <i class="fa fa-envelope-o"></i>\n          \u6d88\u606f\u4e2d\u5fc3\n          <i class="pull-right fa fa-caret-down"></i>\n        </a>\n      </h4>\n    </div>\n    <div id="collapse4" class="panel-collapse collapse" role="tabpanel">\n      <div>\n        <a href="/push_list" class="list-group-item">\u6d88\u606f\u63a8\u9001</a>\n        <a href="/sms_record" class="list-group-item">\u77ed\u4fe1\u53d1\u9001\u8bb0\u5f55</a>\n        <a href="/sms_template" class="list-group-item">\u77ed\u4fe1\u6a21\u677f</a>\n      </div>\n    </div>\n  </div>\n\n  <div class="panel panel-default">\n    <div class="panel-heading" role="tab">\n      <h4 class="panel-title">\n        <a href="#collapse5" data-toggle="collapse" data-parent="#accordion"\n           class="collapsed">\n          <i class="fa fa-comments"></i>\n          \u516c\u4f17\u53f7\u7ba1\u7406\n          <i class="pull-right fa fa-caret-down"></i>\n        </a>\n      </h4>\n    </div>\n    <div id="collapse5" class="panel-collapse collapse" role="tabpanel">\n      <div>\n        <a href="/official_accounts_config" class="list-group-item">\u5173\u6ce8\u89c4\u5219</a>\n        <a href="/official_accounts_manage" class="list-group-item">\u516c\u4f17\u53f7\u7ba1\u7406</a>\n        <a href="/merchant_config" class="list-group-item">\u5546\u6237\u914d\u7f6e</a>\n        <a href="/mchnt_change_log" class="list-group-item">\u5207\u6362\u64cd\u4f5c\u8bb0\u5f55</a>\n        <a href="/set_mpconf" class="list-group-item">\u516c\u4f17\u53f7\u914d\u7f6e</a>\n        <a href="/tag" class="list-group-item">\u6807\u7b7e\u7ba1\u7406</a>\n      </div>\n    </div>\n  </div>\n\n</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"16": 0, "27": 21, "21": 2}, "uri": "main/menu.html", "filename": "templates/main/menu.html"}
__M_END_METADATA
"""
