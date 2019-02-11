# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1529461547.360026
_enable_loop = True
_template_filename = 'templates/sales_audit_list.html'
_template_uri = 'sales_audit_list.html'
_source_encoding = 'utf-8'
_exports = [u'addition_header', u'page', u'title']


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
    return runtime._inherit_from(context, u'main/main.html', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        def addition_header():
            return render_addition_header(context._locals(__M_locals))
        def page():
            return render_page(context._locals(__M_locals))
        def title():
            return render_title(context._locals(__M_locals))
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'title'):
            context['self'].title(**pageargs)
        

        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'addition_header'):
            context['self'].addition_header(**pageargs)
        

        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'page'):
            context['self'].page(**pageargs)
        

        return ''
    finally:
        context.caller_stack._pop_frame()


def render_addition_header(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def addition_header():
            return render_addition_header(context)
        __M_writer = context.writer()
        __M_writer(u'\n  <link rel="stylesheet" href="/static/common/css/jquery.dataTables.min.css">\n  <script src="/static/common/js/jquery.dataTables.js"></script>\n  <script src="/static/common/js/jQueryRotate.js"></script>\n  <link rel="stylesheet" href="/static/common/css/font-awesome.min.css">\n  <script src="/static/main/js/tools.js"></script>\n  <script src="/static/main/js/sales_audit_list.js?20180529"></script>\n  <link rel="stylesheet" href="/static/main/css/OfficialAccountsManage.css">\n\n')
        __M_writer(u'  <link rel="stylesheet" href="/static/common/css/bootstrap-select.min.css">\n  <script src="/static/common/js/bootstrap-select.min.js"></script>\n  <script src="/static/common/js/i18n/defaults-zh_CN.min.js"></script>\n    <script type="text/javascript" src="/static/common/js/laydate/laydate.js"></script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_page(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def page():
            return render_page(context)
        __M_writer = context.writer()
        __M_writer(u'\n<div>\n    <div class="top1 form-inline">\n        <div class="form-group form-inline">\n            <!--placeholder="\u591a\u4e2a\u4ee5\u9017\u53f7\u9694\u5f00"-->\n            <label for="">\u5546\u6237ID:</label>\n            <input  id="mchntid"  style="height: 34px;">\n        </div>\n\n        <div class="form-group form-inline">\n            <label for="">\u6d3b\u52a8\u7c7b\u578b:</label>\n            <select id="type"  >\n\n                <option value="">\u5168\u90e8</option>\n                <option value="1">\u5fae\u4fe1\u7eff\u6d32</option>\n                <option value="2">\u652f\u4ed8\u5b9d\u84dd\u6d77</option>\n\n            </select>\n        </div>\n\n\n        <div class="form-group form-inline">\n            <label for="">\u5ba1\u6838\u72b6\u6001:</label>\n            <select id="state"  >\n\n                <option value="">\u5168\u90e8</option>\n                <option value="3">\u5f85\u5ba1</option>\n                <option value="1">\u5ba1\u6838\u901a\u8fc7</option>\n                <option value="2">\u5ba1\u6838\u5931\u8d25</option>\n\n            </select>\n        </div>\n\n\n         <div class="form-group form-inline">\n            <label for="">\u521b\u5efa\u65f6\u95f4:</label>\n            <!--<select name="" id="time" class="selectpicker show-menu-arrow" style="width: 100px;">\n                <option value="30">\u6700\u8fd130\u5929</option>\n                <option value="7">\u6700\u8fd1\u4e00\u5468</option>\n                <option value="14">\u6700\u8fd1\u4e24\u5468</option>\n                <option value="21">\u6700\u8fd1\u4e09\u5468</option>\n            </select>\n            -->\n             <input placeholder="\u8bf7\u8f93\u5165\u65e5\u671f" id="startdate" class="laydate-icon1 layui-input" readonly="readonly" style="height: 34px;">\n            <label for="startdate"><i class="fa fa-calendar"></i></label>\n             <!--<input placeholder="\u8bf7\u8f93\u5165\u65e5\u671f" id="" class="laydate-icon1 layui-input" onClick="laydate({istime: true, format: \'YYYY-MM-DD hh:mm:ss\'})">-->\n            <!--<label class="glyphicon glyphicon-calendar" id="startdateL"></label>-->\n            \u81f3\n            <!--<input type=\'text\' class="form-control" id=\'enddateI\'/>-->\n            <input placeholder="\u8bf7\u8f93\u5165\u65e5\u671f" id="enddate" class="laydate-icon2 layui-input" readonly="readonly" style="height: 34px">\n            <label for="enddate"><i class="fa fa-calendar"></i></label>\n         </div>\n\n         <button class="btn btn-primary" id="query_sales" style="margin-left: 80px;margin-top:8px;">\u67e5\u8be2</button>\n\n        <button class="btn btn-primary" id="export_sales" style="margin-left: 80px;margin-top:8px;">\u5bfc\u51faEXCEL</button>\n\n\n        <button class="btn btn-primary" id="zip" style="margin-left: 80px;margin-top:8px;">\u5bfc\u51fa\u56fe\u7247</button>\n\n\n\n        <button class="btn btn-primary" id="audit_sales" style="margin-left: 80px;margin-top:8px;">\u6279\u91cf\u5ba1\u6838</button>\n\n\n        <button class="btn btn-primary" id="audit_import" style="margin-left: 80px;margin-top:8px;">\u6279\u91cf\u5bfc\u5165</button>\n    </div>\n\n    <div style="margin-top: 20px;">\n        <table id="OfficialAccountManageTable" class="table table-striped">\n            <thead>\n                <tr>\n                    <th>\u5546\u6237ID</th>\n                    <th>\u6d3b\u52a8\u7c7b\u578b</th>\n                    <th>\u521b\u5efa\u65f6\u95f4</th>\n                    <th>\u521b\u5efa\u4eba</th>\n                    <th>\u5ba1\u6838\u72b6\u6001</th>\n                    <th>\u5907\u6ce8</th>\n                    <th>\u5ba1\u6838\u4eba</th>\n                    <th>\u5ba1\u6838\u65f6\u95f4</th>\n                </tr>\n            </thead>\n        </table>\n    </div>\n</div>\n\n\n\n<div class="modal fade" id="modal_add" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">\n    <div class="modal-dialog" style="width: 700px;opacity: 1;background-color: #F5F5F5;" >\n        <div class="modal-header">\n            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\n            <h4 class="modal-title" id="myModalLabel" style="text-align: center">\u7b7e\u7ea6\u5b9d\u5ba1\u6838</h4>\n            <label id="change_id" hidden></label>\n        </div>\n        <div class="modal-body">\n\n\n\n\n                <div class="form-inline">\n                    <div class="col-md-1"></div>\n                    <div class="col-md-2">\n                        <label style="height: 34px;line-height: 34px;"></label>\n                    </div>\n                    <div class="col-md-1" style="padding: 0px;">\n                        <label for="" style="height: 34px;line-height: 34px;">\u5546\u6237ID:</label>\n                    </div>\n                    <div class="form-inline col-md-8">\n                        <div>\n                           <textarea placeholder="\u591a\u4e2a\u7528\u82f1\u6587\u9017\u53f7\u5206\u9694" name="" id="userid_group" cols="30" rows="8" style="width: 365px;height: 150px">\n\n                    </textarea>\n                        </div>\n                    </div>\n                </div>\n\n\n            <div class="form-inline">\n                    <div class="col-md-1"></div>\n                    <div class="col-md-2">\n                        <label style="height: 34px;line-height: 34px;"></label>\n                    </div>\n                    <div class="col-md-1" style="padding: 0px;">\n                        <label for="" style="height: 34px;line-height: 34px;">\u7c7b\u578b:</label>\n                    </div>\n                    <div class="form-inline col-md-8">\n                        <div>\n                            <select id="stype" >\n                                <option value=\'1\'>\u5fae\u4fe1\u7eff\u6d32</option>\n                                <option value=\'2\'>\u652f\u4ed8\u5b9d\u84dd\u6d77</option>\n                            </select>\n                        </div>\n                    </div>\n                </div>\n\n             <div style="clear: both"></div>\n\n            <div class="form-inline">\n                    <div class="col-md-1"></div>\n                    <div class="col-md-2">\n                        <label style="height: 34px;line-height: 34px;"></label>\n                    </div>\n                    <div class="col-md-1" style="padding: 0px;">\n                        <label for="" style="height: 34px;line-height: 34px;">\u5907\u6ce8:</label>\n                    </div>\n                    <div class="form-inline col-md-8">\n                        <div>\n                           <input type = \'text\' class="form-control" id="memo" style="width:365px;"  />\n                        </div>\n                    </div>\n                </div>\n\n\n\n            <div style="clear: both"></div>\n\n            <div class="form-inline">\n                <div class="col-md-2 col-md-offset-4">\n                    <button class="btn btn-primary" onclick="doaudit(\'1\')">\u5ba1\u6838\u901a\u8fc7</button>\n                </div>\n                <div class="col-md-2 " style="margin-left: 150px;">\n                    <button class="btn btn-primary" onclick="doaudit(\'2\')">\u5ba1\u6838\u5931\u8d25</button>\n                </div>\n            </div>\n\n            <div style="clear: both"></div>\n        </div>\n    </div>\n</div>\n\n\n\n    <div class="modal fade" id="modal_add_dao" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">\n    <div class="modal-dialog" style="width: 700px;opacity: 1;background-color: #F5F5F5;" >\n        <div class="modal-header">\n            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\n            <h4 class="modal-title" id="myModalLabel" style="text-align: center">\u5bfc\u5165excel</h4>\n            <label id="change_id" hidden></label>\n        </div>\n        <div class="modal-body">\n\n\n\n\n                <div class="form-inline">\n                    <div class="col-md-1"></div>\n                    <div class="col-md-2">\n                        <label style="height: 34px;line-height: 34px;"></label>\n                    </div>\n                    <div class="col-md-1" style="padding: 0px;">\n                        <label for="" style="height: 34px;line-height: 34px;">\u4e0a\u4f20\u6587\u4ef6:</label>\n                    </div>\n                    <div class="form-inline col-md-8">\n                        <div>\n                           <input type="file" name="file" id="file_upload">\n                        </div>\n                    </div>\n                </div>\n\n\n            <div style="clear: both"></div>\n\n            <div class="form-inline">\n                <div class="col-md-2 col-md-offset-4">\n                    <button class="btn btn-primary" onclick="FileUpload()">\u786e\u8ba4</button>\n                </div>\n\n            </div>\n\n            <div style="clear: both"></div>\n        </div>\n    </div>\n</div>\n\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def title():
            return render_title(context)
        __M_writer = context.writer()
        __M_writer(u'\u7b7e\u7ea6\u5b9d\u5ba1\u6838')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"96": 90, "65": 7, "66": 17, "59": 7, "38": 2, "39": 3, "72": 23, "44": 5, "78": 23, "49": 21, "84": 5, "90": 5, "27": 0}, "uri": "sales_audit_list.html", "filename": "templates/sales_audit_list.html"}
__M_END_METADATA
"""
