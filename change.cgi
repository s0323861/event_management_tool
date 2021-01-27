#!/usr/local/bin/perl

use Encode qw(is_utf8);
use CGI qw(:standard);
use strict;
use Jcode;
use URI;

# 入力チェック
my $id = param("id");
my $sid = param("sid");
my $edit = param("edit");

# エラーのチェック
my $msg;
if($id eq "" or $sid eq ""){
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

# イベントの変数
my($name, $memo, $date1, $date2, $date3);

# 個人の変数
my($disp, $ans1, $ans2, $ans3, $com);

# 編集してから遷移した場合
if($edit eq "go"){
  $disp = param("display");
  $ans1 = param("date1");
  $ans2 = param("date2");
  $ans3 = param("date3");
  $com = param("comment");

  # 禁則文字のエスケープ処理
  $disp =~ s/\$/＄/g;
  $disp =~ s/\?/？/g;
  $disp =~ s/\./．/g;
  $disp =~ s/\\t/ /g;
  $disp =~s/<[^>]*>//g;
  $com =~ s/\$/＄/g;
  $com =~ s/\?/？/g;
  $com =~ s/\./．/g;
  $com =~ s/\\t/ /g;
  $com =~s/<[^>]*>//g;

  # ファイルを開き、配列へ入れる
  open(IN, $file);
  flock(IN, 1);
  my @all = <IN>;
  close(IN);

  # 配列を書きかえる
  my @new;
  my $i = 0;
  foreach my $line (@all){
    chomp $line;
    if($i == 0){
      $name = $line;
    }elsif($i == 1){
      $memo = $line;
    }elsif($i == 2){
      ($date1, $date2, $date3) = split(/\t/, $line);
    }else{
      my ($tmp1, $tmp2, $tmp3, $tmp4, $tmp5, $tmp6) = split(/\t/, $line);
      if($tmp5 eq $sid){
        $line = $disp . "\t" . $ans1 . "\t" . $ans2. "\t" . $ans3. "\t" . $sid . "\t" . $com;
      }
    }
    $line = $line . "\n";
    push (@new, $line);
    $i++;
  }

  # 配列をファイルに書き込む
  open(OUT, ">" . $file);
  flock(OUT, 2);
  truncate(OUT, 0);
  seek(OUT, 0, 0);
  foreach (@new){
    print OUT $_;
  }
  flock(OUT, 8);
  close(OUT);

}else{

  # ファイルを開く
  open(my $fh, "<" . $file);
  my $i = 0;
  my $j = 0;
  # readline関数で、一行読み込む
  while(my $line = readline $fh){ 
    # chomp関数で、改行を取り除く
    chomp $line;

    # $line に対して何らかの処理
    if($i == 0){
      $name = $line;
    }elsif($i == 1){
      $memo = $line;
    }elsif($i == 2){
      ($date1, $date2, $date3) = split(/\t/, $line);
    }else{
      my ($tmp1, $tmp2, $tmp3, $tmp4, $tmp5, $tmp6) = split(/\t/, $line);
      if($tmp5 eq $sid){
        $disp = $tmp1;
        $ans1 = $tmp2;
        $ans2 = $tmp3;
        $ans3 = $tmp4;
        $com = $tmp6;
      }
      $j++;
    }

    $i++;
    # ファイルがEOF( END OF FILE ) に到達するまで1行読みこみを繰り返す
  }

  close $fh;
}

# ラジオボタンの設定
my($check1, $check2, $check3, $check4, $check5, $check6, $check7, $check8, $check9);
if($ans1 eq "yes"){
  $check1 = " checked";
}elsif($ans1 eq "notyet"){
  $check2 = " checked";
}elsif($ans1 eq "nono"){
  $check3 = " checked";
}

if($ans2 eq "yes"){
  $check4 = " checked";
}elsif($ans2 eq "notyet"){
  $check5 = " checked";
}elsif($ans2 eq "nono"){
  $check6 = " checked";
}

if($ans3 eq "yes"){
  $check7 = " checked";
}elsif($ans3 eq "notyet"){
  $check8 = " checked";
}elsif($ans3 eq "nono"){
  $check9 = " checked";
}




my $tt2;

# 候補2が入っている場合
if($date2 ne ""){

$tt2 = <<EOF;
              <tr>
                <td>$date2</td>
                <td>
                  <div class="radio">
                    <label>
                      <input type="radio" name="date2" id="optionsRadios1" value="yes"$check4>
                      <i class="fa fa-circle-o"></i>
                    </label>
                  </div>
                </td>
                <td>
                  <div class="radio">
                    <label>
                      <input type="radio" name="date2" id="optionsRadios2" value="notyet"$check5>
                      <i class="fa fa-question"></i>
                    </label>
                  </div>
                </td>
                <td>
                  <div class="radio">
                    <label>
                      <input type="radio" name="date2" id="optionsRadios3" value="nono"$check6>
                      <i class="fa fa-times"></i>
                    </label>
                  </div>
                </td>
              </tr>
EOF
}

# 候補3が入っている場合
if($date3 ne ""){

$tt2 .= <<EOF;
              <tr>
                <td>$date3</td>
                <td>
                  <div class="radio">
                    <label>
                      <input type="radio" name="date3" id="optionsRadios1" value="yes"$check7>
                      <i class="fa fa-circle-o"></i>
                    </label>
                  </div>
                </td>
                <td>
                  <div class="radio">
                    <label>
                      <input type="radio" name="date3" id="optionsRadios2" value="notyet"$check8>
                      <i class="fa fa-question"></i>
                    </label>
                  </div>
                </td>
                <td>
                  <div class="radio">
                    <label>
                      <input type="radio" name="date3" id="optionsRadios3" value="nono"$check9>
                      <i class="fa fa-times"></i>
                    </label>
                  </div>
                </td>
              </tr>
EOF
}

my $html = <<HTML;
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <title>幹事くん</title>
  <link rel="shortcut icon" href="favicon.ico">
  <link rel="stylesheet" type="text/css" href="./css/bootstrap.css">
  <link href="//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css" rel="stylesheet">
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
        <a href="./" class="navbar-brand"><i class="fa fa-calendar-o"></i> 幹事くん</a>
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

  <!-- Forms
  ================================================== -->
  <section id="enter" class="section">
    <div class="row">
      <div class="col-lg-12">
        <div class="page-header">
          <h1 id="forms">出欠を入力する</h1>
          <a class="btn btn-primary" href="./detail.cgi?id=$id"><i class="fa fa-chevron-left"></i> 戻る</a>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-lg-12">
        <div class="well bs-component">
          <form class="form-horizontal" method="post" action="change.cgi?id=$id&sid=$sid" data-toggle="validator">
          <input type="hidden" name="edit" value="go">
          <input type="hidden" name="id" value="$id">
          <input type="hidden" name="sid" value="$sid">
            <fieldset>

              <div class="form-group">
                <label for="inputName" class="col-lg-2 control-label">表示名</label>
                <div class="col-lg-10">
                  <input type="text" class="form-control" id="inputName" name="display" value="$disp" required>
                </div>
              </div>

              <div class="form-group">
                <label for="inputDate" class="col-lg-2 control-label">日にち候補</label>
                <div class="col-lg-10">

          <table class="table table-striped table-hover ">
            <tbody>
              <tr>
                <td>$date1</td>
                <td>
                  <div class="radio">
                    <label>
                      <input type="radio" name="date1" id="optionsRadios1" value="yes"$check1>
                      <i class="fa fa-circle-o"></i>
                    </label>
                  </div>
                </td>
                <td>
                  <div class="radio">
                    <label>
                      <input type="radio" name="date1" id="optionsRadios2" value="notyet"$check2>
                      <i class="fa fa-question"></i>
                    </label>
                  </div>
                </td>
                <td>
                  <div class="radio">
                    <label>
                      <input type="radio" name="date1" id="optionsRadios3" value="nono"$check3>
                      <i class="fa fa-times"></i>
                    </label>
                  </div>
                </td>
              </tr>
$tt2
            </tbody>
          </table> 

                </div>
              </div>

              <div class="form-group">
                <label for="inputComment" class="col-lg-2 control-label">コメント</label>
                <div class="col-lg-10">
                  <input type="text" class="form-control" name ="comment" id="inputComment" value="$com">
                </div>
              </div>

              <div class="form-group">
                <div class="col-lg-10 col-lg-offset-2">
                  <button type="submit" class="btn btn-primary"><i class="fa fa-refresh"></i> 更新する</button>
                </div>
              </div>

              <hr>

              <div class="form-group">
                <div class="col-lg-10 col-lg-offset-2">
                  <a href="detail.cgi?id=$id&sid=$sid&edit=delete" type="button" class="btn btn-danger"><i class="fa fa-trash"></i> 削除する</a>
                </div>
              </div>

            </fieldset>
          </form>
        </div>
      </div>
    </div>

    </section>

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

        <!-- Footer -->
        <footer>
            <div class="row">
                <div class="col-lg-12">
                    <p>Copyright &copy; Akira Mukai 2021</p>
                </div>
                <!-- /.col-lg-12 -->
            </div>
            <!-- /.row -->
        </footer>

</div>

<script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
<script src="./js/bootstrap.min.js"></script>
<script type="text/javascript" src="./js/validator.js"></script>

</body>
</html>
HTML

print header( -type => 'text/html',-charset => 'UTF-8');
print $html;
