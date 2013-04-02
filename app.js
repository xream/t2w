var Twit = require('twit'),
  needle = require('needle'),
  Weibo = require('./Weibo');
  
var weibo = new Weibo();

var T = new Twit({
  consumer_key: '',
  consumer_secret: '',
  access_token: '',
  access_token_secret: '',
})


// http://www.idfromuser.com/
var config = {
  twitter_id: ,
  weibo_username: '',
  weibo_password: ''
}
var stream = T.stream('statuses/filter', { follow: config.twitter_id })

stream.on('disconnect', function (disconnectMessage) {
  console.log('disconnect start')
  console.log(disconnectMessage)
  console.log('disconnect end')
});

stream.on('connect', function (request) {
  console.log('connect start')
  console.log(request)
  console.log('connect end')
});

stream.on('reconnect', function (request, response, connectInterval) {
  console.log('reconnect start')
  console.log(request)
  console.log(response)
  console.log(connectInterval)
  console.log('reconnect end')
});

stream.on('tweet', function (tweet) {
  var content = tweet.text;
  var reg = new RegExp(/@|#/i);
  if (!content.match(reg)) {
    if ('media' in tweet.entities) {
      var media_url = tweet.entities.media[0].media_url+':large';
      content = content.replace(tweet.entities.media[0].url,'').replace('https://','').replace('http://','');
      weibo.access_token(config.weibo_username, config.weibo_password, function(access_token) {
        content = content|| Date.now().toString();
        weibo.upload_url_text(access_token, content, media_url);
      });
    } else {
      content = content.replace('https://','').replace('http://','');
      weibo.access_token(config.weibo_username, config.weibo_password, function(access_token) {
        weibo.update(access_token, content);
      });
    };
  };
});