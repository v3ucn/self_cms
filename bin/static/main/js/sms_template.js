/**
 * Created by qfpay on 2018/01/02.
 */

var oTable = null;
function initTable() {
    $.fn.dataTable.ext.errMode = 'none'; //不显示任何错误信息
    var table = $("#table").DataTable({
        "paging": true,
        "pagingType": "full_numbers",
        "lengthMenu": [10, 20, 50],
        "processing": true,
        "searching": true, //是否开启搜索
        "serverSide": true, //开启服务器获取数据
        "ordering": false, //禁止排序
        "ajax": { // 获取数据
            "url": "/api/v1/sms_template",
            "timeout": 15000,
            "data": function (d) {
                d.name = $('#name').val();
                d.state = $('#state').val();
            },
            "async": true,
            "type": "GET",
            "dataType": "json", //返回来的数据形式
            "complete": function (XMLHttpRequest) {
                if(XMLHttpRequest.responseJSON.msg) {
                    toastr.info(XMLHttpRequest.responseJSON.msg);
                }
            },
            "error" : function(XMLHttpRequest, textStatus, errorThrown){ //请求完成后最终执行参数
                if(textStatus == 'timeout'){
                    toastr.error('抱歉，数据量过大，臣妾做不到！');
                }else {
                    toastr.error('抱歉，查询失败！');
                }
            }

        },
        "columns": [ //定义列数据来源
            {'title': "ID", 'data': "id"},
            {'title': "模板名称", 'data': "name"},
            {'title': "模板内容", 'data': "content", 'class': "align-center"},
            {'title': "类型", 'data': null, 'class': "align-center"},
            {'title': "状态", 'data': null, 'class': "align-center"},
            {'title': "操作", 'data': null, 'class': "align-center"}
        ],
        "columnDefs": [ //自定义列
            {
                "targets": 3, //改写哪一列
                "data": null,
                "render": function (data, type, row) {
                    var types = {
                        1: "人工创建",
                        2: "系统内置",
                        3: "客服专用"
                    };
                    var htmlStr = types[row.type] || row.type;
                    return htmlStr;
                }
            },
            {
                "targets": 4, //改写哪一列
                "data": null,
                "render": function (data, type, row) {
                    var states = {
                        0: "新建",
                        1: "有效",
                        2: "无效"
                    };

                    var htmlStr = states[row.state] || row.state;
                    return htmlStr;
                }
            },
            {
                "targets": 5, //改写哪一列
                "data": null,
                "render": function (data, type, row) {
                    var htmlStr = "<a href='#' onclick=edit(" + row.id + ") data-toggle='modal' data-target='#modalEdit'><i class='fa fa-edit'></i></a>";
                    return htmlStr;
                }
            },
            {
                "targets": [0, 1, 2, 3, 4, 5],
                "orderable": false  //禁止排序
            }
        ],
        "language": { // 定义语言
            "sProcessing": "加载中...",
            "sLengthMenu": "每页显示 _MENU_ 条记录",
            "sZeroRecords": "没有匹配的结果",
            "sInfo": "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
            "sInfoEmpty": "显示第 0 至 0 项结果，共 0 项",
            "sInfoFiltered": "(由 _MAX_ 项结果过滤)",
            "sInfoPostFix": "",
            "sSearch": "搜索:",
            "sUrl": "",
            "sEmptyTable": "表中数据为空",
            "sLoadingRecords": "...",
            "sInfoThousands": ",",
            "oPaginate": {
                "sFirst": "首页",
                "sPrevious": "上一页",
                "sNext": "下一页",
                "sLast": "末页"
            },
            "oAria": {
                "sSortAscending": ": 以升序排列此列",
                "sSortDescending": ": 以降序排列此列"
            }
        }
    });
    return table;
}

$(function () {
    oTable = initTable();

    $("#form").submit(function () {
        oTable.ajax.reload();
        return false;
    });

    $("#confirmNew").click(function () {
        if (checkInputNew() == false) {
            toastr.warning("请输入必要信息！");
            return false;
        }
        var jsonData = {};
        jsonData.type = $("#typeNew").val();
        jsonData.state = $("#stateNew").val();
        jsonData.name = $("#nameNew").val();
        jsonData.content = $("#contentNew").val();
        // submit
        $.ajax({
            async: true,
            dataType: 'json',
            url: '/api/v1/sms_template',
            type: 'POST',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(jsonData),
            success: function (result) {
                if (result && result.ok) {
                    alert(result.msg);
                    $('#modal').modal('hide');
                    oTable.ajax.reload();
                } else {
                    toastr.warning(result.msg);
                }
            },
            error: function (msg) {
                toastr.error('操作失败 ！');
            }
        });
    });

    $("#confirmEdit").click(function () {
        if (checkInputEdit() == false) {
            toastr.warning("请输入必要信息！");
            return false;
        }
        var jsonData = {};
        jsonData.id = $("#idEdit").val();
        jsonData.type = $("#typeEdit").val();
        jsonData.state = $("#stateEdit").val();
        jsonData.name = $("#nameEdit").val();
        jsonData.content = $("#contentEdit").val();

        // submit
        $.ajax({
            async: true,
            dataType: 'json',
            url: '/api/v1/sms_template',
            type: 'PUT',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(jsonData),
            success: function (result) {
                if (result && result.ok) {
                    toastr.success(result.msg);
                    $('#modalEdit').modal('hide');
                    oTable.ajax.reload();
                } else {
                    toastr.warning(result.msg);
                }
            },
            error: function (msg) {
                toastr.error('操作失败 ！');
            }
        });
    });
});

function checkInputNew() {
    var nameNew = $('#nameNew').val().trim();
    var contentNew = $('#contentNew').val().trim();
    if (nameNew.length == 0 || contentNew.length == 0) {
        return false;
    }
}

function checkInputEdit() {
    var nameEdit = $('#nameEdit').val().trim();
    var contentEdit = $('#contentEdit').val().trim();
    if (nameEdit.length == 0 || contentEdit.length == 0) {
        return false;
    }
}

function edit(editID) {
    $.ajax({
        async: true,
        dataType: 'json',
        url: '/api/v1/sms_template',
        type: 'GET',
        data: {"id": editID},
        success: function (result) {
            if (result && result.data) {
                console.log(result.data);
                $("#idEdit").val(result.data.id);
                $("#typeEdit").val(result.data.type);
                $("#stateEdit").val(result.data.state);
                $("#nameEdit").val(result.data.name);
                $("#contentEdit").val(result.data.content);
            } else {
                toastr.error('操作失败 ！');
            }
        },
        error: function (msg) {
            toastr.error('操作失败 ！');
        }
    });
}
