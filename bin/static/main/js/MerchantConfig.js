/**
 * Created by qfpay on 2018/3/12.
 */
//商户配置
var list_table = null;
var history_table = null;
var recordsTotal = 0;
var uids = [];
var id_names = [];
var select_uids = [];
var all_ids = [];
var select_ids = [];
var id_mcc = {};
var groupIDtoName = {};
var wechatIDtoName = {};
var _all_conf = [];
var chnlcodeToName = {
    1:'中信普通',
    2:'光大',
    3:'富友',
    4:'中信围餐',
    5:'汇宜普通',
    6:'汇宜快捷',
    7:'中信零费率',
    8:'大则',
    9:'网商',
    10:'大则积分',
    11:'收款宝',
    12:'汇通',
    13:'微信'
};
var chnlidToName = {};
Array.prototype.remove = function(val) {
    var index = this.indexOf(val);
    if (index > -1) {
        this.splice(index, 1);
    }
};
Array.prototype.in_array = function (element) {
　　for (var i = 0; i < this.length; i++) {
    　　if (this[i] == element) {
    　　  return true;
        }
    }
    return false;
};

$(function () {
     init_select();
    init_cate_name()
     getData();
     list_table = initMerchantConfigTableTable();
     clickEvent();
     // $('#c_appid').val('jhaskhfdj');
});

