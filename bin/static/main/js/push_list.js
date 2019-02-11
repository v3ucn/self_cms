/**
 * Created by qfpay on 2017/10/16.
 */
var oTable = null;
var historyTable = null;
var rate_bid = null;
var push_save = null;

function initTable() {
    var table = $("#push_listTable").DataTable({
        "paging": true,
        "pagingType": "full_numbers",
        "lengthMenu": [10, 20],
        "processing": true,
        "bAutoWidth" : true,
        "searching": true, //是否开启搜索
        "serverSide": false, //开启服务器获取数据
                  // "order": [[ 0, "desc" ]],//默认排序
        "ajax": { // 获取数据
            "url": "/push_list_api",
            "data": function (d) {
                // d.role = rate_bid;
            },
            "type": "GET",
            "dataType": "json" //返回来的数据形式
        },
        "order": [[12, "desc" ]],
        //
        "columns": [ //定义列数据来源
            {'title': "消息类别", 'data':null},
            {'title': "平台", 'data': "platforms"},
            {'title': "Apptype", 'data': "apptypes"},
            {'title': "标题", 'data': "title"},
            {'title': "内容", 'data': "content"},
            {'title': "链接", 'data': "link"},
            {'title': "用户id", 'data': null},
            {'title': "是否跳转", 'data': "actiontype"},
            {'title': "推送方式", 'data': "mode_str"},
            {'title': "一级标签", 'data': "tag_type_str"},
            {'title': "推送确认", 'data': "status"},

            // {'title': "关联对象id", 'data': "ref_id"},
            // {'title': "关联对象类型", 'data': "ref_type"},
            {'title': "关联对象名称", 'data': "ref_title"},
            {'title': "创建时间", 'data': "create_time"},
            {'title': "操作", 'data':null}

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

                    if(row.ref_title == ''){


                        var _zhi = "''";

                    }else{


                        var _zhi = row.ref_title;

                    }

                    _zhi = encodeURIComponent(_zhi);

                    var htmlStr = "<button class='btn btn-primary' data-tag_type='"+row.tag_type+"' data-action='push' data-ref_title="+_zhi+" data-id="+row.id+" data-mode="+row.mode+"  data-platforms="+row.platforms+" data-apptypes="+row.apptypes+" data-title="+row.title+" data-content="+encodeURIComponent(row.content)+"  data-mtype="+row.mtype+" data-actiontype="+row.actiontype+" data-to='"+row.to+"' data-link="+row.link+"  >推送</button>";
                    return htmlStr;
                }
            },
            {
                "targets": 6, //改写哪一列
                "data": "id",
                "render": function (data, type, row) {

                    var _to = row.to;
                    var _tolist = _to.split(",");

                    if(row.mode == '2'){

                        y_str = '用户';

                    }else{


                        y_str = '渠道';


                    }

                    if(_tolist.length <= 4){

                        var _tostr = _to;

                    }else{

                        var _tostr = _tolist[0]+","+_tolist[1]+","+_tolist[2]+","+_tolist[3]+"等"+_tolist.length+"个"+y_str;

                    }

                    var htmlStr = _tostr;
                    return htmlStr;
                }
            },
            {
                "targets": 0, //改写哪一列
                "data": "id",
                "render": function (data, type, row) {

                    if(row.ref_title == ''){


                        var _zhi = "''";

                    }else{


                        var _zhi = row.ref_title;

                    }

                    _zhi = encodeURIComponent(_zhi);

                    var htmlStr = "<a data-action='edit' href=\"JavaScript:void(0)\" data-tag_type='"+row.tag_type+"' data-ref_title="+_zhi+"  data-id="+row.id+" data-mode="+row.mode+" data-platforms="+row.platforms+"  data-apptypes="+row.apptypes+" data-title="+row.title+" data-content="+encodeURIComponent(row.content)+" data-mtype="+row.mtype+" data-actiontype="+row.actiontype+" data-to='"+row.to+"' data-link="+row.link+"    >"+row.mtype_str+"</a>";
                    return htmlStr;
                }
            }
            // {
            //     "targets": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            //     "orderable": true  //禁止排序
            // }
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

   original_rate = '';
   ori_base_currency = '';
   ori_foreign_currency = '';
    //新建按钮点击事件
    $("#create").click(function () {

$("#delete_confirm").hide();

        $("#push_id").val('');
       $("#title").val('');
       $("#content").val('');
       $("#mode").val('');
       $("#to").val('');
       $("#actiontype").val("0");
       $("#link").val('');
       $("#mtype").val('1');
       $("#ref_title").val('');


       var items = document.getElementsByName("tag_type");


        for (var i = 0; i < items.length; i++) {


                items[i].checked = false;


        }

       var items = document.getElementsByName("platforms");


        for (var i = 0; i < items.length; i++) {


                items[i].checked = false;


        }





       var items = document.getElementsByName("apptypes");


        for (var i = 0; i < items.length; i++) {



                items[i].checked = false;





        }



       $("#create_confirm").attr('data-savetype','0');
       $("#myModalLabel").text('新建商户消息推送');
       $("#rate_id").val('');
       $("#base_currency").val('');
       $("#foreign_currency").val('');
       $("#rate").val('');
       $("#unit").val('100');
       $("#rate_resources").val('');
       $("#comments").val('');
       //$("#myCreate").modal('show');
       $('#myCreate').modal({backdrop: 'static', keyboard: false});
    });

   //修改按钮的点击事件
   $(document).on('click',"[data-action='edit']",function () {

        //$("#delete_confirm").show();
       $("#create_confirm").attr('data-savetype','1');
       $("#myModalLabel").text('修改商户消息推送');

       $("#push_id").val(this.dataset.id);
       $("#title").val(this.dataset.title);
       $("#content").val(decodeURIComponent(this.dataset.content));
       $("#mode").val(this.dataset.mode);
       $("#to").val(this.dataset.to);
       $("#actiontype").val(this.dataset.actiontype);
       $("#link").val(this.dataset.link);
       $("#mtype").val(this.dataset.mtype);
       $("#ref_title").val(decodeURIComponent(this.dataset.ref_title));



       var _platforms = this.dataset.platforms;
       _platforms =  _platforms.split(",");



       var items = document.getElementsByName("platforms");


        for (var i = 0; i < items.length; i++) {

            for (var j = 0; j < _platforms.length; j++) {

                if(String(_platforms[j]) == String(items[i].value)){

                items[i].checked = true;

                }

            }

        }


        var _tag_type = this.dataset.tag_type;
       _tag_type =  _tag_type.split(",");



       var items = document.getElementsByName("tag_type");


        for (var i = 0; i < items.length; i++) {

            for (var j = 0; j < _tag_type.length; j++) {

                if(String(_tag_type[j]) == String(items[i].value)){

                items[i].checked = true;

                }

            }

        }


        var _apptypes = this.dataset.apptypes;
       _apptypes =  _apptypes.split(",");



       var items = document.getElementsByName("apptypes");


        for (var i = 0; i < items.length; i++) {

            for (var j = 0; j < _apptypes.length; j++) {

                if(String(_apptypes[j]) == String(items[i].value)){

                items[i].checked = true;

                }

            }

        }



       $('#myCreate').modal('show');
   });


    //二次确定窗口(取消)
    $("#sure_cancel").click(function () {

       $("#mySure").modal('hide');


   });


    //二次确认modal的确认按钮点击事件 (确认)
   $("#sure_confirm").click(function () {


       var jsonData = push_save;

       var self = $(this);



       $.ajax({
               async: true,
               dataType: 'json',
               url: '/push_act',
               type: 'POST',
               contentType: "application/json; charset=utf-8",
               data: JSON.stringify(jsonData),
                beforeSend: function(){
    self.attr('disabled',true);
    $("#mySure_title").html("正在push......请勿关闭对话框");
    },
               complete: function () {
      self.attr('disabled',false);
      $("#mySure_title").html("确定push吗?");
    },
               success: function (result) {
                   if (result && result.ok){
                       oTable.ajax.reload();
                       toastr.success(result.msg);
                       $("#mySure").modal('hide');


                        setTimeout(function(){  window.location.reload(); },2000);

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


    //push点击事件
   $(document).on('click',"[data-action='push']",function () {


       var _now = {};

       _now['push_id'] = this.dataset.id;
       _now['title'] = this.dataset.title;
       _now['content'] = decodeURIComponent(this.dataset.content);
       _now['mode'] = this.dataset.mode;
       _now['to'] = this.dataset.to;
       _now['actiontype'] = this.dataset.actiontype;
       _now['link'] = this.dataset.link;
       _now['mtype'] = this.dataset.mtype;

       _now['platforms'] = this.dataset.platforms;
       _now['apptypes'] = this.dataset.apptypes;
       _now['ref_title'] = decodeURIComponent(this.dataset.ref_title);
       _now['tag_type'] = this.dataset.tag_type;

       push_save = _now;


       $("#mySure").modal('show');

   });


    //删除消息窗口
    $("#delete_confirm").click(function () {

        $('#myCreate').modal('hide');
       $("#mySure").modal('show');
    });


   //新建modal的确认提交按钮的事件
   $("#create_confirm").click(function () {
       base_currency = $("#title").val().replace(/\s+/g,"");
       _title = base_currency;
       if (base_currency.length == 0){
           toastr.warning('请输入标题');
           return;
       }


       base_currency = $("#content").val().replace(/\s+/g,"");
       if (base_currency.length == 0){
           toastr.warning('请输入内容');
           return;
       }
       _content = base_currency;


     
       var _items = '';
       var items = document.getElementsByName('tag_type');
        for(var i=0;i<items.length;i++) {
        if (items[i].checked){

            _items +=  items[i].value + ',';

        }}
        _tag_type = _items;
        _tag_type = _tag_type.replace(/\,$/,'');


        if(_tag_type == ''){

            toastr.warning('请选择一级标签');
           return;

        }
       
       
       

       base_currency = $("#mode").val().replace(/\s+/g,"");
       if (base_currency.length == 0){
           toastr.warning('请选择推送方式');
           return;
       }

       _mode = $("#mode").val().replace(/\s+/g,"");
       _to = $("#to").val();
       if (_to == '' && ($("#mode").val() == '2' || $("#mode").val() == '3')){
           toastr.warning('请输入id');
           return;
       }


       var _items = '';
       var items = document.getElementsByName('platforms');
        for(var i=0;i<items.length;i++) {
        if (items[i].checked){

            _items +=  items[i].value + ',';

        }}
        _platforms = _items;
        _platforms = _platforms.replace(/\,$/,'');


        if(_platforms == ''){

            toastr.warning('请选择平台');
           return;

        }

        var _items = '';
       var items = document.getElementsByName('apptypes');
        for(var i=0;i<items.length;i++) {
        if (items[i].checked){

            _items +=  items[i].value + ',';

        }}
        _apptypes = _items;
        _apptypes = _apptypes.replace(/\,$/,'');


        if(_apptypes == ''){

            toastr.warning('请选择Apptypes');
           return;

        }


           var jsonData = {};
           jsonData.title = _title;
           jsonData.content = _content;
           jsonData.mode = _mode;
           jsonData.to = _to;
           jsonData.platforms = _platforms;
           jsonData.apptypes = _apptypes;
           jsonData.mtype = $("#mtype").val();
           jsonData.id = $("#push_id").val();
           jsonData.link = $("#link").val();
           jsonData.actiontype = $("#actiontype").val();
           jsonData.ref_title = $("#ref_title").val();
           jsonData.tag_type = _tag_type;



           var _method = 'POST';


           if ($("#create_confirm").attr('data-savetype') == 1){


               _method = 'PUT';


           }else{


               _method = 'POST';


           }




           $.ajax({
               async: true,
               dataType: 'json',
               url: '/push_list_api',
               type: _method,
               contentType: "application/json; charset=utf-8",
               data: JSON.stringify(jsonData),
               beforeSend: function(){
     $("#create_confirm").attr('disabled',true);
    },
               complete: function () {
       $("#create_confirm").attr('disabled',false);
    },
               success: function (result) {
                   if (result && result.ok){


                       toastr.success(result.msg);
                       $('#myCreate').modal('hide');

                       setTimeout(function(){  window.location.reload(); },1000);




                   }else {
                       toastr.warning(result.msg);
                   }


               },
               error: function (msg) {
                   toastr.error('操作失败 ！');



               }
           });


   });






});