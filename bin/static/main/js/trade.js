/**
 * Created by qfpay on 2017/11/14.
 */

var oTable = null;
function initTable() {
    $.fn.dataTable.ext.errMode = 'none'; //不显示任何错误信息
    var table = $("#tradeTable").DataTable({
        // 'bAutoWidth': false,
        "autoWidth": false,
        "paging": true,
        "destroy":true,
        "pagingType": "full_numbers",
        "lengthMenu": [10 ,20, 50],
        // "bDestory": true,
        "bLengthChange": false,
        "processing": true,
        "searching": false, //是否开启搜索
        "serverSide": false, //开启服务器获取数据
        "ajax": { // 获取数据
            "url": "/api/v1/trade",
            "timeout": 15000,
            "data": function (d) {
                d.uid = $('#uid').val();
                d.chnlid = $('#chnlid').val();
                d.syssn = $('#syssn').val();
                d.groupid = $('#groupid').val();
                d.chnluserid = $('#chnluserid').val();
                d.startdate = $('#startdate').val();
                d.enddate = $('#enddate').val();
                d.starttxamt = $('#starttxamt').val();
                d.endtxamt = $('#endtxamt').val();
                d.status = $('#status').val();
                d.txcurrcd = $('#txcurrcd').val();
                d.busicd = $('#busicd').val();
                d.chnlsn = $('#chnlsn').val();
            },
            "async":true,
            "type": "GET",
            "dataType": "json", //返回来的数据形式
            "error" : function(XMLHttpRequest, textStatus, errorThrown){ //请求完成后最终执行参数
                if(textStatus == 'timeout'){
                    toastr.error('抱歉，数据量过大，臣妾做不到！');
                }else {
                    toastr.error('抱歉，查询失败！');
                }
            }

        },
        // "aoColumnDefs": [
        //     { "sWidth": "200px", "aTargets": [0]}
        // ],
        "columns": [ //定义列数据来源
            {'title': "用户ID", 'data': "userid"},
            {'title': "支付通道<br>通道商户号", 'data': null, 'class': "align-center"},
            {'title': "交易金额<br>币种", 'data': null, 'class': "align-center"},
            {'title': "支付类型", 'data': "busicd"},
            {'title': "交易状态<br>返回码", 'data': null},
            {'title': "取消状态", 'data': "cancel"},
            // {'title': "返回码", 'data': "retcd"},
            {'title': "钱方流水号<br>第三方订单号", 'data': null, 'class': "align-center"},
            // {'title': "原钱方流水号<br>原第三方订单号", 'data': null, 'class': "align-center"},
            {'title': "创建时间", 'data': null, 'class': "align-center"},
            {'title': "渠道ID", 'data': "groupid"},
            {'title': "操作", 'data': null, 'class': 'align-center'} // 自定义列
        ],
        "columnDefs": [ //自定义列
            {
                "targets": -1, //改写哪一列
                "data": null,
                "render": function (data, type, row) {
                    var htmlStr = "<button class='btn btn-primary' id='detail' data-action='detail' data-toggle='modal' data-target='#modal' data-syssn=" + row.syssn + " data-table=" + row.table_name + ">详情</button>";
                    return htmlStr;
                }
            },
            {
                "targets": 1, //改写哪一列
                "data": null,
                "render": function (data, type, row) {
                    var htmlStr = row.chnlid+"/"+row.chnlname+"<br>"+row.chnluserid;
                    return htmlStr;
                }
            },
            {
                "targets": 2, //改写哪一列
                "data": null,
                "render": function (data, type, row) {
                    var htmlStr = parseInt(row.txamt)/100+"<br>"+row.txcurrcd;
                    return htmlStr;
                }
            },
            {
                "targets": 4, //改写哪一列
                "data": null,
                "render": function (data, type, row) {
                    var htmlStr = "<span>"+row.trade_status+"</span><br><a href='#' title='"+ row.retcd_name+"'>"+row.retcd+"</a>";

                    return htmlStr;
                }
            },
            {
                "targets": 6, //改写哪一列
                "data": null,
                "render": function (data, type, row) {
                    var htmlStr = row.syssn+"<br>"+row.chnlsn;
                    return htmlStr;
                }
            },
            // {
            //     "targets": 8, //改写哪一列
            //     "data": null,
            //     "render": function (data, type, row) {
            //         var htmlStr = row.origssn+"<br>"+'暂无';
            //         return htmlStr;
            //     }
            // },
            {
                "targets": 7, //改写哪一列
                "data": null,
                "render": function (data, type, row) {
                    var htmlStr = "<span style='width: 200px'>" + row.txdtm + "</span>";
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
    $('#chnlid').selectpicker({
        style: 'btn-inverse',
        width: 180,
    });

    $.ajax({
        async:true,
        url:'/get_channel',
        type:'POST',
        dataType:'json',
        data:{},
        success:(function (json) {
            var chnlid_str = '';
            $('#chnlid').html("<option value=''>全部</option>");
            $.each(json.data,function (i,item) {
                chnlid_str += "<option value='"+ item.id +"'>" + item.name +"</option>"
            });
            $('#chnlid').append(chnlid_str);
            $('#chnlid').selectpicker('refresh');

        }),
        error:(function () {

        })
    });
    /*日历插件的初始化*/
    laydate.render({
        elem: '#startdate'
        ,type: 'datetime'
        ,theme: '#009688'
        ,max: 1
        ,value: new Date()
        ,done: function(value, date, endDate) {
            $('.btn-date').toggleClass('btn-primary active',false).toggleClass('btn-default',true);
        }
    });
    /*日历插件的初始化*/
    laydate.render({
        elem: '#enddate'
        ,type: 'datetime'
        ,theme: '#009688'
        ,max: 1
        ,value: new Date()
        ,done: function(value, date, endDate) {
            $('.btn-date').toggleClass('btn-primary active',false).toggleClass('btn-default',true);
        }
    });
    // 初始化两个日期的其实和终止时间
    $('#enddate').val(getNowFormatDate(0));
    $('#startdate').val(fun_date(0));

    // oTable = initTable();

    $('.btn-date').click(function () {
        $(this).toggleClass('btn-default active',false);
        $(this).toggleClass('btn-primary active',true);
        $(this).siblings().toggleClass('btn-default',true);
        $(this).siblings().toggleClass('btn-primary active',false);
    });

    $('.advanced').click(function () {
        $('#high-grade').toggle();
    });

    $('#query').click(function () {
        if(checkdate() == 0) {
            return;
        }
        if(checkmoney() == 0)
        {
            return;
        }
        if(!oTable){
            oTable = initTable();
        }else {
           oTable.destroy();
           oTable = initTable();
           // oTable.ajax.reload();
        }
        // //以下为发生错误时的事件处理，如不处理，可不管。
        // $('#tradeTable').on( 'error.dt', function ( e, settings, techNote, message ){
        //     //这里可以接管错误处理，也可以不做任何处理
        //     toastr.error('数据获取失败，请刷新重试！')
        // }).DataTable();
    });

    $('#export').click(function () {
        if(checkdate() == 0) {
            return;
        }
        if(checkmoney() == 0)
        {
            return;
        }
        uid = $('#uid').val();
        chnlid = $('#chnlid').val();
        syssn = $('#syssn').val();
        groupid = $('#groupid').val();
        chnluserid = $('#chnluserid').val();
        startdate = $('#startdate').val();
        enddate = $('#enddate').val();
        starttxamt = $('#starttxamt').val();
        endtxamt = $('#endtxamt').val();
        status = $('#status').val();
        txcurrcd = $('#txcurrcd').val();
        busicd = $('#busicd').val();
        chnlsn = $('#chnlsn').val();
        // window.open("/api/v1/trade_excel?uid="+uid+"&chnlid="+chnlid+"&syssn="+syssn+"&groupid"+groupid+"&chnluserid="
        //     +chnluserid+"&startdate="+startdate+"&enddate="+enddate+"&starttxamt="+starttxamt+"&endtxamt="+endtxamt+"&status="
        //     +status+"&txcurrcd="+txcurrcd+"&busicd="+busicd);

        var form=$("<form>");//定义一个form表单

        form.attr("style","display:none");
        form.attr("target","_blank");
        form.attr("method","post");
        form.attr("action","/api/v1/trade_excel");

        var inputuid=$("<input>");
        inputuid.attr("type","hidden");
        inputuid.attr("name","uid");
        inputuid.attr("value",uid);
        form.append(inputuid);

        var inputchnlid=$("<input>");
        inputchnlid.attr("type","hidden");
        inputchnlid.attr("name","chnlid");
        inputchnlid.attr("value",chnlid);
        form.append(inputchnlid);

        var inputsyssn=$("<input>");
        inputsyssn.attr("type","hidden");
        inputsyssn.attr("name","syssn");
        inputsyssn.attr("value",syssn);
        form.append(inputsyssn);

        var inputgroupid=$("<input>");
        inputgroupid.attr("type","hidden");
        inputgroupid.attr("name","groupid");
        inputgroupid.attr("value",groupid);
        form.append(inputgroupid);

        var inputchnluserid=$("<input>");
        inputchnluserid.attr("type","hidden");
        inputchnluserid.attr("name","chnluserid");
        inputchnluserid.attr("value",chnluserid);
        form.append(inputchnluserid);

        var inputstartdate=$("<input>");
        inputstartdate.attr("type","hidden");
        inputstartdate.attr("name","startdate");
        inputstartdate.attr("value",startdate);
        form.append(inputstartdate);

        var inputenddate=$("<input>");
        inputenddate.attr("type","hidden");
        inputenddate.attr("name","enddate");
        inputenddate.attr("value",enddate);
        form.append(inputenddate);

        var inputstarttxamt=$("<input>");
        inputstarttxamt.attr("type","hidden");
        inputstarttxamt.attr("name","starttxamt");
        inputstarttxamt.attr("value",starttxamt);
        form.append(inputstarttxamt);

        var inputendtxamt=$("<input>");
        inputendtxamt.attr("type","hidden");
        inputendtxamt.attr("name","endtxamt");
        inputendtxamt.attr("value",endtxamt);
        form.append(inputendtxamt);

        var inputstatus=$("<input>");
        inputstatus.attr("type","hidden");
        inputstatus.attr("name","status");
        inputstatus.attr("value",status);
        form.append(inputstatus);

        var inputtxcurrcd=$("<input>");
        inputtxcurrcd.attr("type","hidden");
        inputtxcurrcd.attr("name","txcurrcd");
        inputtxcurrcd.attr("value",txcurrcd);
        form.append(inputtxcurrcd);

        var inputbusicd=$("<input>");
        inputbusicd.attr("type","hidden");
        inputbusicd.attr("name","busicd");
        inputbusicd.attr("value",busicd);
        form.append(inputbusicd);

        var inputchnlsn=$("<input>");
        inputbusicd.attr("type","hidden");
        inputbusicd.attr("name","chnlsn");
        inputbusicd.attr("value",chnlsn);
        form.append(inputchnlsn);

        $("body").append(form);//将表单放置在web中
        form.submit();//表单提交
    });

    $('#seetotal').click(function () {
        if(checkdate() == 0) {
            return;
        }
        if(checkmoney() == 0) {
            return;
        }
        $('#td_num').text('--');
        $('#td_total').text('--');
        $('#td_re_num').text('--');
        $('#td_re_total').text('--');
        $('#td_final_num').text('--');
        $('#td_final_total').text('--');
        $.ajax({
            async: true,
            timeout: 15000,
            dataType: "json",
            type: "GET",
            url: '/api/v1/trade_total',
            data: {
                uid : $('#uid').val(),
                chnlid : $('#chnlid').val(),
                syssn : $('#syssn').val(),
                groupid : $('#groupid').val(),
                chnluserid : $('#chnluserid').val(),
                startdate : $('#startdate').val(),
                enddate : $('#enddate').val(),
                starttxamt : $('#starttxamt').val(),
                endtxamt : $('#endtxamt').val(),
                status : $('#status').val(),
                txcurrcd : $('#txcurrcd').val(),
                busicd : $('#busicd').val(),
                chnlsn : $('#chnlsn').val(),
            },
            success: function (json) {
                if (json && json.code == 200 && json.data) {
                    $('#td_num').text(json.data.num);
                    $('#td_total').text(json.data.total/100);
                    $('#td_re_num').text(json.data.re_num);
                    $('#td_re_total').text(json.data.re_total/100);
                    $('#td_final_num').text(json.data.final_num);
                    $('#td_final_total').text(json.data.final_total/100);
                }else{
                    toastr.warning('加载失败');
                    $('#td_num').text('--');
                    $('#td_total').text('--');
                    $('#td_re_num').text('--');
                    $('#td_re_total').text('--');
                    $('#td_final_num').text('--');
                    $('#td_final_total').text('--');
                }
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                if(textStatus == 'timeout'){
                    toastr.error('抱歉，数据量过大，臣妾做不到！');
                }else {
                    toastr.error('抱歉，查询失败！');
                }

            }
        })
    });

    $(document).on('click','#detail',function () {
        clearlabel();
        var syssn = $(this).attr('data-syssn');
        var table_name = $(this).attr('data-table');
        $.ajax({
            async:true,
            dataType:"json",
            type:"GET",
            url:"/api/v1/trade_detail",
            data:{
                syssn:syssn,
                table_name:table_name,
            },
            success:function (json) {
                if(json && json.code == 200){
                    $('#m_userid').html(json.data.userid);
                    $('#m_nick_name').html(json.data.nick_name);
                    $('#m_groupid').html(json.data.groupid);
                    $('#m_qudaoname').html(json.data.qudaoname);
                    $('#m_syssn').html(json.data.syssn);
                    $('#m_out_trade_no').html(json.data.out_trade_no);
                    $('#m_orderno').html(json.data.orderno);
                    $('#m_txamt').html(json.data.txamt/100);
                    $('#m_txcurrcd').html(json.data.txcurrcd);
                    $('#m_coupon_amt').html(json.data.coupon_amt);
                    $('#m_txdtm').html(json.data.txdtm);
                    $('#m_paydtm').html(json.data.paydtm);
                    $('#m_status').html(json.data.status);
                    $('#m_retcd').html(json.data.retcd);
                    $('#m_busicd_name').html(json.data.busicd_name);
                    $('#m_busicd').html(json.data.busicd);
                    $('#m_cancel').html(json.data.cancel);
                    $('#m_origssn').html(json.data.origssn);
                    $('#m_chnlsn').html(json.data.chnlsn);
                    // $('#m_refund').html(json.data.refund/100);
                    if(json.data.haspwd == 0){
                        $('#m_haspwd').html('否');
                    }else {
                        $('#m_haspwd').html('是');
                    }
                    // $('#m_haspwd').html(json.data.haspwd);
                    if(json.data.sign == 0){
                        $('#m_sign').html('否');
                    }else{
                        $('#m_sign').html('是');
                    }
                    // $('#m_sign').html(json.data.sign);
                    $('#m_chnlid').html(json.data.chnlid);
                    $('#m_chnluserid').html(json.data.chnluserid);
                    $('#m_chnltermid').html(json.data.chnltermid);
                    $('#m_cardtp').html(json.data.cardtp);
                    $('#m_cardcd').html(json.data.cardcd);
                    $('#m_issuerbank').html(json.data.issuerbank);
                    $('#m_os').html(json.data.os);
                    $('#m_phonemodel').html(json.data.phonemodel);
                    $('#m_appver').html(json.data.appver);
                    $('#m_terminalid').html(json.data.terminalid);
                    $('#m_psamid').html(json.data.psamid);
                }else {
                    clearlabel();
                }
            },
            error:function () {
               clearlabel();
            }
        });
        $('#tradeDetail').modal('show');
    });
    // 今天
    $('#today').click(function () {
        $('#startdate').val(fun_date(0));
        $('#enddate').val(getNowFormatDate(0));
    });
    // 昨天
    $('#yesterday').click(function () {
        $('#startdate').val(fun_date(-1));
        $('#enddate').val(getNowFormatDate(-1));
    });
    // 最近7天
    $('#seven').click(function () {
        $('#startdate').val(fun_date(-7));
        $('#enddate').val(getNowFormatDate(0));
    });
    // 最近30天
    $('#thirty').click(function () {
        $('#startdate').val(fun_date(-30));
        $('#enddate').val(getNowFormatDate(0));
    });

    var uid = GetQueryString("id");
    if (uid) {
        $('#uid').val(uid);
        $('#seven').click();
        $('#query').click();
    }
});

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

function checkdate() {
    var d1=new Date($('#startdate').val());
    var d2=new Date($('#enddate').val());
    var d3=(d2-d1)/1000;
    if(d3<0){
        toastr.warning('时间区间选择不合法，请重新选择！');
        return 0;
    }
    var d4=(d2-d1)/1000/86400;

    if(d4>31){
        toastr.warning('日期超出范围，请查询30天以内的数据！');
        return 0;
    }
    date1 = $('#startdate').val();
    date2 = $('#enddate').val();
    date1 = date1.split("-");
    date2 = date2.split("-");
    //获取年,月数
    var year1 = parseInt(date1[0]) ,
        month1 = parseInt(date1[1]) ,
        year2 = parseInt(date2[0]) ,
        month2 = parseInt(date2[1]);
        //通过年,月差计算月份差
    months = (year2 - year1) * 12 + (month2-month1);
    if (months>1){
        toastr.warning('当前功能仅支持连续两个月份的查询！');
        return 0;
    }
    return 1;
}

function checkmoney() {
    if ($('#starttxamt').val() && $('#endtxamt').val()){

        var money1 = parseInt($('#starttxamt').val());
        var money2 = parseInt($('#endtxamt').val());
        if (money2 < money1){
            toastr.warning('金额范围不合法，请重新选择金额范围！');
            return 0;
        }
    }
    return 1;
}
// 清空
function clearlabel() {
    $('#m_userid').html('--');
    $('#m_nick_name').html('--');
    $('#m_groupid').html('--');
    $('#m_syssn').html('--');
    $('#m_out_trade_no').html('--');
    $('#m_orderno').html('--');
    $('#m_txamt').html('--');
    $('#m_txcurrcd').html('--');
    $('#m_coupon_amt').html('--');
    $('#m_txdtm').html('--');
    $('#m_paydtm').html('--');
    $('#m_status').html('--');
    $('#m_retcd').html('--');
    $('#m_busicd_name').html('--');
    $('#m_busicd').html('--');
    $('#m_cancel').html('--');
    $('#m_origssn').html('--');
    $('#m_chnlsn').html('--');
    // $('#m_refund').html('--');
    $('#m_haspwd').html('--');
    $('#m_sign').html('--');
    $('#m_chnlid').html('--');
    $('#m_chnltermid').html('--');
    $('#m_cardtp').html('--');
    $('#m_cardcd').html('--');
    $('#m_issuerbank').html('--');
    $('#m_os').html('--');
    $('#m_phonemodel').html('--');
    $('#m_appver').html('--');
    $('#m_terminalid').html('--');
    $('#m_psamid').html('--');
    $('#m_qudaoname').html('--');
}


