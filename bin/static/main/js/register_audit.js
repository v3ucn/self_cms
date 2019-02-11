/**
 * Created by qfpay on 2017/12/27.
 */
$(function ()
{
    $('#groupid').selectpicker({
        style: 'btn-inverse',
    });


   $.ajax({
        async: true,
        timeout: 15000,
        dataType: "json",
        type: "POST",
        url: '/audit_getgroups',
        data: {

        },
        success:function (json) {
            if(json && json.code == 200 && json.data){
                // var str;
                // $.each(json.data,function (i,item) {
                //     str += "<option value='"+item.qd_uid+"'>"+item.name+"</option>"
                // });
                // $('#groupid').append(str);
                $('#groupid').html("<option value='-1'>请选择</option>");
                var str = '';
                $.each(json.data,function (i,item) {
                    str += "<option value='"+item.qd_uid+"'>"+item.name+"</option>"
                });
                $('#groupid').append(str);
                $('#groupid').selectpicker('refresh');
                // $('#groupid').selectpicker('val',-1);
            }
        }
    });


    $('.advanced').click(function () {
        $('.senior').toggle();
    });
    //审核状态复选框
    $('.audit_type').click(function () {
        if(this.id == 'audit_type_all'){
            if($(this).is(':checked')){
                $('.audit_type').each(function () {
                    $(this).prop('checked',false);
                });
                $(this).prop('checked',true);
            }else {
                $('.audit_type').each(function () {
                    $(this).prop('checked',false);
                });
                $(this).prop('checked',false);
            }
        }else {
            $('#audit_type_all').prop('checked',false);
        }
        var is_have_select = false;
        $('.audit_type').each(function () {
            if($(this).is(':checked')){
                is_have_select = true;
            }
        });
        if(!is_have_select){
            $('#audit_type_all').prop('checked',true);
        }
    });
    //商户类型复选框
    $('.merchant_type').click(function () {
        if(this.id == 'merchant_type_all'){
            if($(this).is(':checked')){
                $('.merchant_type').each(function () {
                    $(this).prop('checked',false);
                });
                $(this).prop('checked',true);
            }else {
                $('.merchant_type').each(function () {
                    $(this).prop('checked',false);
                });
                $(this).prop('checked',false);
            }

        }else {
            $('#merchant_type_all').prop('checked',false);
        }
        var is_have_select = false;
        $('.merchant_type').each(function () {
            if($(this).is(':checked')){
                is_have_select = true;
            }
        });
        if(!is_have_select){
            $('#merchant_type_all').prop('checked',true);
        }
    });
    //门店类型复选框
    $('.store_type').click(function () {
        if(this.id == 'store_type_all'){
            if($(this).is(':checked')){
                $('.store_type').each(function () {
                    $(this).prop('checked',false);
                });
                $(this).prop('checked',true);
            }else {
                $('.store_type').each(function () {
                    $(this).prop('checked',false);
                });
                $(this).prop('checked',false);
            }

        }else {
            $('#store_type_all').prop('checked',false);
        }
        var is_have_select = false;
        $('.store_type').each(function () {
            if($(this).is(':checked')){
                is_have_select = true;
            }
        });
        if(!is_have_select){
            $('#store_type_all').prop('checked',true);
        }
    });
    // 列表页审核按钮的点击事件
    $('#audit').click(function () {
        window.open('/register_audit_detail','_blank');
    });
    $(document).on("click","[data-action='audit']",function () {
        var userid = $(this).attr('data-id');
        var aid = $(this).attr('data-aid');
        window.open('/register_audit_detail?userid='+userid+'&aid='+aid,'_blank');
    });

    //列表页查询按钮点击事件
    $('#query_btn').click(function () {

        if(!oTable){
            oTable = initTable();
        }else {
            oTable.ajax.reload();
        }
    });

    // //********  detail详情部分的js代码 ********
    // // 图片查看大图的插件的初始化
    // $('#audit_photo').viewer();
    // // 图片左旋转的点击事件
    // $(document).on('click','.rotation_left',function () {
    //     var img = $(this).siblings('img');
    //     angle = parseInt(img.attr('data-angle'));
    //     angle += 90;
    //     $(this).siblings('img').rotate(angle);
    //     img.attr('data-angle',angle);
    //     img.toggleClass('max');
    // });
    // // 图片右旋转的点击事件
    // $(document).on('click','.rotation_right',function () {
    //     var img = $(this).siblings('img');
    //     angle = parseInt(img.attr('data-angle'));
    //     angle -= 90;
    //     $(this).siblings('img').rotate(angle);
    //     img.attr('data-angle',angle);
    //     img.toggleClass('max');
    // });
    // /*审核图片部分img的宽高相等*/
    // var imgs = $('img');
    // for(var i=0;i<imgs.length;i++){
    //     var img_width = imgs[i].width;
    //     imgs[i].height = img_width;
    // }
    //
    // /*
    // 二级联动，图片审核备注信息的内容对应关系，
    // content_1为一级显示给用户的，
    // content_2为用户选择一级选项后对应的二级选项；
    // content_3为用户选择二级选项后，需要追加到审核备注的对应的内容
    //  */
    // var one = $('.audit_sug_1');
    // var two = $('.audit_sug_2');
    // var content_1 = ['请选择','身份证照片','营业执照','店铺内景照片，店铺外景照片','开户许可证','银行卡正面','授权书照片','连锁店说明','手持签名照','通道进件失败'];
    // var content_2 = [
    //     ['请选择'],
    //     ['请选择','身份证名称填写错误（小微）','身份证号码填写错误','无申请人身份证照（小微）','无申请人身份证照（提补充证件）','身份证已过期（重提身份证）',
    //     '身份证已过期（提补充证件）','身份证照片不清晰','身份证照片不完整','身份证照片非证件原件','身份证正、反面非同一证件','身份证件已入网不可重复入网',
    //     '证件疑似作假','无法人身份证照片','无被授权人身份证照片','手持身份证合照不清楚','无实际申请人合照','手持身份证合照不合规','身份证名称系统不支持（带点）',
    //     '身份证件非大陆人申请系统-不支持','身份证件非大陆人申请系统-支持'],
    //     ['请选择','营业执照公司名称错误','营业执照法人名称错误','营业执照号错误','营业执照模糊','开通刷卡-无营业执照','商户类型选择错误','无营业执照'],
    //     ['请选择','内外景非原件','内外景无法体现经营项目','无外景照片','无内景照片','内外景非同一场所','内外景无法判断公司类型','无法体现经营项目',
    //     '收据名称不符合填写规范','收据名称与店铺门头不一致','小微商户，收据名称不可含“公司”字样'],
    //     ['请选择','开户许可证模糊、缺失','开户许可证账号错误'],
    //     ['请选择','账户名错误','卡号错误','收款账户名格式系统不支持','开户行信息错误'],
    //     ['请选择','无授权书照片','授权书模糊','授权书非此申请人信息'],
    //     ['请选择','无连锁店说明照片','连锁店说明模糊'],
    //     ['请选择','非申请人手写签名、未提供签名照'],
    //     ['请选择','账户信息银行验证失败']
    // ];
    // var content_3 = [
    //     ['请选择'],
    //     ['请选择','店主姓名填写有误(请确保填写的与申请人身份证中姓名一致、无错别字);','身份证号填写有误（请确认是否为申请人的或是否有错位，若以公司或个体注册时请填写法人的身份证号）;',
    //         '无申请人身份证照片，请重新提供有效期内的二代身份证正反面照片（要求证件拍摄完整，露出四角边缘、无反光，字迹清晰，字迹完整，不可翻拍图片）;',
    //         '提供驾驶证、社保卡、市民证、护照等资质中的任意一种时，还同时需要提供有效期内的二代身份证正反面或临时身份证正反面照片或户口本中申请人本人信息页照片;',
    //         '身份证已过期，请提供有效期内的二代身份证正反面照片（要求证件拍摄完整，露出四角边缘、无反光，字迹清晰，字迹完整，不可翻拍图片）;',
    //         '身份证已过期，方式一：请提供有效期内的二代身份证正反面照片；方式二：提供户口簿本人信息页、有效期的临时身份证、驾驶证、社保卡、市民卡、护照签证、港澳台通行证中任意一种作为辅助证明;',
    //         '身份证正、反面照片不清晰，请重新提供清晰的身份证照片（要求证件拍摄完整，露出四角边缘、无反光，字迹清晰，字迹完整，不可翻拍图片）;',
    //         '身份证正、反面照片拍摄不完整，请重新提供清晰的身份证照片（要求证件拍摄完整，露出四角边缘、无反光，字迹清晰，字迹完整，不可翻拍图片）;',
    //         '请提供申请人身份证正反面“原件”照片（不可提供复印件或翻拍图片）;',
    //         '申请人身份证非同一身份证的正反面照片，请业务员核实后再提交（要求证件拍摄完整，露出四角边缘、无反光，字迹清晰，字迹完整，不可翻拍图片）;',
    //         '同一个身份证只能注册一个账户，重复申请，拒绝入网;',
    //         '入网资料疑似作假，审核拒绝;',
    //         '无法人身份证正反面照片，请提供（要求证件拍摄完整，露出四角边缘、无反光，字迹清晰，字迹完整，不可翻拍图片）;',
    //         '无被授权人身份证正反面照片，请提供（要求证件拍摄完整，露出四角边缘、无反光，字迹清晰，字迹完整，不可翻拍图片）;',
    //         '申请人照片不清晰，请重新提供申请人手持本人身份证在实际经营店铺收银台内拍摄的清晰的大范围合影照片（请拍正面照片,申请人请勿美颜、带帽、墨镜、口罩、侧脸、翻拍图片）;',
    //         '无实际申请人，请重新提供申请人手持本人身份证在实际经营店铺收银台内拍摄的清晰的大范围合影照片（请拍正面照片,申请人请勿美颜、带帽、墨镜、口罩、侧脸、翻拍图片）;',
    //         '无法判断申请人与身份证为同一人，请重新提供申请人手持本人身份证在实际经营店铺收银台内拍摄的清晰的大范围合影照片（请拍正面照片,申请人请勿美颜、带帽、墨镜、口罩、侧脸）;',
    //         '系统暂不支持姓名中带点的注册，请换申请人注册;',
    //         '系统暂不支持非大陆18位身份证号的注册，请换申请人注册；',
    //         '请提供有效期内的港澳台通行证或内地居留证件（要求证件拍摄完整，露出四角边缘、无反光，字迹清晰，字迹完整，不可翻拍图片）;'],
    //         ['请选择','公司名称与营业执照名称不一致(请确保填写的无错别字、不少字、多字)，请修改;',
    //         '法人姓名，与营业执照法人名称不一致(请确保填写的无错别字)，请修改;',
    //         '营业执照号填写有误（请优先填写执照上的社会信用统一代码，如果无则填写营业执照注册号）;',
    //         '营业执照不清晰，请重新提供;',
    //         '[开通刷卡]请提供营业执照（必须与申请人相关，或与店铺信息相关的才可以）;',
    //         '提供执照时请根据执照类型按个体户或企业类型注册;',
    //         '以个体户或公司入网需要提供营业执照，请提供;'],
    //         ['请选择','提供的照片为截图或翻拍的，请重新提供实际拍摄的大范围店铺内、外景照片（不可只拍门头或特写）;',
    //          '所提交的照片资料无法体现经营内容（项目），请提供可体现的资料（包括不限于营业执照、进出货单据、宣传页、官网截图、发票、包含此店有关的库房信息等等）;',
    //          '请提供店铺的外部整体环境照片（如有门头需包含店铺门头或门牌号）;',
    //          '请提供店铺大范围的内景照片，需体现出实际经营项目;',
    //          '提供的店铺内景照片与外景照片非同一家店，请重新确认后提供资料;',
    //          '请提供此公司的大范围公司前台照片、公司内部照片;',
    //          '收据名称（店铺名称）、所提交资料均无法判断实际经营项目，请确认实际经营项目修改后提交复审;',
    //          '收据显示名称（店铺名称）错误，不要只填写申请人姓名、太宽泛或者无法判断经营项目的店铺名称,请参照签约宝中收据名称填写规范重新修改;',
    //          '收据名称（店铺名称）与提交的店铺照片门头名称不一致，请填写商户真实店铺门头名称，请核实后再提交;',
    //          '未提供营业执照，收据显示名称（店铺名称）不可带有“公司”字样，可写门头名称或个体户+申请人姓名+经营项目，若要收据显示名称为公司名称，需要提交该公司营业执照才可。'],
    //         ['请选择','请提供清楚的完整的开户许可证照片;',
    //          '入对公账号，银行账户名称应填写开户许可证中的名称，并请确认填写的卡号是否正确;'],
    //         ['请选择','开户名错误，入对私应与申请人身份证姓名保持一致，入对公应与营业执照上名称保持一致(请确保填写的无错别字)，请修改;',
    //          '填写的银行卡（账）号错误，请重新核实进行修改后提交;',
    //          '系统暂不支持姓名中带点的清算，请换申请人注册;',
    //          '开户银行信息错误，请联系发卡行客服确认正确的开户支行和12位数字的联行号（如果开户行无联行号，请咨询客服此开户行所属的上级分行，然后补件时选择此开户行所属的上级分行），进行修改后再提交复审，以免影响商户的正常清算，谢谢！;'],
    //         ['请选择','请选择','企业入对私账户（无论入法人还是非法人账户）、个体户入非法人对私均需提供关系证明（填写模板请咨询小Q），请填写完整后提供;',
    //          '关系证明不清楚，请提供清晰的;',
    //          '关系证明中填写内容非此申请人的，请确认正确性并重新填写正确后，提供清晰的;'],
    //         ['请选择','无连锁店说明照片，[连锁店统一收款]请在分店中上传分店说明;',
    //          '连锁店说明不清楚，请提供清晰的;'],
    //         ['请选择','请提供申请人手写签名照片（要求字迹清晰，字迹完整）;'],
    //         ['请选择','账户名、卡号、开户银行经银行验证失败，请核实后重新提交;']
    // ];
    // one.html("");
    // for(var i=0;i<content_1.length;i++){
    //     one.append("<option>"+content_1[i]+"</option>");
    // }
    // /*默认输出第一个对应的内容*/
    // for(var i=0;i<content_2[0].length;i++){
    //     two.append("<option>"+content_2[0][i]+"</option>");
    // }
    // /*定义onchange事件 根据index输出对应的内容*/
    // var firstIndex;
    // // 一级的change事件
    // one.change(function(){
    //     var index=this.selectedIndex;
    //     firstIndex = index;
    //     two.html("");
    //     for(var i=0;i<content_2[index].length;i++){
    //         two.append("<option>"+content_2[index][i]+"</option>");
    //     }
    // });
    // // 二级的change事件
    // two.change(function () {
    //     var index=this.selectedIndex;
    //     if(index == 0){
    //
    //     }else {
    //         var memo = content_3[firstIndex][index];
    //         $('#audit_memo').append("\n"+memo);
    //     }
    // });
    // // 下拉搜索列表的js MCC
    // $('#select_mcc').selectpicker({
    //     style: 'btn-inverse',
    //
    // });
    // // 下拉搜索列表的js 风控等级
    // $('#select_risk_level').selectpicker({
    //     style: 'btn-inverse',
    // });
    // //跟随定位框audit_sug_photo
    // $('.no_pass_btn').click(function () {
    //
    //     // var photo_type=this.data_photo_type;
    //     var index = 1;
    //     // if(photo_type == ''){
    //     //     index = 1;
    //     // }else if(photo_type == ''){
    //     //     index = 2
    //     // }else if(photo_type == ''){
    //     //     index = 3
    //     // }else if(photo_type == ''){
    //     //     index = 4
    //     // }else if(photo_type == ''){
    //     //     index = 5
    //     // }else if(photo_type == ''){
    //     //     index = 6
    //     // }else if(photo_type == ''){
    //     //     index = 7
    //     // }else if(photo_type == ''){
    //     //     index = 8
    //     // }else if(photo_type == ''){
    //     //     index = 9
    //     // }
    //
    //     $('.audit_sug_photo').html("");
    //     for(var i=0;i<content_2[index].length;i++){
    //         $('.audit_sug_photo').append("<option>"+content_2[index][i]+"</option>");
    //     }
    //     easyDialog.open({
    //         container : 'nopass_memo_div',
    //         follow : this,
    //         followX : -225,
    //         followY : 25
    //     });
    // });
    // //图片审核下拉框的关闭按钮点击事件，用于关闭下拉框
    // $('.photomemo_close_btn').click(function () {
    //     easyDialog.close();
    // });
    //
    // // 查看更多按钮的点击事件 身份证号更多
    // $('.card_more').click(function () {
    //     if(moreTable == null){
    //         moreTable = initMoreTable();
    //     }else {
    //         moreTable.destroy();
    //         moreTable = initMoreTable();
    //     }
    //
    //     $('#more_user').modal('show');
    // });
    // // 查看更多按钮的点击事件 关联店铺更多
    // $('.store_more').click(function () {
    //     if(moreTable == null){
    //         moreTable = initMoreTable();
    //     }else {
    //         moreTable.destroy();
    //         moreTable = initMoreTable();
    //     }
    //     $('#more_user').modal('show');
    // });
    // // 查看更多按钮的点击事件 银行卡更多
    // $('.bank_more').click(function () {
    //     if(moreTable == null){
    //         moreTable = initMoreTable();
    //     }else {
    //         moreTable.destroy();
    //         moreTable = initMoreTable();
    //     }
    //     $('#more_user').modal('show');
    // });
    // //图片审核下拉框的选择回调，关闭弹框和审核备注中内容的追加
    // $('.audit_sug_photo').change(function () {
    //     var index=this.selectedIndex;
    //     if(index == 0){
    //
    //     }else {
    //         var memo = content_3[1][index];
    //         $('#audit_memo').append("\n"+memo);
    //     }
    //     easyDialog.close();
    // });
    // // 通道进件结果备注信息的内容对应关系，chnl_memo_content1为显示给用户的，chnl_memo_content2为用户选择后对应其选择需要追加到审核备注中的内容
    // var chnl_memo_content1 = ['请选择','账户信息银行验证失败','收款人错误','预留手机号错误','银行卡错误'];
    // var chnl_memo_content2 = ['','账户名、卡号、开户银行经银行验证失败，请核实后重新提交;','填写的银行账户信息或收款人的身份证号有误，请检查确认后提交正确的信息进行复审；','填写的银行账户预留手机号有误，请检查确认后提交正确的信息进行复审；','填写的银行账户信息无效（可能已注销、挂失、未启用、暂不支持的银行卡等等），请换一张收款银行卡信息，填写后提交复审；']
    // // 通道审核备注按钮点击事件
    // $('#chnl_memo').click(function () {
    //     $('.chnl_memo_select').html('');
    //     for(var i=0;i<chnl_memo_content1.length;i++){
    //         $('.chnl_memo_select').append("<option>"+chnl_memo_content1[i]+"</option>");
    //     }
    //     easyDialog.open({
    //         container : 'chnl_memo_div',
    //         follow : this,
    //         followX : -225,
    //         followY : -35
    //     });
    // });
    // //关闭通道进件下拉框的点击事件
    // $('.chnl_memo_close_btn').click(function () {
    //     easyDialog.close();
    // });
    // //通道进件结果的下拉框的选择回调，关闭下拉框和审核备注中内容的追加
    // $('.chnl_memo_select').change(function () {
    //     var index=this.selectedIndex;
    //     if(index == 0){
    //
    //     }else {
    //         var memo = chnl_memo_content2[index];
    //         $('#audit_memo').append("\n"+memo);
    //     }
    //     easyDialog.close();
    // });
});



