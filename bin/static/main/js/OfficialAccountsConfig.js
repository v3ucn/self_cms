/**
 * Created by qfpay on 2018/3/5.
 */
var table = null;
var area_count = 0;
var industry_count = 0;
var provincesArr = [{'全部':'全部'}];//省份列表
var mccaArr = [{'全部':'全部'}];//mcc列表
var id_mcca = {};
var id_mcc = {};
var id_pro = {};
var submit_type;// 1 新增 ;2 修改
var qd_uids = [];
var id_appname = [];
var qudaoids_arr = [];
var groupid_names = {};
var mcca_total = {};//每个省份id和这个id下的城市数量的关系字典
var pro_total = {};//每个一级行业id和该行业下的二级行业的数量的关系字典
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
Array.prototype.in_array = function (element) {
　　for (var i = 0; i < this.length; i++) {
    　　if (this[i] == element) {
    　　  return true;
        }
    }
    return false;
};
Array.prototype.remove = function(val) {
    var index = this.indexOf(val);
    if (index > -1) {
        this.splice(index, 1);
    }
};

$(function () {
    // 列表页公众号名称
    $('#officialAccountName').selectpicker({
        style: 'btn-inverse',
    });
    //列表页状态
    $('#status').selectpicker({
        style: 'btn-inverse',
        width: 100,
    });
    $('#status').selectpicker('refresh');
    //列表页查询
    $('#query').click(function () {
        table = initOfficialAccountTable();
        table.on('order.dt search.dt', function() {
            table.column(0, {search: 'applied', order: 'applied'}).nodes().each(function(cell, i) {
                cell.innerHTML = i + 1;
            });
        }).draw();
    });


    function load_app_conf(chnlcode) {
        $.ajax({
            async: true,
            url: '/get_app_config',
            type: 'POST',
            dataType: 'json',
            data: {
                chnlcode: JSON.stringify(chnlcode)
            },
            success: (function (json) {
                    var _rs = json.data;
                    _all_conf = _rs;
                    var str_add = "";
                    $('#account_name').html("");
                    str_add += "<option value='0'>请选择</option>";
                    for(var i=0;i<_rs.length;i++) {
                        str_add += "<option value='"+ _rs[i]['appid'] +"'>" + _rs[i]['appname'] + "</option>";
                    }
                    $('#account_name').append(str_add);
                    $('#account_name').selectpicker('refresh');
            }),
            error: (function () {
                toastr.error('网络异常，请重试！');
            })
        });
    };

    //列表页新增
    $('#add').click(function () {
        submit_type = 1;
        $('#myModalLabel').text('新增 公众号配置');
        var obj = document.getElementById("group_area");
        obj.style.border = '1px gainsboro solid';
        // 新增清除原数据
        // $("#account_name").selectpicker('val','');
        if(id_appname.length){
            $("#account_name").selectpicker('val',id_appname[0].appid);
            $("#account_name").selectpicker('refresh');
            $('#appid').val(id_appname[0].appid);
        }
        // $('#appid').val('');
        $('#cid').val('');
        $('#main').val('');

        $('#pay_appid').val('');
        $('#menu').val('');
        $("#chnlcode").selectpicker('refresh');
        $('#add_status').selectpicker('val',1);
        $('#level').val('');
        $('select.province').each(function () {
            if($(this).attr('id') == 'province_0'){

            }else {
                $(this).parent().parent().parent().parent().remove();
                area_count = 0;
            }
        });
        $('select.mcca').each(function () {
            if($(this).attr('id') == 'industry_f0'){

            }else {
                $(this).parent().parent().parent().parent().remove();
                industry_count = 0;
            }
        });


        $('#chnlcode').selectpicker('destroy');
        //$('#chnlcode').html('<option value="9">网商</option> <option value="3">富有</option> <option value="13">微信</option> <option value="14">富有绿洲</option> ');
        $('#chnlcode').selectpicker({
            style: 'btn-inverse',
            width: 365,
            // actionsBox:true,
        });
        $('#chnlcode').selectpicker('refresh');


        $('#account_name').selectpicker('destroy');
        $('#account_name').html('<option value="0">请选择</option>');
        $('#account_name').selectpicker({
            style: 'btn-inverse',
            width: 365,
            // actionsBox:true,
        });
        $('#account_name').selectpicker('refresh');



        $('.province').selectpicker('val','全部');
        $('.city').selectpicker('destroy');
        $('.city').html("<option value='全部'>"+ '全部' +"</option>");
        $('.city').selectpicker({
            style: 'btn-inverse',
            width: 180,
            // actionsBox:true,
        });
        $('.city').selectpicker('refresh');
        $('.city').selectpicker('val',['全部']);

        $('.mcca').selectpicker('val','全部');
        $('.mcc').selectpicker('destroy');
        $('.mcc').html("<option value='全部'>"+ '全部' +"</option>");
        $('.mcc').selectpicker({
            style: 'btn-inverse',
            width: 180,
            // actionsBox:true,
        });
        $('.mcc').selectpicker('refresh');
        $('.mcc').selectpicker('val',['全部']);
        var str_qudao = '';
        $('#qudao_select').selectpicker('destroy');
        $('#qudao_select').html("");
        $.each(qudaoids_arr,function (i,item) {
           str_qudao += "<option value='"+ item.qd_uid +"'>" + item.name +"</option>"
        });
        $('#qudao_select').append(str_qudao);
        $('#qudao_select').selectpicker({
            style: 'btn-inverse',
            width: 365,
            actionsBox:true,
        });
        $('#qudao_select').selectpicker('refresh');
        $('#qudao_select').selectpicker('selectAll');
        $('#group_area').val(qd_uids.join(','));
        // 修改请求数据
        var chnlcode = $('#chnlcode').val()
        console.log(chnlcode)
        load_app_conf(chnlcode)
        $('#modal_add').modal('show');
    });


    //*********************************************************
    // 新增修改页公众号名称


    $('#chnlcode').selectpicker({
        style: 'btn-inverse',
        width: '365px',
    });

    $('#account_name').selectpicker({
        style: 'btn-inverse',
        width: '365px',
    });
    $('#account_name').selectpicker('refresh');
    // 新增修改页状态
    $('#add_status').selectpicker({
        style: 'btn-inverse',
        width: '365px',
    });
    $('#add_status').selectpicker('refresh');
    // 新增修改页初始展示的省份
    $('#province_0').selectpicker({
        style: 'btn-inverse',
        width: '180px',
    });
    $('#province_0').selectpicker('refresh');
    // 新增修改页初始展示的城市
    $('#city_0').selectpicker({
        style: 'btn-inverse',
        width: '180px',
        actionsBox:true,
    });
    $('#city_0').selectpicker('refresh');

    // 省份城市加号点击的事件
    $('#area_add').click(function () {
        // var p = $('#province_0').selectpicker('val');
        // if (p == '全部'){
        //     return;
        // }
        area_count = area_count + 1;
        str = "<div class='form-inline'>\
                    <div class='col-md-1'></div>\
                    <div class='col-md-2'>\
                        <label style='height: 34px;line-height: 34px;'></label>\
                    </div>\
                    <div class='col-md-1' style='padding: 0px;'>\
                        <label style='height: 34px;line-height: 34px;'></label>\
                    </div>\
                    <div class='form-inline col-md-8'>\
                        <div>\
                            <select name='' id='province_"+ area_count +"' class='selectpicker show-menu-arrow province' data-live-search='true' style='width: 100px'>\
                            </select>\
                            <select name='' id='city_"+ area_count +"' class='selectpicker show-menu-arrow city' multiple data-live-search='true' style='width: 100px'>\
                            </select>\
                            <button class='area_delete'><span class='fa fa-minus' aria-hidden='true'></button>\
                        </div>\
                    </div>\
                </div>\
                <div style='clear: both'></div>";

        $('#area').append(str);

        $('#province_'+area_count).selectpicker({
            style: 'btn-inverse',
            width: '180px',
        });
        var str_provnce = '';
        $('#province_'+area_count).html("<option value='全部'>"+ '全部' + "</option>");
        $.each(provincesArr, function (i,item) {
            str_provnce += "<option value='"+ item.id +"'>" + item.area_name + "</option>"
        });
        $('#province_'+area_count).append(str_provnce);
        $('#province_'+area_count).selectpicker('refresh');
        $('#city_'+area_count).html("<option value='全部'>"+ '全部' + "</option>");
        $('#city_'+area_count).selectpicker({
            style: 'btn-inverse',
            width: '180px',
            // actionsBox:true,
        });
        // $('#city_'+area_count).selectpicker('val',['全部']);
        $('#city_'+area_count).selectpicker('refresh');
        $('#city_'+area_count).selectpicker('selectAll');

    });

    // 行业点击加号的事件
    $('#industry_add').click(function () {
        // var m = $('#industry_f0').selectpicker('val');
        // if (m == '全部'){
        //     return;
        // }
        industry_count = industry_count + 1;
        str = "<div class='form-inline'>\
                    <div class='col-md-1'></div>\
                    <div class='col-md-2'>\
                        <label style='height: 34px;line-height: 34px;'></label>\
                    </div>\
                    <div class='col-md-1' style='padding: 0px;'>\
                        <label style='height: 34px;line-height: 34px;'></label>\
                    </div>\
                    <div class='form-inline col-md-8'>\
                        <div>\
                            <select name='' id='industry_f"+ industry_count +"' class='selectpicker show-menu-arrow mcca' data-live-search='true' style='width: 100px'>\
                            </select>\
                            <select name='' id='industry_s"+ industry_count +"' class='selectpicker show-menu-arrow mcc' multiple data-live-search='true' style='width: 100px'>\
                            </select>\
                            <button class='industry_delete'><span class='fa fa-minus' aria-hidden='true'></button>\
                        </div>\
                    </div>\
                </div>\
                <div style='clear: both'></div>";
        $('#industry').append(str);
        $('#industry_f'+industry_count).selectpicker({
            style: 'btn-inverse',
            width: '180px',
        });
        var str_mcc = '';
        $('#industry_f'+industry_count).html("<option value='全部'>"+ '全部' + "</option>");
        $.each(mccaArr, function (i, item) {
            str_mcc += "<option value='" + item.id + "'>" + item.mcca_name + "</option>";
        });
        $('#industry_f'+industry_count).append(str_mcc);
        $('#industry_f'+industry_count).selectpicker('refresh');

        $('#industry_s'+industry_count).html("<option value='全部'>"+ '全部' + "</option>");
        $('#industry_s'+industry_count).selectpicker({
            style: 'btn-inverse',
            width: '180px',
        });
        // $('#industry_s'+industry_count).selectpicker('val',['全部']);
        $('#industry_s'+industry_count).selectpicker('refresh');
        $('#industry_s'+industry_count).selectpicker('selectAll');
    });
    // 初始化第一行第一列行业下拉选框
    $('#industry_f0').selectpicker({
        style: 'btn-inverse',
        width: '180px',
    });
    $('#industry_f0').selectpicker('refresh');
    // 初始化第一行第二列行业下拉选框
    $('#industry_s0').selectpicker({
        style: 'btn-inverse',
        width: '180px',
    });
    $('#industry_s0').selectpicker('refresh');
    // 初始化渠道下拉选框
    $('#qudao_select').selectpicker({
        style: 'btn-inverse',
        width: '365px',
    });
    $('#qudao_select').selectpicker('refresh');
    $('#qudao_select').change(function () {
        var index = this.selectedIndex;
        $('#group_area').val(String($('#qudao_select').val()));
    });
    // 失去焦点的事件
    $('#group_area').blur(function () {
        var group_str = $('#group_area').val();
        var group_strl = group_str.replace(/，/g,',');
        // group_strl = $.trim(group_strl);
        group_strl = group_strl.replace(/\s|\xA0/g,"");
        // var group_arr = new Array();
        laststr = group_strl.substr(group_strl.length-1,1);
        if(laststr.indexOf(',') != -1){
            group_strl = group_strl.substr(0,group_strl.length-1);
        }
        group_arr = group_strl.split(',');
        $('#qudao_select').selectpicker('val',group_arr);
    });
    // 进入页面后获取一些基本数据的请求
    $.ajax({
        async: true,
        url:'/get_select_data',
        type:'POST',
        dataType:'json',
        data:{},
        success:(function (json) {
            // 列表页的公众号名称数据初始化
            var str = '';
            $('#officialAccountName').html("<option value=''>"+'请选择'+"</option>");
            $.each(json.data.id_names, function (i,item) {
                str += "<option value='"+ item.nick_name +"'>" + item.nick_name + "</option>"
            });
            $('#officialAccountName').append(str);
            $('#officialAccountName').selectpicker('refresh');
            id_appname = json.data.id_names;
            // 新增修改页的公众号名称数据初始化
            var str_add = '';
            // $('#account_name').html("");
            // $.each(json.data.id_names, function (i,item) {
            //     str_add += "<option value='"+ item.appid +"'>" + item.nick_name + "</option>"
            // });
            // $('#account_name').append(str_add);
            // $('#account_name').selectpicker('refresh');
            // id_appname = json.data.id_names;
            // $("#account_name").selectpicker('val',id_appname[0].appid);
            // $("#account_name").selectpicker('refresh');
            $('#appid').val(id_appname[0].appid);
            // 新增修改页的省份数据初始化
            var str_provnce = '';
            $('#province_0').html("<option value='全部'>" + '全部' + "</option>");
            $.each(json.data.provinces, function (i,item) {
                str_provnce += "<option value='"+ item.id +"'>" + item.area_name + "</option>"
            });
            $('#province_0').append(str_provnce);
            $('#province_0').selectpicker('refresh');
            provincesArr = json.data.provinces;
            // 新增修改页的行业一级初始化
            var str_mcca = '';
            $('#industry_f0').html("<option value='全部'>" + '全部' + "</option>");
            $.each(json.data.mcca, function (i,item) {
                str_mcca += "<option value='"+ item.id +"'>" + item.mcca_name + "</option>"
            });
            $('#industry_f0').append(str_mcca);
            $('#industry_f0').selectpicker('refresh');
            mccaArr = json.data.mcca;
            // 新增修改页的渠道初始化
            qd_uids = [];
            var str_qudao = '';
            // $('#qudao_select').html("<option value='全部'>"+ '全部' +"</option>");
            $('#qudao_select').html("");
            $.each(json.data.groupids,function (i,item) {
               str_qudao += "<option value='"+ item.qd_uid +"'>" + item.name +"</option>"
               qd_uids.push(item.qd_uid);
            });
            qudaoids_arr = json.data.groupids;
            $('#qudao_select').append(str_qudao);
            $('#qudao_select').selectpicker({
                style: 'btn-inverse',
                width: 365,
                actionsBox:true,
            });
            $('#qudao_select').selectpicker('refresh');
            $('#qudao_select').selectpicker('selectAll');

            id_mcca = json.data.id_mcca;
            id_mcca['全部'] = '全部';
            id_mcc = json.data.id_mcc;
            id_mcc['全部'] = '全部';
            id_pro = json.data.id_pro;
            id_pro['全部'] = '全部';

            console.log(json.data.groupid_names);
            groupid_names = json.data.groupid_names;
            mcca_total = json.data.mcca_total;
            pro_total = json.data.pro_total;
            table = initOfficialAccountTable();
            table.on('order.dt search.dt', function() {
                table.column(0, {search: 'applied', order: 'applied'}).nodes().each(function(cell, i) {
                    cell.innerHTML = i + 1;
                });
            }).draw();




        }),
        error:(function () {
            toastr.error('网络异常，请重试！');
        })
    });
    $('#account_name').change(function () {
        //$('#appid').val($('#account_name').val());


        console.log($('#account_name').val());

        var _appid = $('#account_name').val();

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

                    $('#account_name').html("");

                    str_add += "<option value='0'>请选择</option>";

                    for(var i=0;i<_rs.length;i++) {

                        str_add += "<option value='"+ _rs[i]['appid'] +"'>" + _rs[i]['appname'] + "</option>";

                    }


                    $('#account_name').append(str_add);

                    $('#account_name').selectpicker('refresh');




            }),
            error: (function () {
                toastr.error('网络异常，请重试！');
            })
        });


    });





    $(document).on('change','select.province',function () {
        var pro = $(this);
        var city = $(this).parent().next().children('select');
        var index = this.selectedIndex;

        $.ajax({
            async: true,
            url: '/get_city',
            type: 'POST',
            dataType: 'json',
            data: {
                area_no: $(this).val(),
            },
            success: (function (json) {
                // $('#industry_f0').html("");
                // city.html("<option value='全部'>" + "全部" + "</option>");
                if(pro.val() == '全部'){
                    // alert('全部');
                    city.selectpicker('destroy');
                    city.html("<option value='全部'>" + "全部" + "</option>");
                    city.selectpicker({
                        style: 'btn-inverse',
                        width: '180px',
                        // actionsBox:true,
                    });
                    city.selectpicker('refresh');
                    city.selectpicker('selectAll');
                }else {
                    // alert('不是全部');
                    var str_city = '';
                    city.selectpicker('destroy');
                    city.html("");
                    $.each(json.data.citys, function (i,item) {
                        // str_city += "<option value='"+ item.area_id +"'>" + item.city_name + "</option>";
                        str_city += "<option value='"+ item.city_name +"'>" + item.city_name + "</option>";
                    });
                    city.append(str_city);
                    city.selectpicker({
                        style: 'btn-inverse',
                        width: '180px',
                        actionsBox:true,
                    });
                    city.selectpicker('refresh');
                    city.selectpicker('selectAll');
                }

            }),
            error: (function () {
                toastr.error('网络异常，请重试！');
            })
        });

    });
    $(document).on('change','select.mcca',function () {
        var mcca = $(this);
        var mcc = $(this).parent().next().children('select');
        $.ajax({
            async: true,
            url: '/get_mccs',
            type: 'POST',
            dataType: 'json',
            data: {
                mcca_id: $(this).val(),
            },
            success: (function (json) {
                if(mcca.val() == '全部'){
                    mcc.selectpicker('destroy');
                    mcc.html("<option value='全部'>" + "全部" + "</option>");
                    mcc.selectpicker({
                        style: 'btn-inverse',
                        width: '180px',
                        // actionsBox:true,
                    });
                    mcc.selectpicker('refresh');
                    mcc.selectpicker('selectAll');
                }else {
                    var str_mcc = '';
                    mcc.selectpicker('destroy');
                    mcc.html("");
                    $.each(json.data.mccs, function (i, item) {
                        str_mcc += "<option value='" + item.id + "'>" + item.mcc_name + "</option>";
                    });
                    mcc.append(str_mcc);
                    mcc.selectpicker({
                        style: 'btn-inverse',
                        width: '180px',
                        actionsBox:true,
                    });
                    mcc.selectpicker('refresh');
                    mcc.selectpicker('selectAll');
                }
            }),
            error: (function () {
                toastr.error('网络异常，请重试！');
            })
        })
    });
    // 地区后面的删除按钮的预绑定事件
    $(document).on('click','.area_delete',function () {
        area_count = area_count - 1;
       $(this).parent().parent().parent().remove();
    });
    // 行业后面的删除按钮的预绑定事件
    $(document).on('click','.industry_delete',function () {
       industry_count = industry_count - 1;
       $(this).parent().parent().parent().remove();
    });

    // 提交按钮
    $('#submit').click(function () {
        if(!chenckIsEmpty()){
            return;
        }
        var cid = $('#cid').val();

        var options =$("#account_name option:selected");

        var areas = [];
        $('select.province').each(function () {
            var data = {};
            data['pro'] = $(this).children('option:selected').text();
            // data['city'] = JSON.stringify($(this).parent().next().children('select').val());
            data['city'] = $(this).parent().next().children('select').val();
            areas.push(data)
        });

        var chnlcode = $("#chnlcode").val();

        var mcc = [];
        $('select.mcca').each(function () {
           var data = {};
           data['mcca'] = $(this).children('option:selected').val();
           // data['mcc'] = JSON.stringify($(this).parent().next().children('select').val());
            data['mcc'] = $(this).parent().next().children('select').val();
           mcc.push(data);
        });

        var group_str = $('#group_area').val();
        var group_strl = group_str.replace(/，/g,',');
        // group_strl = $.trim(group_strl);
        group_strl = group_strl.replace(/\s|\xA0/g,"");
        // var group_arr = new Array();
        laststr = group_strl.substr(group_strl.length-1,1);
        if(laststr.indexOf(',') != -1){
            group_strl = group_strl.substr(0,group_strl.length-1);
        }
        group_arr = group_strl.split(',');

        var menu_str = $('#menu').val();
        var menu_strl = menu_str.replace(/，/g,',');
        var menu_arr = new Array();
        menu_arr = menu_strl.split(',');

        //设置post参数
        var appname = options.text(); // 公众号名称
        var appid = options.val();  // appid
        var pay_appid = $('#pay_appid').val();
        // var menu = JSON.stringify(menu_arr);  // 支付目录
        var menu = menu_arr;  // 支付目录
        var state = $('#add_status').val();  // 状态
        var level = $('#level').val();  // 优先级
        // var area = JSON.stringify(areas);  // 地区
        // var trade = JSON.stringify(mcc);  // 行业
        // var group = JSON.stringify(group_arr);  // 渠道
        var area = areas;  // 地区
        var trade = mcc;  // 行业
        // var group = group_arr;  // 渠道
        var group;
        if (qd_uids.toString() == group_arr.toString()) {
            group = ["全部"];
        }else {
            group = group_arr;
        }

        console.log(qd_uids.toString());
        console.log(group_arr.toString());
        // return;
        if(submit_type == 1){
            $.ajax({
                async: true,
                url: '/app_rule_insert',
                type: 'POST',
                dataType: 'json',
                contentType: 'application/json;',
                data: JSON.stringify({
                    'cid':cid,
                    'appname':appname,
                    'appid':appid,
                    'pay_appid':pay_appid,
                    'menu':menu,
                    'state':state,
                    'level':level,
                    'area':area,
                    'trade':trade,
                    'group':group,
                    'chnlcode':chnlcode
                }),
                success:(function (json) {
                    if (json.ok){
                        toastr.success('添加成功！');
                        $('#modal_add').modal('hide');
                        table = initOfficialAccountTable();
                        table.on('order.dt search.dt', function() {
                            table.column(0, {search: 'applied', order: 'applied'}).nodes().each(function(cell, i) {
                                cell.innerHTML = i + 1;
                            });
                        }).draw();
                    }else {
                        toastr.error(json.msg);
                    }
                }),
                error: (function () {
                    toastr.error('网络异常，请重试！');
                })
            })
        }else if (submit_type == 2){
            $.ajax({
                async: true,
                url: '/app_rule_update',
                type: 'POST',
                dataType: 'json',
                contentType: 'application/json;',
                data: JSON.stringify({
                    'cid':cid,
                    'id':$('#change_id').text(),
                    'appname':appname,
                    'appid':appid,
                    'pay_appid':pay_appid,
                    'menu':menu,
                    'state':state,
                    'level':level,
                    'area':area,
                    'trade':trade,
                    'group':group,
                    'chnlcode':$("#chnlcode").val()
                }),
                success:(function (json) {
                    if (json.ok){
                        toastr.success('修改成功！');
                        $('#modal_add').modal('hide');
                        table = initOfficialAccountTable();
                        table.on('order.dt search.dt', function() {
                            table.column(0, {search: 'applied', order: 'applied'}).nodes().each(function(cell, i) {
                                cell.innerHTML = i + 1;
                            });
                        }).draw();
                    }else {
                        toastr.error(json.msg);
                    }
                }),
                error: (function () {
                    toastr.error('网络异常，请重试！');
                })
            })
        }
    });

    //取消按钮
    $('#cancel').click(function () {
        $('#modal_add').modal('hide');
    });

    // 修改按钮预绑定
    $(document).on("click","[data-action='appchange']",function () {
        submit_type = 2;
        $('#myModalLabel').text('修改 公众号配置');
        var obj = document.getElementById("group_area");
        obj.style.border = '1px gainsboro solid';
        var c_id = $(this).attr('data-id');
        $('#change_id').text(c_id);
        $.ajax({
            async: true,
            url: '/app_rule_getone',
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json;',
            data: JSON.stringify({'id':c_id}),
            success: (function (json) {
                var cid = json.data[0].cid;
                var id = json.data[0].id;
                var appid = json.data[0].appid;
                var pay_appid = json.data[0].pay_appid;
                var appname = json.data[0].appname;
                var area = JSON.parse(json.data[0].area);
                var group = JSON.parse(json.data[0].group);
                var trade = JSON.parse(json.data[0].trade);
                var menu = JSON.parse(json.data[0].menu);
                var state = json.data[0].state;
                var level = json.data[0].level;
                var chnlcode = JSON.parse(json.data[0].chnlcode);

                console.log(chnlcode);

                $('#chnlcode').selectpicker('val',chnlcode);
                $('#chnlcode').selectpicker('refresh');











                $('#cid').val(cid);

                $('#appid').val(appid);
                $('#pay_appid').val(pay_appid);
                $('#menu').val(menu.join(','));
                $('#add_status').selectpicker('val',state);
                $('#level').val(level);



                $.ajax({
            async: false,
            url: '/get_app_config',
            type: 'POST',
            dataType: 'json',
            data: {
                chnlcode: JSON.stringify($('#chnlcode').val())
            },
            success: (function (json) {

                    var _rs = json.data;

                    _all_conf = _rs;

                    var str_add = "";

                    $('#account_name').html("");

                    str_add += "<option value='0'>请选择</option>";

                    _main = '';


                    console.log(_rs);

                    for(var i=0;i<_rs.length;i++) {

                        str_add += "<option value='"+ _rs[i]['appid'] +"'>" + _rs[i]['appname'] + "</option>";

                        if(_rs[i]['appid'] == appid){


                            _main = _rs[i]['main'];
                            $("#cid").val(_rs[i]['cid']);
                            $("#pay_appid").val(_rs[i]['pay_appid']);
                            $("#menu").val(_rs[i]['menu']);
                        }

                    }

                    $("#main").val(_main);

                    $('#account_name').append(str_add);

                    $('#account_name').selectpicker('refresh');


                    $('#account_name').selectpicker('val',appid);
                    $('#account_name').selectpicker('refresh');








            }),
            error: (function () {
                toastr.error('网络异常，请重试！');
            })
        });

                /*
                依次遍历class为province的select标签，留下第一个id为province_0的，清除掉后边的，以便后续重新初始化
                for循环area，因为保留了第一个，所以后续需要增加的就是area.length-1，每增加一个就初始化一个，
                初始化完成后再依次遍历，依据数据源对每个province进行赋值，赋值完成后再ajax请求省份下的city，对city标签进行初始化
                然后再根据city的数组对city进行赋值（纠结了一段时间的bug，city赋值要在ajax请求city成功success中进行，不可在ajax外
                对city标签进行$('#city_'+i).selectpicker('val',JSON.parse(area[i].city));操作，ajax异步请求，放在ajax外部数据还没
                请求成功，对city进行赋值显示的永远是空，小问题，bug却找了很久）
                 */
                $('select.province').each(function () {
                    if($(this).attr('id') == 'province_0'){

                    }else {
                        $(this).parent().parent().parent().parent().remove();
                        area_count = 0;
                    }
                });
                for (var i=0;i<area.length-1;i++) {
                    area_count = area_count + 1;
                    var str = "<div class='form-inline'>\
                                    <div class='col-md-1'></div>\
                                    <div class='col-md-2'>\
                                        <label style='height: 34px;line-height: 34px;'></label>\
                                    </div>\
                                    <div class='col-md-1' style='padding: 0px;'>\
                                        <label style='height: 34px;line-height: 34px;'></label>\
                                    </div>\
                                    <div class='form-inline col-md-8'>\
                                        <div>\
                                            <select name='' id='province_" + area_count + "' class='selectpicker show-menu-arrow province' data-live-search='true' style='width: 100px'>\
                                            </select>\
                                            <select name='' id='city_" + area_count + "' class='selectpicker show-menu-arrow city' multiple data-live-search='true' style='width: 100px'>\
                                            </select>\
                                            <button class='area_delete'><span class='fa fa-minus' aria-hidden='true'></button>\
                                        </div>\
                                    </div>\
                                </div>\
                                <div style='clear: both'></div>";
                    $('#area').append(str);
                    $('#province_'+area_count).selectpicker({
                        style: 'btn-inverse',
                        width: '180px',
                    });
                    var str_provnce = '';
                    $('#province_'+area_count).html("<option value='全部'>"+ '全部' + "</option>");
                    $.each(provincesArr, function (i,item) {
                        str_provnce += "<option value='"+ item.id +"'>" + item.area_name + "</option>"
                    });
                    $('#province_'+area_count).append(str_provnce);
                    $('#province_'+area_count).selectpicker('refresh');

                    // $('#city_'+area_count).selectpicker({
                    //     style: 'btn-inverse',
                    //     width: '180px',
                    //     actionsBox:true,
                    // });
                    // $('#city_'+area_count).selectpicker('refresh');
                }

                $('select.province').each(function (i,item) {
                    $('#province_'+i).selectpicker('val',id_pro[area[i].pro]);
                    $.ajax({
                        async: true,
                        url: '/get_city',
                        type: 'POST',
                        dataType: 'json',
                        data: {
                            area_no: id_pro[area[i].pro],
                        },
                        success: (function (json) {
                            if(area[i].pro == '全部'){
                                $('#city_'+i).selectpicker('destroy');
                                $('#city_'+i).html("<option value='全部'>" + "全部" + "</option>");
                                $('#city_'+i).selectpicker({
                                    style: 'btn-inverse',
                                    width: '180px',
                                });
                                $('#city_'+i).selectpicker('refresh');
                                $('#city_'+i).selectpicker('selectAll');
                            }else {
                                var str_city = '';
                                $('#city_'+i).selectpicker('destroy');
                                $('#city_'+i).html("");
                                $.each(json.data.citys, function (i,item) {
                                    str_city += "<option value='"+ item.city_name +"'>" + item.city_name + "</option>";
                                });
                                $('#city_'+i).append(str_city);
                                $('#city_'+i).selectpicker({
                                    style: 'btn-inverse',
                                    width: '180px',
                                    actionsBox:true,
                                });
                                $('#city_'+i).selectpicker('refresh');
                                $('#city_'+i).selectpicker('val',area[i].city);
                            }
                        }),
                        error: (function () {
                            toastr.error('网络异常，请重试！');
                        })
                    });
                });

                /*
                行业mcc部分清除再赋值
                 */
                $('select.mcca').each(function () {
                    if($(this).attr('id') == 'industry_f0'){

                    }else {
                        $(this).parent().parent().parent().parent().remove();
                        industry_count = 0;
                    }
                });
                for (var i=0;i<trade.length-1;i++){
                    industry_count = industry_count + 1;
                    str = "<div class='form-inline'>\
                                <div class='col-md-1'></div>\
                                <div class='col-md-2'>\
                                    <label style='height: 34px;line-height: 34px;'></label>\
                                </div>\
                                <div class='col-md-1' style='padding: 0px;'>\
                                    <label style='height: 34px;line-height: 34px;'></label>\
                                </div>\
                                <div class='form-inline col-md-8'>\
                                    <div>\
                                        <select name='' id='industry_f"+ industry_count +"' class='selectpicker show-menu-arrow mcca' data-live-search='true' style='width: 100px'>\
                                        </select>\
                                        <select name='' id='industry_s"+ industry_count +"' class='selectpicker show-menu-arrow mcc' multiple data-live-search='true' style='width: 100px'>\
                                        </select>\
                                        <button class='industry_delete'><span class='fa fa-minus' aria-hidden='true'></button>\
                                    </div>\
                                </div>\
                            </div>\
                            <div style='clear: both'></div>";
                    $('#industry').append(str);
                    $('#industry_f'+industry_count).selectpicker({
                        style: 'btn-inverse',
                        width: '180px',
                    });
                    var str_mcc = '';
                    $('#industry_f'+industry_count).html("<option value='全部'>"+ '全部' + "</option>");
                    $.each(mccaArr, function (i, item) {
                        str_mcc += "<option value='" + item.id + "'>" + item.mcca_name + "</option>";
                    });
                    $('#industry_f'+industry_count).append(str_mcc);
                    $('#industry_f'+industry_count).selectpicker('refresh');

                    // $('#industry_s'+industry_count).selectpicker({
                    //     style: 'btn-inverse',
                    //     width: '180px',
                    // });
                    // $('#industry_s'+industry_count).selectpicker('refresh');
                }
                $('select.mcca').each(function (i,item) {
                    $('#industry_f'+i).selectpicker('val',trade[i].mcca);
                    $.ajax({
                        async: true,
                        url: '/get_mccs',
                        type: 'POST',
                        dataType: 'json',
                        data: {
                            mcca_id: trade[i].mcca,
                        },
                        success: (function (json) {
                            if(trade[i].mcca == '全部'){
                                $('#industry_s'+i).selectpicker('destroy');
                                $('#industry_s'+i).html("<option value='全部'>" + "全部" + "</option>");
                                $('#industry_s'+i).selectpicker({
                                    style: 'btn-inverse',
                                    width: '180px',
                                });
                                $('#industry_s'+i).selectpicker('refresh');
                                $('#industry_s'+i).selectpicker('selectAll');
                            }else {
                                var str_mcc = '';
                                $('#industry_s'+i).html("");
                                $.each(json.data.mccs, function (i, item) {
                                    str_mcc += "<option value='" + item.id + "'>" + item.mcc_name + "</option>";
                                });
                                $('#industry_s'+i).append(str_mcc);
                                $('#industry_s'+i).selectpicker({
                                    style: 'btn-inverse',
                                    width: '180px',
                                    actionsBox:true,
                                });
                                $('#industry_s'+i).selectpicker('refresh');
                                $('#industry_s'+i).selectpicker('val',trade[i].mcc)
                            }
                        }),
                        error: (function () {
                            toastr.error('网络异常，请重试！');
                        })
                    })
                });
                $('#qudao_select').selectpicker('destroy');
                $('#qudao_select').selectpicker({
                    style: 'btn-inverse',
                    width: 365,
                    actionsBox:true,
                });
                if(group.in_array('全部')){
                    $('#qudao_select').selectpicker('refresh');
                    $('#qudao_select').selectpicker('selectAll');
                    $('#group_area').val(qd_uids.join(','));
                }else {
                    $('#qudao_select').selectpicker('refresh');
                    $('#qudao_select').selectpicker('val',group);
                    $('#group_area').val(group.join(','));
                }


            }),
            error: (function () {
                toastr.error('网络异常，请重试！');
            })
        });
        $('#modal_add').modal('show');
    });



});
//验证字符串是否是数字
function checkNumber(theObj) {
    if(isNaN(theObj)){
        return false;
    }else {

    }
    return true;
}

