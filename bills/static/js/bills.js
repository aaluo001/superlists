/*==============================
 * bills.js
 *==============================
 * Author: Tangjianwei
 * Create: 2019-11-07
 *==============================
 */

function view_billyms(url, selected_billym_id) {
    $.get(url).done(function(response){
        if (response.length > 0) {
            var htmls = '';
            for (var i=0; i < response.length; i++) {
                var billym = response[i];
                htmls += '<table id="id_billyms_table" class="table table-bordered table-condensed">';
                htmls += '<tr>';
                htmls += '<td id="id_billym_row_' + (i + 1) + '"';
                if (billym.id == selected_billym_id) {
                    htmls += 'class="app-selected"';
                }
                htmls += '>';
                htmls += '<a href="' + billym.url + '">';
                htmls += billym.year + '年' + billym.month + '月';
                htmls += '</a><br>';
                htmls += '</td>';
                htmls += '</tr>';
                htmls += '</table>';
                $('#id_view_billyms').html(htmls);
            }
        } else {
            $('#id_view_billyms').html('没有找到您的账单！');
        }
    });
}

function view_aggregates_on_selected_billym(url) {
    $.get(url).done(function(response) {
        if (response) {
            $('#id_billym_title').html(response.year + '年' + response.month + '月');
            $('#id_expends').html('<div class="text-danger">' + response.expends +'</div>');
            $('#id_incomes').html(response.incomes);
            var html_balance = '';
            if (response.balance < 0) {
                html_balance += '<div class="text-danger">';
                html_balance += response.balance;
                html_balance += '</div>';
            } else {
                html_balance += response.balance;
            }
            $('#id_balance').html(html_balance);
        }
    });
}

function view_bill_records(url) {
    // console.log('url: ' + url);
    $.get(url).done(function(response) {
        if (response.length > 0) {
            var htmls = '';
            htmls += '<table id="id_bill_records_table" class="table table-striped table-condensed">';
            htmls += '<thead><tr>';
            htmls += '<th>日期</th>';
            htmls += '<th class="text-right">收入支出</th>';
            htmls += '<th>备注</th>';
            htmls += '<th><br></th>';
            htmls += '</tr></thead>';
            htmls += '<tbody>';
            for (var i=0; i < response.length; i++) {
                var bill = response[i];
                htmls += '<tr>';
                htmls += '<td width="90">' + bill.date + '</td>';
                htmls += '<td width="140" class="text-right">';
                if (bill.money < 0) {
                    htmls += '<div class="text-danger">' + bill.money + '</div>';
                } else {
                    htmls += bill.money;
                }
                htmls += '</td>';
                htmls += '<td width="400">' + bill.comment + '</td>';
                htmls += '<td><br></td>';
                htmls += '</tr>';
            }
            htmls += '</tbody>';
            htmls += '</table>';
            // console.log('htmls: ' + htmls);
            $('#id_view_bill_records').html(htmls);
        }
    });
}
