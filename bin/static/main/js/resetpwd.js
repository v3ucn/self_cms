/**
 * Created by qfpay on 2017/9/24.
 */
$(function () {
    //检测大小写
    $('#password').keypress(function(e) {
        var s = String.fromCharCode( e.which );
        if ( s.toUpperCase() === s && s.toLowerCase() !== s && !e.shiftKey ) {
            $('.capslock').show();
        }else {
            $('.capslock').hide();
        }
    });

    $('#rpassword').keypress(function(e) {
        var s = String.fromCharCode( e.which );
        if ( s.toUpperCase() === s && s.toLowerCase() !== s && !e.shiftKey ) {
            $('.capslock1').show();
        }else {
            $('.capslock1').hide();
        }
    });
    // $('#aldiv').hide();

    var nameok = false;
    var passok = false;
    var rpassok = false;

    function CheckUserName() {
        var userinput = $('#username');
        if(userinput.val().length==0){
            // $('#aluname').show();
            nameok = false;
        }else{
            // $('#aluname').hide();
            nameok = true;
        };
    };

    function CheckPassWord() {
        var passinput = $('#password');
        if(passinput.val().length==0){
            // $('#alpwd').show();
            passok = false;

        }else {
            // $('#alpwd').hide();
            passok = true;
        };
    };

    function CheckRpassWord() {
        var passinput = $('#rpassword');
        if(passinput.val().length==0){
            // $('#alpwd').show();
            rpassok = false;

        }else {
            // $('#alpwd').hide();
            rpassok = true;
        };
    };

    $('#reset').submit(function () {
        CheckUserName();
        CheckPassWord();
        CheckRpassWord();
        toastr.remove();
        if (!nameok){
            toastr.warning('请输入用户名');
            return false;
        }else if(!passok){
            toastr.warning('请输入原密码');
            return false;
        }else if(!rpassok){
            toastr.warning('请输入新密码');
            return false;
        }

        return nameok && passok && rpassok;
    });
});