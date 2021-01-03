
from dotenv import load_dotenv
from API import Twitter
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


BEARER_TOKEN = os.getenv("Token")
followers = []
api = None
tweet = None


def login():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api


def menu():
    myMenu = ('New Tweet', 'My Profile', 'Get Feed',
              'Following', 'Followers', 'Get Non Followers')
    option = range(0, 4)
    print("What do you want to do?")
    for index, value in enumerate(myMenu):
        print("%d: %s" % (index, value))
    print("\nType 'exit' to quit")


def save_file(filename, content):
    with open("%s.json" % (filename), 'w') as outfile:
        json.dump(content, outfile)
        # Overwrite File


def get_followers():
    global api
    followers = tweepy.Cursor(api.followers).items()
    #followers = followers[1]._json
    # print(followers)
    formatted = []
    for follower in followers:
        formatted.append(follower._json)
        print(follower._json)
        print("**********************")
    save_file('followers', formatted)
    print('Currently have %d followers'%(len(formatted)))

def get_following():
    global api
    followings = tweepy.Cursor(api.friends).items()
    #print(followings)
    #followers = followers[1]._json
    # print(followers)
    formatted = []
    for following in followings:
        formatted.append(following._json)
        print(following)
        print("**********************")
    save_file('following', formatted)
    print('Currently following %d users'%(len(formatted)))

def unfollow(id):
    global api
    response = api.destroy_friendship(id)
    print(response)

def get_feed():
    global api
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)


def followers_menu():
    myMenu = ('Get Followers', 'View Followers')
    print("\n\n**Followers Menu**")
    for index, value in enumerate(myMenu):
        print("4%d: %s" % (index, value))
    print("4%d: %s" % (len(myMenu), "Back"))


def following_menu():
    myMenu = ('Get Following', 'View Following')
    print("\n\n**Followers Menu**")
    for index, value in enumerate(myMenu):
        print("3%d: %s" % (index, value))
    print("3%d: %s" % (len(myMenu), "Back"))


def load_file(filename):
    with open("%s.json" % (filename)) as json_file:
        data = json.load(json_file)
        return data

def load_following():
    followings = load_file('following')
    for following in followings:
        print(following)

def load_followers():
    followers = load_file('followers')
    for follower in followers:
        print(follower)

def new_tweet():
    global tweet,api
    
    print("\n\n**New Tweet Menu**")

    tweet = input("What's happening?\nType: 01 to cancel\n")
    if tweet == '01':
        menu()
    else:
        response = api.update_status(tweet)
        tweet = response._json.text
        print("Successfully tweeted '%s' "%(tweet))
        menu()

def Diff(li1, li2):
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))
 


def my_profile():
    global api
    me = api.me()
    print('**Account Information**\n')
    id = me._json['id']
    username = me._json['screen_name']
    name = me._json['name']
    bio = me._json['description']
    followers = me._json['followers_count']
    following = me._json['friends_count']
    location = me._json['location']
    tweets = me._json['statuses_count']
    #retweets = me._json['retweets_count']
    link = me._json['url']
    likes = me._json['favourites_count']
    private = me._json['protected']
    print("id:%d\nusername:%s\nDisplay Name:%s\nPrivate:%s\nBio:%s\nFollowers:%d\nFollowing:%d\nLocation:%s\nTweets:%d\nLink:%s\nLikes:%d\n"%(id,username,name,private,bio,followers,following,location,tweets,link,likes))
    

def non_followers_menu():
    myMenu = ('View non Followers', 'Unfollow non followers')
    print("\n\n**Non Followers Menu**")
    for index, value in enumerate(myMenu):
        print("5%d: %s" % (index, value))
    print("5%d: %s" % (len(myMenu), "Back\n"))

def get_non_followers():
    followers_ids = []
    following_ids = []

    followers_list=load_file('followers')
    following_list=load_file('following')

    for follower in followers_list:
        followers_ids.append(follower['id'])

    for following in following_list:
        following_ids.append(following['id'])

    non_followers_list = Diff(following_ids,followers_ids)

    print("Found %d non followers "%(non_followers_list))

    return non_followers_list

def unfollow_non_followers():
    non_followers_list = get_non_followers()
    for non_follower in non_followers_list:
        print(non_follower)
        unfollow(non_follower)
        timeToSleep=random.randint(5,10)
        time.sleep(timeToSleep)
        #Delay the number of request intentionally


    #print(non_followers_list)


def main():

    
    
    # Access Global Variables

    option = 1
    global followers, api
    
    api = login()

    try:
        while(option != 'exit'):
            menu()
            option = input()
            if option == '0':
                print('New Tweet')
                new_tweet()
            elif option == '1':
                my_profile()
            elif option == '2':
                get_feed()
            elif option == '3':
                following_menu()
                option = input()

            elif option == '30':
                get_following()
                following_menu()
                option = input()
            elif option == '31':
                get_following()
                following_menu()
                option = input()
            elif option == '32':
                load_following()
                following_menu()
                option = input()
            elif option == '4':
                followers_menu()
                option = input()
            elif option == '41':
                get_followers()
                followers_menu()
                option = input()

            elif option == '42':
                load_followers()
                followers_menu()
                option = input()
            elif option == '5':
                non_followers_menu()
            elif option == '50':
                get_non_followers()
                non_followers_menu()
                option = input()
            elif option == '51':
                unfollow_non_followers()
                non_followers_menu()
                option = input()

            elif option == '10':
                get_following()
                following_menu()
                option = input()
            elif option == '20':
                get_followers()
                followers_menu()
                option = input()
            elif option == '42' or option == '32' or option == '52' :
                menu()
                option = input()
    
        
    except KeyboardInterrupt:
        print('Have a nice day!')

        
    
    

if __name__ == "__main__":
    main()
