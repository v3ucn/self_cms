/**
 * Created by qfpay on 2018/3/19.
 */
// 公众号管理
var MerchantConfigTableTable = null; //列表table
var select_ids = []; //已经选择的id
var ids = []; //全部的id
$(function () {
    $.ajax({
        async: true,
        url:'/getAppID',
        type:'POST',
        dataType:'json',
        data:{},
        success:(function (json) {
            var str = '';
            $('#officialAccountName').html("<option value=''>"+'全部'+"</option>");
            $.each(json.data.appid, function (i,item) {
                str += "<option value='"+ item.appid +"'>" + item.nick_name + "</option>"
            });
            $('#officialAccountName').append(str);
            $('#officialAccountName').selectpicker('refresh');
        }),
        error:(function () {
            toastr.error('网络异常，请重试！');
        })
    });
    initToastr();
    initSelect();
    clickEvent();
    MerchantConfigTableTable = initMerchantConfigTableTable();
});
function initToastr() {
     //设置显示配置
     var messageOpts = {
         "closeButton" : true,//是否显示关闭按钮
         "debug" : false,//是否使用debug模式
         "positionClass" : "toast-top-right",//弹出窗的位置
         "onclick" : null,
         "showDuration" : "300",//显示的动画时间
         "hideDuration" : "1000",//消失的动画时间
         "timeOut" : "2000",//展现时间
         "extendedTimeOut" : "1000",//加长展示时间
         "showEasing" : "swing",//显示时的动画缓冲方式
         "hideEasing" : "linear",//消失时的动画缓冲方式
         "showMethod" : "fadeIn",//显示时的动画方式
         "hideMethod" : "fadeOut" //消失时的动画方式
     };
     toastr.options = messageOpts;
}

function daochu_change(_id) {


    var form=$("<form>");//定义一个form表单

        form.attr("style","display:none");
        form.attr("target","_blank");
        form.attr("method","post");
        form.attr("action","/mchnt_log_tradeExcel");

        var inputuid=$("<input>");
        inputuid.attr("type","hidden");
        inputuid.attr("name","id");
        inputuid.attr("value",_id);
        form.append(inputuid);

        $("body").append(form);//将表单放置在web中
        form.submit();//表单提交

}

function clickEvent() {
    //查询按钮的点击事件
    $('#query').click(function () {
        select_ids = [];
        $('#check_all').prop('checked',false);
        MerchantConfigTableTable.destroy();
        MerchantConfigTableTable = initMerchantConfigTableTable();
    });
    //导出按钮的点击事件
    $('#export').click(function () {
        console.log(select_ids);
        if (select_ids.length == 0){
            toastr.info('请选择您要导出的条目！');
            return;
        }
        var form=$("<form>");//定义一个form表单

        form.attr("style","display:none");
        form.attr("target","_blank");
        form.attr("method","post");
        form.attr("action","/app_excel");

        select_str = select_ids.join(',');
        var inputuid=$("<input>");
        inputuid.attr("type","hidden");
        inputuid.attr("name","ids");
        inputuid.attr("value",select_str);
        form.append(inputuid);

        $("body").append(form);//将表单放置在web中
        form.submit();//表单提交
    });
    //全部选取的check
    $('#check_all').click(function () {
        if($(this).is(':checked') == true){
            $('.id_check').prop('checked',true);
            select_ids = $.extend(true,select_ids,ids);
            // $.extend(true,select_ids,ids);
        }else if($(this).is(':checked') == false){
            $('.id_check').prop('checked',false);
            select_ids = [];
        }
        console.log(select_ids);
    });
    //单个选中按钮的点击事件
    $(document).on('click','.id_check',function () {
        if($(this).is(':checked') == true){
            // $('.uid_check').prop('checked',true);
            select_ids.push(parseInt($(this).siblings('span').text()));
            if(select_ids.length == ids.length){
                $('#check_all').prop('checked',true);
            }
        }else if($(this).is(':checked') == false){
            $('#check_all').prop('checked',false);
            select_ids.remove(parseInt($(this).siblings('span').text()));
        }
    });
}
//selectpicker组件初始化
function initSelect() {
    // $('#officialAccountName').selectpicker({
    //     style: 'btn-inverse',
    // });
    // $('#time').selectpicker({
    //     style: 'btn-inverse',
    // });
    //
    // alert("123");

    var date_t = new Date();
    var date_y = new Date(date_t.getTime()-24*60*60*1000);
    var date_30 = new Date(date_t.getTime()-24*60*60*1000*30);
    laydate.render({
        elem: '#startdate'
        // ,type: 'datetime'
        ,format: 'yyyy-MM-dd'
        ,theme: 'molv'
        ,istoday: false
        ,value: date_30
        ,mark: {
            '0-5-1': '劳动节'
            ,'0-10-1': '国庆节'
        }
        // ,max: laydate.now() //最大日期

    });

    laydate.render({
        elem: '#enddate'
        // ,type: 'datetime'
        ,format: 'yyyy-MM-dd'
        ,theme: 'molv'
        ,istoday: false
        ,value: date_t
        ,mark: {
            '0-5-1': '劳动节'
            ,'0-10-1': '国庆节'
        }
        // ,max: laydate.now() //最大日期

    });

}
function getNowFormatDate(num) {
    var date1 = new Date();
    var date = new Date(date1.getTime()+24*60*60*1000*num);

    var seperator1 = "-";
    var seperator2 = ":";
    var month = date.getMonth() + 1;
    var strDate = date.getDate();
    if (month >= 1 && month <= 9) {
        month = "0" + month;
    }
    if (strDate >= 0 && strDate <= 9) {
        strDate = "0" + strDate;
    }
    // var currentdate = date.getFullYear() + seperator1 + month + seperator1 + strDate
    //         + " " + date.getHours() + seperator2 + date.getMinutes()
    //         + seperator2 + date.getSeconds();
    // var currentdate = date.getFullYear() + seperator1 + month + seperator1 + strDate
    //         + " " + "23:59:59";
    var currentdate = date.getFullYear() + seperator1 + month + seperator1 + strDate;
    return currentdate;
}

