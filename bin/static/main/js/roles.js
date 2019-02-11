var oTable = null;
var allPermissions = [];
var selPermissions = [];
var oriPermissions = [];
function initTable() {
    var table = $("#roleTable").DataTable({
        "paging": true,
        "pagingType": "full_numbers",
        "lengthMenu": [10, 20],
        "processing": true,
        "searching": true, //是否开启搜索
        "serverSide": false, //开启服务器获取数据
//                   "order": [[ 0, "desc" ]], //默认排序
        "ajax": { // 获取数据
            "url": "/api/v1/roles",
            "data": function (d) {
                d.role = $('#role').val();
            },
            "type": "GET",
            "dataType": "json" //返回来的数据形式
        },
        "columns": [ //定义列数据来源
            {'title': "ID", 'data': "id"},
            {'title': "角色", 'data': "name"},
            {'title': "更新时间", 'data': "utime"},
            {'title': "操作", 'data': null, 'class': "align-center"} // 自定义列
        ],
        "columnDefs": [ //自定义列
            {
                "targets": -1, //改写哪一列
                "data": "id",
                "render": function (data, type, row) {
                    // var htmlStr = "<button class='btn btn-info' data-action='show' data-code=" + row.code + ">查看详情</button>";
                    var htmlStr = "<button class='btn btn-primary' data-action='edit' data-toggle='modal' data-name=" + row.name + " data-target='#myModal' data-code=" + row.code + " data-group=" + row.group + ">修改</button>";
                    return htmlStr;
                }
            },
            {
                "targets": [0, 1, 2, 3],
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
    $('#create').click(function () {
        $("#save").attr('data-savetype','0');
        $("#role-name").attr("readOnly",false);
        $("#al-span").show();
        $("#role-name").attr('data-code','');
        $("#role-name").attr('data-group','');
        $('[data-group=role]').each(function () {
             if($(this).is(':checked') == true){
                 $(this).click();
             }
        })
        $('#role-name').val('');

    });

    $(document).on('click','[data-action=edit]',function () {
        $("#save").attr('data-savetype','1');
        //不可编辑，可以传值
        $("#role-name").attr("readOnly",true);
        $("#al-span").hide();
        $('[data-group=role]').each(function () {
             if($(this).is(':checked') == true){
                 $(this).click();
             }
        })
        role_code = this.dataset.code;
        $('#role-name').val(this.dataset.name);
        $("#role-name").attr('data-code',this.dataset.code);
        $("#role-name").attr('data-group',this.dataset.group);
        // get selected permission list
        $.ajax({
            async:false,
            dataType: "json",
            url: '/api/v1/p_r_map',
            data: {
                role: role_code
            },
            type: "GET",
            dataType: "json", //返回来的数据形式
            success: function (json) {
                if (json && json.data && json.data.length) {
                    selPermissions = json.data;
                    oriPermissions = [];
                    console.log(selPermissions);
                    for (var i=0;i<selPermissions.length;i++){
                        // selPermissions[i].permission_code
                        for (var j=0;j<allPermissions.length;j++){
                            for (var k=0;k<allPermissions[j].permissions.length;k++){
                                if (selPermissions[i].permission_code == allPermissions[j].permissions[k].code){
                                    $("[data-id=" + allPermissions[j].permissions[k].code + "]").click();
                                    var ori_data = {}
                                    ori_data.name = allPermissions[j].permissions[k].name;
                                    ori_data.code = allPermissions[j].permissions[k].code;
                                    ori_data.group = allPermissions[j].permissions[k].group;
                                    oriPermissions.push(ori_data);
                                }
                            }
                        }
                    }
                }
            }
        })

    });
    // get permission list
    $.ajax({
        async: false,
        dataType: "json",
        url: '/api/v1/permissions',
        success: function (json) {
            if (json && json.data && json.data.length) {
                allPermissions = json.data;
                var all_permissions_str = '';
                $('.all-role-div').html('');
                for (var i=0; i<allPermissions.length;i++){
                    if(allPermissions[i].group == ''){
                        allPermissions[i].group = '未分组1'
                    }
                    if(allPermissions[i].group == null){
                        allPermissions[i].group = '未分组2'
                    }
                    all_permissions_str = all_permissions_str + "<span class='form-group left-checkgroup'><label><input type='checkbox' data-action='check' data-group='group' name=" + allPermissions[i].group + " value=" + allPermissions[i].group + ">" + allPermissions[i].group + " </label></span>"
                    for (var j=0;j<allPermissions[i].permissions.length;j++){
                        all_permissions_str = all_permissions_str + "<span class='form-group left-check'><label><input type='checkbox' data-action='check' data-group='role' name=" + allPermissions[i].group + " value=" + allPermissions[i].permissions[j].name + " data-id=" + allPermissions[i].permissions[j].code + ">" + allPermissions[i].permissions[j].name + "</label> </span>"
                    }
                }
                $('.all-role-div').html(all_permissions_str)

            }
        }
    });

    $("#form").submit(function () {
        oTable.ajax.reload();
        return false;
    });

});


$(function () {


    $("input[type='checkbox'][data-group='role']").click(function () {
        var isAllChecked = true;
        $("input[type='checkbox'][name='"+ this.name +"'][data-group='role']").each(function () {
            if($(this).is(':checked') == false){
                isAllChecked = false;
            }
        });

        if (isAllChecked){
            $("input[type='checkbox'][data-group='group'][name='"+ this.name +"']").prop('checked',true);
        }else{
            $("input[type='checkbox'][data-group='group'][name='"+ this.name +"']").prop('checked',false);
        }

        var arr_v = new Array();
        var content_str = ''
        $('#roleGroupSel').html('');
        $("input[type='checkbox'][data-group='role']:checked").each(function(){
            arr_v.push(this.value);
            content_str = content_str+"<span class='form-group right-check' data-group=" + this.name + " data-code=" + this.dataset.id + " data-name=" + this.value + ">"+
            "<label>"+this.value+"</label><button class='x-close' data-bid='"+this.dataset.id+"'>X</button></span>"
        });
        $('#roleGroupSel').append(content_str);
    });

    $("input[type='checkbox'][data-group='group']").click(function () {
        var checkgroup = $(this);
        if(checkgroup.is(':checked')){
            $("input[type='checkbox'][name="+ this.name +"][data-group='role']").each(function () {
                var checkrole = $(this);
                if(checkrole.is(':checked') == false){
                    checkrole.click();
                }
            })
        }else {
            $("input[type='checkbox'][name="+ this.name +"][data-group='role']").each(function () {
                var checkrole = $(this);
                if($(this).is(':checked') == true){
                    checkrole.click();
                }
            })
        }
    });

    $(document).on('click','.x-close',function () {
        $("[data-id='"+this.dataset.bid+"']").click();
    });


    $("#save").click(function () {
        if ($("#role-name").val().length == 0){
            toastr.warning('请输入角色名');
            return;
        }
        //新建0 编辑1 $(this).attr('data-savetype')
        if ($(this).attr('data-savetype') == 0){
            selPermissions = [];
            $('.right-check').each(function () {
                var sel_data = {}
                sel_data.name = this.dataset.name;
                sel_data.code = this.dataset.code;
                sel_data.group = this.dataset.group;
                selPermissions.push(sel_data);
            });
             var permissionsBind = selPermissions;
            // var permissionsBind = Array.minus(selPermissions, allPermissions);
            // var permissionsUnbind = Array.minus(allPermissions, selPermissions);
            var jsonData = {};
            jsonData.role = {'name':$("#role-name").val()};
            jsonData.permissionsBind = permissionsBind;
            // jsonData.permissionsUnbind = permissionsUnbind;
            $.ajax({
                async: false,
                dataType: "json",
                url: '/api/v1/roles',
                type: 'POST',
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify(jsonData),
                success: function (result) {
                    if (result && result.ok) {
                        // 提示成功
                        // alert(result.msg);
                        toastr.success(result.msg);
                        $('#myModal').modal('hide');
                        oTable.ajax.reload();
                    }
                    else {
                        // 提示失败
                        // alert(result.msg);
                        toastr.warning(result.msg);
                    }
                },
                error: function (msg) {
                    // alert(msg);
                    toastr.error(msg);
                }
            });
        } else if($(this).attr('data-savetype') == 1){
            selPermissions = [];
            $('.right-check').each(function () {
                var sel_data = {}
                sel_data.name = this.dataset.name;
                sel_data.code = this.dataset.code;
                sel_data.group = this.dataset.group;
                selPermissions.push(sel_data);
            });
            var permissionsBind = Array.minus(selPermissions, oriPermissions);
            var permissionsUnbind = Array.minus(oriPermissions, selPermissions);
            console.log(permissionsBind);
            console.log(permissionsUnbind);
            var jsonData = {};
            jsonData.role = {'name':$("#role-name").val(),'code':$("#role-name").attr('data-code'),'group':$("#role-name").attr('data-group')};
            jsonData.permissionsBind = permissionsBind;
            jsonData.permissionsUnbind = permissionsUnbind;
            $.ajax({
                async: false,
                dataType: "json",
                url: '/api/v1/roles',
                type: 'PUT',
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify(jsonData),
                success: function (result) {
                    if (result && result.ok) {
                        // 提示成功
                        // alert(result.msg);
                        toastr.success(result.msg);
                        $('#myModal').modal('hide');
                        oTable.ajax.reload();
                    }
                    else {
                        // 提示失败
                        // alert(result.msg);
                        toastr.warning(result.msg);
                    }
                },
                error: function (msg) {
                    // alert(msg);
                    toastr.error(msg);
                }
            });
        }


    });
})
