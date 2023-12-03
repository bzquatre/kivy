from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import pyrebase,json

Firebase = pyrebase.initialize_app({
        "apiKey": "AIzaSyDrCnFFzoIQ5Y7Vh-PncyHq-m2t50CsWa0",
        "authDomain": "cvbz4-7dfdc.firebaseapp.com",
        "databaseURL": "https://cvbz4-7dfdc-default-rtdb.firebaseio.com",
        "projectId": "cvbz4-7dfdc",
        "storageBucket": "cvbz4-7dfdc.appspot.com",
        "messagingSenderId": "832945689098",
        "appId": "1:832945689098:web:87a98f3c115eedb92945f3",
        "measurementId": "G-0LLXZGCDJG"
    })
class SkillItem(BoxLayout):
    name = ""
    level = 0
class LoginScreen(Screen):
    def toggle_password_visibility(self, *args):
        password_input = self.ids.password_input
        password_input.password = not password_input.password
        password_input.icon_right = "eye" if password_input.password else "eye-off"
class MainScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.db=Firebase.database()
    def on_enter(self, *args):
        data = self.db.child("Fr").get()
        self.ids.name_cv.text=data.val()['name']
        self.ids.job_cv.text=data.val()['Job']
        self.ids.email_cv.text=data.val()['Email']
        self.ids.phone_cv.text=data.val()['Phone']
        self.ids.website_cv.text=data.val()['Site']
class MainApp(MDApp):
    def build(self):
        self.auth = Firebase.auth()
        Builder.load_file("main.kv")
        try:
            refreshToken=json.load(open("user.json"))["refreshToken"]
            self.user = self.auth.refresh(refreshToken)
        except  Exception as e:
            print(e)
            
        else:
            self.root.current='main'
    
    def login(self,email,password):
        self.auth=Firebase.auth()
        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
            with open("user.json", 'w') as json_file:
                json.dump(user, json_file, indent=4)
        except Exception as e:
            pass
        else:
            self.root.transition.direction = 'left'
            self.root.current = 'main'

    def logout(self):
        self.auth.current_user = None  # Clear the current user
        self.root.transition.direction = 'right'
        self.root.current = 'login'
        with open("user.json","w") as user:
            user.write('')

    

if __name__ == '__main__':
    MainApp().run()