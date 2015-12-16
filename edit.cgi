#!/usr/bin/perl

use Encode qw(is_utf8);
use CGI qw(:standard);
use strict;
use Jcode;
use URI;

# 入力チェック
my $id = param("id");
my $sid = param("sid");

# エラーのチェック
my $msg;
if($id eq ""){
  $msg = "idが取得できませんでした。";
}

# このイベントのURL
my $q = CGI->new();
my $base = $q->url;
my $uri = URI->new_abs('./detail.cgi', $base);
my $url = $uri . "?id=" . $id;

# ファイル名
my $file = "./data/" . $id . ".txt";
if ( -e $file ){

}else{
  $msg = "ファイルが存在しません。";
}

my($name, $memo, $date1, $date2, $date3);

my $edit = param("edit");

# 「更新する」ボタンを押した場合
if($edit eq "go"){
  $name = param("name");
  $memo = param("memo");

  # 禁則文字のエスケープ処理
  $memo =~ s/\$/＄/g;
  $memo =~ s/\?/？/g;
  $memo =~ s/\./．/g;
  $memo =~ s/\\t/ /g;
  $memo =~s/<[^>]*>//g;
  $memo =~ s/\r\n/<br>/g;

  $name =~ s/\$/＄/g;
  $name =~ s/\?/？/g;
  $name =~ s/\./．/g;
  $name =~ s/\\t/ /g;
  $name =~s/<[^>]*>//g;

  $date1 = param("date1");
  $date2 = param("date2");
  $date3 = param("date3");

  open(IN, $file);
  flock(IN, 1);
  my @all = <IN>;
  close(IN);

  # ファイルに書き込む
  open(OUT, ">" . $file);
  flock(OUT, 2);
  truncate(OUT, 0);
  seek(OUT, 0, 0);
  print OUT $name . "\n";
  print OUT $memo . "\n";
  print OUT $date1 . "\t" . $date2 . "\t" . $date3 ."\n";
  my $cnt = 0;
  foreach (@all){
    if($cnt > 2){
      print OUT $_;
    }
    $cnt++;
  }
  flock(OUT, 8);
  close(OUT);

  $memo =~ s/<br>/\r\n/g;

# 画面遷移だけの場合
}else{

  # ファイルを開く
  open(my $fh, "<" . $file);
  my $i = 0;
  # readline関数で、一行読み込む。
  while(my $line = readline $fh){ 
    # chomp関数で、改行を取り除く
    chomp $line;

    # $line に対して何らかの処理。
    if($i == 0){
      $name = $line;
    }elsif($i == 1){
      $memo = $line;
      $memo =~ s/<br>/\r\n/g;
    }elsif($i == 2){
      ($date1, $date2, $date3) = split(/\t/, $line);
    }

    $i++;
    # ファイルがEOF( END OF FILE ) に到達するまで1行読みこみを繰り返す。
  }

  close $fh;
}

my $html = <<HTML;
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <title>出欠幹事くん</title>
  <link rel="shortcut icon" href="favicon.ico">
  <link rel="stylesheet" type="text/css" href="./css/bootstrap.css">
  <link rel="stylesheet" type="text/css" href="./css/bootstrap-datetimepicker.css">
  <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">

  <style type="text/css">
  body { padding-top: 80px; }
  \@media ( min-width: 768px ) {
    #banner {
      min-height: 300px;
      border-bottom: none;
    }
    .bs-docs-section {
      margin-top: 4em;
    }
    .bs-component {
      position: relative;
    }
    .bs-component .modal {
      position: relative;
      top: auto;
      right: auto;
      left: auto;
      bottom: auto;
      z-index: 1;
      display: block;
    }
    .bs-component .modal-dialog {
      width: 90%;
    }
    .bs-component .popover {
      position: relative;
      display: inline-block;
      width: 220px;
      margin: 20px;
    }
    .nav-tabs {
      margin-bottom: 15px;
    }
    .progress {
      margin-bottom: 10px;
    }
  }
  </style>

  <!--[if lt IE 9]>
    <script src="//oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
    <script src="//oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
  <![endif]-->

</head>
<body>

<header>
  <div class="navbar navbar-default navbar-fixed-top">
    <div class="container">
      <div class="navbar-header">
        <a href="./" class="navbar-brand"><i class="fa fa-calendar-o"></i> 出欠幹事くん</a>
        <button class="navbar-toggle" type="button" data-toggle="collapse" data-target="#navbar-main">
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
        </button>
      </div>
      <div class="navbar-collapse collapse" id="navbar-main">
        <ul class="nav navbar-nav">
          <li><a href="$url"><span class="glyphicon glyphicon-home"></span> Top</a></li>

        </ul>
      </div>
    </div>
  </div>
</header>

<div class="container">

HTML

