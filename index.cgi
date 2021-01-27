#!/usr/local/bin/perl

use Encode qw(is_utf8);
use CGI qw(:standard);
use strict;
use Jcode;

my $id = param("id");
my $cmd = param("cmd");

my $file = "./data/" . $id . ".txt";

if($cmd eq "delete"){
  if(-e $file){
    unlink $file;
  }
}

# 10桁のランダムな文字列を生成する
my $rand_str = &randstr(10);

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

my $html = <<HTML;
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="keywords" content="出欠管理,ツール,使い捨て,webサービス">
  <meta name="description" content="結婚式の２次会、同窓会、歓送迎会、忘年会、新年会、飲み会、オフ会などの参加者の出欠をとるwebサービスです。">
  <title>幹事くん - イベントの出欠管理・スケジュール調整ツール</title>
  <link rel="shortcut icon" href="favicon.ico">
  <link rel="stylesheet" type="text/css" href="./css/bootstrap.css">
  <link rel="stylesheet" type="text/css" href="./css/bootstrap-datetimepicker.css">
  <link rel="stylesheet" type="text/css" href="//maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css">
  <style type="text/css">
  body { padding-top: 80px; }
  \@media ( min-width: 768px ) {
    #banner {
      min-height: 300px;
      border-bottom: none;
    }
    .bs-docs-section {
      margin-top: 1em;
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

  .wizard {
      margin: 20px auto;
      background: #fff;
  }

  .wizard .nav-tabs {
      position: relative;
      margin: 40px auto;
      margin-bottom: 0;
      border-bottom-color: #e0e0e0;
  }

  .wizard > div.wizard-inner {
      position: relative;
      background: #fafafa url(http://subtlepatterns.com/patterns/geometry2.png);
      background-size: 30%;
  }

  .connecting-line {
      height: 2px;
      background: #e0e0e0;
      position: absolute;
      width: 80%;
      margin: 0 auto;
      left: 0;
      right: 0;
      top: 50%;
      z-index: 1;
  }

  .wizard .nav-tabs > li.active > a, .wizard .nav-tabs > li.active > a:hover, .wizard .nav-tabs > li.active > a:focus {
      color: #555555;
      cursor: default;
      border: 0;
      border-bottom-color: transparent;
  }

  span.round-tab {
      width: 70px;
      height: 70px;
      line-height: 70px;
      display: inline-block;
      border-radius: 100px;
      background: #fff;
      border: 2px solid #e0e0e0;
      z-index: 2;
      position: absolute;
      left: 0;
      text-align: center;
      font-size: 25px;
  }
  span.round-tab i{
      color:#555555;
  }
  .wizard li.active span.round-tab {
      background: #fff;
      border: 2px solid #5bc0de;
      
  }
  .wizard li.active span.round-tab i{
      color: #5bc0de;
  }

  span.round-tab:hover {
      color: #333;
      border: 2px solid #333;
  }

  .wizard .nav-tabs > li {
      width: 25%;
  }

  .wizard li:after {
      content: " ";
      position: absolute;
      left: 46%;
      opacity: 0;
      margin: 0 auto;
      bottom: 0px;
      border: 5px solid transparent;
      border-bottom-color: #5bc0de;
      transition: 0.1s ease-in-out;
  }

  .wizard li.active:after {
      content: " ";
      position: absolute;
      left: 46%;
      opacity: 1;
      margin: 0 auto;
      bottom: 0px;
      border: 10px solid transparent;
      border-bottom-color: #5bc0de;
  }

  .wizard .nav-tabs > li a {
      width: 70px;
      height: 70px;
      margin: 20px auto;
      border-radius: 100%;
      padding: 0;
  }

  .wizard .nav-tabs > li a:hover {
      background: transparent;
  }

  .wizard .tab-pane {
      position: relative;
      padding-top: 50px;
  }

  .wizard h3 {
      margin-top: 0;
  }

  .btn-outline-rounded{
      padding: 10px 40px;
      margin: 20px 0;
      border: 2px solid transparent;
      border-radius: 25px;
  }

  .btn.green{
      background-color:#5cb85c;
      /*border: 2px solid #5cb85c;*/
      color: #ffffff;
  }

  \@media( max-width : 585px ) {

      .wizard {
          width: 90%;
          height: auto !important;
      }

      span.round-tab {
          font-size: 16px;
          width: 50px;
          height: 50px;
          line-height: 50px;
      }

      .wizard .nav-tabs > li a {
          width: 50px;
          height: 50px;
          line-height: 50px;
      }

      .wizard li.active:after {
          content: " ";
          position: absolute;
          left: 35%;
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
          <li><a href="./"><span class="glyphicon glyphicon-home"></span> Top</a></li>
        </ul>
      </div>
    </div>
  </div>
</header>

<section style="background:#efefe9;">
<div class="container">
    <div class="row">
        <div class="wizard">
            <div class="wizard-inner">
                <div class="connecting-line"></div>
                <ul class="nav nav-tabs" role="tablist">

                    <li role="presentation" class="active">
                        <a href="#step1" data-toggle="tab" aria-controls="step1" role="tab" title="ホーム">
                            <span class="round-tab">
                                <i class="glyphicon glyphicon-home"></i>
                            </span>
                        </a>
                    </li>

                    <li role="presentation" class="disabled">
                        <a href="#step2" data-toggle="tab" aria-controls="step2" role="tab" title="Step 1">
                            <span class="round-tab">
                                <i class="glyphicon glyphicon-pencil"></i>
                            </span>
                        </a>
                    </li>

                    <li role="presentation" class="disabled">
                        <a href="#step3" data-toggle="tab" aria-controls="step3" role="tab" title="Step 2">
                            <span class="round-tab">
                                <i class="fa fa-calendar-plus-o"></i>
                            </span>
                        </a>
                    </li>

                    <li role="presentation" class="disabled">
                        <a href="#complete" data-toggle="tab" aria-controls="complete" role="tab" title="完成">
                            <span class="round-tab">
                                <i class="glyphicon glyphicon-ok"></i>
                            </span>
                        </a>
                    </li>
                </ul>
            </div>

            <div class="tab-content">
                <div class="tab-pane active" role="tabpanel" id="step1">
                    <h3 class="head text-center">「幹事くん」にようこそ <span style="color:#f48260;"><i class="glyphicon glyphicon-heart"></i></span></h3>
                      <p class="text-center">
                          「幹事くん」はイベント・歓送迎会・忘年会・新年会・同窓会などの日程調整＆出欠確認を行うツールです。<br>無料・登録不要・使い捨て型のWebサービスです！
                      </p>
          
                    <ul class="list-inline text-center">
                        <li><button type="button" class="btn btn-success btn-outline-rounded next-step green">始める <span class="glyphicon glyphicon-chevron-right"></span></button></li>
                    </ul>

                </div>

                <div class="tab-pane" role="tabpanel" id="step2">
                    <h3 class="head text-center"><span class="label label-danger">Step 1</span></h3>

                    <form role="form" class="form-horizontal">

                    <div class="col-sm-6 col-sm-offset-3">

                        <div class="form-group">
                            <input type="text" maxlength="50" class="form-control" id="inputName" name="name" placeholder="イベントの名前を入力してください">
                        </div>

                        <div class="form-group">
                            <textarea class="form-control" rows="3" id="textArea" maxlength="200" name="memo" placeholder="メモ（任意）"></textarea>
                        </div>

                        <ul class="list-inline text-center">
                            <li><button type="button" class="btn btn-default prev-step"><span class="glyphicon glyphicon-chevron-left"></span> 前へ</button></li>
                            <li><button type="button" class="btn btn-primary btn-info-full next-step" id="stp1btn">次へ <span class="glyphicon glyphicon-chevron-right"></span></button></li>
                        </ul>

                    </div>

                </div>


                <div class="tab-pane" role="tabpanel" id="step3">
                    <h3 class="head text-center"><span class="label label-danger">Step 2</span></h3>

                    <div class="col-sm-6 col-sm-offset-3">

                        <div class="form-group">
                        <label for="datetimepicker1" class="control-label">候補日程1</label>
                            <div class="input-group date" id="datetimepicker1">
                            <input type="text" class="form-control date-1" name="date1" placeholder="日時を右のアイコンを押して選択してください" required>
                            <span class="input-group-addon">
                            <span class="glyphicon glyphicon-calendar"></span>
                            </span>
                            </div>
                        </div>

                        <div class="form-group">
                        <label for="datetimepicker2" class="control-label">候補日程2（任意）</label>
                            <div class="input-group date" id="datetimepicker2">
                            <input type="text" class="form-control date-2" name="date2">
                            <span class="input-group-addon">
                            <span class="glyphicon glyphicon-calendar"></span>
                            </span>
                            </div>
                        </div>

                        <div class="form-group">
                        <label for="datetimepicker3" class="control-label">候補日程3（任意）</label>
                            <div class="input-group date" id="datetimepicker3">
                            <input  type="text" class="form-control date-3" name="date3">
                            <span class="input-group-addon">
                            <span class="glyphicon glyphicon-calendar"></span>
                            </span>
                        </div>
                    </div>

                    <input type="hidden" name="id" value="$rand_str" id="eventid">
                    </form>

                    <ul class="list-inline text-center">
                        <li><button type="button" class="btn btn-default prev-step"><span class="glyphicon glyphicon-chevron-left"></span> 前へ</button></li>
                        <li><button type="button" class="btn btn-outline-rounded btn-success green" id="stp2btn"><span class="glyphicon glyphicon-send"></span> 出欠表をつくる</button></li>
                    </ul>

                    </div>

                </div>

                <div class="tab-pane" role="tabpanel" id="complete">
                    <h3 class="head text-center">完成 <span style="color:#f48260;"><i class="glyphicon glyphicon-heart"></i></span></h3>
                    <p class="text-center">
                    下記のURLを参加メンバーに共有してください。<br>
                    以後このURLページにてメンバーの回答を入力してください。

                    <div class="alert alert-info text-center" role="alert">
                        <div id="result1"></div>
                    </div>

                    <ul class="list-inline text-center">
                        <li><div id="result2"></div></li>
                    </ul>

                    </p>
                </div>
                <div class="clearfix"></div>
            </div>
        </div>
    </div>

    <hr>

    <!-- Footer -->
    <footer>
        <div class="row">
            <div class="col-lg-12">
                <p>Developed by Akira Mukai 2021</p>
            </div>
            <!-- /.col-lg-12 -->
        </div>
        <!-- /.row -->
    </footer>

</div>
</section>

<script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
<script src="./js/bootstrap.min.js"></script>
<script src="./js/moment.js"></script>
<script src="./js/moment-with-locales.js"></script>
<script src="./js/bootstrap-datetimepicker.js"></script>
<script src="./js/default.js"></script>
<script src="./js/validator.js"></script>

</body>
</html>
HTML

print header( -type => 'text/html',-charset => 'UTF-8');
print $html;
