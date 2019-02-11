$(function(){
    console.log('ada')
    $('.operation').click(function(e) {
        var id = e.target.getAttribute('id');
        var mpconf_id = e.target.getAttribute('mpconf_id');
        var op = e.target.getAttribute('op');
        console.log('click='+op)
        if (op == 'edit_mpconf') {
            get_edit_mpconf(id)
        }
    });
    $('#query_submit').click(function (){
        data = {}
        query_list = ['appname', 'appid', 'cid', 'main']
        $.each(query_list, function(k,v){
            value = $('#query_'+v).val()
            data[v] = value
        })
        var data = JSON.stringify(data)
        $('#mpconf_table').DataTable().search(data).draw(true)

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

    $('#add_submit').click(function(){
        $('#add_modal').modal({backdrop: 'static'});
    })

    $('#add_appname').change(uni_select)

    function uni_select() {
        var appname_select = document.getElementById('add_appname')
        var appid = appname_select.options[appname_select.selectedIndex].value
        $('#add_appid').val(appid)
    }
    uni_select()

    $('#expo_submit').click(function (){
        data = {}
        query_list = ['appname', 'appid', 'cid', 'main']
        $.each(query_list, function(k,v){
            value = $('#query_'+v).val()
            data[v] = value
        })
        location.href = '/set_mpconf_list?mode=expo_excel' + urlEncode(data)
    })

    function get_edit_mpconf(mpconf_id){
        edit_list = [
            'main', 'cid', 'pay_appid', 'menu', 'appname',
            'uid', 'appid', 'chnlcode',
        ]
        var data = {}
        data.id = mpconf_id
        $.ajax({
            url: '/set_mpconf_list',
            type: 'GET',
            data: data,
            success: function(resp) {
                if (resp['respcd'] == '0000') {
                    mpconf = resp['data']['list'][0]
                    $.each(edit_list, function(k,v){
                        if (v == 'chnlcode') {
                            mpconf_chnlcode = mpconf['chnlcode']
                            var mpconf_chnlcode_list = []
                            if (mpconf_chnlcode) {
                                mpconf_chnlcode_list = mpconf_chnlcode.split(',')
                            }
                            $.each(mpconf_chnlcode_list, function(i,j){
                                $('#edit_'+v).val(j)
                            })
                            $('#edit_'+v).selectpicker('refresh')
                        }else {
                            $('#edit_'+v).val(mpconf[v])
                        }
                    })
                    $('#mpconf_id').html(mpconf_id)
                    $('#edit_modal').modal({backdrop: 'static'});
                } else {
                    toastr.error(msg=resp['respmsg'], title='获取信息数据失败');
                }
            },
            error:function(data) {
                toastr.warning('网络不好， 请稍后重试!!!');
                location.href = '/mkm/error'
            }
        })
    }

    function clear_modal_add(){
        add_list = [
            'main', 'cid', 'pay_appid', 'menu', 'appname',
            'uid', 'chnlcode',
        ]
        $.each(add_list, function(k,v){
            $('#add_'+v).val('')
        })
    }

    $('#modal_submit_cancel').click(function (){
        $('#add_modal').modal('hide');
        clear_modal_add()
    })

    $('.close').click(function(){
        clear_modal_add()
    })


    $('#modal_submit_add').click(function (){
        data = {}
        add_list = [
            'main', 'cid', 'pay_appid', 'menu', 'appname',
            'uid', 'chnlcode', 'appid',
        ]
        $.each(add_list, function(k,v){
            var value = ''
            if (v == 'appname') {
                value = $('#add_'+v).find('option:selected').text()
            } else {
                value = $('#add_'+v).val()
            }
            data[v] = value
        })
        data.mode = 'add_mpconf'
        $.ajax({
            url: '/set_mpconf_manage',
            type: 'POST',
            data: data,
            success: function(data) {
                if (data['respcd'] == '0000') {
                    $('#add_modal').modal('hide');
                    $('#mpconf_table').DataTable().draw(false);
                    toastr.success(msg='保存成功');
                    clear_modal_add()
                } else {
                    toastr.error(msg=data.respmsg, title='保存失败');
                }
            },
            error: function (data) {
                toastr.warning('网络不好， 请稍后重试!!!');
            }
        })
    })


    $('#modal_submit').click(function (){
        data = {}
        edit_list = [
            'main', 'cid', 'pay_appid', 'menu', 'appname',
            'uid', 'appid', 'chnlcode',
        ]
        $.each(edit_list, function(k,v){
            value = $('#edit_'+v).val()
            data[v] = value
        })
        data.mode = 'edit_mpconf'
        data.id = $('#mpconf_id').html()
        $.ajax({
            url: '/set_mpconf_manage',
            type: 'POST',
            data: data,
            success: function(data) {
                if (data['respcd'] == '0000') {
                    $('#edit_modal').modal('hide');
                    $('#mpconf_table').DataTable().draw(false);
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
    })


    $('#mpconf_table').dataTable({
        serverSide: true,
        autoWidth: false,
        ajax : function(data, callback, settings) {
            var search_data = data.search.value ? JSON.parse(data.search.value) : {};
            search_data['offset'] = data.start;
            search_data['pageSize'] = data.length;
            $.ajax({
                url: '/set_mpconf_list',
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
                data : 'main',
                createdCell: function(td) {
                    $(td).attr('data-title', '主体名称');
                },
                render: function (data, type, row) {
                    var htmlStr = '';
                    htmlStr += "<div style='word-wrap:break-word;width: 100px'>" + data + "</div>";
                    return htmlStr
                }
            },
            {
                data : 'cid',
                createdCell: function(td) {
                    $(td).attr('data-title', '微信渠道号');
                }
            },
            {
                data : 'pay_appid',
                createdCell: function(td) {
                    $(td).attr('data-title', '支付appid');
                }
            },
            {
                data : 'menu',
                createdCell: function(td) {
                    $(td).attr('data-title', '支付目录');
                },
                render: function (data, type, row) {
                    var htmlStr = '';
                    htmlStr += "<div style='word-wrap:break-word;width: 180px'>" + data + "</div>";
                    return htmlStr
                }
            },
            {
                data : 'appname',
                createdCell: function(td) {
                    $(td).attr('data-title', '公众号名称');
                }
            },
            {
                data : 'appid',
                createdCell: function(td) {
                    $(td).attr('data-title', '公众号appid');
                }
            },
            {
                data : 'uid',
                createdCell: function(td) {
                    $(td).attr('data-title', '商户ID');
                },
                render: function (data, type, row) {
                    var htmlStr = '';
                    htmlStr += "<div style='word-wrap:break-word;width: 90px'>" + data + "</div>";
                    return htmlStr
                }
            },
            {
                data : 'chnlcode_display',
                createdCell: function(td) {
                    $(td).attr('data-title', '支持交易通道');
                },
                render : function(data, type, row) {
                    var htmlStr = '';
                    htmlStr += "<div style='word-wrap:break-word;width: 40px'>" + data + "</div>";
                    return htmlStr
                }
            },
            {
                orderable : false,
                data : null,
                createdCell: function(td) {
                    $(td).attr('data-title', '操作');
                },
                render : function(data, type, row) {
                        var ret = '<button class="btn btn-primary btn-sm" ';
                        ret += ' id="'+data.id+'"';
                        ret += ' op="edit_mpconf">';
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
