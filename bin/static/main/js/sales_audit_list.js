/**
 * Created by qfpay on 2018/3/19.
 */
// 公众号管理
var MerchantConfigTableTable = null; //列表table
var select_ids = []; //已经选择的id
var ids = []; //全部的id


function getCookie(name){
var strcookie = document.cookie;
var arrcookie = strcookie.split("; ");
//遍历匹配
for ( var i = 0; i < arrcookie.length; i++) {
var arr = arrcookie[i].split("=");
if (arr[0] == name){
return arr[1];
}
}
return "";
}

$(function () {


    initSelect();

    initMerchantConfigTableTable();




    $('#audit_sales').click(function () {

        $("#userid_group").val("");
        $("#memo").val("");

        // 修改请求数据
        $('#modal_add').modal('show');
    });


    $('#audit_import').click(function () {


        $("#file_upload").val("");

        $('#modal_add_dao').modal('show');
    });








    $('#query_sales').click(function () {
        var d1=new Date($('#startdate').val());
    var d2=new Date($('#enddate').val());
    var d3=(d2-d1)/1000;
    if(d3<0){
        toastr.info('时间区间选择不合法，请重新选择！');
        return false;
    }
        initMerchantConfigTableTable();
    });




    $("#zip").click(function () {

        var _uid = getCookie("uid");

        $.ajax({
        async: true,
        url:'/sales_download', timeout: 50000,
        type:'POST',
        dataType:'json',
            "beforeSend": function(){
$('#zip').attr("disabled",true);
    },
    "complete": function(){
     $('#zip').attr("disabled",false);
    },
        data:{
            'mchntid' : $("#mchntid").val(),
            'state' : $("#state").val(),
            'type' : $("#type").val(),
            'startdate' : $("#startdate").val(),
            'enddate' : $("#enddate").val()
        },
        success:(function (json) {
           var url = "/static/common/zip/zip_"+_uid+".zip";
           window.open(url);
        }),
        error:(function () {
            toastr.error('网络异常，请重试！');
        })
    });



    });



    $('#export_sales').click(function () {
       // console.log(select_ids);

        var form=$("<form>");//定义一个form表单

        form.attr("style","display:none");
        form.attr("target","_blank");
        form.attr("method","post");
        form.attr("action","/salesexcel");

        var inputuid=$("<input>");
        inputuid.attr("type","hidden");
        inputuid.attr("name","mchntid");
        inputuid.attr("value",$("#mchntid").val());
        form.append(inputuid);

        var inputuid=$("<input>");
        inputuid.attr("type","hidden");
        inputuid.attr("name","type");
        inputuid.attr("value",$("#type").val());
        form.append(inputuid);

        var inputuid=$("<input>");
        inputuid.attr("type","hidden");
        inputuid.attr("name","state");
        inputuid.attr("value",$("#state").val());
        form.append(inputuid);

        var inputuid=$("<input>");
        inputuid.attr("type","hidden");
        inputuid.attr("name","startdate");
        inputuid.attr("value",$("#startdate").val());
        form.append(inputuid);

        var inputuid=$("<input>");
        inputuid.attr("type","hidden");
        inputuid.attr("name","enddate");
        inputuid.attr("value",$("#enddate").val());
        form.append(inputuid);

        $("body").append(form);//将表单放置在web中
        form.submit();//表单提交
    });



});


function FileUpload() {
            var form_data = new FormData();
            var file_info =$( '#file_upload')[0].files[0];
            form_data.append('file',file_info);
            //if(file_info==undefined)暂且不许要判断是否有附件
                //alert('你没有选择任何文件');
                //return false
            $.ajax({
                url:'/upload_ajax',
                type:'POST',
                data: form_data,
                processData: false,  // tell jquery not to process the data
                contentType: false, // tell jquery not to set contentType
                success: function(callback) {

                    if(callback.code = 200){

                    $('#modal_add_dao').modal('hide');
                    initMerchantConfigTableTable();

                    }else{


                        toastr.error(callback.msg);

                    }
                }
            });

    }


