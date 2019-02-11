var oTable = null;
var allRoles = [];
var oriRoles = [];
var selRoles = [];

function initTable() {
    var table = $("#userTable").DataTable({
        "paging": true,
        "pagingType": "full_numbers",
        "lengthMenu": [10, 20],
        "processing": true,
        "searching": true, //是否开启搜索
        "serverSide": false, //开启服务器获取数据
//                   "order": [[ 0, "desc" ]], //默认排序
        "ajax": { // 获取数据
            "url": "/api/v1/users",
            "data": function (d) {
                d.mobile = $('#mobile').val();
                d.fullname = $('#fullname').val();
                d.role = $('#role').val();
                d.isActive = $('#isActive').val();
            },
            "type": "GET",
            "dataType": "json" //返回来的数据形式
        },
        "columns": [ //定义列数据来源
            {'title': "ID", 'data': "uid"},
            {'title': "手机号", 'data': "mobile"},
            {'title': "真实姓名", 'data': "name"},
            {'title': "角色", 'data': "roles"},
            {'title': "创建时间", 'data': "date_joined"},
            {'title': "最后登录时间", 'data': "last_login"},
            {'title': "操作", 'data': null, 'class': "align-center"} // 自定义列
        ],
        "columnDefs": [ //自定义列
            {
                "targets": -1, //改写哪一列
                "data": "uid",
                "render": function (data, type, row) {
                    var htmlStr = "<button class='btn btn-primary' data-action='edit' data-toggle='modal' data-target='#modal' data-id=" + row.uid + ">修改</button>";
                    return htmlStr;
                }
            },
            {
                "targets": 3, //改写哪一列
                "data": "roles",
                "render": function (data, type, row) {
                    var htmlStr = "";
                    for (var i = 0; i < data.length; i++) {
                        htmlStr += (data[i].name) + "<br/>";
                    }
                    return htmlStr;
                }
            },
//                             {
//                                 "targets":2,
//                                 "visible":false //隐藏列
//                             },
            {
                "targets": [0, 1, 2, 3, 4, 5, 6],
                "orderable": false  //禁止排序
            }
//                             {
//                                 "targets":[0, 1, 2, 3, 4, 5],
//                                 "searchable":false //禁止搜索
//                             }
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
            "sLoadingRecords": "载入中...",
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
        },
        "createdRow": function (row, data, index) {
            //行回调函数
        }
    });
    return table;
}

$(function () {
    oTable = initTable();

    // get role list
    $.ajax({
        async: false,
        dataType: "json",
        url: '/api/v1/roles',
        success: function (json) {
            if (json && json.data && json.data.length) {
                allRoles = json.data;
                $("#roleGroup").html("");
                for (var i = 0; i < allRoles.length; i++) {
                    var role = allRoles[i];
                    $("#roleGroup").append(
                        "<span class='input-group-addon'><label><input type='checkbox' data-action='check' data-code='" + role.code + "'/>" + role.name + "</label></span>"
                    );
                }
            }
        }
    });

    $("#form").submit(function () {
        oTable.ajax.reload();
        return false;
    });

    $(document).on("click", "[data-action=edit]", function () {
        var editData = {};
        editData.uid = $(this).attr("data-id");
        var tableData = oTable.data();
        for (var i = 0; i < tableData.length; i++) {
            if (tableData[i].uid == editData.uid) {
                editData = tableData[i];
                break;
            }
        }
        $("#userId").val(editData.uid);
        $("#mobileEdit").val(editData.mobile);
        $("#fullnameEdit").val(editData.name);

        selRoles = [];
        oriRoles = [];
        $("[type=checkbox][data-action=check]:checked").click();
        for (var i = 0; i < editData.roles.length; i++) {
            var tempRole = editData.roles[i];
            oriRoles.push(tempRole);
            $("[type=checkbox][data-code=" + tempRole.code + "]").click();
        }
    });

    $(document).on("change", "[type=checkbox][data-action=check]", function () {
        var code = $(this).attr("data-code");
        var roleObj = {};
        for (var i = 0; i < allRoles.length; i++) {
            if (code == allRoles[i].code) {
                roleObj = allRoles[i];
                break;
            }
        }
        if ($(this).is(':checked')) {
            selRoles.push(roleObj);
        }
        else {
            selRoles.removeByValue(roleObj);
        }

        var roleStr = "";
        for (var i = 0; i < selRoles.length; i++) {
            roleStr += selRoles[i].name;
            if (i < selRoles.length - 1) {
                roleStr += " | ";
            }
        }
        $("#rolesEdit").val(roleStr);
    });

    $("#save").click(function () {
        var rolesUnbind = Array.minus(oriRoles, selRoles);
        var rolesBind = Array.minus(selRoles, oriRoles);
        var jsonData = {};
        jsonData.uid = $("#userId").val();
        jsonData.mobile = $("#mobileEdit").val();
        jsonData.rolesBind = rolesBind;
        jsonData.rolesUnbind = rolesUnbind;
        $.ajax({
            async: false,
            dataType: "json",
            url: '/api/v1/users',
            type: 'PUT',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(jsonData),
            success: function (result) {
                if (result && result.ok) {
                    // 提示成功
                    alert(result.msg);
                    $('#modal').modal('hide');
                    oTable.ajax.reload();
                }
                else {
                    // 提示失败
                    alert(result.msg);
                }
            },
            error: function (msg) {
                alert(msg);
            }
        });
    });

});
