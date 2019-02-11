/**
 * Created by qfpay on 2018/01/02.
 */

var oTable = null;
function initTable() {
    $.fn.dataTable.ext.errMode = 'none'; //不显示任何错误信息
    var table = $("#table").DataTable({
        "paging": true,
        "pagingType": "full_numbers",
        "lengthMenu": [20, 50, 100],
        "processing": true,
        "searching": true, //是否开启搜索
        "serverSide": true, //开启服务器获取数据
        "ordering": false, //禁止排序
        "ajax": { // 获取数据
            "url": "/api/v1/sms_record",
            "timeout": 15000,
            "data": function (d) {
                d.phone = $('#phone').val();
                d.sms_type = $('#sms_type').val();
                d.month = $('#month').val();
            },
            "async": true,
            "type": "GET",
            "dataType": "json", //返回来的数据形式
            "complete": function (XMLHttpRequest) {
                if(XMLHttpRequest.responseJSON && XMLHttpRequest.responseJSON.msg) {
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
            {'title': "手机号", 'data': "phone"},
            {'title': "内容", 'data': "content", 'class': "align-center"},
            {'title': "时间", 'data': "add_time"},
            {'title': "短信通道", 'data': null, 'class': "align-center"},
            {'title': "短信类型", 'data': null, 'class': "align-center"}
        ],
        "columnDefs": [ //自定义列
            {
                "targets": 4, //改写哪一列
                "data": null,
                "render": function (data, type, row) {
                    var channel = row.channel;
                    if (channel.startsWith("dahantc")) {
                        channel = "大汉";
                    }
                    else if (channel.startsWith("huasenyidong")) {
                        channel = "华森";
                    }
                    else if (channel.startsWith("cmaysms")) {
                        channel = "创美";
                    }

                    var htmlStr = channel;
                    return htmlStr;
                }
            },
            {
                "targets": 5, //改写哪一列
                "data": null,
                "render": function (data, type, row) {
                    var htmlStr = row.sms_type;
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
    laydate.render({
        elem: '#month',
        type: 'month',
        theme: '#009688',
        format: 'yyyyMM',
        value: new Date()
    });

    laydate.render({
        elem: '#timing',
        type: 'datetime',
        theme: '#009688',
        max: 1,
        value: new Date()
    });

    oTable = initTable();
    // // 伪实时检测
    // setInterval("checkNew()", 100);
    // setInterval("checkEdit()", 100);

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

function edit(editData) {
    var data = editData.split("|");
    $("#idEdit").val(data[0]);
    $("#typeEdit").val(data[1]);
    $("#stateEdit").val(data[2]);
    $("#valueEdit").val(data[3]);
}
