$(function () {

    //Initialize tooltips
    $('.nav-tabs > li a[title]').tooltip();

    //Wizard
    $('a[data-toggle="tab"]').on('show.bs.tab', function (e) {
        var $target = $(e.target);
        if ($target.parent().hasClass('disabled')) {
            return false;
        }
    });

    $(".next-step").click(function (e) {
        var $active = $('.wizard .nav-tabs li.active');
        $active.next().removeClass('disabled');
        nextTab($active);
    });

    $(".prev-step").click(function (e) {
        var $active = $('.wizard .nav-tabs li.active');
        prevTab($active);
    });

    // 入力チェック（ボタンを押させない）
    if ($('#inputName').val().length == 0) {
        $('#stp1btn').prop('disabled', true);
    }
    $('#inputName').on('keydown keyup keypress change', function() {
        if ($(this).val().length > 0) {
            $('#stp1btn').prop('disabled', false);
        } else {
            $('#stp1btn').prop('disabled', true);
        }
    });

    // 入力チェック（ボタンを押させない）
    if ($(".date-1").val().length == 0) {
        $('#stp2btn').prop('disabled', true);
    }
    $(".date-1").on('keydown keyup keypress change', function() {
        if ($(this).val().length > 0) {
            $('#stp2btn').prop('disabled', false);
        } else {
            $('#stp2btn').prop('disabled', true);
        }
    });

    // 非同期通信を行ない結果を表示する
    $('#stp2btn').click(function () {
        $.ajax({
            type: "POST",
            url: "comp.php", //PHPを呼び出す
            dataType: 'json',
            data: {
                name: $('#inputName').val(), 
                memo: $('#textArea').val(), 
                date1: $(".date-1").val(), 
                date2: $(".date-2").val(), 
                date3: $(".date-3").val(), 
                id: $('#eventid').val()
            }
        })
        .done(function (response) {
            $('#result1').html(response.data1);
            $('#result2').html(response.data2);
        })
        .fail(function () {
            // jqXHR, textStatus, errorThrown と書くのは長いので、argumentsでまとめて渡す
            // (PHPのfunc_get_args関数の返り値のようなもの)
            $('#result1').val('失敗');
            $('#result2').val(errorHandler(arguments));
        });
        var $active = $('.wizard .nav-tabs li.active');
        $active.next().removeClass('disabled');
        nextTab($active);
    });

    $('#datetimepicker1').datetimepicker({
        locale: 'ja',
        format : 'YYYY/M/D(dd) HH:mm',
        sideBySide : true
    });

    // 入力後、ボタンを押せるようになる
    $('#datetimepicker1').on("dp.change",function (e) {
        $('#stp2btn').prop('disabled', false);
    });

    $('#datetimepicker2').datetimepicker({
        locale: 'ja',
        format : 'YYYY/M/D(dd) HH:mm',
        sideBySide : true
    });
    $('#datetimepicker3').datetimepicker({
        locale: 'ja',
        format : 'YYYY/M/D(dd) HH:mm',
        sideBySide : true
    });

});

function nextTab(elem) {
    $(elem).next().find('a[data-toggle="tab"]').click();
}
function prevTab(elem) {
    $(elem).prev().find('a[data-toggle="tab"]').click();
}
