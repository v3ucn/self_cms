$(function(){
    $('.operation').click(function(e) {
        var id = e.target.getAttribute('id');
        var tag_id = e.target.getAttribute('tag_id');
        var op = e.target.getAttribute('op');
        console.log('click='+op)
        if (op == 'edit_cate') {
            get_edit_cate(id)
        }
    });
    $('#query_submit').click(function (){
        data = {}
        query_list = ['cate_name', 'status', 'remark']
        $.each(query_list, function(k,v){
            value = $('#query_'+v).val()
            if (v == 'cate_name') {
                data['cate_code'] = value
            } else {
                data[v] = value
            }
        })
        var data = JSON.stringify(data)
        $('#tag_table').DataTable().search(data).draw(true)

    })
    init_cate_name()
    function init_cate_name(){
        $('#query_cate_name option').remove()
        $('#query_cate_name').append('<option value="">全部</option>')
        var data = {}
        data.mode = 'get_cates'
        $.ajax({
            url: '/tag_manage',
            type: 'POST',
            data: data,
            success: function(resp) {
                if (resp['respcd'] == '0000') {
                    cate_dict = resp['data']['cate_dict']
                    console.log(cate_dict)
                    $.each(cate_dict, function(k,v){
                        $('#query_cate_name').append('<option value='+k+'>'+v+'</option>')
                    })
                    $('#query_cate_name').selectpicker('refresh')
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
    $('#add_submit').click(function(){
        $('#add_modal').modal({backdrop: 'static'});
    })

    $('#modal_cancel_submit').click(function(){
        $('#add_cate_name').val('')
        $('#add_remark').val('')
        $('#add_modal').modal('hide');
    })

    $('#modal_add_submit').click(function(){
        var data = {}
        data.mode = 'add_cate'
        add_list = [
            'cate_name', 'remark', 'status'
        ]
        $.each(add_list, function(k,v){
            data[v] = $('#add_'+v).val()
        })
        $.ajax({
            url: '/tag_manage',
            type: 'POST',
            data: data,
            async: false,
            success: function(resp) {
                if (resp['respcd'] == '0000') {
                    $('#add_modal').modal('hide');
                    $('#tag_table').DataTable().draw(false);
                    toastr.success(msg='添加成功');
                } else {
                    toastr.error(msg=resp['respmsg'], title='获取信息数据失败');
                }
            },
            error:function(data) {
                toastr.warning('网络不好， 请稍后重试!!!');
                //location.href = '/mkm/error'
            }
        })
        init_cate_name()
        $('#add_cate_name').val('')
        $('#add_remark').val('')
    })

    var urlEncode = function (param, key, encode) {
      if(param==null) return '';
      var paramStr = '';
      var t = typeof (param);
      if (t == 'string' || t == 'number' || t == 'boolean') {
          paramStr += '&' + key + '=' + ((encode==null||encode) ? encodeURIComponent(param) : param);
        } else {
            for (var i in param) {
                  var k = key == null ? i : key + (param instanceof Array ? '[' + i + ']' : '.' + i);
                  paramStr += urlEncode(param[i], k, encode);
                }
          }
      return paramStr;
    };


    $('#expo_submit').click(function (){
        data = {}
        query_list = ['cate_name', 'status', 'remark']
        $.each(query_list, function(k,v){
            value = $('#query_'+v).val()
            data[v] = value
        })
        location.href = '/tag_list?mode=expo_excel' + urlEncode(data)
    })

    function get_edit_cate(cate_code){
        edit_list = [
            'cate_name', 'remark', 'status'
        ]
        var data = {}
        data.cate_code = cate_code
        $.ajax({
            url: '/tag_list',
            type: 'GET',
            data: data,
            success: function(resp) {
                if (resp['respcd'] == '0000') {
                    tag = resp['data']['list'][0]
                    $.each(edit_list, function(k,v){
                        $('#edit_'+v).val(tag[v])
                    })
                    $('#edit_status').selectpicker('refresh')
                    $('#cate_code').html(cate_code)
                    $('#edit_modal').modal({backdrop: 'static'});
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
    $('#modal_submit').click(function (){
        data = {}
        edit_list = [
            'cate_name', 'remark', 'status'
        ]
        $.each(edit_list, function(k,v){
            data[v] = $('#edit_'+v).val()
        })
        data.mode = 'edit_cate'
        data.cate_code = $('#cate_code').html()
        $.ajax({
            url: '/tag_manage',
            type: 'POST',
            data: data,
            async: false,
            success: function(data) {
                if (data['respcd'] == '0000') {
                    $('#edit_modal').modal('hide');
                    $('#tag_table').DataTable().draw(false);
                    toastr.success(msg='修改成功');
                } else {
                    toastr.error(msg=data.respmsg, title='修改失败');
                }
            },
            error: function (data) {
                toastr.warning('网络不好， 请稍后重试!!!');
                //location.href = '/mkm/error'
            }
        })
        init_cate_name()
    })


    $('#tag_table').dataTable({
        serverSide: true,
        autoWidth: false,
        ajax : function(data, callback, settings) {
            var search_data = data.search.value ? JSON.parse(data.search.value) : {};
            search_data['offset'] = data.start;
            search_data['pageSize'] = data.length;
            $.ajax({
                url: '/tag_list',
                type: 'GET',
                dataType: 'json',
                data: search_data,
                success: function(data) {
                    if (data['respcd'] == '0000') {
                        resp = data.data;
                        callback({
                            recordsTotal: resp.total,
                            recordsFiltered: resp.total,
                            data: resp.list
                        });
                    } else {
                        callback({
                            recordsTotal: 0,
                            recordsFiltered: 0,
                            data: []
                        });
                        toastr.error(msg=data.respmsg, title='获取列表失败');
                    }
                },
                error:function(data) {
                    toastr.warning('网络不好， 请稍后重试!!!');
                    //location.href = '/mkm/error'
                }
            })
        },
        columns : [
            {
                data : 'cate_name',
                createdCell: function(td) {
                    $(td).attr('data-title', '标签名称');
                },
                render: function (data, type, row) {
                    var htmlStr = '';
                    htmlStr += "<div style='word-wrap:break-word;width: 140px'>" + data + "</div>";
                    return htmlStr
                }
            },
            {
                data : 'remark',
                createdCell: function(td) {
                    $(td).attr('data-title', '标签解释');
                },
                render: function (data, type, row) {
                    var htmlStr = '';
                    htmlStr += "<div style='word-wrap:break-word;width: 330px'>" + data + "</div>";
                    return htmlStr
                }
            },
            {
                data : 'user_count',
                createdCell: function(td) {
                    $(td).attr('data-title', '商户数量');
                },
                render: function (data, type, row) {
                    var htmlStr = '';
                    htmlStr += "<div style='word-wrap:break-word;width:80px;text-align:center'>" + data + "</div>";
                    return htmlStr
                }
            },
            {
                data : 'ctime',
                createdCell: function(td) {
                    $(td).attr('data-title', '创建时间');
                },
            },
            {
                data : 'utime',
                createdCell: function(td) {
                    $(td).attr('data-title', '更新时间');
                }
            },
            {
                data : 'status_str',
                createdCell: function(td) {
                    $(td).attr('data-title', '状态');
                },
            },
            {
                orderable : false,
                data : null,
                createdCell: function(td) {
                    $(td).attr('data-title', '操作');
                },
                render : function(data, type, row) {
                        var ret = '<button class="btn btn-primary btn-sm" ';
                        ret += ' id="'+data.cate_code+'"';
                        ret += ' op="edit_cate">';
                        ret += '编辑</button>';
                        return ret ;
                    }
            },
        ],
        ordering : false,
        sDom:'<t><"row m-r m-l" <"col-sm-6" <"col-sm-5 m-t-sm" l><"col-sm-offset-4" i>><"col-sm-6" p>><"clear">',
        language : {url:'/static/common/lang/DT.Chinese.json'},
    });
})