// 表格初始化
function initMerchantConfigTableTable() {
    var table = $("#OfficialAccountManageTable").DataTable({
        "paging": true,
        "order": [],
        "pagingType": "full_numbers",
        "lengthMenu": [10],
        "bDestory": true,
        "destroy":true,
        "autoWidth":false,
        "bLengthChange": false,
        "processing": true,
        "searching": false, //是否开启搜索
        "serverSide": true, //开启服务器获取数据
        "ajax": { // 获取数据
            "url": "/mchnt_change_log_list",
            "contentType": 'application/json;',
            "type": "POST",
            "dataType": "json", //返回来的数据形式
            "data": function (d) {
                // d.state = $('#status').val();
                _mchntid = $('#mchntid').val();
                _mchntid = _mchntid.replace(/，/g,',');
                d.uid = _mchntid;
                // var receive_time = $('#time').val();
                // if(receive_time){
                //     var start_time = getNowFormatDate(0-parseInt(receive_time));
                //     var end_time = getNowFormatDate(0);
                //     d.start_time = start_time;
                //     d.end_time = end_time;
                // }else {
                //     d.start_time = "";
                //     d.end_time = "";
                // }
                d.start_time = $("#startdate").val();
                d.end_time = $("#enddate").val();

                return JSON.stringify(d);
            },
        },
        "columnDefs": [ //自定义列
            {
                "targets": 0,
                "width": 20,
                "render": function (data, type, row) {
                    var htmlStr = "<label>"+row.id+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 1,
                "width": 130,
               "render": function (data, type, row) {
                    var htmlStr = "<label>"+row.mchnt+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 2,
                "width": 150,
                "render": function (data, type, row) {
                    var htmlStr = "<label>"+row.appname+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 3, //改写哪一列
                "width": 100,
                "render": function (data, type, row) {
                    var htmlStr = "<label>"+row.appid+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 4, //改写哪一列
                "width": 100,
                "render": function (data, type, row) {
                    var htmlStr = "<label>"+row.user+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 5, //改写哪一列
                "width": 100,
                 "render": function (data, type, row) {
                    var htmlStr = "<label>"+row.ctime+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 6, //改写哪一列
                "width": 100,
                "render": function (data, type, row) {
                    var htmlStr = "<label>"+row.memo+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 7, //改写哪一列
                'width':130,
                "render": function (data, type, row) {
                    var htmlStr = "<div><a href='#' onclick=\"daochu_change('"+row.id+"')\" >下载</a></div>";
                    return htmlStr;
                }
            },
            {
                "targets": [0, 1, 2, 3, 4, 5, 6,7],
                "orderable": false  //禁止排序
            }
        ],
        "initComplete": function (settings, json) {
            // alert( '初始化完成' );
            //ids = json.id;
            //console.log(ids);
        },
        "drawCallback": function(settings) {
            // alert( '表格重绘了' );
            // if($('#check_all').is(':checked') == true){
            //     $('.id_check').prop('checked',true);
            // }else {
            //     $('.id_check').each(function (i,item) {
            //         if (select_ids.in_array(parseInt($(this).siblings('span').text()))){
            //             $(this).prop('checked',true);
            //         }
            //     })
            // }
        },
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
                // "sSortAscending": ": 以升序排列此列",
                // "sSortDescending": ": 以降序排列此列"
            }
        }
    });
    return table;
}

