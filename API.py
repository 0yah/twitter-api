
from dotenv import load_dotenv
import os
import tweepy

import json
import time
import random

# Load the Keys from the .env file in the project directory
load_dotenv()

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")


class Twitter():

    def __init__(self,CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET):
        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)


    def get_followers(self):
        followers = tweepy.Cursor(self.api.followers).items()
        #followers = followers[1]._json
        # print(followers)
        formatted = []
        for follower in followers:
            formatted.append(follower._json)
            print(follower._json)
            print("**********************")
        print('Currently have %d followers' % (len(formatted)))
        return formatted

    def get_following(self):

        # The cursor fetches all following
        followings = tweepy.Cursor(self.api.friends).items()
        formatted = []
        for following in followings:
            formatted.append(following._json)
            print(following._json)
            print("**********************")
        print('Currently have %d followers' % (len(formatted)))
        return formatted

    def new_tweet(self, tweet):
        try:
            response = self.api.update_status(tweet)
            tweet = response._json.text
            return (True, tweet)
        except tweepy.RateLimitError:
            return (False)

    def new_tweet_media(self, tweet, path=None):
        try:
            if path == None:
                print('No File specified!')
                self.new_tweet(tweet)
                return
            result = self.api.update_with_media(filename=path, status=tweet)
            return (True, result)
        except tweepy.RateLimitError:
            return (False)

    def follow(self, id):
        try:
            result = self.api.create_friendship(id)
            return (False, result)
        except tweepy.RateLimitError:
            print("Try again later")

    def unfollow(self, id):
        try:
            result = self.api.destroy_friendship(id)
            return (False, result)
        except tweepy.RateLimitError:
            return (False)

    def get_feed(self):
        try:
            feed = tweepy.Cursor(self.api.home_timeline).items()
            return (True, feed)
        except tweepy.RateLimitError:
            return (False)

    def get_profile(self):
        try:
            me = self.api.me()
            id = me._json['id']
            username = me._json['screen_name']
            name = me._json['name']
            bio = me._json['description']
            followers = me._json['followers_count']
            following = me._json['friends_count']
            location = me._json['location']
            tweets = me._json['statuses_count']
            link = me._json['url']
            likes = me._json['favourites_count']
            private = me._json['protected']
            info = {
                id, username, name, bio, followers, following, location, tweets, link, likes, private
            }
            return (True, info)
        except tweepy.RateLimitError:
            return (False)

    def update_profile(self, name="", location="",link="", bio=""):
        try:
            result = self.api.update_profile(name,link,location,bio)
            return (True,result)
        except tweepy.RateLimitError:
            return (False)

    def update_profile_pic(self, path=None):
        try:
            if path != None:
                result = self.api.update_profile_image(path)
                return (True,result)
            return(False)
        except tweepy.RateLimitError:
            return (False)
