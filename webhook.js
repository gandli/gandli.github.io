const http = require('http')
const createHandler = require('github-webhook-handler') //这个插件使用前先安装 npm i github-webhook-handler -D

function run_cmd (cmd, args, callback) {
  var spawn = require('child_process').spawn;
  var child = spawn(cmd, args);
  var resp = "";
  child.stdout.on('data', function (buffer) {
    resp += buffer.toString();
  });
  child.stdout.on('end', function () {
    console.log('Deploy 完成')
    callback(resp)
  });
}

const handler = createHandler({
  path: '/resume-hook', // url 后缀
  secret: 'webhook' // 你的密码
})

// ?? 注意要在阿里云安全组里面添加开放端口
// ?? 还要在ubuntu防火墙关闭对应端口
http.createServer((req, res) => {
  handler(req, res, err => {
    res.statusCode = 404
    res.end('no such location')
  })
}).listen(7778, () => {
  console.log('Webhook listen at 7778')
})

handler.on('error', err => {
  console.error('Error', err.message)
})

// 拦截push，执行 Deploy 脚本
handler.on('push', function (event) {
  console.log('Received a push event for %s to %s', event.payload.repository.name, event.payload.ref);
  // 分支判断
  if (event.payload.ref === 'refs/heads/master') {
    console.log('deploy master..')
    run_cmd('sh', ['./autoDeploy.sh'], function (text) { console.log(text) });
  }
})