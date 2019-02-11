/**
 * Created by qfpay on 2018/01/02.
 */

var oTable = null;
function initTable() {
    $.fn.dataTable.ext.errMode = 'none'; //不显示任何错误信息
    var table = $("#table").DataTable({
        "paging": true,
        "pagingType": "full_numbers",
        "lengthMenu": [100, 50, 20, 10],
        "processing": true,
        "searching": true, //是否开启搜索
        "serverSide": false, //开启服务器获取数据
        "ordering": false, //禁止排序
        "ajax": { // 获取数据
            "url": "/api/v1/audit_black",
            "timeout": 15000,
            "data": function (d) {
                d.value = $('#value').val();
                d.type = $('#type').val();
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
            {'title': "类型", 'data': null, 'class': "align-center"},
            {'title': "值", 'data': "value"},
            {'title': "状态", 'data': null, 'class': "align-center"},
            {'title': "更新时间", 'data': "utime"},
            {'title': "操作", 'data': null, 'class': "align-center"}
        ],
        "columnDefs": [ //自定义列
            {
                "targets": 1, //改写哪一列
                "data": null,
                "render": function (data, type, row) {
                    var types = {
                        1: "名字",
                        2: "身份证号",
                        3: "手机号",
                        4: "卡号"
                    };
                    var htmlStr = types[row.type] || row.type;
                    return htmlStr;
                }
            },
            {
                "targets": 3, //改写哪一列
                "data": null,
                "render": function (data, type, row) {
                    var status = {
                        0: "无效",
                        1: "有效"
                    };
                    var htmlStr = status[row.state] || row.state;
                    return htmlStr;
                }
            },
            {
                "targets": -1, //改写哪一列
                "data": null,
                "render": function (data, type, row) {
                    var htmlStr = "";
                    var editData = "\'" + row.id + "|" + row.type + "|" + row.state + "|" + row.value + "\'";
                    htmlStr += "<a href='#' onclick=edit(" + editData + ") data-toggle='modal' data-target='#modalEdit'><i class='fa fa-edit'></i></a>";
                    // htmlStr += "<a href='#' onclick=del(" + row.id + ")><i class='fa fa-trash-o'></i></a>";
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
    // 伪实时检测
    setInterval("checkNew()", 100);
    setInterval("checkEdit()", 100);

    $("#form").submit(function () {
        oTable.ajax.reload();
        return false;
    });

    $("#confirmNew").click(function () {
        var values = checkNew();
        if(values == false) {
            toastr.error("格式错误，请重新输入");
            return;
        }
        var jsonData = {};
        jsonData.type = $("#typeNew").val();
        jsonData.state = $("#stateNew").val();
        jsonData.values = values;
        // submit
        $.ajax({
            async: true,
            dataType: 'json',
            url: '/api/v1/audit_black',
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
        var value = checkEdit();
        if(value == false) {
            toastr.error("格式错误，请重新输入");
            return;
        }

        var jsonData = {};
        jsonData.id = $("#idEdit").val();
        jsonData.type = $("#typeEdit").val();
        jsonData.state = $("#stateEdit").val();
        jsonData.value = value;
        // submit
        $.ajax({
            async: true,
            dataType: 'json',
            url: '/api/v1/audit_black',
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

// 成功返回 values
function checkNew() {
    var values = checkInputNew();
    if (values == false) {
        $('#valueNew').addClass("invalid");
        return false;
    }
    $('#valueNew').removeClass("invalid");
    return values;
}

function checkEdit() {
    var value = checkInputEdit();
    if (value == false) {
        $('#valueEdit').addClass("invalid");
        return false;
    }
    $('#valueEdit').removeClass("invalid");
    return value;
}

// 检测新增输入合法性，成功返回 values
function checkInputNew() {
    $('#valueNew').val($('#valueNew').val().toUpperCase());
    var valueNew = $('#valueNew').val();
    var values = valueNew.split(",");
    var valuesTrimed = [];
    for (var i = 0; i < values.length; i++) {
        var value = values[i].trim();
        if (value.length) {
            valuesTrimed.push(value);
        }
    }
    if (valuesTrimed.length == 0) {
        return false;
    }
    // 默认正则匹配 id，全是数字就行
    var r = /^\d+$/;
    var typeNew = $('#typeNew').val();
    if (typeNew == "2") {
        // 身份证号，18位数字，最后一位可以是x
        r = /^\d{17}(\d|X)$/;
    }
    else if (typeNew == "3") {
        // 手机号，11-13位数字
        r = /^\d{11,13}$/;
    }
    else if (typeNew == "4") {
        // 银行卡号，15-28位数字
        r = /^\d{15,28}$/;
    }
    for (var i = 0; i < valuesTrimed.length; i++) {
        if (!r.test(valuesTrimed[i])) {
            return false;
        }
    }
    return valuesTrimed;
}

// 检测编辑输入合法性，成功返回 value
function checkInputEdit() {
    $('#valueEdit').val($('#valueEdit').val().toUpperCase());
    var valueEdit = $('#valueEdit').val().trim();
    if (valueEdit.length == 0) {
        return false;
    }
    // 默认正则匹配 id，全是数字就行
    var r = /^\d+$/;
    var typeEdit = $('#typeEdit').val();
    if (typeEdit == "2") {
        // 身份证号，18位数字，最后一位可以是x
        r = /^\d{17}(\d|X)$/;
    }
    else if (typeEdit == "3") {
        // 手机号，11-13位数字
        r = /^\d{11,13}$/;
    }
    else if (typeEdit == "4") {
        // 银行卡号，15-28位数字
        r = /^\d{15,28}$/;
    }
    if (!r.test(valueEdit)) {
        return false;
    }
    return valueEdit;
}

function del(id) {
    if (confirm("确实要删除 ID:" + id + " 的记录吗?")) {
        $.ajax({
            async: true,
            dataType: 'json',
            url: '/api/v1/audit_black?' + $.param({"id": id}),
            type: 'DELETE',
            contentType: "application/json; charset=utf-8",
            data: {"id": id},
            success: function (result) {
                if (result && result.ok) {
                    toastr.success(result.msg);
                    oTable.ajax.reload();
                } else {
                    toastr.warning(result.msg);
                }
            },
            error: function (msg) {
                toastr.error('操作失败 ！');
            }
        });
    }
}

function edit(editData) {
    var data = editData.split("|");
    $("#idEdit").val(data[0]);
    $("#typeEdit").val(data[1]);
    $("#stateEdit").val(data[2]);
    $("#valueEdit").val(data[3]);
}
