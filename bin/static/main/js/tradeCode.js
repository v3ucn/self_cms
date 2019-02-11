/**
 * Created by qfpay on 2017/11/22.
 */
$(function () {
    $('#codeQuery').click(function () {
        content = $('#codeuserid').val().replace(/\s+/g,"");
        if(content.length == 0){
            toastr.warning('请输入用户id');
            return;
        }
        $('#code').hide();
        $('.fig').show();

        $('#jhcode').html('');
        $('#jhcode').attr('src','/static/common/img/default.jpg');
        $('#jhurl').html('--');

         $('#czcode').html('');
        $('#czcode').attr('src','/static/common/img/default.jpg');
        $('#czurl').html('--');

        $('#dccode').html('');
        $('#dccode').attr('src','/static/common/img/default.jpg');
        $('#dcurl').html('--');
        $.ajax({
            async:true,
            dataType:"json",
            type:"POST",
            url:"/api/v1/qrcode",
            data:{
                userid:content,
            },
            success:function (json) {

                if(json && json.code == 200){
                    $('#code').show();
                    $('.fig').hide();
                    // $('#jhcode').attr('src',json.data.jhcode);
                    jQuery('#jhcode').qrcode({
                        render: "canvas", //也可以替换为table
                        width: 200,
                        height: 200,
                        foreground: "#FFA500",
                        background: "#FFF",
                        text: json.data.jhcode
                    });
                    $('#jhurl').html(json.data.jhcode);

                    // $('#czcode').attr('src',json.data.czcode);
                    jQuery('#czcode').qrcode({
                        render: "canvas", //也可以替换为table
                        width: 200,
                        height: 200,
                        foreground: "#FFA500",
                        background: "#FFF",
                        text: json.data.czcode
                    });
                    $('#czurl').html(json.data.czcode);

                    // $('#dccode').attr('src',json.data.dccode);
                    jQuery('#dccode').qrcode({
                        render: "canvas", //也可以替换为table
                        width: 200,
                        height: 200,
                        foreground: "#FFA500",
                        background: "#FFF",
                        text: json.data.dccode
                    });
                    $('#dcurl').html(json.data.dccode);
                }else {
                    $('#code').hide();
                    $('.fig').hide();
                    toastr.warning('加载失败！');
                }
            },
            error:function () {
                $('#code').hide();
                $('.fig').hide();
                toastr.warning('加载失败！');
            }
        })
    });
});

