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
from kivy.config import Config
Config.set('graphics', 'resizable', False)


class TwitterAPIUI(App):
    def build(self):

        Window.size = (600, 400)

        self.title = 'Twitter API'
        self.root = RelativeLayout()
        self.CONSUMER_KEY = None
        self.CONSUMER_SECRET = None
        self.ACCESS_TOKEN = None
        self.ACCESS_TOKEN_SECRET = None

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
        self.buttonLayout = BoxLayout(orientation='vertical', spacing=5,  size_hint=(.2, .2),
                                      pos_hint={'x': .79, 'y': .75})
        self.getFollowers = Button(text="Get Followers")
        self.getFollowing = Button(text="Get Following")
        self.newTweet = Button(text="New Tweet")

        self.root.add_widget(self.buttonLayout)
        return self.root

    def subCredentials(self, instance):
        if self.ACCESS_TOKEN and self.ACCESS_TOKEN_SECRET and self.CONSUMER_KEY and self.CONSUMER_SECRET:
            self.popup.dismiss()
            self.buttonLayout.add_widget(self.newTweet)
            self.buttonLayout.add_widget(self.getFollowers)
            self.buttonLayout.add_widget(self.getFollowing)
        else:
            print('Credentials has not been set')


TwitterAPIUI().run()
