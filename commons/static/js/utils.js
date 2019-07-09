/*==============================
 * utils.js
 *==============================
 * Author: Tangjianwei
 * Create: 2019-06-29
 *==============================
 */

 /*==============================
  * 确认对话框
  *==============================
  * dialogId: 表示对话框，$("div#id")
  * buttonName: 弹出对话框的按钮，$('button=[name="buttonName"]')
  * callback: 点击对话框OK按钮时执行回调函数
  * ==============================
  */
function initConfirmDialog(dialogId, buttonName, callback) {
    // 定义确认对话框
    $("div#" + dialogId).dialog({
        autoOpen: false,
        resizable: false,
        modal: true,
        height: "auto",
        width: 400,
        buttons: {
            "OK": function() {
                $(this).dialog("close");
                callback();
            },
            "Cancel": function() {
                $(this).dialog("close");
            }
        }
    });

    // 注册确认对话框
    $('button[name=' + buttonName + ']').click(function(event) {
        $("div#" + dialogId).dialog("open");
        //console.log($("div.ui-dialog-buttonset>button:eq(0)").text());
        //console.log($("div.ui-dialog-buttonset>button:eq(1)").text());
        event.preventDefault();
    });
}

