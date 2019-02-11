/**
 * Created by shangerdi on 2017-09-20.
 */

function arrayExtend() {
    Array.prototype.contains = function (item) {
        for (var i = 0; i < this.length; i++) {
            if (this[i].name == item.name) {
                return true;
            }
        }
        return false;
    };
    Array.prototype.uniquelize = function () {
        var ra = new Array();
        for (var i = 0; i < this.length; i++) {
            if (!ra.contains(this[i])) {//indexOf(“str”) != -1
                ra.push(this[i]);
            }
        }
        return ra;
    };
    Array.prototype.each = function (fn) {
        fn = fn || Function.K;
        var a = [];
        var args = Array.prototype.slice.call(arguments, 1);
        for (var i = 0; i < this.length; i++) {
            var res = fn.apply(this, [this[i], i].concat(args));
            if (res != null) a.push(res);
        }
        return a;
    };
    Array.prototype.removeByValue = function (val) {
        for (var i = 0; i < this.length; i++) {
            if (this[i] == val) {
                this.splice(i, 1);
                break;
            }
        }
    };
//补集
    Array.complement = function (a, b) {
        return Array.minus(Array.union(a, b), Array.intersect(a, b));
    };
//交集
    Array.intersect = function (a, b) {
        return a.uniquelize().each(function (o) {
            return b.contains(o) ? o : null
        });
    };
//差集
    Array.minus = function (a, b) {
        return a.uniquelize().each(function (o) {
            return b.contains(o) ? null : o
        });
    };
//并集
    Array.union = function (a, b) {
        return a.concat(b).uniquelize();
    };

}

function GetQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]); return null;
}

$(function () {
    // set highlight menu item
    var pathname = window.location.pathname;
    var items = $("a.list-group-item[href=\"" + location.pathname + "\"]");
    if (items.length) {
        items.addClass("solso-active");
        $(".panel-collapse").removeClass("in");
        items.closest(".panel-collapse").addClass("in");
    }
    // extend default array
    arrayExtend();
});