function chenckIsEmpty() {
    var cid = $('#cid').val();
    if (!cid){
        toastr.warning('请输入通道渠道号！');
        return false;
    }
    var appname = $("#account_name").selectpicker('val');
    if(!appname){
        toastr.warning('请选择公众号名称！');
        return false;
    }

    var pay_appid = $('#pay_appid').val();
    if(!pay_appid){
        toastr.warning('请输入支付APPID！');
        return false;
    }

    var menu_str = $('#menu').val();
    if(!menu_str){
        toastr.warning('请输入支付目录！');
        return false;
    }

    // var state = $('#add_status').val();  // 状态
    var level = $('#level').val();  // 优先级
    if(!level){
        toastr.warning('请输入优先级！');
        return false;
    }
    if(!checkNumber(level)){
        toastr.warning('请输入合法的优先级！');
        return false;
    }
    var _isInvalidArea = true;
    $('select.province').each(function () {
        var data = {};
        data['pro'] = $(this).children('option:selected').text();
        if(!data['pro']){
            toastr.warning('请选择省份！');
            _isInvalidArea = false;
            return false;
        }
        data['city'] = $(this).parent().next().children('select').val();
        if(!data['city'].length){
            toastr.warning('请选择城市！');
            _isInvalidArea = false;
            return false;
        }
        if(data['city'].in_array('全部') && data['city'].length > 1){
            // toastr.warning("城市选择中，'全部'无法与其他城市同时选中提交，请检查后重新提交！ ");
            alert("城市选择中，'全部'无法与其他城市同时选中提交，请检查后重新提交！ ");
            _isInvalidArea = false;
            return false;
        }
    });
    if(!_isInvalidArea){
        return false;
    }
    var _isInvalidMcc = true;
    $('select.mcca').each(function () {
       var data = {};
       data['mcca'] = $(this).children('option:selected').val();
       if(!data['mcca']){
           toastr.warning('请选择一级行业！');
           _isInvalidMcc = false;
            return false;
        }
       data['mcc'] = $(this).parent().next().children('select').val();
       if(!data['mcc'].length){
           toastr.warning('请选择二级行业！');
           _isInvalidMcc = false;
           return false
       }
       if(data['mcc'].in_array('全部') && data['mcc'].length > 1){
           // toastr.warning("二级行业选择中，'全部'无法与其他行业同时选中提交，请检查后重新提交！ ");
           alert("二级行业选择中，'全部'无法与其他行业同时选中提交，请检查后重新提交！ ");
           _isInvalidMcc = false;
           return false;
       }
    });
    if(!_isInvalidMcc){
        return false;
    }
    var group_str = $('#group_area').val();
    var group_strl = group_str.replace(/，/g,',');
    // group_strl.replace(/\s+/g, "");
    group_strl = group_strl.replace(/\s|\xA0/g,"");
    var group_arr = new Array();
    laststr = group_strl.substr(group_strl.length-1,1);
    if(laststr.indexOf(',') != -1){
        group_strl = group_strl.substr(0,group_strl.length-1);
    }
    group_arr = group_strl.split(',');
    if(!group_str){
        toastr.warning('请选择渠道！');
        return false;
    }
    var err_arr = [];
    $.each(group_arr,function (i,item) {
        if (!qd_uids.in_array(item)){
            err_arr.push(item);
        }
    });
    if(err_arr.length > 0){
        var obj = document.getElementById("group_area");
        obj.style.border = '1px red solid';
        alert(err_arr+'等渠道id不合法，请检查后重新输入！');
        return false;
    }
    if(group_arr.in_array('全部') && group_arr.length > 1){
        // toastr.warning("渠道选择中，'全部'无法与其他渠道同时选中提交，请检查后重新提交！ ");
        alert("渠道选择中，'全部'无法与其他渠道同时选中提交，请检查后重新提交！ ");
        return false;
     }
    return true;
}

