/**
 * Created by qfpay on 2018/2/27.
 */

var changListTable = null;
$(function () {

     /*日历插件的初始化*/
    laydate.render({
        elem: '#createtime'
        // ,type: 'datetime'
        ,theme: '#009688'
        ,type: 'datetime'
        ,max: 1
        ,value: null
        ,done: function(value, date, endDate) {

        }
        ,change: function(value, date){

        }
    });
    /*日历插件的初始化*/
    laydate.render({
        elem: '#dealtime'
        // ,type: 'datetime'
        ,theme: '#009688'
        ,type: 'datetime'
        ,max: 1
        ,value: null
        ,done: function(value, date, endDate) {

        }
        ,change: function(value, date){

        }
    });

    laydate.render({
        elem: '#startdate'
//                ,type: 'datetime'
        ,theme: '#009688'
        ,max: 1
        ,value: new Date()
        ,done: function(value, date, endDate) {
            $('.btn-date').toggleClass('btn-primary active',false).toggleClass('btn-default',true);
        }
    });

    laydate.render({
        elem: '#enddate'
//                ,type: 'datetime'
        ,theme: '#009688'
        ,max: 1
        ,value: new Date()
        ,done: function(value, date, endDate) {
            $('.btn-date').toggleClass('btn-primary active',false).toggleClass('btn-default',true);
        }
    });

    $('#usertype').selectpicker({
        style: 'btn-inverse',
    });

    $('#userstatus').selectpicker({
        style:'btn-inverse',
    });
    $('#mccselect').selectpicker({
        style:'btn-inverse',
    });
    $('#provice').selectpicker({
        style:'btn-inverse',
        width:'125px',
    });
    $('#city').selectpicker({
        style:'btn-inverse',
        width:'125px',
    });
    $('#check_provice').selectpicker({
        style:'btn-inverse',
        width:'125px',
    });
    $('#check_city').selectpicker({
        style:'btn-inverse',
        width:'125px',
    });

    $(".myfile").fileinput({
        showUpload: false, //是否显示上传按钮
        showCaption: false,//是否显示标题
        allowedFileTypes: ['image'],//配置允许文件上传的类型
        allowedPreviewTypes : [ 'image' ],//配置所有的被预览文件类型
        allowedPreviewMimeTypes : [ 'jpg', 'png', 'gif' ],//控制被预览的所有mime类型
        browseClass: "btn btn-primary", //按钮样式
        language : 'zh'
    });

    $('#add_btn').click(function () {
        $('#add_modal').modal('show');
    });

    $('#add_close').click(function () {
        $('#add_modal').modal('hide');
    });

    $('#query_btn').click(function () {
        changListTable = initChangeListTable();
    });

    $('#add_sure').click(function () {
        // $('#add_modal').modal('hide');
        if($('#change_type').val() == '0'){
            $('#baseinfo_change').modal('show');
        }else if($('#change_type').val() == '1'){
            $('#accountinfo_change').modal('show');
        }else if($('#change_type').val() == '2'){
            $('#rate_change').modal('show');
        }else if($('#change_type').val() == '3'){
            $('#certificate_change').modal('show');
        }else if($('#change_type').val() == '4'){
            $('#baseinfo_check').modal('show');
        }else if($('#change_type').val() == '5'){
            $('#accountinfo_check').modal('show');
        }else if($('#change_type').val() == '6'){
            $('#rate_check').modal('show');
        }else if($('#change_type').val() == '7'){
            $('#certificate_check').modal('show');
        }
    });
});

function initChangeListTable() {
    var table = $("#change_list").DataTable({
        "paging": true,
        "pagingType": "full_numbers",
        "lengthMenu": [10],
        "bDestory": true,
        "destroy":true,
        // "retrieve": true,
        "bLengthChange": false,
        "processing": true,
        "searching": false, //是否开启搜索
        "serverSide": true, //开启服务器获取数据
        "ajax": { // 获取数据
            "url": "/api/v1/change_list",
            "data": function (d) {
                d.uid_mobile = $('#uid_mobile').val(),
                d.createtime = $('#createtime').val(),
                d.dealtime = $('#dealtime').val()
            },
            "type": "POST",
            "dataType": "json" //返回来的数据形式
        },
        "columns": [ //定义列数据来源
            {'title': "序号", 'data': null},
            {'title': "用户ID", 'data': null},
            {'title': "类型", 'data': null},
            {'title': "审核状态", 'data': null},
            {'title': "来源", 'data': null},
            {'title': "创建时间", 'data': null},
            {'title': "处理时间", 'data': null},
            {'title': "审核备注", 'data': null},
            {'title': "通道同步", 'data': null},
            {'title': "通道同步", 'data': null},
            {'title': "操作", 'data': null},
        ],
        "columnDefs": [ //自定义列
            {
                "targets": 0, //改写哪一列
                // "data": "uid",
                "render": function (data, type, row) {
                    var htmlStr = "";
                    return htmlStr;
                }
            },
            {
                "targets": -1, //改写哪一列
                // "data": "uid",
                "render": function (data, type, row) {
                    var htmlStr = "<button>"+'审核'+"</button>";
                    return htmlStr;
                }
            },

            {
                "targets": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
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