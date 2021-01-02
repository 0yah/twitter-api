
from dotenv import load_dotenv
import os
import tweepy
import json

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
    print("%d: %s" % (len(myMenu), "Exit"))


def save_file(filename, content):
    with open("%s.json" % (filename), 'w') as outfile:
        json.dump(content, outfile)
        # Overwrite File


def get_followers():
    global api
    followers = api.followers()
    #followers = followers[1]._json
    # print(followers)
    formatted = []
    for follower in followers:
        formatted.append(follower._json)
        print(follower._json)
        print("**********************")
    save_file('followers', formatted)


def get_following():
    global api
    followings = api.friends()
    #followers = followers[1]._json
    # print(followers)
    formatted = []
    for following in followings:
        formatted.append(following._json)
        # print(following._json)
        # print("**********************")
    save_file('following', formatted)


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

def new_tweet_menu():
    global tweet,api
    
    print("\n\n**New Tweet Menu**")

    tweet = input("What's happening?\n\nType: 01 to cancel")
    if tweet == '01':
        menu()
    else:
        response = api.update_status(tweet)
        print(response)
        menu()

    

def new_tweet():
    global tweet

def main():
    # Access Global Variables
    option = 1
    global followers, api
    api = login()
    while(option != 'exit'):
        menu()
        option = input()
        if option == 0:
            print('New Tweet')
        elif option == '1':
            print('My Profile')
        elif option == '2':
            get_feed()
        elif option == '3':
            following_menu()
            option = input()
        elif option == '4':
            followers_menu()
            option = input()
        elif option == '5':
            print("Get non Followers")
        elif option == '10':
            get_following()
            following_menu()
        elif option == '20':
            get_followers()
            followers_menu()
        elif option == '42' or option == '32' :
            menu()


if __name__ == "__main__":
    main()
