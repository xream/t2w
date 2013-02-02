#!/usr/bin/env python
# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

from weibo import APIClient
import time
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from configobj import ConfigObj

config = ConfigObj('config.ini')

class Weibo(object):
    """docstring for Weibo"""

    def __init__(self):
        self.app_key = config['weibo']['app_key']
        self.app_secret = config['weibo']['app_secret']
        self.callback_url = config['weibo']['callback_url']
        self.client = APIClient(app_key=self.app_key, app_secret=self.app_secret, redirect_uri=self.callback_url)
        self.access_token = config['weibo']['access_token']
        self.expires_in = config['weibo']['expires_in']
        if self.access_token == '' or self.expires_in == '' or self.expires_in <= time.time():
            self.get_token()
        self.client.set_access_token(self.access_token, self.expires_in)

    def get_token(self):
        url = self.client.get_authorize_url()
        code = raw_input(('\n').join(('open the url in your browser:', url, 'input the code:', '> ')))
        r = self.client.request_access_token(code)
        self.access_token = r.access_token
        self.expires_in = r.expires_in
        config['weibo']['access_token'] = self.access_token
        config['weibo']['expires_in'] = self.expires_in
        config.write()

    def update(self, status, pic=None):
        if not pic:
            self.client.statuses.update.post(status=status)
        else:
            f = open(pic, 'rb')
            self.client.statuses.upload.post(status=status, pic=f)
            f.close()

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream. 
    This is a basic listener that just prints received tweets to stdout.

    """
    # def on_data(self, data):
    #     print data
    #     return True
    def on_status(self, status):
        try:
            t = str(status.text)
            # filter
            if "#" not in t and "@" not in t:
                Weibo().update(t)
                print t
        except Exception, e:
            print e
        return True

    def on_delete(self, status_id, user_id):
        return True

    def on_limit(self, track):
        return True

    def on_error(self, status_code):
        return True

    def on_timeout(self):
        return True

if __name__ == '__main__':
    Weibo()

    consumer_key = config['twitter']['consumer_key']
    consumer_secret = config['twitter']['consumer_secret']
    access_token = config['twitter']['access_token']
    access_token_secret = config['twitter']['access_token_secret']
    user_id = config['twitter']['user_id']

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(follow=[user_id])
