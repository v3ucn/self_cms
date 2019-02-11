/**
 * Created by qfpay on 2018/3/21.
 */
Array.prototype.remove = function(val) {
    var index = this.indexOf(val);
    if (index > -1) {
        this.splice(index, 1);
    }
};
Array.prototype.in_array = function (element) {
　　for (var i = 0; i < this.length; i++) {
    　　if (this[i] == element) {
    　　  return true;
        }
    }
    return false;
};