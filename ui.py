from API import Twitter
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.recycleview import RecycleView

from kivy.config import Config
Config.set('graphics', 'resizable', False)

Builder.load_string('''
<RV>:
    viewclass: 'Label'
    RecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
''')


class RV(RecycleView):
    def __init__(self, data, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = data


class TwitterAPIUI(App):

    def credentialPopUp(self):
        # Pop up layout
        self.credentialsRootLayout = AnchorLayout(
            anchor_x='center', anchor_y='center', padding=(5, 5, 5, 5))
        # Content Layout
        self.credentialsContentLayout = BoxLayout(
            orientation='vertical', spacing=20)
        self.consumerKey = TextInput(
            hint_text="CONSUMER KEY")
        self.consumerSecret = TextInput(
            hint_text="CONSUMER SECRET KEY")
        self.accessToken = TextInput(
            hint_text="ACCESS_TOKEN")
        self.accessTokenSecret = TextInput(
            hint_text="ACCESS_TOKEN_SECRET")
        self.submitCreds = Button(text='Login', on_press=self.subCredentials)

        # Add items to the pop up layout
        self.credentialsContentLayout.add_widget(self.consumerKey)
        self.credentialsContentLayout.add_widget(self.consumerSecret)
        self.credentialsContentLayout.add_widget(self.accessToken)
        self.credentialsContentLayout.add_widget(self.accessTokenSecret)
        self.credentialsContentLayout.add_widget(self.submitCreds)

        # Attach the content Layout to the root layout
        self.credentialsRootLayout.add_widget(self.credentialsContentLayout)
        # Create the pop up and attach the layout
        self.popup = Popup(title="Credentials",
                           content=self.credentialsRootLayout, auto_dismiss=False)

        self.popup.open()

    def build(self):

        Window.size = (600, 400)
        self.title = 'Twitter API'
        self.root = RelativeLayout()

        self.CONSUMER_KEY = None
        self.CONSUMER_SECRET = None
        self.ACCESS_TOKEN = None
        self.ACCESS_TOKEN_SECRET = None
        self.twitter = None
        self.followers = []
        self.following = []
        self.non_followers = []

        # Get API credentials First
        # self.credentialPopUp()

        self.buttonLayout = BoxLayout(orientation='vertical', spacing=5,  size_hint=(.2, .2),
                                      pos_hint={'x': .79, 'y': .75})
        self.getFollowers = Button(
            text="Get Followers", on_press=self.get_followers)
        self.getFollowing = Button(
            text="Get Following", on_press=self.get_following)
        self.newTweet = Button(text="New Tweet")

        self.buttonLayout.add_widget(self.newTweet)
        self.buttonLayout.add_widget(self.getFollowers)
        self.buttonLayout.add_widget(self.getFollowing)

        self.data = [{'text': str(x)} for x in range(20)]
        self.itemLayout = RV(self.data)

        self.root.add_widget(RV(self.data))
        self.root.add_widget(self.buttonLayout)
        return self.root

    def get_followers(self):
        self.followers = self.twitter.get_followers()
        # Save the list to a json file
        self.twitter.save_file('followers', self.followers)
        # TODO : Figure out whether how the recyclerview displays dictonaries
        self.itemLayout.data = self.followers
        # Refresh the list
        self.itemLayout.refresh_from_data()

    def get_following(self):
        self.following = self.twitter.get_following()
        # Save the list to a json file
        self.twitter.save_file('following', self.following)
        # TODO : Figure out whether how the recyclerview displays dictonaries
        self.itemLayout.data = self.following
        # Refresh the list
        self.itemLayout.refresh_from_data()

    def subCredentials(self, instance):

        if self.consumerKey.text.find(" ") > -1 or self.consumerSecret.text.find(" ") > -1 or self.accessToken.text.find(" ") > -1 or self.accessTokenSecret.text.find(" ") > -1:
            # TODO : Make pop up message
            print("Token cannot have spaces")
            return
        elif self.consumerKey.text == "" or self.consumerSecret.text == "" or self.accessToken.text == "" or self.accessTokenSecret.text == "":
            # TODO : Make pop up message
            print("Fill in the input spaces")
            return
        else:
            self.ACCESS_TOKEN = self.accessToken.text
            self.ACCESS_TOKEN_SECRET = self.accessTokenSecret.text
            self.CONSUMER_KEY = self.consumerKey.text
            self.CONSUMER_SECRET = self.consumerSecret.text
            self.twitter = Twitter(
                self.CONSUMER_KEY, self.CONSUMER_SECRET, self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)

            self.popup.dismiss()
            self.buttonLayout.add_widget(self.newTweet)
            self.buttonLayout.add_widget(self.getFollowers)
            self.buttonLayout.add_widget(self.getFollowing)


TwitterAPIUI().run()
