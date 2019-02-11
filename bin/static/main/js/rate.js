/**
 * Created by qfpay on 2017/10/16.
 */
var oTable = null;
var historyTable = null;
var rate_bid = null;
function initTable() {
    var table = $("#rateTable").DataTable({
        "paging": true,
        "pagingType": "full_numbers",
        "lengthMenu": [10, 20],
        "processing": true,
        "searching": true, //是否开启搜索
        "serverSide": false, //开启服务器获取数据
                  // "order": [[ 0, "desc" ]],//默认排序
        "ajax": { // 获取数据
            "url": "/api/v1/rate",
            "data": function (d) {
                // d.role = rate_bid;
            },
            "type": "GET",
            "dataType": "json" //返回来的数据形式
        },
        //
        "columns": [ //定义列数据来源
            {'title': "基准货币", 'data': "base_currency"},
            {'title': "外币", 'data': "foreign_currency"},
            {'title': "兑换单位", 'data': "unit"},
            {'title': "汇率", 'data': "rate"},
            {'title': "更新时间", 'data': "utime"},
            {'title': "汇率来源", 'data': "src"},
            {'title': "备注", 'data': "comments"},
            {'title': "操作人", 'data': "operator"},
            {'title': "操作", 'data': null},
            {'title': "历史记录", 'data': null},

            // {'title': "ID", 'data': "id"},
            // {'title': "角色", 'data': "name"},
            // {'title': "更新时间", 'data': "utime"},
            // {'title': "操作", 'data': null, 'class': "align-center"} // 自定义列
        ],
        "columnDefs": [ //自定义列
            {
                "targets": -1, //改写哪一列
                "data": "id",
                "render": function (data, type, row) {

                    var htmlStr = "<button class='btn btn-primary' data-action='history' data-id="+row.id+" data-toggle='modal' data-target=''>查看历史</button>";
                    return htmlStr;
                }
            },
            {
                "targets": -2, //改写哪一列
                "data": "id",
                "render": function (data, type, row) {
                    var htmlStr = "<button class='btn btn-primary' data-action='edit' data-id="+row.id+" data-base_currency="+row.base_currency+" data-foreign_currency="+row.foreign_currency+" data-unit="+row.unit+" data-rate="+row.rate+" data-rate_resources="+row.src+" data-comments="+row.comments+" data-toggle='modal' data-target=''>编辑</button>";
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
        },
        "createdRow": function (row, data, index) {
            //行回调函数
        }
    });
    return table;
}
function initHistoryTable() {
    var table = $("#history_table").DataTable({
        "paging": true,
        "bDestory": true,
        "bLengthChange": false,
        "pagingType": "full_numbers",
        "bSort": false,
        "lengthMenu": [10, 20],
        "processing": true,
        "searching": false, //是否开启搜索
        "serverSide": false, //开启服务器获取数据
                  // "order": [[ 0, "desc" ]],//默认排序
        "ajax": { // 获取数据
            "url": "/api/v1/rate_history",
            "data": function (d) {
                d.bid = rate_bid;
            },
            "type": "GET",
            "dataType": "json" //返回来的数据形式
        },
        //
        "columns": [ //定义列数据来源
            {'title': "基准货币", 'data': "base_currency"},
            {'title': "外币", 'data': "foreign_currency"},
            {'title': "兑换单位", 'data': "unit"},
            {'title': "汇率", 'data': "rate"},
            {'title': "更新时间", 'data': "utime"},
            {'title': "汇率来源", 'data': "src"},
            {'title': "备注", 'data': "comments"},
            {'title': "操作人", 'data': "operator"},

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
        },
        "createdRow": function (row, data, index) {
            //行回调函数
        }
    });
    return table;
}

function checkNum(obj) {
    //检查是否是非数字值
    if (isNaN(obj.value)) {
        obj.value = "";
    }
    if (obj != null) {
        //检查小数点后是否对于两位
        if (obj.value.toString().split(".").length > 1 && obj.value.toString().split(".")[1].length > 4) {
            toastr.warning("小数点后不能多于四位 ！");
            obj.value = "";
        }
    }
};


$(function () {

   oTable = initTable();
   historyTable = initHistoryTable();
   original_rate = '';
   ori_base_currency = '';
   ori_foreign_currency = '';
    //新建按钮点击事件
    $("#create").click(function () {
       original_rate = '';
       ori_base_currency = '';
       ori_foreign_currency = '';
       $("#create_confirm").attr('data-savetype','0');
       $("#myModalLabel").text('新建汇率');
       $("#rate_id").val('');
       $("#base_currency").val('');
       $("#foreign_currency").val('');
       $("#rate").val('');
       $("#unit").val('100');
       $("#rate_resources").val('');
       $("#comments").val('');
       $("#myCreate").modal('show');
    });

   //修改按钮的点击事件
   $(document).on('click',"[data-action='edit']",function () {
       original_rate = this.dataset.rate.replace(/\s+/g,"");
       ori_base_currency = this.dataset.base_currency.replace(/\s+/g,"");
       ori_foreign_currency = this.dataset.foreign_currency.replace(/\s+/g,"");
       $("#create_confirm").attr('data-savetype','1');
       $("#myModalLabel").text('修改汇率');
       $("#rate_id").val(this.dataset.id);
       $("#base_currency").val(this.dataset.base_currency);
       $("#foreign_currency").val(this.dataset.foreign_currency);
       $("#rate").val(this.dataset.rate);
       $("#unit").val(this.dataset.unit);
       $("#rate_resources").val(this.dataset.rate_resources);
       $("#comments").val(this.dataset.comments);
       $('#myCreate').modal('show');
   });

   // 查看历史
   $(document).on('click',"[data-action='history']",function () {
       // historyTable = initHistoryTable();
       // $.ajax({
       //     async: false,
       //     dataType: 'json',
       //     url: '/api/v1/rate_history',
       //     data: {
       //          bid: this.dataset.id
       //      },
       //     type: 'GET',
       //     success: function (result) {
       //         if (result && result.ok){
       //             toastr.success(result.msg);
       //             $('#myCreate').modal('hide');
       //             oTable.ajax.reload();
       //         }else {
       //             toastr.warning(result.msg);
       //         }
       //     },
       //     error: function (msg) {
       //         toastr.error(msg);
       //     }
       // });
       rate_bid = this.dataset.id;

       historyTable.ajax.reload();
       $("#history_modal").modal('show');
   });
   //新建modal的确认提交按钮的事件
   $("#create_confirm").click(function () {
       base_currency = $("#base_currency").val().replace(/\s+/g,"");
       if (base_currency.length == 0){
           toastr.warning('请输入基础货币 ！');
           return;
       }
       if (base_currency.length > 20){
           toastr.warning('请输入20个字符以内的基础货币标识符 ！');
           return;
       }
       foreign_currency = $("#foreign_currency").val().replace(/\s+/g,"");
       if (foreign_currency.length == 0){
           toastr.warning('请输入外币 ！');
           return;
       }
       if (foreign_currency.length > 20){
           toastr.warning('请输入20个字符以内的外币标识符 ！');
           return;
       }
       rateStr = $("#rate").val().replace(/\s+/g,"");
       if (rateStr.length == 0){
           toastr.warning('请输入汇率 ！');
           return;
       }
       unit = $("#unit").val().replace(/\s+/g,"");
       if (unit.length == 0){
           toastr.warning('请输入兑换单位 ！');
           return;
       }
       if (unit.length > 9){
           toastr.warning('请输入9位以内的兑换单位数值 ！');
           return;
       }
       rate_resources = $("#rate_resources").val().replace(/\s+/g,"");
       if (rate_resources.length == 0){
           toastr.warning('请输入汇率来源 ！');
           return;
       }
       if (rate_resources.length > 20){
           toastr.warning('请输入20个字符以内的汇率来源 ！');
           return;
       }
       comments = $("#comments").val().replace(/\s+/g,"");
       if (comments.length == 0){
           toastr.warning('请输入备注信息 ！');
           return;
       }
       if (comments.length > 50){
           toastr.warning('请输入50个字符以内的备注信息 ！');
           return;
       }

       if ($("#create_confirm").attr('data-savetype') == 1){

           result = Math.abs(parseFloat(rateStr) - parseFloat(original_rate))/parseFloat(original_rate);
           if (result >= 0.05){
               $("#five_al").show();
           }else {
               $("#five_al").hide();
           }

           $("#original_rate").val(original_rate);
           $("#changed_rate").val(rateStr);
           $("#mySure").modal('show');
       }else {
           var jsonData = {};
           jsonData.base_currency = base_currency;
           jsonData.foreign_currency = foreign_currency;
           jsonData.rate = rateStr;
           jsonData.unit = unit;
           jsonData.rate_resources = rate_resources;
           jsonData.comments = comments;

           $.ajax({
               async: false,
               dataType: 'json',
               url: '/api/v1/rate',
               type: 'POST',
               contentType: "application/json; charset=utf-8",
               data: JSON.stringify(jsonData),
               success: function (result) {
                   if (result && result.ok){
                       toastr.success(result.msg);
                       $('#myCreate').modal('hide');
                       oTable.ajax.reload();
                   }else {
                       toastr.warning(result.msg);
                   }
               },
               error: function (msg) {
                   toastr.error('操作失败 ！');
               }
           });
       }

   });

   //二次确认modal的取消按钮点击事件
   $("#sure_cancel").click(function () {
       $("#mySure").modal('hide');
   });

   //二次确认modal的确认按钮点击事件
   $("#sure_confirm").click(function () {

       base_currency = $("#base_currency").val().replace(/\s+/g,"");
       foreign_currency = $("#foreign_currency").val().replace(/\s+/g,"");
       rate = $("#rate").val().replace(/\s+/g,"");
       unit = $("#unit").val().replace(/\s+/g,"");
       rate_resources = $("#rate_resources").val().replace(/\s+/g,"");
       comments = $("#comments").val().replace(/\s+/g,"");
       rate_id = $("#rate_id").val();
       var jsonData = {};
       jsonData.ori_base_currency = ori_base_currency;
       jsonData.ori_foreign_currency = ori_foreign_currency;
       jsonData.rate_id = rate_id;
       jsonData.base_currency = base_currency;
       jsonData.foreign_currency = foreign_currency;
       jsonData.rate = rate;
       jsonData.unit = unit;
       jsonData.rate_resources = rate_resources;
       jsonData.comments = comments;
       $.ajax({
               async: true,
               dataType: 'json',
               url: '/api/v1/rate',
               type: 'PUT',
               contentType: "application/json; charset=utf-8",
               data: JSON.stringify(jsonData),
               success: function (result) {
                   if (result && result.ok){
                       toastr.success(result.msg);
                       $("#mySure").modal('hide');
                       $("#myCreate").modal('hide');
                       oTable.ajax.reload();
                   }else {
                       $("#mySure").modal('hide');
                       toastr.warning(result.msg);
                   }
               },
               error: function (result) {
                   $("#mySure").modal('hide');
                   toastr.error('操作失败 ！');
               }
       });
   });



});



$(function() {

    var currency_list = [
        {'fullname':'AED - 阿联酋迪拉姆（United Arab Emirates Dirham）','abbreviation':'AED'},
        {'fullname':'AFN - 阿富汗尼（Afghan Afghani）','abbreviation':'AFN'},
        {'fullname':'ALL - 阿尔巴尼列克（Albania Lek）','abbreviation':'ALL'},
        {'fullname':'AMD - 亚美尼亚德拉姆（Armenia Dram）','abbreviation':'AMD'},
        {'fullname':'ANG - 荷兰盾（Dutch Guilder）','abbreviation':'ANG'},
        {'fullname':'AOA - 安哥拉宽扎（Angola Kwanza）','abbreviation':'AOA'},
        {'fullname':'ARS - 阿根廷比索（Argentina Peso）','abbreviation':'ARS'},
        {'fullname':'AUD - 澳元（Australia Dollar）','abbreviation':'AUD'},
        {'fullname':'AWG - 阿鲁巴弗罗林（Aruba Florin）','abbreviation':'AWG'},
        {'fullname':'AZN - 阿塞拜疆马纳特（Azerbaijan Manat）','abbreviation':'AZN'},
        {'fullname':'BAM - 波黑可兑换马克（Bosnia Convertible Mark）','abbreviation':'BAM'},
        {'fullname':'BBD - 巴巴多斯元（Barbados Dollar）','abbreviation':'BBD'},
        {'fullname':'BDT - 孟加拉国塔卡（Bangladesh Taka）','abbreviation':'BDT'},
        {'fullname':'BGN - 保加利亚列弗（Bulgaria Lev）','abbreviation':'BGN'},
        {'fullname':'BHD - 巴林第纳尔（Bahrain Dinar）','abbreviation':'BHD'},
        {'fullname':'BIF - 布隆迪法郎（Burundi Franc）','abbreviation':'BIF'},
        {'fullname':'BMD - 百慕大元（Bermudian Dollar）','abbreviation':'BMD'},
        {'fullname':'BND - 文莱元（Brunei Dollar）','abbreviation':'BND'},
        {'fullname':'BOB - 玻利维亚诺（Bolivian Boliviano）','abbreviation':'BOB'},
        {'fullname':'BRL - 巴西雷亚尔（Brazilian Real）','abbreviation':'BRL'},
        {'fullname':'BSD - 巴哈马元（Bahamian Dollar）','abbreviation':'BSD'},
        {'fullname':'BTN - 不丹努扎姆（Bhutanese Ngultrum）','abbreviation':'BTN'},
        {'fullname':'BWP - 博茨瓦纳普拉（Botswana Pula ）','abbreviation':'BWP'},
        {'fullname':'BYR - 白俄罗斯卢布（Belarusian Ruble）','abbreviation':'BYR'},
        {'fullname':'BZD - 伯利兹元（Belize Dollar）','abbreviation':'BZD'},
        {'fullname':'CAD - 加元（Canadian Dollar）','abbreviation':'CAD'},
        {'fullname':'CDF - 刚果法郎（Congolese Franc）','abbreviation':'CDF'},
        {'fullname':'CHF - 瑞士法郎（Swiss Franc）','abbreviation':'CHF'},
        {'fullname':'CLF - 智利比索(基金)（Chilean Unidad de Fomento）','abbreviation':'CLF'},
        {'fullname':'CLP - 智利比索（Chilean Peso）','abbreviation':'CLP'},
        {'fullname':'CNH - 中国离岸人民币（Chinese Offshore Renminbi）','abbreviation':'CNH'},
        {'fullname':'CNY - 人民币（Chinese Yuan）','abbreviation':'CNY'},
        {'fullname':'COP - 哥伦比亚比索（Colombia Peso ）','abbreviation':'COP'},
        {'fullname':'CRC - 哥斯达黎加科朗（Costa Rica Colon）','abbreviation':'CRC'},
        {'fullname':'CUP - 古巴比索（Cuban Peso）','abbreviation':'CUP'},
        {'fullname':'CVE - 佛得角埃斯库多（Cape Verde Escudo）','abbreviation':'CVE'},
        {'fullname':'CYP - 塞普路斯镑（Cyprus Pound）','abbreviation':'CYP'},
        {'fullname':'CZK - 捷克克朗（Czech Republic Koruna）','abbreviation':'CZK'},
        {'fullname':'DEM - 德国马克（Deutsche Mark）','abbreviation':'DEM'},
        {'fullname':'DJF - 吉布提法郎（Djiboutian Franc）','abbreviation':'DJF'},
        {'fullname':'DKK - 丹麦克朗（Danish Krone）','abbreviation':'DKK'},
        {'fullname':'DOP - 多米尼加比索（Dominican Peso）','abbreviation':'DOP'},
        {'fullname':'DZD - 阿尔及利亚第纳尔（Algerian Dinar ）','abbreviation':'DZD'},
        {'fullname':'ECS - 厄瓜多尔苏克雷（Ecuadorian Sucre）','abbreviation':'ECS'},
        {'fullname':'EGP - 埃及镑（Egyptian Pound）','abbreviation':'EGP'},
        {'fullname':'ERN - 厄立特里亚纳克法（Eritrean Nakfa ）','abbreviation':'ERN'},
        {'fullname':'ETB - 埃塞俄比亚比尔（Ethiopian Birr）','abbreviation':'ETB'},
        {'fullname':'EUR - 欧元（Euro）','abbreviation':'EUR'},
        {'fullname':'FJD - 斐济元（Fiji Dollar）','abbreviation':'FJD'},
        {'fullname':'FKP - 福克兰群岛镑（Falkland Islands Pound）','abbreviation':'FKP'},
        {'fullname':'FRF - 法国法郎（French Franc）','abbreviation':'FRF'},
        {'fullname':'GBP - 英镑（British Pound）','abbreviation':'GBP'},
        {'fullname':'GEL - 格鲁吉亚拉里（Georgian Lari）','abbreviation':'GEL'},
        {'fullname':'GHS - 加纳塞地（Ghanaian Cedi）','abbreviation':'GHS'},
        {'fullname':'GIP - 直布罗陀镑（Gibraltar Pound）','abbreviation':'GIP'},
        {'fullname':'GMD - 冈比亚达拉西（Gambian Dalasi）','abbreviation':'GMD'},
        {'fullname':'GNF - 几内亚法郎（Guinean Franc）','abbreviation':'GNF'},
        {'fullname':'GTQ - 危地马拉格查尔（Guatemalan Quetzal）','abbreviation':'GTQ'},
        {'fullname':'GYD - 圭亚那元（Guyanese Dollar）','abbreviation':'GYD'},
        {'fullname':'HKD - 港币（Hong Kong Dollar）','abbreviation':'HKD'},
        {'fullname':'HNL - 洪都拉斯伦皮拉（Honduran Lempira）','abbreviation':'HNL'},
        {'fullname':'HRK - 克罗地亚库纳（Croatian Kuna）','abbreviation':'HRK'},
        {'fullname':'HTG - 海地古德（Haitian Gourde）','abbreviation':'HTG'},
        {'fullname':'HUF - 匈牙利福林（Hungarian Forint）','abbreviation':'HUF'},
        {'fullname':'IDR - 印度尼西亚卢比（Indonesian Rupiah）','abbreviation':'IDR'},
        {'fullname':'IEP - 爱尔兰镑（Irish Pound）','abbreviation':'IEP'},
        {'fullname':'ILS - 以色列新谢克尔（Israeli New Shekel）','abbreviation':'ILS'},
        {'fullname':'INR - 印度卢比（Indian Rupee）','abbreviation':'INR'},
        {'fullname':'IQD - 伊拉克第纳尔（Iraqi Dinar）','abbreviation':'IQD'},
        {'fullname':'IRR - 伊朗里亚尔（Iranian Rial）','abbreviation':'IRR'},
        {'fullname':'ISK - 冰岛克郎（Icelandic Krona）','abbreviation':'ISK'},
        {'fullname':'ITL - 意大利里拉（Italian Lira）','abbreviation':'ITL'},
        {'fullname':'JMD - 牙买加元（Jamaican Dollar）','abbreviation':'JMD'},
        {'fullname':'JOD - 约旦第纳尔（Jordanian Dinar）','abbreviation':'JOD'},
        {'fullname':'JPY - 日元（Japanese Yen）','abbreviation':'JPY'},
        {'fullname':'KES - 肯尼亚先令（Kenyan Shilling）','abbreviation':'KES'},
        {'fullname':'KGS - 吉尔吉斯斯坦索姆（Kyrgyzstani Som）','abbreviation':'KGS'},
        {'fullname':'KHR - 柬埔寨瑞尔（Cambodian Riel）','abbreviation':'KHR'},
        {'fullname':'KMF - 科摩罗法郎（Comorian franc）','abbreviation':'KMF'},
        {'fullname':'KPW - 朝鲜元（North Korean Won）','abbreviation':'KPW'},
        {'fullname':'KRW - 韩元（South Korean Won）','abbreviation':'KRW'},
        {'fullname':'KWD - 科威特第纳尔（Kuwaiti Dinar）','abbreviation':'KWD'},
        {'fullname':'KYD - 开曼群岛元（Cayman Islands Dollar）','abbreviation':'KYD'},
        {'fullname':'KZT - 哈萨克斯坦坚戈（Kazakstani Tenge）','abbreviation':'KZT'},
        {'fullname':'LAK - 老挝基普（Lao kip）','abbreviation':'LAK'},
        {'fullname':'LBP - 黎巴嫩镑（Lebanese Pound）','abbreviation':'LBP'},
        {'fullname':'LKR - 斯里兰卡卢比（Sri Lankan Rupee）','abbreviation':'LKR'},
        {'fullname':'LRD - 利比里亚元（Liberian dollar）','abbreviation':'LRD'},
        {'fullname':'LSL - 莱索托洛蒂（Lesotho Loti）','abbreviation':'LSL'},
        {'fullname':'LTL - 立陶宛立特（Lithuanian Litas）','abbreviation':'LTL'},
        {'fullname':'LVL - 拉脱维亚拉特（Latvian Lats）','abbreviation':'LVL'},
        {'fullname':'LYD - 利比亚第纳尔（Libyan Dinar）','abbreviation':'LYD'},
        {'fullname':'MAD - 摩洛哥迪拉姆（Moroccan Dirham）','abbreviation':'MAD'},
        {'fullname':'MDL - 摩尔多瓦列伊（Moldovan Leu）','abbreviation':'MDL'},
        {'fullname':'MGA - 马达加斯加阿里亚里（Malagasy Ariary）','abbreviation':'MGA'},
        {'fullname':'MKD - 马其顿代纳尔（Macedonian Denar）','abbreviation':'MKD'},
        {'fullname':'MMK - 缅甸元（Myanmar Kyat）','abbreviation':'MMK'},
        {'fullname':'MNT - 蒙古图格里克（Mongolian Tugrik）','abbreviation':'MNT'},
        {'fullname':'MOP - 澳门元（Macau Pataca）','abbreviation':'MOP'},
        {'fullname':'MRO - 毛里塔尼亚乌吉亚（Mauritania Ouguiya）','abbreviation':'MRO'},
        {'fullname':'MUR - 毛里求斯卢比（Mauritian Rupee）','abbreviation':'MUR'},
        {'fullname':'MVR - 马尔代夫拉菲亚（Maldives Rufiyaa）','abbreviation':'MVR'},
        {'fullname':'MWK - 马拉维克瓦查（Malawian Kwacha）','abbreviation':'MWK'},
        {'fullname':'MXN - 墨西哥比索（Mexican Peso）','abbreviation':'MXN'},
        {'fullname':'MXV - 墨西哥(资金)（Mexican Unidad De Inversion）','abbreviation':'MXV'},
        {'fullname':'MYR - 林吉特（Malaysian Ringgit）','abbreviation':'MYR'},
        {'fullname':'MZN - 莫桑比克新梅蒂卡尔（New Mozambican Metical）','abbreviation':'MZN'},
        {'fullname':'NAD - 纳米比亚元（Namibian Dollar）','abbreviation':'NAD'},
        {'fullname':'NGN - 尼日利亚奈拉（Nigerian Naira）','abbreviation':'NGN'},
        {'fullname':'NIO - 尼加拉瓜新科多巴（Nicaraguan Cordoba Oro）','abbreviation':'NIO'},
        {'fullname':'NOK - 挪威克朗（Norwegian Krone）','abbreviation':'NOK'},
        {'fullname':'NPR - 尼泊尔卢比（Nepalese Rupee）','abbreviation':'NPR'},
        {'fullname':'NZD - 新西兰元（New Zealand Dollar）','abbreviation':'NZD'},
        {'fullname':'OMR - 阿曼里亚尔（Omani Rial）','abbreviation':'OMR'},
        {'fullname':'PAB - 巴拿马巴波亚（Panamanian Balboa）','abbreviation':'PAB'},
        {'fullname':'PEN - 秘鲁新索尔（Peruvian Nuevo Sol）','abbreviation':'PEN'},
        {'fullname':'PGK - 巴布亚新几内亚基那（Papua New Guinea Kina）','abbreviation':'PGK'},
        {'fullname':'PHP - 菲律宾比索（Philippine Peso）','abbreviation':'PHP'},
        {'fullname':'PKR - 巴基斯坦卢比（Pakistan Rupee）','abbreviation':'PKR'},
        {'fullname':'PLN - 波兰兹罗提（Polish Zloty）','abbreviation':'PLN'},
        {'fullname':'PYG - 巴拉圭瓜拉尼（Paraguayan Guarani）','abbreviation':'PYG'},
        {'fullname':'QAR - 卡塔尔里亚尔（Qatari Riyal）','abbreviation':'QAR'},
        {'fullname':'RON - 罗马尼亚列伊（Romanian Leu）','abbreviation':'RON'},
        {'fullname':'RSD - 塞尔维亚第纳尔（Serbian Dinar）','abbreviation':'RSD'},
        {'fullname':'RUB - 俄罗斯卢布（Russian Ruble）','abbreviation':'RUB'},
        {'fullname':'RWF - 卢旺达法郎（Rwandan Franc）','abbreviation':'RWF'},
        {'fullname':'SAR - 沙特里亚尔（Saudi Arabian Riyal）','abbreviation':'SAR'},
        {'fullname':'SBD - 所罗门群岛元（Solomon Islands Dollar）','abbreviation':'SBD'},
        {'fullname':'SCR - 塞舌尔卢比（Seychelles Rupee）','abbreviation':'SCR'},
        {'fullname':'SDG - 苏丹磅（Sudanese Pound）','abbreviation':'SDG'},
        {'fullname':'SEK - 瑞典克朗（Swedish Krona）','abbreviation':'SEK'},
        {'fullname':'SGD - 新加坡元（Singapore Dollar）','abbreviation':'SGD'},
        {'fullname':'SHP - 圣赫勒拿镑（Saint Helena Pound）','abbreviation':'SHP'},
        {'fullname':'SIT - 斯洛文尼亚托拉尔（Slovenian Tolar）','abbreviation':'SIT'},
        {'fullname':'SLL - 塞拉利昂利昂（Sierra Leonean Leone）','abbreviation':'SLL'},
        {'fullname':'SOS - 索马里先令（Somali Shilling）','abbreviation':'SOS'},
        {'fullname':'SRD - 苏里南元（Suriname Dollar）','abbreviation':'SRD'},
        {'fullname':'STD - 圣多美多布拉（Sao Tome Dobra）','abbreviation':'STD'},
        {'fullname':'SVC - 萨尔瓦多科朗（Salvadoran Colon）','abbreviation':'SVC'},
        {'fullname':'SYP - 叙利亚镑（Syrian Pound）','abbreviation':'SYP'},
        {'fullname':'SZL - 斯威士兰里兰吉尼（Swazi Lilangeni）','abbreviation':'SZL'},
        {'fullname':'THB - 泰铢（Thai Baht）','abbreviation':'THB'},
        {'fullname':'TJS - 塔吉克斯坦索莫尼（Tajikistan Somoni）','abbreviation':'TJS'},
        {'fullname':'TMT - 土库曼斯坦马纳特（Turkmenistan Manat）','abbreviation':'TMT'},
        {'fullname':'TND - 突尼斯第纳尔（Tunisian Dinar）','abbreviation':'TND'},
        {'fullname':'TOP - 汤加潘加（Tongan Pa Anga）','abbreviation':'TOP'},
        {'fullname':'TRY - 土耳其里拉（Turkish Lira）','abbreviation':'TRY'},
        {'fullname':'TTD - 特立尼达多巴哥元（Trinidad and Tobago Dollar）','abbreviation':'TTD'},
        {'fullname':'TWD - 新台币（New Taiwan Dollar）','abbreviation':'TWD'},
        {'fullname':'TZS - 坦桑尼亚先令（Tanzanian Shilling）','abbreviation':'TZS'},
        {'fullname':'UAH - 乌克兰格里夫纳（Ukrainian Hryvnia）','abbreviation':'UAH'},
        {'fullname':'UGX - 乌干达先令（Ugandan Shilling）','abbreviation':'UGX'},
        {'fullname':'USD - 美元（United States Dollar）','abbreviation':'USD'},
        {'fullname':'UYU - 乌拉圭比索（Uruguayan Peso）','abbreviation':'UYU'},
        {'fullname':'UZS - 乌兹别克斯坦苏姆（Uzbekistani Som）','abbreviation':'UZS'},
        {'fullname':'VEF - 委内瑞拉玻利瓦尔（Venezuelan Bolivar Fuerte）','abbreviation':'VEF'},
        {'fullname':'VND - 越南盾（Viet Nam Dong）','abbreviation':'VND'},
        {'fullname':'VUV - 瓦努阿图瓦图（Vanuatu Vatu）','abbreviation':'VUV'},
        {'fullname':'WST - 萨摩亚塔拉（Samoa Tala）','abbreviation':'WST'},
        {'fullname':'XAF - 中非法郎（Central African CFA Franc）','abbreviation':'XAF'},
        {'fullname':'XAG - 银价盎司（Ounces of Silver）','abbreviation':'XAG'},
        {'fullname':'XAU - 金价盎司（Ounces of Gold）','abbreviation':'XAU'},
        {'fullname':'XCD - 东加勒比元（East Caribbean Dollar）','abbreviation':'XCD'},
        {'fullname':'XCP - 铜价盎司（Ounces of Copper）','abbreviation':'XCP'},
        {'fullname':'XDR - IMF特别提款权（IMF Special Drawing Rights）','abbreviation':'XDR'},
        {'fullname':'XOF - 西非法郎（West African CFA）','abbreviation':'XOF'},
        {'fullname':'XPD - 钯价盎司（Ounces of Palladium）','abbreviation':'XPD'},
        {'fullname':'XPF - 太平洋法郎（French Pacific Franc）','abbreviation':'XPF'},
        {'fullname':'XPT - 珀价盎司（Ounces of Platinum）','abbreviation':'XPT'},
        {'fullname':'YER - 也门里亚尔（Yemeni Rial）','abbreviation':'YER'},
        {'fullname':'ZAR - 南非兰特（South African Rand）','abbreviation':'ZAR'},
        {'fullname':'ZMW - 赞比亚克瓦查（Zambian Kwacha）','abbreviation':'ZMW'},
        {'fullname':'ZWL - 津巴布韦元（Zimbabwean Dollar）','abbreviation':'ZWL'},
        ]
    // $('#foreign_currency_select').html('');
    $.each(currency_list,function (i,item) {
        $('#foreign_currency_select').append("<option value='"+ item.abbreviation +"'>"+ item.abbreviation +"</option>");
    });
    $('#foreign_currency_select').comboSelect();
    $('#foreign_currency_div').children('.combo-select').children('input').attr('id','foreign_currency');


    $.each(currency_list,function (i,item) {
        $('#base_currency_select').append("<option value='"+ item.abbreviation +"'>"+ item.abbreviation +"</option>");
        console.log(item.fullname);
    });
    $('#base_currency_select').comboSelect();
    $('#base_currency_div').children('.combo-select').children('input').attr('id','base_currency');
});