var oTable = null;
// 审核列表的datatables初始化
function initTable() {
    var table = $("#auditTable").DataTable({
        "paging": true,
        "pagingType": "full_numbers",
        "lengthMenu": [5, 10, 20, 50],
        "bDestory": true,
        "bLengthChange": true,
        "processing": true,
        "searching": false, //是否开启搜索
        "serverSide": true, //开启服务器获取数据
        "ajax": { // 获取数据
            "url": "/api/v1/register_auditList",
            "data": function (d) {
                d.uid_mobile = $('#uid_mobile').val();
                // d.gid = $('#groupid').val();
                d.gid = $('#groupid').selectpicker('val');
                d.src = $('#src').val();
                var chk_value =[];//定义一个数组
                $('input[name="manual_status"]:checked').each(function(){//遍历每一个名字为interest的复选框，其中选中的执行函数
                    chk_value.push($(this).val());//将选中的值添加到数组chk_value中
                });
                var statusString = JSON.stringify(chk_value);
                d.manual_status = statusString;
            },
            "type": "POST",
            "dataType": "json" //返回来的数据形式
        },
        "columns": [ //定义列数据来源
            {'title': "用户ID", 'data': "userid"},
            {'title': "签约实体", 'data': "name"},
            {'title': "商户类型", 'data': null},
            {'title': "收据名称", 'data': "nickname"},
            {'title': "MCC", 'data': "mcc"},
            {'title': "渠道", 'data': "channel_name"},
            {'title': "业务员", 'data': "salesmanname"},
            {'title': "用户来源", 'data': "src"},
            {'title': "审核状态", 'data': null},
            {'title': "门店类型", 'data': "shoptype"},
            {'title': "操作", 'data': null, 'class': "align-center"} // 自定义列
        ],
        "columnDefs": [ //自定义列
            {
                "targets": 0,
//                        "width":"900px"
            },
            {
                "targets": 2, //改写哪一列
                "data": "",
                "render": function (data, type, row) {
                    var username;
                    if (row.usertype == 1){
                        username = '小微';
                    }else if (row.usertype == 2){
                        username = '个体工商户';
                    }else if (row.usertype == 3){
                        username = '企业';
                    }else {
                        username = '--';
                    }
                    var htmlStr = "<label>"+ username +"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": 8, //改写哪一列
                "data": "",
                "render": function (data, type, row) {
                    var manual_status_name;
                    if (row.manual_status == 1){
                        manual_status_name = '待审核'
                    }else if (row.manual_status == 2){
                        manual_status_name = '审核中'
                    }else if (row.manual_status == 3){
                        manual_status_name = '审核失败'
                    }else if (row.manual_status == 4){
                        manual_status_name = '审核成功'
                    }else if (row.manual_status == 5){
                        manual_status_name = '审核拒绝'
                    }else {
                        manual_status_name = '--'
                    }
                    var htmlStr = "<label>"+ manual_status_name +"</label>";
                    return htmlStr;
                }
            },
            {
                "targets": -1, //改写哪一列
                "data": "",
                "render": function (data, type, row) {
                    console.log(row.id.toString());
                    var htmlStr = "<button class='btn btn-primary' data-action='audit' data-toggle='modal' data-target='#modal' data-id=" + row.userid + " data-aid=" + row.id + "><span class='fa fa-pencil-square-o' aria-hidden='true'></span>审核</button>";
                    return htmlStr;
                }
            },
            {
                "targets": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
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

// var moreTable = null;
// // 更多查询时弹出的datatables的初始化
// function initMoreTable() {
//     var table = $("#moreRelationTable").DataTable({
//         "paging": true,
//         "pagingType": "full_numbers",
//         "lengthMenu": [20],
//         "bDestory": true,
//         "bLengthChange": false,
//         "processing": true,
//         "searching": false, //是否开启搜索
//         "serverSide": false, //开启服务器获取数据
//         "ajax": { // 获取数据
//             "url": "/api/v1/",
//             "data": function (d) {
//
//             },
//             "type": "GET",
//             "dataType": "json" //返回来的数据形式
//         },
//         "columns": [ //定义列数据来源
//             {'title': "用户ID", 'data': ""},
//             {'title': "收据显示名称", 'data': ""},
//             {'title': "MCC", 'data': ""},
//             {'title': "费率信息", 'data': ""},
//             {'title': "所属渠道", 'data': ""},
//             {'title': "用户状态", 'data': ""},
//             {'title': "最近交易", 'data': ""},
//             {'title': "审核状态", 'data': ""},
//             {'title': "经营省市", 'data': ""},
//             {'title': "门店类型", 'data': ""},
//         ],
//         "columnDefs": [ //自定义列
//             {
//                 "targets": 0,
// //                        "width":"900px"
//             },
//             {
//                 "targets": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
//                 "orderable": false  //禁止排序
//             }
//         ],
//         "language": { // 定义语言
//             "sProcessing": "加载中...",
//             "sLengthMenu": "每页显示 _MENU_ 条记录",
//             "sZeroRecords": "没有匹配的结果",
//             "sInfo": "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
//             "sInfoEmpty": "显示第 0 至 0 项结果，共 0 项",
//             "sInfoFiltered": "(由 _MAX_ 项结果过滤)",
//             "sInfoPostFix": "",
//             "sSearch": "搜索:",
//             "sUrl": "",
//             "sEmptyTable": "表中数据为空",
//             "sLoadingRecords": "载入中...",
//             "sInfoThousands": ",",
//             "oPaginate": {
//                 "sFirst": "首页",
//                 "sPrevious": "上一页",
//                 "sNext": "下一页",
//                 "sLast": "末页"
//             },
//             "oAria": {
//                 "sSortAscending": ": 以升序排列此列",
//                 "sSortDescending": ": 以降序排列此列"
//             }
//         }
//     });
//     return table;
// }