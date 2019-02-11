/**
 * Created by qfpay on 2018/01/02.
 */

var oTable = null;
function initTable() {
    $.fn.dataTable.ext.errMode = 'none'; //不显示任何错误信息
    var table = $("#fundTable").DataTable({
        "paging": true,
        "pagingType": "full_numbers",
        "lengthMenu": [10, 20, 30, 40, 50],
        "processing": true,
        "searching": true, //是否开启搜索
        "serverSide": false, //开启服务器获取数据
        "ordering": false, //禁止排序
        "ajax": { // 获取数据
            "url": "/api/v1/fund",
            "timeout": 15000,
            "data": function (d) {
                d.uid = $('#uid').val();
                d.start_date = $('#start_date').val();
                d.end_date = $('#end_date').val();
                d.account_type = $('#account_type').val();
                d.action_type = $('#action_type').val();
            },
            "async": false,
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
            {'title': "用户ID", 'data': "userid"},
            {'title': "账户名称", 'data': null, 'class': "align-center"},
            {'title': "余额详情", 'data': null, 'class': "align-center"},
            {'title': "业务时间", 'data': "biz_time"},
            {'title': "金额（元）", 'data': null, 'class': "align-center"},
            {'title': "商户姓名", 'data': "name"},
            {'title': "银行账号", 'data': "cardno"},
            {'title': "开户支行", 'data': "bank_brch"},
            {'title': "联行号", 'data': "bank_code"},
            {'title': "出款状态", 'data': null, 'class': "align-center"},
            {'title': "退票原因", 'data': "remitback_memo", 'class': "align-center"}
        ],
        "columnDefs": [ //自定义列
            {
                "targets": 1, //改写哪一列
                "data": null,
                "render": function (data, type, row) {
                    var account_types = {
                        1000: "交易账户",
                        2000: "现金账户-钱方",
                        2001: "现金账户-汇宜",
                        2002: "现金账户-汇宜无卡",
                        2003: "现金账户-中信",
                        2004: "现金账户-富友",
                        2005: "现金账户-中信围餐",
                        2006: "现金账户-汇宜无卡快捷",
                        2007: "现金账户-中信补贴",
                        2008: "现金账户-汇宜T0",
                        2009: "现金账户-网商",
                        2010: "现金账户-微信海外",
                        2011: "现金账户-微信直连CNY",
                        2012: "现金账户-微信直连HKD",
                        2014: "现金账户-支付宝海外迪拜AED",
                        2015: "现金账户-支付宝海外柬埔塞USD",
                        2016: "现金账户-微信小微",
                        2017: "现金账户-合利宝",
                        2018: "现金账户-网商蓝海",
                        2100: "现金账户-代付"
                    };
                    var htmlStr = account_types[row.account_type_id] || row.account_type_id;
                    return htmlStr;
                }
            },
            {
                "targets": 2, //改写哪一列
                "data": null,
                "render": function (data, type, row) {
                    var nameDict = {
                        1: "交易",
                        2: "结算",
                        3: "出款",
                        4: "退票",
                        5: "手续费",
                        6: "扣款",
                        7: "冻结"
                    };
                    var htmlStr = nameDict[row.action_type] || row.action_type;
                    return htmlStr;
                }
            },
            {
                "targets": 4, //改写哪一列
                "data": null,
                "render": function (data, type, row) {
                    var htmlStr = (row.amt / 100).toFixed(2);
                    return htmlStr;
                }
            },
            {
                "targets": -2, //改写哪一列
                "data": null,
                "render": function (data, type, row) {
                    var htmlStr = "";
                    if(row.action_type == 3) {
                        htmlStr = "--";
                        if(row.remitback_id == 0) {
                            // 已出款
                            htmlStr = "已出款";
                        }
                        else if(row.remitback_id > 0) {
                            // 已退款
                            htmlStr = "<div style='color: red'>已退款</div>";
                        }
                    }
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
var oTable2 = null;
function initTable2() {
    $.fn.dataTable.ext.errMode = 'none'; //不显示任何错误信息
    var table = $("#balanceTable").DataTable({
        "autoWidth": false,
        "paging": false,
        "processing": true,
        "searching": false, //是否开启搜索
        "serverSide": false, //开启服务器获取数据
        "ajax": { // 获取数据
            "url": "/api/v1/account",
            "timeout": 15000,
            "data": function (d) {
                d.uid = $('#uid').val();
            },
            "async": false,
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
        "columns": [ //定义列数据来源
            {'title': "账户名称", 'data': null, 'class': "align-left"},
            {'title': "金额（元）", 'data': null, 'class': "align-right"},
            {'title': "冻结金额", 'data': null, 'class': "align-right"}
        ],
        "columnDefs": [ //自定义列
            {
                "targets": 0, //改写哪一列
                "data": null,
                "render": function (data, type, row) {
                    var account_types = {
                        0: "账户余额",
                        1000: "交易账户",
                        2000: "现金账户-钱方",
                        2001: "现金账户-汇宜",
                        2002: "现金账户-汇宜无卡",
                        2003: "现金账户-中信",
                        2004: "现金账户-富友",
                        2005: "现金账户-中信围餐",
                        2006: "现金账户-汇宜无卡快捷",
                        2007: "现金账户-中信补贴",
                        2008: "现金账户-汇宜T0",
                        2009: "现金账户-网商",
                        2010: "现金账户-微信海外",
                        2011: "现金账户-微信直连CNY",
                        2012: "现金账户-微信直连HKD",
                        2014: "现金账户-支付宝海外迪拜AED",
                        2015: "现金账户-支付宝海外柬埔塞USD",
                        2016: "现金账户-微信小微",
                        2017: "现金账户-合利宝",
                        2018: "现金账户-网商蓝海",
                        2100: "现金账户-代付"
                    };
                    var htmlStr = account_types[row.account_type_id] || row.account_type_id;
                    return htmlStr;
                }
            },
            {
                "targets": 1, //改写哪一列
                "data": null,
                "render": function (data, type, row) {
                    var htmlStr = (row.amt / 100).toFixed(2);
                    return htmlStr;
                }
            },
            {
                "targets": 2, //改写哪一列
                "data": null,
                "render": function (data, type, row) {
                    var htmlStr = (row.frozen_amt / 100).toFixed(2);
                    return htmlStr;
                }
            },
            {
                "targets": [0, 1, 2],
                "orderable": false  //禁止排序
            }
        ],
        "language": { // 定义语言
            "sProcessing": "加载中...",
            "sLengthMenu": "每页显示 _MENU_ 条记录",
            "sZeroRecords": "没有匹配的结果",
            "sInfo": "",
            "sInfoEmpty": "",
            "sInfoFiltered": "",
            "sInfoPostFix": "",
            "sSearch": "",
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
        elem: '#start_date'
        ,type: 'date'
        ,theme: '#009688'
        ,max: 1
        ,value: new Date((new Date()).setDate(1)) // '2017-12-01' //
    });
    laydate.render({
        elem: '#end_date'
        ,type: 'date'
        ,theme: '#009688'
        ,max: 1
        ,value: new Date() // '2017-12-31' //
    });

    $("#form").submit(function () {
        if(checkParams() == 0) {
            return false;
        }
        if(!oTable) {
            oTable = initTable();
        }
        else {
            oTable.ajax.reload();
        }
        if(!oTable2) {
            oTable2 = initTable2();
        }
        else {
            oTable2.ajax.reload();
        }
        return false;
    });

    var uid = GetQueryString("id");
    if (uid) {
        $('#uid').val(uid);
        $("#form").submit();
    }
});

function checkParams() {
    if($('#uid').val().trim().length == 0) {
        toastr.warning('请先输入用户ID/手机号');
        return 0;
    }
    var d1=new Date($('#start_date').val());
    var d2=new Date($('#end_date').val());
    if(d2 - d1 < 0 || d1 == "Invalid Date" || d2 == "Invalid Date"){
        toastr.warning('时间区间选择不合法，请重新选择！');
        return 0;
    }
    // var d4=(d2-d1)/1000/86400;
    //
    // if(d4>31){
    //     toastr.warning('日期超出范围，请查询30天以内的数据！');
    //     return 0;
    // }
    // date1 = $('#start_date').val();
    // date2 = $('#end_date').val();
    // date1 = date1.split("-");
    // date2 = date2.split("-");
    // //获取年,月数
    // var year1 = parseInt(date1[0]) ,
    //     month1 = parseInt(date1[1]) ,
    //     year2 = parseInt(date2[0]) ,
    //     month2 = parseInt(date2[1]);
    //     //通过年,月差计算月份差
    // months = (year2 - year1) * 12 + (month2-month1);
    // if (months>1){
    //     toastr.warning('当前功能仅支持连续两个月份的查询！');
    //     return 0;
    // }
    return 1;
}
