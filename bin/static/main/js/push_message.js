$(function(){
    var title_flag = false;
    var content_flag = false;
    var to_flag = false;
    var link_flag = false;
    var plateform_flag = false;
    var apptype_flag = false;

   $("form").submit(function(e){

       title_flag = check_input($("#title"),title_flag);
       content_flag = check_input($("#content"),content_flag);
       link_flag = check_input($("#link_url"),link_flag);
       to_flag = check_input($("#to_w"),to_flag);
       plateform_flag = chech_check($("#plateform li input:checkbox:checked"),plateform_flag);
       apptype_flag = chech_check($("#apptype li input:checkbox:checked"),apptype_flag);

       if (title_flag && content_flag && to_flag && plateform_flag && apptype_flag){
           return true;
       }
       else{
           return false;
       }

   });

    function chech_check(node,flag_name){

        var real_length = node.length;

        if (real_length > 0){
            flag_name = true;
            $("#check_ms").hide()
        }
        else{
            flag_name = false;
            $("#check_ms").show()
        }
        return flag_name;
    }

    function check_input(node,flag_name){
        var real_value = node.val().replace(" ","");

        if (real_value.length > 0){
            flag_name = true;
            $("#input_ms").hide();
        }
        else{
            $("#input_ms").show();
            flag_name = false;
        }
        return flag_name;
    }
});