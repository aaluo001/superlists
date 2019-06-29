/*==============================
 * test_lists.js
 *==============================
 * Author: Tangjianwei
 * Create: 2019-06-23
 *==============================
 */

QUnit.module("执行键盘输入操作测试");
QUnit.test("执行键盘输入操作时，错误提示会消失", function(assert) {
    initItemText();
    $('input[name="text"]').trigger('keypress');
    assert.equal($(".has-error").is(":visible"), false);
});

QUnit.test("不采取任何操作时，会显示错误提示", function(assert) {
    initItemText();
    assert.equal($(".has-error").is(":visible"), true);
});


QUnit.module("删除清单对话框测试");
QUnit.test("没有点击删除清单按钮时，对话框是不可见的", function(assert) {
    initRemoveList();
    assert.equal($("#id_remove_list_dialog").is(":visible"), false);
});

QUnit.test("点击删除清单按钮时，弹出对话框", function(assert) {
    initRemoveList();
    // 点击删除清单按钮，弹出对话框
    //$('button[name="remove_list"]').trigger("click");
    $('button[name="remove_list"]').click();

    // 提示信息
    assert.equal($("#id_remove_list_dialog").is(":visible"), true);
    assert.equal($("#id_remove_list_dialog").text().trim(), "您确定要删除该清单吗？");
    // 按钮
    assert.equal($("div.ui-dialog-buttonset>button:eq(0)").text(), "OK");
    assert.equal($("div.ui-dialog-buttonset>button:eq(1)").text(), "Cancel");

    // 点击右上角[✖]按钮，关闭对话框
    $("#id_remove_list_dialog").dialog("close");
    assert.equal($("#id_remove_list_dialog").is(":visible"), false);
});

QUnit.test("点击Cancel按钮时，关闭对话框，但不会提交页面", function(assert) {
    // 错误消息是不可见的
    initItemText();
    $('input[name="text"]').trigger('keypress');
    assert.equal($(".has-error").is(":visible"), false);

    // 页面提交时，错误消息可见
    $('form[name="remove_list"]').on("submit", function() {
        $(".has-error").show();
        return false;
    });

    initRemoveList();
    // 打开对话框
    $("#id_remove_list_dialog").dialog("open");

    // 点击Cancel按钮，关闭对话框
    $("div.ui-dialog-buttonset>button:eq(1)").click()
    assert.equal($("#id_remove_list_dialog").is(":visible"), false);

    // 错误消息是不可见的（说明没有提交页面）
    assert.equal($(".has-error").is(":visible"), false);
});

QUnit.test("点击OK按钮时，关闭对话框，并提交页面", function(assert) {
    // 错误消息是不可见的
    initItemText();
    $('input[name="text"]').trigger('keypress');
    assert.equal($(".has-error").is(":visible"), false);

    // 页面提交时，错误消息可见
    $('form[name="remove_list"]').on("submit", function() {
        $(".has-error").show();
        return false;
    });

    initRemoveList();
    // 打开对话框
    $("#id_remove_list_dialog").dialog("open");

    // 点击OK按钮，关闭对话框
    $("div.ui-dialog-buttonset>button:eq(0)").click()
    assert.equal($("#id_remove_list_dialog").is(":visible"), false);

    // 错误消息是可见的（说明提交页面了）
    assert.equal($(".has-error").is(":visible"), true);
});