function doaudit(_type){


    if($('#userid_group').val() == ""){

    toastr.warning("商户ID不能为空");
    return;
    }


    _mchntid = $('#userid_group').val();
                _mchntid = _mchntid.replace(/，/g,',');


    $.ajax({
        async: true,
        url:'/sales_do_audit',
        type:'POST',
        dataType:'json',
        // data:function (d) {
        //         // d.state = $('#status').val();
        //
        //         d.memo = $("#memo").val();
        //         d.type = _type;
        //         return JSON.stringify(d);
        //     },
        data: {
                uids: _mchntid,
                memo:$("#memo").val(),
                type : _type,
                stype:$("#stype").val()
            },
        success:(function (json) {

            $('#modal_add').modal('hide');
            initMerchantConfigTableTable();
        }),
        error:(function () {
            toastr.error('网络异常，请重试！');
        })
    });






}


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
         ,type: 'datetime'
        //,format: 'yyyy-MM-dd'
        ,theme: 'molv'
        ,istoday: false
        ,value: new Date()
        ,mark: {
            '0-5-1': '劳动节'
            ,'0-10-1': '国庆节'
        }
        // ,max: laydate.now() //最大日期

    });

    laydate.render({
        elem: '#enddate'
         ,type: 'datetime'
        //,format: 'yyyy-MM-dd'
        ,theme: 'molv'
        ,istoday: false
        ,value: new Date()
        ,mark: {
            '0-5-1': '劳动节'
            ,'0-10-1': '国庆节'
        }
        // ,max: laydate.now() //最大日期

    });

    $('#enddate').val(getNowFormatDate(0));
    $('#startdate').val(fun_date(0));

}


function fun_date(num){
    var date1 = new Date();
    // // time1=date1.getFullYear()+"-"+(date1.getMonth()+1)+"-"+date1.getDate();//time1表示当前时间
    // var date2 = new Date();
    // date2.setDate(date1.getDate()+num);
    // var time2 = date2.getFullYear()+"-"+(date2.getMonth()+1)+"-"+date2.getDate()+" "+"00:00:00";
    // return time2;
    var date2 = new Date();
    date2.setDate(date1.getDate()+num);
    var month = date2.getMonth()+1;
    var strDate = date2.getDate();
    if (month >= 1 && month <= 9) {
        month = "0" + month;
    }
    if (strDate >= 0 && strDate <= 9) {
        strDate = "0" + strDate;
    }
    var time2 = date2.getFullYear() + "-" + month + "-" + strDate + " " + "00:00:00";
    return time2
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
    var currentdate = date.getFullYear() + seperator1 + month + seperator1 + strDate
            + " " + "23:59:59";
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
            "url": "/sales_audit_list",
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

                d.type = $("#type").val();
                d.state = $("#state").val();

                return JSON.stringify(d);
            },
        },
        "columnDefs": [ //自定义列
            {
                "targets": 0,
                "width": 20,
                "render": function (data, type, row) {
                    var htmlStr = "<label>"+row.userid+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 1,
                "width": 130,
               "render": function (data, type, row) {
                    var htmlStr = "<label>"+row.type+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 2,
                "width": 150,
                "render": function (data, type, row) {
                    var htmlStr = "<label>"+row.ctime+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 3, //改写哪一列
                "width": 100,
                "render": function (data, type, row) {
                    var htmlStr = "<label>"+row.sls_uid+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 4, //改写哪一列
                "width": 100,
                "render": function (data, type, row) {
                    var htmlStr = "<label>"+row.state+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 5, //改写哪一列
                "width": 100,
                 "render": function (data, type, row) {
                    var htmlStr = "<label>"+row.memo+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 6, //改写哪一列
                "width": 100,
                "render": function (data, type, row) {
                    var htmlStr = "<label>"+row.admin_userid+"</label>";
                    return htmlStr;
                }
            },
           {
                "targets": 7, //改写哪一列
                "width": 100,
                "render": function (data, type, row) {
                    var htmlStr = "<label>"+row.atime+"</label>";
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

