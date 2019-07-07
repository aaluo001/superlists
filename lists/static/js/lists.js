/*==============================
 * lists.js
 *==============================
 * Author: Tangjianwei
 * Create: 2019-06-19
 *==============================
 */

function initItemText() {
    $('input[name="text"]').focus();
    $('input[name="text"]').on('keypress', function() {
        $(".has-error").hide();
    });
}

function initRemoveList() {
    initConfirmDialog("id_remove_list_dialog", "remove_list", function() {
        $('form[name="remove_list"]').submit();
    });
}


$(document).ready(function() {
    initItemText();
    initRemoveList();
});
