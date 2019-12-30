/*==============================
 * bills.js
 *==============================
 * Author: Tangjianwei
 * Create: 2019-12-29
 *==============================
 */

function initBillMoney() {
    $('input[name="money"]').focus();
    $('input[name="money"]').on('keypress', function() {
        $("#id_error_money").hide();
    });
}

function initBillComment() {
    $('input[name="comment"]').on('keypress', function() {
        $("#id_error_comment").hide();
    });
}


$(document).ready(function() {
    initBillMoney();
    initBillComment();
});
