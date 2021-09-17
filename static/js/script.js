// スクロールーーーーーーーーーーーーーーーー
$.scrollify({
  section: ".box",//1ページスクロールさせたいエリアクラス名
  scrollbars: "false",//スクロールバー表示・非表示設定
  interstitialSection: "#header,#footer",//ヘッダーフッターを認識し、1ページスクロールさせず表示されるように設定
  easing: "swing", // 他にもlinearやeaseOutExpoといったjQueryのeasing指定可能
  scrollSpeed: 1000, // スクロール時の速度

  //以下、ページネーション設定
  before: function (i, panels) {
    var ref = panels[i].attr("data-section-name");
    $(".pagination .active").removeClass("active");
    $(".pagination").find("a[href=\"#" + ref + "\"]").addClass("active");
  },
  afterRender: function () {
    var pagination = "<ul class=\"pagination\">";
    var activeClass = "";
    $(".box").each(function (i) {//1ページスクロールさせたいエリアクラス名を指定
      activeClass = "";
      if (i === $.scrollify.currentIndex()) {
        activeClass = "active";
      }
      pagination += "<li><a class=\"" + activeClass + "\" href=\"#" + $(this).attr("data-section-name") + "\"><span class=\"hover-text\">" + $(this).attr("data-section-name").charAt(0).toUpperCase() + $(this).attr("data-section-name").slice(1) + "</span></a></li>";
    });
    pagination += "</ul>";

    $("#box1").append(pagination);//はじめのエリアにページネーションを表示
    $(".pagination a").on("click", $.scrollify.move);
  }

});
// ーーーーーーーーーーーーーーーーーーーー

// タイピングアルファベットーーーーーーーーーーーー
// TextTypingというクラス名がついている子要素（span）を表示から非表示にする定義
function TextTypingAnime() {
  $('.TextTyping').each(function () {
    var elemPos = $(this).offset().top - 50;
    var scroll = $(window).scrollTop();
    var windowHeight = $(window).height();
    var thisChild = "";
    if (scroll >= elemPos - windowHeight) {
      thisChild = $(this).children(); //spanタグを取得
      //spanタグの要素の１つ１つ処理を追加
      thisChild.each(function (i) {
        var time = 100;
        //時差で表示する為にdelayを指定しその時間後にfadeInで表示させる
        $(this).delay(time * i).fadeIn(time);
      });
    } else {
      thisChild = $(this).children();
      thisChild.each(function () {
        $(this).stop(); //delay処理を止める
        $(this).css("display", "none"); //spanタグ非表示
      });
    }
  });
}

// 画面をスクロールをしたら動かしたい場合の記述
$(window).scroll(function () {
  TextTypingAnime();/* アニメーション用の関数を呼ぶ*/
});// ここまで画面をスクロールをしたら動かしたい場合の記述

// 画面が読み込まれたらすぐに動かしたい場合の記述
$(window).on('load', function () {
  //spanタグを追加する
  var element = $(".TextTyping");
  element.each(function () {
    var text = $(this).html();
    var textbox = "";
    text.split('').forEach(function (t) {
      if (t !== " ") {
        textbox += '<span>' + t + '</span>';
      } else {
        textbox += t;
      }
    });
    $(this).html(textbox);

  });

  TextTypingAnime();/* アニメーション用の関数を呼ぶ*/
});// ここまで画面が読み込まれたらすぐに動かしたい場合の記述
// ーーーーーーーーーーーーーーーーーーーーーーーーーー


// トリミングーーーーーーーーーーーーーーーーーーーーーーー
// <!-- Croppie   参考リンク  https://www.for-engineer.life/entry/python-croppie/  -->
$('#upload').on('change', function (e) {
  var reader = new FileReader();
  reader.onload = function (e) {
      $('.ui.modal')
          .modal('show')
          ;
      $("#preview").croppie("bind", {
          url: event.target.result
      });
  }
  reader.readAsDataURL(e.target.files[0]);
});


var $image_crop = $('#preview').croppie({
  viewport: {
      width: 60,
      height: 60
  },
  boundary: {
      width: 300,
      height: 300
  },
  enableResize: true,
});

$("#crop_end").click(function (event) {
  $image_crop.croppie('result', {
      type: 'base64',
      size: "viewport",
  }).then(function (response) {
      $.ajax({
          url: "/crop_image",
          type: "POST",
          data: { "croped_image": response },
          success: function (data) {
          }
      });
  })
}
);
// ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー