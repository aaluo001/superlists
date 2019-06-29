/*==============================
 * list.js
 *==============================
 * Author: Tangjianwei
 * Create: 2019-06-19
 *==============================
 */

function initItemText() {
    $('input[name="text"]').on('keypress', function() {
        $(".has-error").hide();
    });
}

function initRemoveList() {
    // 删除清单提示对话框
    $("#id_remove_list_dialog").dialog({
        autoOpen: false,
        width: 400,
        buttons: [
            {
                text: "OK",
                click: function() {
                    $(this).dialog("close");
                    $('form[name="remove_list"]').submit();
                }
            },
            {
                text: "Cancel",
                click: function() {
                    $(this).dialog("close");
                }
            }
        ]
    });

    // 点击"删除按钮"时，弹出提示对话框
    $('button[name="remove_list"]').click(function(event) {
        $("#id_remove_list_dialog").dialog("open");
        //console.log($("#id_remove_list_dialog").text().trim());
        //console.log($("div.ui-dialog-buttonset>button:eq(0)").text());
        //console.log($("div.ui-dialog-buttonset>button:eq(1)").text());
        event.preventDefault();
    });
}

$(document).ready(function() {
    initItemText();
    initRemoveList();
});

