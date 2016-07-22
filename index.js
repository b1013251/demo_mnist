var http = require('http');
var express = require('express');
var async = require('async');
var app = express();

var server = http.Server(app);

var socketIO = require('socket.io');
var io = socketIO.listen(server);
var fs = require('fs');

// static page
app.use(express.static("public"));
app.use(express.static("images"));

// websocket
io.sockets.on('connection', function(socket) {
  console.log("クライアントに接続されました。");

  socket.on('image_from_client',function(data){
    console.log("データを受け取りました。");
    var socketid = socket.id.split("#");

    //async
    async.series([
      //画像保存
      function(callback) {
        console.log("イメージ保存");
        var image = data.replace(/^data:image\/png;base64,/, "");
        fs.writeFile(
          './images/' + socketid[1] + '.png',
          image,'base64',
          function (err) {
            if (err != null) {
              console.log("error" + err);
            }
          });
          callback(null,null);
        },
        //python実行
        function(callback) {
          console.log("判別中…");
          var exec = require('child_process').exec;
          exec("python ./python/load_model_ex.py " + socketid[1] + ".png", function(err, stdout, stderr){
            if (err) { console.log(err); }
            callback(null,stdout);
          });
        }
        //結果を返す
      ],function (err, values) {
        if (err) console.error(err);
        else console.log("解析終了");
        socket.emit("result_from_server",values[1]);
      });
    });

    //画像削除
    socket.on('disconnect',function() {
      var socketid = socket.id.split("#");
      var exec = require('child_process').exec;
      exec("rm -f ./images/" + socketid[1] + ".png", function(err, stdout, stderr){
        if (err) { console.log(err); }
        console.log("画像削除");
      });
    });
  });

  // listen
  server.listen(3000 ,function(){
	  var host = server.address().address;
		var port = server.address().port;

	  console.log('Example app listening at http://%s:%s', host, port);
    console.log("サーバ起動中…")
  });
