var oTable = null;
var relationTable = null;
var IDrelationTable = null;
var curr_id = 0;
var select_ids = []
var ids = []; //全部的id
//function initTable() {
$(function (){
    $("#userTable").dataTable({
        //"paging": true,
        //"pagingType": "full_numbers",
        //"lengthMenu": [10, 20],
        //"processing": true,
        "serverSide": true, //开启服务器获取数据
        "sDom":'<t><"row m-r m-l" <"col-sm-6" <"col-sm-5 m-t" l><"col-sm-offset-4" i>><"col-sm-6" p>><"clear">',
        "ajax": function (data, callback, settings){ // 获取数据
            var search_data = data.search.value ? JSON.parse(data.search.value):{};
            search_data['start'] = data.start;
            search_data['length'] = data.length;
            console.log('search_data', search_data)
            $.ajax({
                url: "/api/v1/merchants",
                data: search_data,
                type: "GET",
                dataType: "json", //返回来的数据形式
                success: function(resp){
                    console.log(resp)
                    //if (resp['respcd'] == '0000') {
                    callback({
                        recordsTotal: resp.total,
                        recordsFiltered: resp.total,
                        data: resp.data
                    })
                    //} else {
                        //callback({
                            //recordsTotal: 0,
                            //recordsFiltered: 0,
                            //data: []
                        //});
                        //toastr.error(msg=data.respmsg, title='获取补丁列表失败');
                    //}
                },
                error:function(data) {
                    toastr.warning('网络不好， 请稍后重试!!!');
                    /*location.href = '/mkm/error'*/
                }
            })
        },
        "columnDefs": [ //自定义列
            {
                "targets": -1, //改写哪一列
                "data": "uid",
                "render": function (data, type, row) {
                    var htmlStr = "<button class='btn btn-primary' data-action='detail' data-toggle='modal' data-target='#modal' data-id=" + row.userid + " data-groupid=" + row.groupid + ">详情</button>";
                    return htmlStr;
                }
            },
            {
                "targets": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                "orderable": false  //禁止排序
            },
            {
                "targets": 0,
                "orderable": false,  //禁止排序
                "data": "userid",
                //"render": function (data, type, row) {
                    //var htmlStr = "<div>"+"<input class='id_check' name='' type='checkbox' value='-1'/>"+"&nbsp;"+"<span hidden>"+row.userid+"</span>"+"<label>"+data+"</label>"+"</div>";
                    //return htmlStr;
                //}
            },
            {
                "targets": 1,
                "orderable": false,  //禁止排序
                "data": "name",
            },
            {
                "targets": 2,
                "orderable": false,  //禁止排序
                "data": "mobile",
            },
            {
                "targets": 3,
                "orderable": false,  //禁止排序
                "data": "nickname",
            },
            {
                "orderable": false,  //禁止排序
                "targets": 4,
                "data": "groupid",
            },
            {
                "targets": 5,
                "orderable": false,  //禁止排序
                "data": "groupname",
            },
            {
                "targets": 6,
                "orderable": false,  //禁止排序
                "data": "lastaudittime",
            },
            {
                "orderable": false,  //禁止排序
                "targets": 7,
                "data": "auditstate",
            },
            {
                "targets": 8,
                "orderable": false,  //禁止排序
                "data": "state",
            },
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
    });
});

function initRelationTable() {
    var table = $("#relationTable").DataTable({
        "paging": true,
        "pagingType": "full_numbers",
        // "lengthMenu": [10, 20],
        "bDestory": true,
        "bLengthChange": false,
        "processing": true,
        "searching": false, //是否开启搜索
        "serverSide": false, //开启服务器获取数据
        "ajax": { // 获取数据
            "url": "/api/v1/Relation",
            "data": function (d) {
                d.uid = curr_id;
            },
            "type": "GET",
            "dataType": "json" //返回来的数据形式
        },
        "columns": [ //定义列数据来源
            {'title': "用户ID", 'data': "userid"},
            {'title': "签约实体", 'data': "name"},
            {'title': "手机号", 'data': "mobile"},
            {'title': "收据名称", 'data': "nickname"},
            {'title': "渠道ID", 'data': "groupid"},
            {'title': "渠道名称", 'data': "groupname"},
            {'title': "审核时间", 'data': "lastaudittime"},
            {'title': "审核状态", 'data': "auditstate"},
            // {'title': "门店类型", 'data': 'shop_type'},
            {'title': "操作", 'data': null, 'class': "align-center"} // 自定义列
        ],
        "columnDefs": [ //自定义列
            {
                "targets": -1, //改写哪一列
                "data": "uid",
                "render": function (data, type, row) {
                    var htmlStr = "<button id='relationBtn' class='btn btn-primary' data-action='' data-toggle='modal' data-target='' data-id=" + row.userid + ">查看</button>";
                    return htmlStr;
                }
            },
            {
                "targets": [0, 1, 2, 3, 4, 5, 6, 7, 8],
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
        }
    });
    return table;
}

function initIDRelationTable() {
    var table = $("#IDrelationTable").DataTable({
        "paging": true,
        "pagingType": "full_numbers",
        // "lengthMenu": [10, 20],
        "bDestory": true,
        "bLengthChange": false,
        "processing": true,
        "searching": false, //是否开启搜索
        "serverSide": false, //开启服务器获取数据
        "ajax": { // 获取数据
            "url": "/api/v1/idcard_relation",
            "data": function (d) {
                d.idnumber = $('#idnumber').html();
                d.uid = $('#id_title').html();
            },
            "type": "GET",
            "dataType": "json" //返回来的数据形式
        },
        "columns": [ //定义列数据来源
            {'title': "用户ID", 'data': "userid"},
            {'title': "签约实体", 'data': "name"},
            {'title': "手机号", 'data': "mobile"},
            {'title': "收据名称", 'data': "nickname"},
            {'title': "渠道ID", 'data': "groupid"},
            {'title': "渠道名称", 'data': "groupname"},
            {'title': "审核时间", 'data': "lastaudittime"},
            {'title': "审核状态", 'data': "auditstate"},
            // {'title': "门店类型", 'data': 'shop_type'},
            {'title': "操作", 'data': null, 'class': "align-center"} // 自定义列
        ],
        "columnDefs": [ //自定义列
            {
                "targets": -1, //改写哪一列
                "data": "uid",
                "render": function (data, type, row) {
                    var htmlStr = "<button id='idrelationBtn' class='btn btn-primary' data-action='' data-toggle='modal' data-target='' data-id=" + row.userid + ">查看</button>";
                    return htmlStr;
                }
            },
            {
                "targets": [0, 1, 2, 3, 4, 5, 6, 7, 8],
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
        }
    });
    return table;
}

function gps2address(gps) {
    if (gps != "") {
        $.ajax({
            url : "http://restapi.amap.com/v3/geocode/regeo?location=" + gps.replace(" ", ",") + "&key=d58fb2d76db22d4b1e63b0d707f22e21&radius=1000&callback=?",
            dataType : "jsonp",
            crossDomain : true,
            timeout : 10000,
            success : function(data) {
                if (data && data["status"] && data["status"] == "1" && data["regeocode"] && data["regeocode"]["formatted_address"]) {
                    $("#address_b").html(data["regeocode"]["formatted_address"]);

                }
            }
        });
    }
}


$(function () {
    $('#uid').val(GetQueryString("id"));
    //oTable = initTable();
    // relationTable = initRelationTable();
    // IDrelationTable = initIDRelationTable();

    $('#query_submit').click(function (){
        d = {}
        d.uid = $('#uid').val();
        d.mobile = $('#mobile').val();
        d.gid = $('#gid').val();
        d.gname = $('#gname').val();
        d.fullname = $('#fullname').val();
        d.nickname = $('#nickname').val();
        d.state = $('#state').val();
        d.cate_codes = $('#cate_code').val().join(',');
        console.log('query',d)
        var d = JSON.stringify(d)
        var tmp = $("#cate_code").val()
        if (tmp.in_array('untagged') && tmp.length > 1 ){
            toastr.info('不允许同时选择无标签和其他标签');
            return
        }

        $('#userTable').DataTable().search(d).draw(true)
    })

    var urlEncode = function (param, key, encode) {
      if(param==null) return '';
      var paramStr = '';
      var t = typeof (param);
      if (t == 'string' || t == 'number' || t == 'boolean') {
          paramStr += '&' + key + '=' + ((encode==null||encode) ? encodeURIComponent(param) : param);
        } else {
            for (var i in param) {
                  var k = key == null ? i : key + (param instanceof Array ? '[' + i + ']' : '.' + i);
                  paramStr += urlEncode(param[i], k, encode);
                }
          }
      return paramStr;
    };

    $('#expo_excel').click(function (){
        d = {}
        d.uid = $('#uid').val();
        d.mobile = $('#mobile').val();
        d.gid = $('#gid').val();
        d.gname = $('#gname').val();
        d.fullname = $('#fullname').val();
        d.nickname = $('#nickname').val();
        d.state = $('#state').val();
        d.cate_codes = $('#cate_code').val().join(',');
        console.log('query',d)
        location.href = "/api/v1/merchants?mode=expo_excel" + urlEncode(d)
    })

    init_cate_name()
    function init_cate_name(){
        $('#cate_code').selectpicker({
            width: 200,
            style: 'btn-inverse',
            actionsBox:true,
        });
        $('#cate_code option').remove()
        $('#cate_code').append('<option value="untagged">无标签用户</option>')
        var data = {}
        data.mode = 'get_cates'
        data.status = '1'
        $.ajax({
            url: '/tag_manage',
            type: 'POST',
            data: data,
            success: function(resp) {
                if (resp['respcd'] == '0000') {
                    cate_dict = resp['data']['cate_dict']
                    console.log(cate_dict)
                    $.each(cate_dict, function(k,v){
                        $('#cate_code').append('<option value='+k+'>'+v+'</option>')
                    })
                    $('#cate_code').selectpicker('refresh')
                } else {
                    toastr.error(msg=resp['respmsg'], title='获取信息数据失败');
                }
            },
            error:function(data) {
                toastr.warning('网络不好， 请稍后重试!!!');
                //location.href = '/mkm/error'
            }
        })
    }

    $("#add_tag").click(function(){
        $('#tag_modal').modal({backdrop: 'static'});
        var data = {}
        data.status = "1"
        data.mode = 'get_cates'
        $.ajax({
            url: '/tag_manage',
            type: 'POST',
            data: data,
            success: function(resp) {
                if (resp['respcd'] == '0000') {
                    cate_dict = resp['data']['cate_dict']
                    html = ''
                    $.each(cate_dict, function(k,v){
                        html += '<div class="checkbox">'
                        html += '<label style="float:left" class="m-l-lg">'
                        html += '<input type="checkbox" class="add_cate_code" value='+ k +'>' + v
                        html += '</label>'
                        html += '</div>'
                    })
                    $('#tags').html(html)
                } else {
                    toastr.error(msg=resp['respmsg'], title='获取信息数据失败');
                }
            },
            error:function(data) {
                toastr.warning('网络不好， 请稍后重试!!!');
                //location.href = '/mkm/error'
            }
        })
    })

    $('#add_submit').click(function(){
        var data = {
            'cate_codes': '',
            'status': '1',
            'userids': $('#userids').val(),
            'mode': 'tag_user',
        }
        var cate_codes = []
        $('.add_cate_code').each(function(k,v){
            if ($(v).prop('checked')){
                cate_codes.push(v.value)
            }
        })
        data.cate_codes = cate_codes.join(',')
        $.ajax({
            url: '/tag_manage',
            type: 'POST',
            data: data,
            success: function(resp) {
                if (resp['respcd'] == '0000') {
                    toastr.success(msg='设置成功');
                    $('#tag_modal').modal('hide');
                    $('#userids').val('')
                } else {
                    toastr.error(msg=resp['respmsg'], title='获取信息数据失败');
                }
            },
            error:function(data) {
                toastr.warning('修改失败，网络不好， 请稍后重试!!!');
            }
        })
    })

    $('#del_submit').click(function(){
        var data = {
            'cate_codes': '',
            'status': '0',
            'userids': $('#userids').val(),
            'mode': 'tag_user',
        }
        var cate_codes = []
        $('.add_cate_code').each(function(k,v){
            if ($(v).prop('checked')){
                cate_codes.push(v.value)
            }
        })
        data.cate_codes = cate_codes.join(',')
        $.ajax({
            url: '/tag_manage',
            type: 'POST',
            data: data,
            success: function(resp) {
                if (resp['respcd'] == '0000') {
                    toastr.success(msg='设置成功');
                    $('#tag_modal').modal('hide');
                    $('#userids').val('')
                } else {
                    toastr.error(msg=resp['respmsg'], title='获取信息数据失败');
                }
            },
            error:function(data) {
                toastr.warning('修改失败，网络不好， 请稍后重试!!!');
            }
        })

    })

    $('#cancel_submit').click(function(){
        $('#tag_modal').modal('hide')
        select_ids = [];
        $('#userids').val('')
    })

    //$("#form").submit(function () {
        //oTable.ajax.reload();
        //return false;
    //});

    // $(document).on("error","img",function(){
    //     $(this).attr('src',"http://easyread.ph.126.net/5s-Byepk6uzaA5WBv0j6-g==/7916558486779044144.jpg");
    // });

    // $('img').error(function(){
    //     $(this).attr('src',"http://easyread.ph.126.net/5s-Byepk6uzaA5WBv0j6-g==/7916558486779044144.jpg");
    // });

    $(document).on("click", "[data-action=detail]", function () {
        // 点击详情
        var detail_id = $(this).attr('data-id');
        var detail_groupid = $(this).attr('data-groupid');
        $('#id_title').html(detail_id);
        // 关联按钮的id
        $('#relation_btn').attr('data-id',detail_id);

        $('#voucher_content').html('');

        $('#user_type').html('--');
         $('#user_state').html('--');
         $('#src').html('--');
         $('#apply_state').html('--');
         $('#applytime').html('--');
         $('#lastaudittime').html('--');
         $('#name').html('--');
         $('#legalperson').html('--');
         $('#idnumber').html('--');
         $('#idenddate').html('--');
         $('#dishonestyinfo').html('--');
         //门店类型
         $('#shop_type').html('--');
         // 其他身份
         $('#cates').html('--');
         $('#mobile_m').html('--');
         $('#nick_name').html('--');
         $('#address_a').html('--');
         $('#businessaddr').html('--');
         $("#address_b").html('--');
         $('#mcc').html('--');
         $('#email').html('--');
         $('#telephone').html('--');
         //用户标签
         $('#user_tag').html('--');
         $('#banktype').html('--');
         $('#bankuser').html('--');
         $('#bankProvince').html('--');
         $('#bankCity').html('--');
         $('#headbankname').html('--');
         $('#bankname').html('--');
         $('#bankaccount').html('--');
         $('#bankcode').html('--');
         $('#pre_phone').html('--');

        $.ajax({
               async: false,
               dataType: 'json',
               url: '/api/v1/voucher',
               type: 'GET',
               data: {
                   uid : detail_id
               },
               contentType: "application/json; charset=utf-8",
               success: function (json) {
                   if (json && json.success){
                        identity_str = '';
                        if(json.data.identity.length>0 && json.data.identity){
                            identity_str += "<div><div class='head'><lable>身份凭证</lable></div>";
                            for (var i=0;i<json.data.identity.length;i++){
                                data = json.data.identity[i];
                                identity_str += "<div class='col-md-3 single_div'><label style='display: block;height: 36px;'>"+ data.name +"</label><button class='btn btn-xs btn-primary col-md-6 rotation_left'>向左转</button> <button class='btn btn-xs btn-primary col-md-6 rotation_right'>向右转</button><img onerror="+"this.src='/static/common/img/default.jpg'"+" style='width: 180px;height: 100px' data-angle='0' src="+ data.imgurl +" data-original="+ data.imgurl +" alt="+ data.name +"><div style='margin:13px 0px 5px; '><label>提交时间：</label> <label>"+ data.submit_time +"</label></div></div>";
                            }
                            identity_str += "<div style='clear: both'></div></div>";
                        }
                        $('#voucher_content').append(identity_str);

                        account_str = '';
                        if(json.data.account.length>0 && json.data.account){
                            account_str += "<div><div class='head'><lable>账户凭证</lable></div>";
                            for (var i=0;i<json.data.account.length;i++){
                                data = json.data.account[i];
                                account_str += "<div class='col-md-3 single_div'><label style='display: block;height: 36px;'>"+ data.name +"</label><button class='btn btn-xs btn-primary col-md-6 rotation_left'>向左转</button> <button class='btn btn-xs btn-primary col-md-6 rotation_right'>向右转</button><img onerror="+"this.src='/static/common/img/default.jpg'"+" style='width: 180px;height: 100px' data-angle='0' src="+ data.imgurl +" data-original="+ data.imgurl +" alt="+ data.name +"><div style='margin:13px 0px 5px; '><label>提交时间：</label> <label>"+ data.submit_time +"</label></div></div>";
                            }
                            account_str += "<div style='clear: both'></div></div>";
                        }
                        $('#voucher_content').append(account_str);

                        shop_str = '';
                        if(json.data.shop.length>0 && json.data.shop){
                            shop_str += "<div><div class='head'><lable>店铺凭证</lable></div>";
                            for (var i=0;i<json.data.shop.length;i++){
                                data = json.data.shop[i];
                                shop_str += "<div class='col-md-3 single_div'><label style='display: block;height: 36px;'>"+ data.name +"</label><button class='btn btn-xs btn-primary col-md-6 rotation_left'>向左转</button> <button class='btn btn-xs btn-primary col-md-6 rotation_right'>向右转</button><img onerror="+"this.src='/static/common/img/default.jpg'"+" style='width: 180px;height: 100px' data-angle='0' src="+ data.imgurl +" data-original="+ data.imgurl +" alt="+ data.name +"><div style='margin:13px 0px 5px; '><label>提交时间：</label> <label>"+ data.submit_time +"</label></div></div>";
                            }
                            shop_str += "<div style='clear: both'></div></div>";
                        }
                        $('#voucher_content').append(shop_str);

                        other_str = '';
                        if(json.data.other.length>0 && json.data.other){
                            other_str += "<div><div class='head'><lable>其他凭证</lable></div>";
                            for (var i=0;i<json.data.other.length;i++){
                                data = json.data.other[i];
                                other_str += "<div class='col-md-3 single_div'><label style='display: block;height: 36px;'>"+ data.name +"</label><button class='btn btn-xs btn-primary col-md-6 rotation_left'>向左转</button> <button class='btn btn-xs btn-primary col-md-6 rotation_right'>向右转</button><img onerror="+"this.src='/static/common/img/default.jpg'"+" style='width: 180px;height: 100px' data-angle='0' src="+ data.imgurl +" data-original="+ data.imgurl +" alt="+ data.name +"><div style='margin:13px 0px 5px; '><label>提交时间：</label> <label>"+ data.submit_time +"</label></div></div>";
                            }
                            other_str += "<div style='clear: both'></div></div>";
                        }
                        $('#voucher_content').append(other_str);

                   }else {
                       toastr.warning('XXX');
                   }
               },
               error: function (msg) {
                   toastr.error('操作失败 ！');
               }
           });

        $.ajax({
             async: false,
             dataType: 'json',
             url: '/api/v1/base_info',
             type: 'GET',
             data: {
                 uid : detail_id
             },
             // contentType: "application/json; charset=utf-8",
             success:(function (json) {
                 if(json.data.success && json.data && json){
                     $('#user_type').html(json.data.info.user_type_name);
                     $('#user_state').html(json.data.info.user_state_name);
                     $('#src').html(json.data.info.src);
                     $('#apply_state').html(json.data.info.apply_state_name);

                     $('#applytime').html(json.data.info.applytime);
                     $('#lastaudittime').html(json.data.info.lastaudittime);
                     $('#name').html(json.data.info.name);
                     $('#legalperson').html(json.data.info.legalperson);
                     $('#idnumber').html(json.data.info.idnumber);
                     $('#idenddate').html(json.data.info.idstatdate + '至' + json.data.info.idenddate);

                     $('#dishonestyinfo').html(json.data.info.dishonestyinfo);
                     //门店类型
                     $('#shop_type').html(json.data.info.shop_type);
                     // 其他身份
                     $('#cates').html(json.data.info.cates);
                     $('#mobile_m').html(json.data.info.mobile);
                     $('#nick_name').html(json.data.info.nickname);
                     $('#address_a').html(json.data.info.province + '-' + json.data.info.city);
                     $('#businessaddr').html(json.data.info.businessaddr);
                     // $('#address_b').html(json.data.info.address);
                     gps2address(json.data.info.longitude+ ' ' + json.data.info.latitude);
                     $('#mcc').html(json.data.info.mcc_name);
                     $('#email').html(json.data.info.email);
                     $('#telephone').html(json.data.info.telephone);
                     //用户标签
                     $('#user_tag').html(json.data.info.user_tag);

                     $('#banktype').html(json.data.info.bank_type_name);
                     $('#bankuser').html(json.data.info.bankuser);
                     $('#bankProvince').html(json.data.info.bankProvince);
                     $('#bankCity').html(json.data.info.bankCity);
                     $('#headbankname').html(json.data.info.headbankname);
                     $('#bankname').html(json.data.info.bankname);
                     $('#bankaccount').html(json.data.info.bankaccount);
                     $('#bankcode').html(json.data.info.brchbank_code);

                     $('#pre_phone').html(json.data.info.bankmobile);

                 }else {

                 }
             }),
             error:function (msg) {
                  toastr.error('操作失败 ！');
             }
        });

        $.ajax({
            async: false,
            dataType: 'json',
            url: '/api/v1/qudao_info',
            type: 'GET',
            data: {
                uid : detail_id,
                qudaoid:detail_groupid
            },
            success:(function (json) {
                if(json.success){
                    $('#channel_type').html(json.info.type_name);
                    $('#channel_uid').html(json.info.qudao_id);
                    $('#channel_name').html(json.info.name);
                    if(json.info.status == 1){
                        $('#channel_status').html('禁用');
                    }else {
                        $('#channel_status').html('启用');
                    }
                    $('#channel_business_mobile').html(json.info.business_mobile);
                    $('#channel_business_name').html(json.info.business_name);
                    $('#channel_manager_name').html(json.info.manager_name);
                    $('#channel_service_manager_name').html(json.info.service_manager_name);
                    $('#channel_memo').html(json.info.memo);
                    str = '';
                    for (var i = 0;i<json.info.area;i++){
                        str += "<tr><td>"+ json.info.area[i].province +"</td><td>"+ json.info.area[i].city +"</td><td>"+ json.info.area[i].county +"</td></tr>";
                    }
                    $('#areas').html(str);
                }else {
                    $('#channel_type').html('--');
                    $('#channel_uid').html('--');
                    $('#channel_name').html('--');
                    $('#channel_status').html('--');
                    $('#channel_business_mobile').html('--');
                    $('#channel_business_name').html('--');
                    $('#channel_manager_name').html('--');
                    $('#channel_service_manager_name').html('--');
                    $('#channel_memo').html('--');
                    $('#areas').html('');
                }
            }),
            error:function (msg) {
                toastr.error('操作失败 ！');
            }
        });
        get_user_tags()
        function get_user_tags(){
            var data = {}
            data.userid = $('#id_title').html()
            data.status = '1'
            data.pageSize = 200
            $.ajax({
                url: '/tag_list',
                type: 'GET',
                data: data,
                dataType: 'json',
                success: function(resp) {
                    if (resp['respcd'] == '0000') {
                        tags = resp['data']['list']
                        html = '<div class="form-group"><h2>'
                        $.each(tags, function(k,v){
                            html += '<span class="label label-primary m-l m-t" style="float:left">'
                            html += v.cate_name
                            html += '</span>'
                        })
                        html += '</h2></div>'
                        $('#tag').html(html)
                    } else {
                        toastr.error(msg=resp['respmsg'], title='获取信息数据失败');
                    }
                },
                error:function(data) {
                    toastr.warning('网络不好， 请稍后重试!!!');
                }
            })
        }



        // 产品及费率
        var busicd = {
            "debit_card": "借记卡",
            "credit_card": "信用卡",
            "800201": "微信正扫",
            "800208": "微信反扫",
            "800207": "微信H5",
            "800101": "支付宝正扫",
            "800108": "支付宝反扫",
            "800107": "支付宝H5",
            "800601": "QQ钱包正扫",
            "800608": "QQ钱包反扫",
            "800607": "QQ钱包H5",
            "800501": "京东正扫",
            "800508": "京东反扫",
            "800507": "京东H5",
        };
        // 初始化显示
        for (var key in busicd) {
            $("#aggregate [type=" + key + "]").html(
                "<td>" + busicd[key] + "</td>" +
                "<td>否</td>" +
                "<td>--</td>" +
                "<td>--</td>" +
                "<td>--</td>" +
                "<td>--</td>" +
                "<td>--</td>" +
                "<td>--</td>" +
                "<td>--</td>"
            );
        }
        $.ajax({
             async: false,
             dataType: 'json',
             url: '/api/v1/fee_ratio',
             type: 'GET',
             data: {
                 uid : detail_id
             },
             success:(function (json) {
                 if(json && json.data) {
                     for(var key in json.data) {
                         $("#aggregate [type=" + key + "]").html(
                             "<td>" + json.data[key].trade_type + "</td>" +
                             "<td>" + json.data[key].available + "</td>" +
                             "<td>" + json.data[key].deduct_type + "</td>" +
                             "<td>" + json.data[key].ratio + "</td>" +
                             "<td>" + json.data[key].max_fee + "</td>" +
                             "<td>" + json.data[key].risk_level + "</td>" +
                             "<td>" + json.data[key].amt_per + "</td>" +
                             "<td>" + json.data[key].settle_cycle + "</td>" +
                             "<td>" + json.data[key].settle_mode + "</td>"
                         );
                     }
                 }else {

                 }
             }),
             error:function (msg) {
                  toastr.error('操作失败 ！');
             }

        });

        // 增值产品
        var goods_codes = {
            "card": "会员服务",
            "diancan": "点餐服务",
            "prepaid": "储值服务"
        };
        // 初始化显示
        for (var key in goods_codes) {
            $("#payInfo [type=" + key + "]").html(
                "<td>" + goods_codes[key] + "</td>" +
                "<td>--</td>" +
                "<td>--</td>" +
                "<td>--</td>" +
                "<td>--</td>" +
                "<td>--</td>" +
                "<td>--</td>" +
                "<td>--</td>"
            );
        }
        $.ajax({
             async: false,
             dataType: 'json',
             url: '/api/v1/pay_info',
             type: 'GET',
             data: {
                 uid : detail_id
             },
             success:(function (json) {
                 if(json && json.data) {
                     for(var key in json.data) {
                         $("#payInfo [type=" + key + "]").html(
                             "<td>" + goods_codes[key] + "</td>" +
                             "<td>" + json.data[key].status + "</td>" +
                             "<td>" + json.data[key].overdue + "</td>" +
                             "<td>" + json.data[key].is_qfgroup + "</td>" +
                             "<td>" + json.data[key].free + "</td>" +
                             "<td>" + json.data[key].left_day + "</td>" +
                             "<td>" + json.data[key].left_warn + "</td>" +
                             "<td>" + json.data[key].expire_time + "</td>"
                         );
                         $("#balance_status").html("提现：" + json.data["balance"].status)
                     }
                 }else {

                 }
             }),
             error:function (msg) {
                  toastr.error('操作失败 ！');
             }

        });

        // 绑定终端
        // 初始化显示
        $("#bind_terminal #terminal_count").html("--");
        $("#bind_terminal #terminals").html("");
        $.ajax({
             async: false,
             dataType: 'json',
             url: '/api/v1/terminal',
             type: 'GET',
             data: {
                 uid : detail_id
             },
             success:(function (json) {
                 if(json && json.data) {
                     $("#bind_terminal #terminal_count").html(json.data.length.toString());
                     var html_str = "";
                     for(var i=0; i<json.data.length; i++) {
                         var t = json.data[i];
                         html_str += '<div class="col-md-12" style="margin-bottom: 20px;border: 1px solid #e5e5e5">';
                         html_str += '<div class="form-group form-inline col-md-6" style="text-align: left">';
                         html_str += '<label>设备编号：</label>';
                         html_str += '<label>' + t.terminalid + '</label>';
                         html_str += '</div>';
                         html_str += '<div class="form-group form-inline col-md-6" style="text-align: left">';
                         html_str += '<label>激活时间：</label>';
                         html_str += '<label>' + t.active_date + '</label>';
                         html_str += '</div>';
                         html_str += '<div class="form-group form-inline col-md-6" style="text-align: left">';
                         html_str += '<label>设备名称：</label>';
                         html_str += '<label>' + t.model + '</label>';
                         html_str += '</div>';
                         html_str += '<div class="form-group form-inline col-md-6" style="text-align: left">';
                         html_str += '<label>状态：</label>';
                         html_str += '<label>' + t.state + '</label>';
                         html_str += '</div>';
                         html_str += '</div>';
                     }
                     $("#bind_terminal #terminals").html(html_str);
                 }else {

                 }
             }),
             error:function (msg) {
                  toastr.error('操作失败 ！');
             }

        });

        $('#myDetail').modal('show');
    });
});

$(function(){
    $(document).on('click','.rotation_left',function () {
        var img = $(this).siblings('img');
        angle = parseInt(img.attr('data-angle'));
        angle += 90;
        $(this).siblings('img').rotate(angle);
        img.attr('data-angle',angle);
        img.toggleClass('max');
    });

    $(document).on('click','.rotation_right',function () {
       var img = $(this).siblings('img');
        angle = parseInt(img.attr('data-angle'));
        angle -= 90;
        $(this).siblings('img').rotate(angle);
        img.attr('data-angle',angle);
    });

    $(document).on('click','img',function () {
        $(this).viewer({url:"data-original"});
    });

    $(document).on('click','#relationBtn',function () {
        $('#uid').val($(this).attr('data-id'));
        $('#mobile').val('');
        $('#gid').val('');
        $('#gname').val('');
        $('#fullname').val('');
        $('#nickname').val('');
        debugger
        cosole.log('click it')

        oTable.ajax.reload();
        $('#relation').modal('hide');
        $('#myDetail').modal('hide');
    });

    $(document).on('click','#idrelationBtn',function () {
        $('#uid').val($(this).attr('data-id'));
        $('#mobile').val('');
        $('#gid').val('');
        $('#gname').val('');
        $('#fullname').val('');
        $('#nickname').val('');
        debugger
        cosole.log('click it')

        oTable.ajax.reload();
        $('#idcard_relation').modal('hide');
        $('#myDetail').modal('hide');
    });

    $('#relation_btn').click(function () {
        curr_id = $(this).attr('data-id');
        // relationTable.ajax.reload();
        // relationTable = initRelationTable();
        if(relationTable){
            relationTable.ajax.reload();
        }else {
            relationTable = initRelationTable();
        }
        $('#relation').modal('show');
    });

    $('#id_relation_btn').click(function () {
        // IDrelationTable.ajax.reload();
        // IDrelationTable = initIDRelationTable();
        if(IDrelationTable){
            IDrelationTable.ajax.reload();
        }else {
            IDrelationTable = initIDRelationTable();
        }
        $('#idcard_relation').modal('show');
    });

});
