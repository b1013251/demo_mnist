$(function(){

  /*************************************
  スマートフォン対応
  *************************************/
  var stopDefault = function(event) {
    if (event.touches[0].target.tagName.toLowerCase() == "li") {return;}
    if (event.touches[0].target.tagName.toLowerCase() == "input") {return;}

    event.preventDefault();
  }

  // タッチイベントの初期化
  document.addEventListener("touchstart", stopDefault, false);
  document.addEventListener("touchmove", stopDefault, false);
  document.addEventListener("touchend", stopDefault, false);
  // ジェスチャーイベントの初期化
  document.addEventListener("gesturestart", stopDefault, false);
  document.addEventListener("gesturechange", stopDefault, false);
  document.addEventListener("gestureend", stopDefault, false);

  $("*")
  .on("touchstart", function(e) {
    Y1 = e.originalEvent.touches[0].clientY;
  })
  .on("touchmove", function(e) {
    Y2 = e.originalEvent.touches[0].clientY;
    if(Math.abs(Y1 - Y2) < 5){
      e.preventDefault();
    }
  });

  /*************************************
  Socket.io
  *************************************/
  var socket = io.connect("http://10.70.86.212:3000");

  socket.on("connected",function(){
    console.log("接続されました。");
    });

  socket.on("result_from_server",function(data) {

    var _canvas = document.createElement('canvas');
    _canvas.width  = 28;
    _canvas.height = 28;
    var _ctx = _canvas.getContext('2d');
    _ctx.drawImage(canvas,0,0,400,400,0,0,28,28);

    var canvas_r = document.getElementById('input');

    var ctx2 = canvas_r.getContext('2d');
    ctx2.drawImage(_canvas,0,0,28,28,0,0,200,200);

    var result = data.split(",")
    var result0 = result[0].split("[")
    $("#result0").text(result0[1]);
    $("#result1").text(result[1]);
    $("#result2").text(result[2]);
    $("#result3").text(result[3]);
    $("#result4").text(result[4]);
    $("#result5").text(result[5]);
    $("#result6").text(result[6]);
    $("#result7").text(result[7]);
    $("#result8").text(result[8]);
    $("#result9").text(result[9]);
  });

  /*************************************
  Canvas
  *************************************/
  // キャンバス取得
  var canvas = document.getElementById('paint');

  if (!canvas || !canvas.getContext) {
    console.log("no canvases");
    return false;
  }
  var ctx = canvas.getContext('2d');

  // 前座標，後座標
  var startX, startY, x, y;

  //フラグ
  var isDrawing = false;

  //画面初期化
  ctx.beginPath();
  ctx.fillStyle = 'rgb(255, 255, 255)';
  ctx.fillRect(0, 0, 336, 336);

  // 描画

  var start = function(event){
    isDrawing = true;
    startX = event.pageX - $(this).offset().left  ;
    startY = event.pageY - $(this).offset().top  ;
  }

  var move = function(event) {
    if(!isDrawing) return;
    x = event.pageX - $(this).offset().left ;
    y = event.pageY - $(this).offset().top  ;

    ctx.beginPath();
    ctx.moveTo(startX,startY);
    ctx.lineTo(x,y);
    ctx.lineWidth = 30;
    ctx.lineCap = "round";
    ctx.stroke();
    startX = x;
    startY = y;
  }

  var end  = function(event) {
    isDrawing = false;
  }

  $('#paint')
  .mousedown(start)
  .mousemove(move)
  .mouseup(end)
  .mouseleave(end);

  // $('#paint')
  // .touchstart(start)
  // .touchmove(move)
  // .touchend(end)
  // .touchcancel(end);
  canvas.addEventListener("touchstart",start);
  canvas.addEventListener("touchmove",move);
  canvas.addEventListener("touchend",move);


  /*************************************
  Button
  *************************************/

  //クリアボタン{
  $('#clear').click(function(){
    console.log("画面をクリアします。");
    ctx.beginPath();
    ctx.fillStyle = 'rgb(255, 255, 255)';
    ctx.fillRect(0, 0, 400, 400);
  });

  //送信ボタン
  $('#send').click(function(){
    console.log("画像を送信します。");

    var _canvas = document.createElement('canvas');
    _canvas.width  = 28;
    _canvas.height = 28;
    var _ctx = _canvas.getContext('2d');
    _ctx.drawImage(canvas,0,0,336,336,0,0,28,28);

    var resized_image = _canvas.toDataURL('image/png');
    console.log(resized_image);
    socket.emit("image_from_client", resized_image);
  });

});//end of jQuery
