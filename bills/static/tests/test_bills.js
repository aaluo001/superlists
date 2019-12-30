/*==============================
 * test_bills.js
 *==============================
 * Author: Tangjianwei
 * Create: 2019-12-29
 *==============================
 */

QUnit.module("初期表示测试");
QUnit.test("光标焦点会在收入支出输入框中", function(assert) {
    initBillMoney();
    initBillComment();
    assert.equal($('input[name="money"]').is(":focus"), true);
    assert.equal($('input[name="comment"]').is(":focus"), false);
});

QUnit.module("执行键盘输入操作测试");
QUnit.test("在收入支出输入框中，执行键盘输入操作时，错误提示会消失", function(assert) {
    initBillMoney();
    initBillComment();
    $('input[name="money"]').trigger('keypress');
    // 收入支出的错误提示会消失
    assert.equal($("#id_error_money").is(":visible"), false);
    // 备注的错误提示不会消失
    assert.equal($("#id_error_comment").is(":visible"), true);
});

QUnit.test("在备注输入框中，执行键盘输入操作时，错误提示会消失", function(assert) {
    initBillMoney();
    initBillComment();
    $('input[name="comment"]').trigger('keypress');
    // 收入支出的错误提示不会消失
    assert.equal($("#id_error_money").is(":visible"), true);
    // 备注的错误提示会消失
    assert.equal($("#id_error_comment").is(":visible"), false);
});

QUnit.test("不采取任何操作时，会显示错误提示", function(assert) {
    initBillMoney();
    initBillComment();
    assert.equal($("#id_error_money").is(":visible"), true);
    assert.equal($("#id_error_comment").is(":visible"), true);
});
