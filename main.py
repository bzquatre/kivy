from kivymd.app import MDApp
from kivyauth.google_auth import initialize_google,login_google,logout_google
from kivy.lang import Builder
import pyrebase,json
class MainApp(MDApp):
    def build(self):
        self.firebase_config = {
            "apiKey": "AIzaSyBT5zKIrU-i0c9LguVK7CYe8DvT4u3J8Ko",
            "authDomain": "get-cv.firebaseapp.com",
            "projectId": "get-cv",
            "storageBucket": "get-cv.appspot.com",
            "databaseURL": "https://get-cv-default-rtdb.firebaseio.com",
            "messagingSenderId": "116998165824",
            "appId": "1:116998165824:web:5140369efbcef9d0df16a5",
            "measurementId": "G-NKQEY7CZE0"
        }

        self.firebase = pyrebase.initialize_app(self.firebase_config)
        self.auth = self.firebase.auth()
        Builder.load_file("main.kv")
        try:
            refreshToken=json.load(open("user.json"))["refreshToken"]
            user = self.auth.refresh(refreshToken)
        except  Exception as e:
            print(e)
            
        else:
            self.root.current='main'
    

    def toggle_password_visibility(self, *args):
        password_input = self.root.ids.password_input
        password_input.password = not password_input.password
        password_input.icon_right = "eye" if password_input.password else "eye-off"

    def login(self):
        email = self.root.ids.email_input.text
        password = self.root.ids.password_input.text

        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
            with open("user.json", 'w') as json_file:
                json.dump(user, json_file, indent=4)
            self.root.transition.direction = 'left'
            self.root.current = 'main'
        except Exception as e:
            self.root.ids.status_label.text = "Login failed"
    def logout(self):
        self.auth.current_user = None  # Clear the current user
        self.root.transition.direction = 'right'
        self.root.current = 'login'
        with open("user.json","w") as user:
            user.write('')

    

if __name__ == '__main__':
    MainApp().run()