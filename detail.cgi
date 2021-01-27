#!/usr/local/bin/perl

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

# ファイル名
my $file = "./data/" . $id . ".txt";
if ( -e $file ){

}else{
  $msg = "ファイルが存在しません。";
}

# ◯、×、△のアイコンを設定する
my $maru = "<i class=\"fa fa-circle-o\"></i>";
my $batsu = "<i class=\"fa fa-times\"></i>";
my $sankaku = "<i class=\"fa fa-question\"></i>";

# このイベントのURL
my $q = CGI->new();
my $base = $q->url;
my $uri = URI->new_abs('./detail.cgi', $base);
my $url = $uri . "?id=" . $id;

my($name, $memo, $date1, $date2, $date3);

# 参加予定者の情報を入れる配列
my @people;

my $edit = param("edit");

# 4桁のランダムな文字列を生成する
my $rand_str = &randstr(4);

# 編集してから遷移した場合
my($disp, $ans1, $ans2, $ans3, $com);
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

  # ファイルに追記する
  open(OUT, ">>" . $file);
  flock(OUT, 2);
  # ファイルの末尾に移動する
  seek(OUT, 0, 2);
  print OUT $disp . "\t" . $ans1 . "\t" . $ans2 . "\t" . $ans3 . "\t" . $rand_str . "\t" . $com . "\n";
  flock(OUT, 8);
  close(OUT);

# 「削除する」ボタンから遷移してきた場合
}elsif($edit eq "delete"){

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
    if($i <= 2){
      $line = $line . "\n";
    }else{
      my ($tmp1, $tmp2, $tmp3, $tmp4, $tmp5, $tmp6) = split(/\t/, $line);
      if($tmp5 ne $sid){
        $line = $line . "\n";
      }else{
        $line = "";
      }
    }
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
}



# ファイルを開く
open(my $fh, "<" . $file);
my $i = 0;
my $j = 0;
# readline関数で、一行読み込む。
while(my $line = readline $fh){ 
  # chomp関数で、改行を取り除く
  chomp $line;

  # $line に対して何らかの処理。
  if($i == 0){
    $name = $line;
  }elsif($i == 1){
    $memo = $line;
  }elsif($i == 2){
    ($date1, $date2, $date3) = split(/\t/, $line);
  }else{
    $people[$j] = $line;
    $j++;
  }

  $i++;
  # ファイルがEOF( END OF FILE ) に到達するまで1行読みこみを繰り返す。
}

close $fh;


# Tableの中身を作成する
my $d1;
foreach my $val (@people){
  my($t1, $t2, $t3, $t4, $t5, $t6) = split(/\t/, $val);

  $t2 =~ s/yes/$maru/g;
  $t2 =~ s/nono/$batsu/g;
  $t2 =~ s/notyet/$sankaku/g;

  $t3 =~ s/yes/$maru/g;
  $t3 =~ s/nono/$batsu/g;
  $t3 =~ s/notyet/$sankaku/g;

  $t4 =~ s/yes/$maru/g;
  $t4 =~ s/nono/$batsu/g;
  $t4 =~ s/notyet/$sankaku/g;

  $d1 .= "<tr>\n";
  $d1 .= "<td><a href=\"./change.cgi?id=" . $id . "&sid=" . $t5 . "\">" . $t1 . "</a></td>\n";
  $d1 .= "<td>" . $t2 . "</td>\n";
  if($date2 ne ""){
    $d1 .= "<td>" . $t3 . "</td>\n";
  }
  if($date3 ne ""){
    $d1 .= "<td>" . $t4 . "</td>\n";
  }
  $d1 .= "<td>" . $t6 . "</td>\n";
  $d1 .= "</tr>\n";
}
my($tt2, $tt3);
$tt3 = "<th>" . $date1 . "</th>\n";

# 候補2が入っている場合
if($date2 ne ""){
  $tt3 .= "<th>" . $date2 . "</th>\n";

$tt2 = <<EOF;
              <tr>
                <td>$date2</td>
                <td>
                  <div class="radio">
                    <label>
                      <input type="radio" name="date2" id="optionsRadios1" value="yes">
                      $maru
                    </label>
                  </div>
                </td>
                <td>
                  <div class="radio">
                    <label>
                      <input type="radio" name="date2" id="optionsRadios2" value="notyet" checked>
                      $sankaku
                    </label>
                  </div>
                </td>
                <td>
                  <div class="radio">
                    <label>
                      <input type="radio" name="date2" id="optionsRadios3" value="nono">
                      $batsu
                    </label>
                  </div>
                </td>
              </tr>
EOF
}
# 候補3が入っている場合
if($date3 ne ""){
  $tt3 .= "<th>" . $date3 . "</th>\n";

$tt2 .= <<EOF;
              <tr>
                <td>$date3</td>
                <td>
                  <div class="radio">
                    <label>
                      <input type="radio" name="date3" id="optionsRadios1" value="yes">
                      $maru
                    </label>
                  </div>
                </td>
                <td>
                  <div class="radio">
                    <label>
                      <input type="radio" name="date3" id="optionsRadios2" value="notyet" checked>
                      $sankaku
                    </label>
                  </div>
                </td>
                <td>
                  <div class="radio">
                    <label>
                      <input type="radio" name="date3" id="optionsRadios3" value="nono">
                      $batsu
                    </label>
                  </div>
                </td>
              </tr>
EOF
}