// 列表页初始化
function initOfficialAccountTable() {
    var table = $("#official_account_table").DataTable({
        "paging": true,
        "order": [],
        "pagingType": "full_numbers",
        "lengthMenu": [10],
        "bDestory": true,
        "destroy":true,
        "autoWidth":true,
        "bLengthChange": false,
        "processing": true,
        "searching": false, //是否开启搜索
        "serverSide": false, //开启服务器获取数据
        "ajax": { // 获取数据
            "url": "/app_rule_list",
            "contentType": 'application/json;',
            "data": function (d) {
                // d.appname = $('#officialAccountName').children('option:selected').text();
                d.appname = $('#officialAccountName').val();
                d.state = $('#status').val();
                d.chnlcode = $('#chnlcode_select').val();
                return JSON.stringify(d);
            },
            "type": "POST",
            "dataType": "json" //返回来的数据形式
        },
        "columns": [ //定义列数据来源
            {'title': "序号", 'data': null},
            {'title': "公众号名称", 'data': null},
            {'title': "APPID", 'data': "appid"},
            {'title': "地区", 'data': null},
            {'title': "行业", 'data': null},
            {'title': "渠道", 'data': null},
            {'title': "通道", 'data': null},
            {'title': "状态", 'data': "state"},
            {'title': "优先级", 'data': "level"},
            {'title': "操作", 'data': null}
        ],
        // "order": [[ 7, 'asc' ]],
        "columnDefs": [ //自定义列
            {
                "targets": 0, //改写哪一列
                "orderable": false ,
                "ordering": false,
                fnDrawCallback : function () {
                    var api = this.api();
                    api.column(0).nodes().each(function(cell, i) {
                        cell.innerHTML = i + 1;
                    })
                }
            },
            {
                "targets": 1,
                // "width": "10%",
                "render": function (data, type, row) {
                    var htmlStr = '';
                    htmlStr += "<div style='word-wrap:break-word;width: 100px'>" + row.appname + "</div>";
                    return htmlStr;
                }
            },
            {
                "targets": 2,
                // "width": "20%",
            },
            {
                "targets": 3, //改写哪一列
                "render": function (data, type, row) {
                    var htmlStr = '';
                    $.each(jQuery.parseJSON(row.area),function (i,item) {
                        if(item.pro == '全部'){
                            htmlStr += "<div style='word-wrap:break-word;width: 150px'>" + '全国' + "</div>";
                        }else {
                            if (item.city.length == pro_total[id_pro[item.pro]]){
                                htmlStr += "<div style='word-wrap:break-word;width: 150px'>" + item.pro + "</div>";
                            }else {
                                htmlStr += "<div style='word-wrap:break-word;width: 150px'>" + item.pro + "-" + item.city.join(',') + "</div>";
                            }
                        }
                    });
                    return htmlStr;

                }
            },
            {
                "targets": 4, //改写哪一列
                // "data": "uid",
                // "width": "15%",
                "render": function (data, type, row) {
                    var htmlStr = '';
                    $.each(jQuery.parseJSON(row.trade),function (i,item) {
                        var arr = [];
                        if(item.mcca == '全部'){
                            htmlStr += "<div style='word-wrap:break-word;width: 170px'>"+'全部'+"</div>";
                        }else {
                            if(item.mcc.length == mcca_total[item.mcca]){
                                htmlStr += "<div style='word-wrap:break-word;width: 170px'>"+id_mcca[item.mcca]+"</div>";
                            }else {
                                $.each(item.mcc,function (n,value) {
                                    arr.push(id_mcc[value]);
                                });
                                htmlStr += "<div style='word-wrap:break-word;width: 170px'>"+arr.join(',')+"</div>";
                            }
                        }
                    });
                    return htmlStr;
                }
            },
            {
                "targets": 5, //改写哪一列
                // "data": "uid",
                // "width":"100px",
                "render": function (data, type, row) {
                    var htmlStr = '';
                    var groupArr = jQuery.parseJSON(row.group);
                    var groupnames = [];
                    if (groupArr.in_array('全部')){
                        htmlStr += "<div style='word-wrap:break-word;width: 170px;max-height: 90px;;overflow:hidden'>"+'全部'+"</div>";
                    }else {
                        $.each(groupArr,function (i,item) {
                            groupnames.push(groupid_names[item]);
                        });
                        htmlStr += "<div style='word-wrap:break-word;width: 170px;max-height: 90px;;overflow:hidden'>"+groupnames.join(',')+"</div>";
                    }

                    return htmlStr;
                }
            },

            {
                "targets": 6, //改写哪一列
                // "data": "uid",
                // "width": "5%",
                "render": function (data, type, row) {
                    var htmlStr = '';
                    htmlStr += "<label>"+ row.chnlcode_str +"</label>";
                    return htmlStr;
                }
            },

            {
                "targets": 7, //改写哪一列
                // "data": "uid",
                // "width": "5%",
                "render": function (data, type, row) {
                    var htmlStr = '';
                    if(row.state == 1){
                        htmlStr += "<label>"+'有效'+"</label>";
                    }else {
                        htmlStr += "<label>"+'无效'+"</label>";
                    }
                    return htmlStr;
                }
            },
            {
                "targets": 8,
                // "width": "5%",
                "orderable": true,
            },
            {
                "targets": -1, //改写哪一列
                // "data": "uid",
                // "width": "5%",
                "render": function (data, type, row) {
                    var htmlStr = "<button class='btn btn-primary btn-sm' data-action='appchange' data-id='"+ row.id +"'>"+ "修改" +"</button>";
                    return htmlStr;
                }
            },

            {
                "targets": [0, 1, 2, 3, 4, 5, 6,7,8],
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
                // "sSortAscending": ": 以升序排列此列",
                // "sSortDescending": ": 以降序排列此列"
            }
        }
    });
    return table;
}