// 标签搜索框
function init_cate_name(){
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
//获取筛选下拉选框的数据
function getData() {
    $.ajax({
        async: false,
        url:'/get_merchant_config_data',
        type:'POST',
        dataType:'json',
        data:{},
        success:(function (json) {
            // 行业下拉一级
            var mccaStr = '';
            $('#mcca').html("<option value=''>"+'全部'+"</option>");
            $.each(json.data.mcca, function (i,item) {
                mccaStr += "<option value='"+ item.id +"'>" + item.mcca_name + "</option>"
            });
            $('#mcca').append(mccaStr);
            $('#mcca').selectpicker('refresh');
            // 省份下拉
            var proStr = '';
            $('#pro').html("<option value=''>"+'全部'+"</option>");
            $.each(json.data.provinces, function (i,item) {
                proStr += "<option value='"+ item.id +"'>" + item.area_name + "</option>"
            });
            $('#pro').append(proStr);
            $('#pro').selectpicker('refresh');

            var namestr = '';
            // $('#appname').html("<option value=''>"+'请选择'+"</option>");
            $('#appname').selectpicker('destroy');
            $('#appname').html("");
            $.each(json.data.id_names, function (i,item) {
                namestr += "<option value='"+ item.appid +"'>" + item.nick_name + "</option>"
            });
            $('#appname').append(namestr);
            $('#appname').selectpicker({
                style: 'btn-inverse',
                width: 100,
                actionsBox:true,
            });
            $('#appname').selectpicker('refresh');
            //$('#appname').selectpicker('selectAll');
            wechatIDtoName = json.data.IDtoName;

            var namestr = '';
            $('#change_appname').html('');
            $.each(json.data.id_names, function (i,item) {
                namestr += "<option value='"+ item.appid +"'>" + item.nick_name + "</option>"
            });
            //$('#change_appname').append(namestr);
            $('#change_appname').selectpicker({
                style: 'btn-inverse',
                width: 360,
            });
            //$('#change_appname').selectpicker('refresh');


            $('#chnlcode').selectpicker({
        style: 'btn-inverse',
        width: '360px',
    });

            // $('#change_appname').selectpicker('selectAll');
            id_names = json.data.id_names;
            $('#c_appid').val(json.data.id_names[0].appid);
            // $('#change_appid').value = '哈哈佛教大会上看见';
            var qudaostr = '';
            $('#qudao').html("<option value=''>"+'全部'+"</option>");
            $.each(json.data.groupids, function (i,item) {
                qudaostr += "<option value='"+ item.qd_uid +"'>" + item.name + "</option>"
            });
            $('#qudao').append(qudaostr);
            $('#qudao').selectpicker('refresh');

            id_mcc = json.data.id_mcc;
            groupIDtoName = json.data.groupIDtoName;
            chnlidToName = json.data.chnlidToName;

        }),
        error:(function () {
            toastr.error('网络异常，请重试！');
        })
    });
}
function checkdate() {
    var d1=new Date($('#startdate').val());
    var d2=new Date($('#enddate').val());
    var d3=(d2-d1)/1000;
    if(d3<0){
        toastr.info('时间区间选择不合法，请重新选择！');
        return 0;
    }
    var d4=(d2-d1)/1000/86400;

    if(d4>31){
        toastr.info('日期超出范围，请查询31天以内的数据！');
        return 0;
    }
    return 1;
}

// 点击事件
function clickEvent() {
    //全部选取的check
    $('#check_all').click(function () {
        if($(this).is(':checked') == true){
            $('.uid_check').prop('checked',true);
            // select_uids = uids;
            select_uids = $.extend(true,select_uids,uids);
            select_ids = $.extend(true,select_ids,all_ids);
        }else if($(this).is(':checked') == false){
            $('.uid_check').prop('checked',false);
            select_uids = [];
            select_ids = [];
        }
    });
    // 列表中每一行的选择
    $(document).on('click','.uid_check',function () {
        if($(this).is(':checked') == true){
            // $('.uid_check').prop('checked',true);
            select_uids.push(parseInt($(this).siblings('span').text()));
            select_ids.push(parseInt($(this).siblings('i').text()));
            if(select_uids.length == uids.length){
                $('#check_all').prop('checked',true);
            }
        }else if($(this).is(':checked') == false){
            $('#check_all').prop('checked',false);
            select_uids.remove(parseInt($(this).siblings('span').text()));
            select_ids.remove(parseInt($(this).siblings('i').text()))
        }
        // console.log('已选ids'+select_ids);
    });
    //查询按钮的点击
    $('#query').click(function () {
        if(!checkdate()){
            return;
        }
        var tmp = $("#cate_code").val()
        if (tmp.in_array('untagged') && tmp.length > 1 ){
            toastr.info('不允许同时选择无标签和其他标签');
            return
        }

        select_uids = [];
        select_ids = [];
        $('#check_all').prop('checked',false);
        list_table = initMerchantConfigTableTable();
    });
    //导出按钮点击事件
    $('#export').click(function () {
        if(!checkdate()){
            return;
        }
        if (select_uids.length == 0){
            toastr.info('请选择您要导出的条目！');
            return;
        }
        var form=$("<form>");//定义一个form表单

        form.attr("style","display:none");
        form.attr("target","_blank");
        form.attr("method","post");
        form.attr("action","/app_mchnt_excel");

        // select_str = select_uids.join(',');
        select_str = select_ids.join(',');
        var inputuid=$("<input>");
        inputuid.attr("type","hidden");
        inputuid.attr("name","uids");
        inputuid.attr("value",select_str);


        // 导出新加
        var id_str = $('#uids').val();
        var id_strl = id_str.replace(/，/g,',');
        // group_strl.replace(/\s+/g, "");
        id_strl = id_strl.replace(/\s|\xA0/g,"");
        var id_arr = new Array();
        laststr = id_strl.substr(id_strl.length-1,1);
        if(laststr.indexOf(',') != -1){
            id_strl = id_strl.substr(0,id_strl.length-1);
        }
        if(id_strl){
            id_arr = id_strl.split(',');
        }else {
            id_arr = []
        }

        // d.startdate = $('#startdate').val();
        var input_startdate=$("<input>");
        input_startdate.attr("type","hidden");
        input_startdate.attr("name","startdate");
        input_startdate.attr("value",$('#startdate').val());
        form.append(input_startdate);

        // d.enddate = $('#enddate').val();
        var input_enddate=$("<input>");
        input_enddate.attr("type","hidden");
        input_enddate.attr("name","enddate");
        input_enddate.attr("value",$('#enddate').val());
        form.append(input_enddate);

        // d.uid = id_arr;
        // d.mcca = $('#mcca').selectpicker('val');
        var input_mcca=$("<input>");
        input_mcca.attr("type","hidden");
        input_mcca.attr("name","mcca");
        input_mcca.attr("value",$('#mcca').selectpicker('val'));
        form.append(input_mcca);

        // d.mcc = $('#mcc').selectpicker('val');
        var input_mcc=$("<input>");
        input_mcc.attr("type","hidden");
        input_mcc.attr("name","mcc");
        input_mcc.attr("value",$('#mcc').selectpicker('val'));
        form.append(input_mcc);

        var options =$("#pro option:selected");
        // d.pro = $('#pro').selectpicker('val');
        if(options.text() == '全部'){
            // d.pro = '';
            var input_pro=$("<input>");
            input_pro.attr("type","hidden");
            input_pro.attr("name","pro");
            input_pro.attr("value",'');
            form.append(input_pro);
        }else {
            // d.pro = options.text();
            var input_pro=$("<input>");
            input_pro.attr("type","hidden");
            input_pro.attr("name","pro");
            input_pro.attr("value",options.text());
            form.append(input_pro);
        }
        // d.city = $('#city').selectpicker('val');
        var input_city=$("<input>");
        input_city.attr("type","hidden");
        input_city.attr("name","city");
        input_city.attr("value",$('#city').selectpicker('val'));
        form.append(input_city);

        // d.groupid = $('#qudao').selectpicker('val');
        var input_groupid=$("<input>");
        input_groupid.attr("type","hidden");
        input_groupid.attr("name","groupid");
        input_groupid.attr("value",$('#qudao').selectpicker('val'));
        form.append(input_groupid);

        // d.group_type = $('#qudao_type').selectpicker('val');
        var input_group_type=$("<input>");
        input_group_type.attr("type","hidden");
        input_group_type.attr("name","group_type");
        input_group_type.attr("value",$('#qudao_type').selectpicker('val'));
        form.append(input_group_type);

        // d.appid = $('#appname').selectpicker('val');
        var input_appid=$("<input>");
        input_appid.attr("type","hidden");
        input_appid.attr("name","appid");
        input_appid.attr("value",$('#appname').selectpicker('val'));
        form.append(input_appid);
        //导出新加
        //
        var input_cate_code=$("<input>");
        var tmp = $("#cate_code").val()
        if (tmp.in_array('untagged') && tmp.length > 1 ){
            toastr.info('不允许同时选择无标签和其他标签');
            return
        }
        input_cate_code.attr("type","hidden");
        input_cate_code.attr("name","cate_code");
        input_cate_code.attr("value",$('#cate_code').selectpicker('val'));
        form.append(input_cate_code);

        form.append(inputuid);

        $("body").append(form);//将表单放置在web中
        form.submit();//表单提交
    });
    // 查看按钮的点击
    $(document).on('click','.detail',function () {
        var userid = $(this).attr('data-id');
        // alert(userid);
        // return;
        history_table = initDetailHistoryTable(userid);
        $('#detail_modal').modal('show');
    });

    $('#change').click(function () {
        if (select_uids.length == 0){
            toastr.info('请选择您要修改的条目！');
            return;
        }
        select_uids = $.unique(select_uids);
        $('#shop_num').text(select_uids.length);
        document.getElementById("change_appname").options.selectedIndex = 0;
        $('#change_appname').selectpicker('refresh');
        $('#c_appid').val(id_names[0].appid);
        $('#pay_appid').val('');
        $('#menu').val('');
        $('#memo').val('');
        $('#cid').val('');
        $('#change_modal').modal('show');
        $('#main').val('');



        $('#chnlcode').selectpicker('destroy');
        //$('#chnlcode').html('<option value="9">网商</option> <option value="3">富有</option><option value="13">微信</option> <option value="14">富有绿洲</option> ');
        $('#chnlcode').selectpicker({
            style: 'btn-inverse',
            width: 365,
            // actionsBox:true,
        });
        $('#chnlcode').selectpicker('refresh');


        $('#change_appname').selectpicker('destroy');
        $('#change_appname').html('<option value="0">请选择</option>');
        $('#change_appname').selectpicker({
            style: 'btn-inverse',
            width: 365,
            // actionsBox:true,
        });
        $('#change_appname').selectpicker('refresh');







    });



    $('#change_appname').change(function () {
        //$('#appid').val($('#account_name').val());


        console.log($('#change_appname').val());

        var _appid = $('#change_appname').val();

        var _appname = '';
        var _main = '';
        var _cid = '';
        var _pay_appid = '';
        var _menu = '';


        for(var i=0;i<_all_conf.length;i++) {

            if (_appid == _all_conf[i]['appid']){


                _appname = _all_conf[i]['appname'];
                _main = _all_conf[i]['main'];

                _pay_appid = _all_conf[i]['pay_appid'];
                _menu = _all_conf[i]['menu'];
                _cid = _all_conf[i]['cid'];


            }



        }

        $('#appid').val(_appid);
        $('#main').val(_main);

        $('#cid').val(_cid);
        $('#menu').val(_menu);
        $('#pay_appid').val(_pay_appid);




    });


    $('#chnlcode').change(function () {


        $.ajax({
            async: true,
            url: '/get_app_config',
            type: 'POST',
            dataType: 'json',
            data: {
                chnlcode: JSON.stringify($(this).val())
            },
            success: (function (json) {

                    var _rs = json.data;

                    _all_conf = _rs;

                    var str_add = "";

                    $('#change_appname').html("");

                    str_add += "<option value='0'>请选择</option>";

                    for(var i=0;i<_rs.length;i++) {

                        str_add += "<option value='"+ _rs[i]['appid'] +"'>" + _rs[i]['appname'] + "</option>";

                    }


                    $('#change_appname').append(str_add);

                    $('#change_appname').selectpicker('refresh');




            }),
            error: (function () {
                toastr.error('网络异常，请重试！');
            })
        });


    });


    //修改modal的提交按钮的点击事件
    $('#change_submit').click(function () {
        // alert(JSON.stringify({
        //         'uids':select_uids,
        //         'appid':$('#change_appname').selectpicker('val')
        //     }));
        var cid = $('#cid').val();
        if(!cid){
            toastr.info('请输入通道渠道号!');
            return;
        }
        var pay_appid = $('#pay_appid').val();
        if(!pay_appid){
            toastr.info('请输入支付APPID!');
            return;
        }
        var menu_str = $('#menu').val();
        if(!menu_str){
            toastr.info('请输入支付目录!');
            return;
        }

        var memo = $('#memo').val();

        memo = memo.replace(/(^\s*)|(\s*$)/g,"");

        if(memo.length > 100){

            toastr.info('备注不能超过100个字符');
            return;
        }

        var menu_strl = menu_str.replace(/，/g,',');
        menu_strl = menu_strl.replace(/\s|\xA0/g,"");
        laststr = menu_strl.substr(menu_strl.length-1,1);
        if(laststr.indexOf(',') != -1){
            menu_strl = menu_strl.substr(0,menu_strl.length-1);
        }
        var menu_arr = [];
        menu_arr = menu_strl.split(',');
        var menu = menu_arr;  // 支付目录

        $.ajax({
            async:true,
            url:'/app_mchnt_change',
            timeout : 30000, //超时时间设置，单位毫秒
            type:'POST',
            dataType:'json',
            contentType: 'application/json;',
            "beforeSend": function(){
$('#change_submit').attr("disabled",true);
    },
    "complete": function(){
     $('#change_submit').attr("disabled",false);
    },
            data:JSON.stringify({
                'chnlcode':$('#chnlcode').val(),
                'cid':cid,
                'pay_appid':pay_appid,
                'menu':menu_arr,
                'memo':memo,
                'uids':select_uids,
                'appid':$('#change_appname').selectpicker('val')
            }),
            success:(function (json) {
                if (json.code == 200){
                    toastr.success('修改成功！');
                    $('#change_modal').modal('hide');
                }else {
                    toastr.error('修改失败，请重试');
                }
            }),
            error:(function () {
                toastr.error('网络异常，请重试！');
            })
        });
    });
    //修改modal的取消按钮的点击事件
    $('#change_cancel').click(function () {
        $('#change_modal').modal('hide');
    });

    //修改modal的取消按钮点击
    $('#change_cancel').click(function () {
        $('#change_modal').modal('hide');
    });

    $(document).on('change','#mcca',function () {
        var mcc = $('#mcc');
        if(!$(this).val()){
            // mcc.selectpicker('destroy');
            mcc.html("<option value=''>" + "全部" + "</option>");
            // mcc.selectpicker({
            //     style: 'btn-inverse',
            //     width: 100,
            // });
            mcc.selectpicker('refresh');
            return;
        }
        $.ajax({
            async: true,
            url: '/get_mccs',
            type: 'POST',
            dataType: 'json',
            data: {
                mcca_id: $(this).val(),
            },
            success: (function (json) {
                var str_mcc = '';
                // mcc.html("<option value='全部'>" + "全部" + "</option>");
                mcc.selectpicker('destroy');
                mcc.html("<option value=''>" + "全部" + "</option>");
                $.each(json.data.mccs, function (i, item) {
                    str_mcc += "<option value='" + item.id + "'>" + item.mcc_name + "</option>";
                });
                mcc.append(str_mcc);
                mcc.selectpicker({
                    style: 'btn-inverse',
                    width: 100,
                    // actionsBox:true,
                });
                mcc.selectpicker('refresh');
                // mcc.selectpicker('selectAll');
            }),
            error: (function () {
                toastr.error('网络异常，请重试！');
            })
        })
    });

    $(document).on('change','#pro',function () {
        var city = $('#city');
        // var city = $(this).parent().next().children('select');
        // var index = this.selectedIndex;
        // city.selectpicker('destroy');
        if(!$(this).val()){
            city.html("<option value=''>" + "全部" + "</option>");
            city.selectpicker('refresh');
            return;
        }
        $.ajax({
            async: true,
            url: '/get_city',
            type: 'POST',
            dataType: 'json',
            data: {
                area_no: $(this).val(),
            },
            success: (function (json) {
                var str_city = '';
                city.selectpicker('destroy');
                city.html("<option value=''>" + "全部" + "</option>");
                $.each(json.data.citys, function (i,item) {
                    str_city += "<option value='"+ item.city_name +"'>" + item.city_name + "</option>";
                });
                city.append(str_city);
                city.selectpicker({
                    style: 'btn-inverse',
                    width: 100,
                    // actionsBox:true,
                });
                city.selectpicker('refresh');
                // city.selectpicker('selectAll');

            }),
            error: (function () {
                toastr.error('网络异常，请重试！');
            })
        });

    });

    $('#change_appname').change(function () {
        $('#c_appid').val($('#change_appname').val());
    });
}
//初始化select下拉选框
function init_select() {
    $('#mcca').selectpicker({
        style: 'btn-inverse',
        width: 100,
    });
    $('#cate_code').selectpicker({
        width: 200,
        style: 'btn-inverse',
        actionsBox:true,
    });
    $('#mcca').selectpicker('refresh');

    $('#mcc').selectpicker({
        style: 'btn-inverse',
        width: 100,
        // actionsBox:true,
    });
    $('#mcc').selectpicker('refresh');

    $('#pro').selectpicker({
        style: 'btn-inverse',
        width: 90,
    });
    $('#pro').selectpicker('refresh');

    $('#city').selectpicker({
        style: 'btn-inverse',
        width: 90,
        // actionsBox:true,
    });
    $('#city').selectpicker('refresh');

    $('#qudao').selectpicker({
        style: 'btn-inverse',
        width: 100,
    });
    $('#qudao').selectpicker('refresh');

    $('#qudao_type').selectpicker({
        style: 'btn-inverse',
        width: 90,
    });
    $('#qudao_type').selectpicker('refresh');

    $('#appname').selectpicker({
        style: 'btn-inverse',
        width: 200,
        actionsBox:true,
    });
    $('#appname').selectpicker('refresh');

    // $('#receive_time').selectpicker({
    //     style: 'btn-inverse',
    //     width: 180,
    // });
    // $('#receive_time').selectpicker('refresh');

    // $('#utime').selectpicker({
    //     style: 'btn-inverse',
    //     width: 180,
    // });
    // $('#utime').selectpicker('refresh');
    var date_t = new Date();
    var date_y = new Date(date_t.getTime()-24*60*60*1000);
    laydate.render({
        elem: '#startdate'
        // ,type: 'datetime'
        ,format: 'yyyy-MM-dd'
        ,theme: 'molv'
        ,istoday: false
        ,value: date_y
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
        ,value: date_y
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
    var table = $("#MerchantConfigTable").DataTable({
        "paging": true,
        // "scrollX": true,
        "scrollCollapse": true,
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
            "url": "/app_mchnt_list",
            "contentType": 'application/json;',
            "type": "POST",
            "beforeSend": function(){
$('#query').attr("disabled",true);
    },
    "complete": function(){
     $('#query').attr("disabled",false);
    },
            "dataType": "json", //返回来的数据形式
            "data": function (d) {
                // d.state = $('#status').val();
                var id_str = $('#uids').val();
                var id_strl = id_str.replace(/，/g,',');
                // group_strl.replace(/\s+/g, "");
                id_strl = id_strl.replace(/\s|\xA0/g,"");
                var id_arr = new Array();
                laststr = id_strl.substr(id_strl.length-1,1);
                if(laststr.indexOf(',') != -1){
                    id_strl = id_strl.substr(0,id_strl.length-1);
                }
                if(id_strl){
                    id_arr = id_strl.split(',');
                }else {
                    id_arr = []
                }
                // id_arr = id_strl.split(',');

                // var receive_time = $('#receive_time').val();
                // if(receive_time){
                //     var start_dtime = getNowFormatDate(0-parseInt(receive_time));
                //     var end_dtime = getNowFormatDate(0);
                //     d.start_dtime = start_dtime;
                //     d.end_dtime = end_dtime;
                // }else {
                //     d.start_dtime = "";
                //     d.end_dtime = "";
                // }


                // var utime = $('#utime').val();
                // if(utime){
                //     var start_stime = getNowFormatDate(0-parseInt(utime));
                //     var end_stime = getNowFormatDate(0);
                //     d.start_stime = start_stime;
                //     d.end_stime = end_stime;
                // }else {
                //     d.start_stime = "";
                //     d.end_stime = "";
                // }
                d.startdate = $('#startdate').val();
                d.enddate = $('#enddate').val();
                d.cate_codes = $('#cate_code').val().join(',');
                d.uid = id_arr;
                d.mcca = $('#mcca').selectpicker('val');
                d.mcc = $('#mcc').selectpicker('val');
                var options =$("#pro option:selected");
                // d.pro = $('#pro').selectpicker('val');
                if(options.text() == '全部'){
                    d.pro = ''
                }else {
                    d.pro = options.text();
                }
                d.city = $('#city').selectpicker('val');
                d.groupid = $('#qudao').selectpicker('val');
                d.group_type = $('#qudao_type').selectpicker('val');
                d.appid = $('#appname').selectpicker('val');

                console.log(JSON.stringify(d));

                return JSON.stringify(d);
            },
        },
        "columnDefs": [ //自定义列
            {
                "targets": 0, //改写哪一列
                'width':100,
                "render": function (data, type, row) {
                    var htmlStr = "<label>"+"<input class='uid_check' name='' type='checkbox' value='-1'/>"+"<span>"+row.uid+"</span>"+"<i hidden>"+row.id+"</i>"+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 1,
                "width": 100,
                "render": function (data, type, row) {
                    if($('#check_all').is(':checked') == true){
                        $('.uid_check').prop('checked',true);
                    }
                    var htmlStr = "<label>"+row.nickname+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 2,
                "width": 100,
                "render": function (data, type, row) {
                    // var htmlStr = "<label>"+row.groupid+"</label>";
                    var htmlStr = "<label>"+row.ctime+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 3,
                "width": 100,
                "render": function (data, type, row) {
                    // var htmlStr = "<label>"+row.groupid+"</label>";
                    var htmlStr = "<label>"+chnlidToName[row.chnlcode+'']+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 4,
                "width": 150,
                "render": function (data, type, row) {
                    // var htmlStr = "<label>"+row.groupid+"</label>";
                    var htmlStr = "<label>"+row.mchnt_id+"</label>";
                    return htmlStr;
                }
            },

            // {
            //     "targets": 7, //改写哪一列
            //     "width": 100,
            //     "render": function (data, type, row) {
            //         var htmlStr = "<label>"+row.dtime+"</label>";
            //         return htmlStr;
            //     }
            // },
            {
                "targets": 5,
                "width": 100,
                "render": function (data, type, row) {
                    var htmlStr = "<label>"+wechatIDtoName[row.appid]+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 6,
                "width": 100,
                "render": function (data, type, row) {
                    var htmlStr = "<label>"+row.stime+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 7,
                "width": 60,
                "render": function (data, type, row) {
                    var htmlStr = "<label>"+row.newfan+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 8,
                "width": 60,
                "render": function (data, type, row) {
                    var htmlStr = "<label>"+row.deal+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 9,
                "width": 60,
                "render": function (data, type, row) {
                    var htmlStr = "<label>"+row.fan+"</label>";
                    return htmlStr;
                }
            },
            // {
            //     "targets": 10,
            //     "width": 100,
            //     "render": function (data, type, row) {
            //         var htmlStr = "<label>"+wechatIDtoName[row.now_appid]+"</label>";
            //         return htmlStr;
            //     }
            // },
            // {
            //     "targets": 11,
            //     "width": 100,
            //     "render": function (data, type, row) {
            //         var htmlStr = "<label>"+row.now_stime+"</label>";
            //         return htmlStr;
            //     }
            // },
            {
                "targets": 10,
                "width": 100,
                "render": function (data, type, row) {
                    var htmlStr = "<label>"+id_mcc[row.mcc]+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 11,
                "width": 60,
                "render": function (data, type, row) {
                    var htmlStr = "<label>"+row.pro+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 12,
                "width": 60,
                "render": function (data, type, row) {
                    var htmlStr = "<label>"+row.city+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 15,
                "width": 80,
                "render": function (data, type, row) {
                    var htmlStr = "<label>"+row.cate_name+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 13,
                "width": 100,
                "render": function (data, type, row) {
                    // var htmlStr = "<label>"+row.groupid+"</label>";
                    var htmlStr = "<label>"+groupIDtoName[row.groupid]+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 14,
                "width": 100,
                "render": function (data, type, row) {
                    var group_name = '';
                    if(row.group_type == 1){
                        group_name = '白牌';
                    }else if (row.group_type == 2){
                        group_name = '联名';
                    }else if (row.group_type == 3){
                        group_name = '合伙人';
                    }else if (row.group_type == 4){
                        group_name = '直营';
                    }else if (row.group_type == 5){
                        group_name = '钱台';
                    }else if (row.group_type == 6){
                        group_name = '网络电销';
                    }

                    //var htmlStr = "<label>"+group_name+"</label>";
                    var htmlStr = "<label>"+row.group_type+"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 16,
                "render": function (data, type, row) {
                    var htmlStr = "<button class='btn btn-info btn-sm detail' data-action='' data-id='"+ row.uid +"'>"+ "查看" +"</button>";
                    return htmlStr;
                }
            },
            {
                "targets": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                "orderable": false  //禁止排序
            }
        ],
        "fnRowCallback": function (nRow, aData, iDisplayIndex, iDisplayIndexFull) {
            // console.log(nRow);
            // console.log(aData);
            // console.log(iDisplayIndex);
            // console.log(iDisplayIndexFull);
            // console.log($('.uid_check'));
            // if(iDisplayIndex == 5){
            //     $.each($('.uid_check'),function (i,item) {
            //         if(i == 5){
            //             $(this).prop('checked',true);
            //         }
            //     })
            // }
        },
        "initComplete": function (settings, json) {
            // alert( '初始化完成' );
            recordsTotal = json.recordsTotal;
            uids = json.uids;
            all_ids = json.ids;
            // console.log('全部ids'+all_ids);
            // if($('#check_all').is(':checked') == true){
            //     $('.uid_check').prop('checked',true);
            // }
        },
        "drawCallback": function(settings) {
            // alert( '表格重绘了' );
            if($('#check_all').is(':checked') == true){
                $('.uid_check').prop('checked',true);
            }else {
                $('.uid_check').each(function (i,item) {
                    if (select_uids.in_array(parseInt($(this).siblings('span').text()))){
                        $(this).prop('checked',true);
                    }
                })
            }
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
            }
        }
    });
    return table;
}


function initDetailHistoryTable(userid) {
    var table = $('#history_detail').DataTable({
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
        "serverSide": false, //开启服务器获取数据
        "ajax": { // 获取数据
            "url": "/app_mchnt_history",
            "contentType": 'application/json;',
            "type": "POST",
            "dataType": "json", //返回来的数据形式
            "data": function (d) {
                d.uid = userid;
                return JSON.stringify(d);
            }
        },
        "columns": [
            {'title': "商户ID", 'data': null},
            {'title': "通道", 'data': null},
            {'title': "通道商户号", 'data': null},
            {'title': "公众号", 'data': null},
            {'title': "关注时间", 'data': null}
        ],
        "columnDefs": [ //自定义列
        {
            "targets": 0, //改写哪一列
            'width':'20%',
            "render": function (data, type, row) {
                var htmlStr = "<label>"+row.uid+"</label>";
                return htmlStr;
            }
        },
            {
            "targets": 1,
            "width": '20%',
            "render": function (data, type, row) {
                // var htmlStr = "<label>"+row.subscribe_appid+"</label>";
                var htmlStr = "<label>"+chnlcodeToName[row.chnlcode]+"</label>";
                return htmlStr;
            }
        },
            {
            "targets": 2,
            "width": '20%',
            "render": function (data, type, row) {
                // var htmlStr = "<label>"+row.subscribe_appid+"</label>";
                var htmlStr = "<label>"+row.mchnt_id+"</label>";
                return htmlStr;
            }
        },
        {
            "targets": 3,
            "width": '20%',
            "render": function (data, type, row) {
                // var htmlStr = "<label>"+row.subscribe_appid+"</label>";
                var htmlStr = "<label>"+wechatIDtoName[row.subscribe_appid]+"</label>";
                return htmlStr;
            }
        },
        {
            "targets": 4,
            "width": '20%',
            "render": function (data, type, row) {
                var htmlStr = "<label>"+row.ctime+"</label>";
                return htmlStr;
            }
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
                // "sSortAscending": ": 以升序排列此列",
                // "sSortDescending": ": 以降序排列此列"
            }
        }
    });
    return table;
}