if($msg eq ""){

$html .= <<HTML;

    <div class="row">
      <div class="col-lg-12">
        <div class="page-header">
        <h1>イベント再編集</h1>
        <a class="btn btn-primary" href="./detail.cgi?id=$id"><i class="fa fa-chevron-left"></i> 戻る</a>
        </div>
      </div>
    </div>

    <form class="form-horizontal" method="post" action="edit.cgi?id=$id" data-toggle="validator">

    <div class="row">
      <div class="col-lg-6">
        <div class="well bs-component">
          <input type="hidden" name="edit" value="go">
          <input type="hidden" name="id" value="$id">
            <fieldset>

              <div class="form-group">
                <label for="inputName" class="col-lg-2 control-label">イベント名</label>
                <div class="col-lg-10">
                  <input type="text" maxlength="50" class="form-control" id="inputName" name="name" value="$name" required>
                </div>
              </div>

              <div class="form-group">
                <label for="textArea" class="col-lg-2 control-label">メモ</label>
                <div class="col-lg-10">
                  <textarea class="form-control" rows="3" id="textArea" name="memo">$memo</textarea>
                </div>
              </div>

            </div>
          </div>

          <div class="col-lg-4 col-lg-offset-1">

            <div class="col-sm-8">

              <div class="form-group">
                <label for="datetimepicker1" class="control-label">候補日程1</label>
                <div class="input-group date" id="datetimepicker1">
                  <input type="text" class="form-control" name="date1" required>
                  <span class="input-group-addon">
                  <span class="glyphicon glyphicon-calendar"></span>
                  </span>
                </div>
              </div>

              <div class="form-group">
                <label for="datetimepicker2" class="control-label">候補日程2（任意）</label>
                <div class="input-group date" id="datetimepicker2">
                  <input type="text" class="form-control" name="date2">
                  <span class="input-group-addon">
                  <span class="glyphicon glyphicon-calendar"></span>
                  </span>
                </div>
              </div>

              <div class="form-group">
                <label for="datetimepicker3" class="control-label">候補日程3（任意）</label>
                <div class="input-group date" id="datetimepicker3">
                  <input type="text" class="form-control" name="date3">
                  <span class="input-group-addon">
                  <span class="glyphicon glyphicon-calendar"></span>
                  </span>
                </div>
              </div>


              <div class="form-group">
                <button type="submit" class="btn btn-primary"><i class="fa fa-refresh"></i> 更新する</button>
              </div>

            </div>

            </fieldset>

          </div>
        </div>

        </form>



    <div class="row">
      <div class="col-lg-12">
        <div class="page-header">
        <button class="btn btn-danger" data-toggle="modal" data-target="#myModal"><i class="fa fa-trash"></i> イベントを削除する</button>
        <p class="text-danger">※一度削除すると復旧はできません。ご注意ください。</p>
        </div>
      </div>
    </div>



<!-- Modal -->
<div id="myModal" class="modal fade" role="dialog">
  <div class="modal-dialog">

    <!-- Modal content-->
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">&times;</button>
        <h4 class="modal-title">確認画面</h4>
      </div>
      <div class="modal-body">
        <p>イベントを削除してよろしいですか？</p>
      </div>
      <div class="modal-footer">
        <a href="./?cmd=delete&id=$id" class="btn btn-primary">OK</a>
        <button type="button" class="btn btn-default" data-dismiss="modal">キャンセル</button>
      </div>
    </div>

  </div>
</div>



HTML

}else{
$html .= <<HTML;

    <div class="row">
      <div class="col-lg-12">
        <h1>エラー</h1>
        <p class="lead">$msg</p>
      </div>
    </div>

HTML
}

$html .= <<HTML;

        <hr>

$adsense

        <!-- Footer -->
        <footer>
            <div class="row">
                <div class="col-lg-12">
                    <p>Developed by Akira Mukai 2015</p>
                </div>
                <!-- /.col-lg-12 -->
            </div>
            <!-- /.row -->
        </footer>

</div>


<script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
<script type="text/javascript" src="./js/bootstrap.min.js"></script>
<script type="text/javascript" src="./js/moment.js"></script>
<script type="text/javascript" src="./js/moment-with-locales.js"></script>
<script type="text/javascript" src="./js/bootstrap-datetimepicker.js"></script>
<script type="text/javascript" src="./js/validator.js"></script>

<script type="text/javascript">
\$(function () {
  \$('#datetimepicker1').datetimepicker({
    locale: 'ja',
    format : 'M/D(dd) HH:mm',
    defaultDate: "$date1"
  });
  \$('#datetimepicker2').datetimepicker({
    locale: 'ja',
    format : 'M/D(dd) HH:mm',
    defaultDate: "$date2"
  });
  \$('#datetimepicker3').datetimepicker({
    locale: 'ja',
    format : 'M/D(dd) HH:mm',
    defaultDate: "$date3"
  });
});
</script>

</body>
</html>
HTML

print header( -type => 'text/html',-charset => 'UTF-8');
print $html;