$tt3 .= "<th>コメント</th>\n";

sub randstr {
  my $length = $_[0];

  my @char_tmp=();

  # 配列にランダム生成する対象の文字列を格納
  # (以下は、小文字のa～z、大文字のA～Z、数字の0～9)
  push @char_tmp, ('a'..'z');
  push @char_tmp, (0..9);

  # 指定文字数分、ランダム文字列を生成する
  my $rand_str_tmp = '';
  my $i;
  for ($i=1; $i<=$length; $i++) {
    $rand_str_tmp .= $char_tmp[int(rand($#char_tmp+1))];
  }

  return $rand_str_tmp;
}

# ボタンの無効化
my $disabled;
if($j >= 1){
  $disabled = "";
}else{
  $disabled = " disabled=\"disabled\"";
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

    <div class="row">
      <div class="col-lg-12">
        <h1>$name</h1>
        <p class="lead">$memo</p>

        <p class="bs-component">
          <a href="./edit.cgi?id=$id" class="btn btn-primary"><i class="fa fa-pencil-square-o"></i> 再編集する</a>
        </p>

      </div>
    </div>


  <!-- 日にち候補
  ================================================== -->

  <div class="bs-docs-section">

    <div class="row">
      <div class="col-lg-12">

        <div class="page-header">
          <h1 id="tables">日にち候補</h1>
        </div>

        <div class="bs-component">
          <table class="table table-striped table-hover ">
            <thead>
              <tr>
                <th>お名前</th>
                $tt3
              </tr>
            </thead>
            <tbody>
              $d1
            </tbody>
          </table> 
        </div><!-- /example -->

        <p class="bs-component">
          <a href="#enter" class="btn btn-primary"><i class="fa fa-user-plus"></i> 出欠を入力する</a>
          <!--<a href="./doc.php?key=$id" class="btn btn-default" target="_blank"$disabled><i class="fa fa-file-pdf-o"></i> PDF出力する</a>-->
        </p>

      </div>
    </div>
  </div>


  <!-- Forms
  ================================================== -->
    <div class="row">
      <div class="col-lg-12">
        <div class="page-header">
          <h1 id="forms">このイベントのURL</h1>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-lg-12">
        <div class="well bs-component">
          <form class="form-horizontal">
            <fieldset>

              <div class="form-group">
                <label for="inputURL" class="col-lg-2 control-label">URL</label>
                <div class="col-lg-10">
                  <input type="text" class="form-control" id="inputURL" value="$url" disabled>
                </div>
              </div>

            </fieldset>
          </form>
        </div>
      </div>
    </div>


  <!-- Forms
  ================================================== -->
  <section id="enter" class="section">
    <div class="row">
      <div class="col-lg-12">
        <div class="page-header">
          <h1 id="forms"><i class="fa fa-user-plus"></i> 出欠を入力する</h1>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-lg-12">
        <div class="well bs-component">
          <form class="form-horizontal" method="post" action="detail.cgi?id=$id" data-toggle="validator">
          <input type="hidden" name="edit" value="go">
          <input type="hidden" name="id" value="$id">
            <fieldset>

              <div class="form-group">
                <label for="inputName" class="col-lg-2 control-label">参加者のお名前</label>
                <div class="col-lg-10">
                  <input type="text" maxlength="15" class="form-control" id="inputName" name="display" required>
                </div>
              </div>

              <div class="form-group">
                <label for="inputDate" class="col-lg-2 control-label">出席／欠席</label>
                <div class="col-lg-10">

          <table class="table table-striped table-hover ">
            <tbody>
              <tr>
                <td>$date1</td>
                <td>
                  <div class="radio">
                    <label>
                      <input type="radio" name="date1" id="optionsRadios1" value="yes">
                      $maru
                    </label>
                  </div>
                </td>
                <td>
                  <div class="radio">
                    <label>
                      <input type="radio" name="date1" id="optionsRadios2" value="notyet" checked>
                      $sankaku
                    </label>
                  </div>
                </td>
                <td>
                  <div class="radio">
                    <label>
                      <input type="radio" name="date1" id="optionsRadios3" value="nono">
                      $batsu
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
                  <input type="text" class="form-control" maxlength="20" name ="comment" id="inputComment">
                </div>
              </div>

              <div class="form-group">
                <div class="col-lg-10 col-lg-offset-2">
                  <button type="submit" class="btn btn-primary"><i class="fa fa-user-plus"></i> 更新する</button>
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
<script type="text/javascript" src="./js/bootstrap.min.js"></script>
<script type="text/javascript" src="./js/validator.js"></script>

</body>
</html>
HTML

print header( -type => 'text/html',-charset => 'UTF-8');
print $html;
