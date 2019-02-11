/**
 * Created by qfpay on 2017/9/20.
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

    $('#aldiv').hide();

    var nameok = false;
    var passok = false;

    function CheckUserName() {
        var userinput = $('#username');
        if (userinput.val().length==0){
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

    $('#login').submit(function () {
        CheckUserName();
        CheckPassWord();
        toastr.remove();
        if (!nameok){
            toastr.warning('请输入用户名');
            return false;
        }else if(!passok){
            toastr.warning('请输入用户名');
            return false;
        }

        return nameok && passok;
    });
});
