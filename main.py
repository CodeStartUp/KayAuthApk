from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock
from kivy.utils import platform
from datetime import datetime
import time
import sys
from KeyAuth import KeyAuth

# Initialize authentication
auth = KeyAuth()

Builder.load_string('''
<LoginScreen>:
    orientation: 'vertical'
    padding: 30
    spacing: 15
    
    BoxLayout:
        orientation: 'vertical'
        spacing: 15
        size_hint_y: None
        height: dp(400)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        
        Label:
            text: 'Login'
            font_size: '24sp'
            bold: True
            size_hint_y: None
            height: dp(40)
            
        TextInput:
            id: username
            hint_text: 'Username'
            size_hint_y: None
            height: dp(50)
            multiline: False
            
        TextInput:
            id: password
            hint_text: 'Password'
            password: True
            size_hint_y: None
            height: dp(50)
            multiline: False
            
        Button:
            text: 'Login'
            size_hint_y: None
            height: dp(50)
            on_press: root.attempt_login()
            background_color: 0, 0.5, 1, 1
            
        Label:
            id: login_status
            text: ''
            color: 1, 0, 0, 1
            size_hint_y: None
            height: dp(30)
            
        Button:
            text: 'Register with License'
            size_hint_y: None
            height: dp(50)
            on_press: root.manager.current = 'register'
            
<RegisterScreen>:
    orientation: 'vertical'
    padding: 30
    spacing: 15
    
    BoxLayout:
        orientation: 'vertical'
        spacing: 15
        size_hint_y: None
        height: dp(500)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        
        Label:
            text: 'Register'
            font_size: '24sp'
            bold: True
            size_hint_y: None
            height: dp(40)
            
        TextInput:
            id: license_key
            hint_text: 'License Key'
            size_hint_y: None
            height: dp(50)
            multiline: False
            
        TextInput:
            id: reg_username
            hint_text: 'Username'
            size_hint_y: None
            height: dp(50)
            multiline: False
            
        TextInput:
            id: reg_password
            hint_text: 'Password (min 6 chars)'
            password: True
            size_hint_y: None
            height: dp(50)
            multiline: False
            
        TextInput:
            id: confirm_password
            hint_text: 'Confirm Password'
            password: True
            size_hint_y: None
            height: dp(50)
            multiline: False
            
        Button:
            text: 'Register'
            size_hint_y: None
            height: dp(50)
            on_press: root.attempt_register()
            background_color: 0, 0.7, 0, 1
            
        Label:
            id: reg_status
            text: ''
            color: 1, 0, 0, 1
            size_hint_y: None
            height: dp(30)
            
        Button:
            text: 'Back to Login'
            size_hint_y: None
            height: dp(50)
            on_press: root.manager.current = 'login'
            
<MainScreen>:
    orientation: 'vertical'
    padding: 20
    spacing: 15
    
    BoxLayout:
        orientation: 'vertical'
        spacing: 15
        
        Label:
            text: 'Welcome, ' + root.username
            font_size: '20sp'
            bold: True
            size_hint_y: None
            height: dp(40)
            
        Label:
            text: 'IP: ' + root.ip_address
            size_hint_y: None
            height: dp(30)
            
        Label:
            text: 'Login Time: ' + root.login_time
            size_hint_y: None
            height: dp(30)
            
        Button:
            text: 'Check Subscription'
            size_hint_y: None
            height: dp(50)
            on_press: root.show_subscription()
            
        Button:
            text: 'Logout'
            size_hint_y: None
            height: dp(50)
            on_press: root.logout()
            background_color: 1, 0, 0, 1
            
<SubscriptionScreen>:
    orientation: 'vertical'
    padding: 30
    spacing: 15
    
    BoxLayout:
        orientation: 'vertical'
        spacing: 15
        size_hint_y: None
        height: dp(300)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        
        Label:
            text: 'Subscription Status'
            font_size: '24sp'
            bold: True
            size_hint_y: None
            height: dp(40)
            
        Label:
            text: 'User: ' + root.username
            size_hint_y: None
            height: dp(30)
            
        Label:
            text: 'Plan: Premium'
            size_hint_y: None
            height: dp(30)
            
        Label:
            text: 'Expires: 2024-12-31'
            size_hint_y: None
            height: dp(30)
            
        Label:
            text: 'Status: Active'
            size_hint_y: None
            height: dp(30)
            color: 0, 0.7, 0, 1
            
        Button:
            text: 'Back'
            size_hint_y: None
            height: dp(50)
            on_press: root.manager.current = 'main'
''')

class LoginScreen(Screen):
    def attempt_login(self):
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()
        
        if not username or not password:
            self.ids.login_status.text = "Username and password required"
            return
            
        self.ids.login_status.text = "Authenticating..."
        
        # Schedule the login attempt to prevent UI freeze
        Clock.schedule_once(lambda dt: self._perform_login(username, password), 0.1)
    
    def _perform_login(self, username, password):
        success, message = auth.login(username, password)
        if success:
            self.ids.login_status.text = ""
            self.manager.current = 'main'
            main_screen = self.manager.get_screen('main')
            main_screen.update_user_info(username)
        else:
            self.ids.login_status.text = message

class RegisterScreen(Screen):
    def attempt_register(self):
        license_key = self.ids.license_key.text.strip()
        username = self.ids.reg_username.text.strip()
        password = self.ids.reg_password.text.strip()
        confirm = self.ids.confirm_password.text.strip()
        
        if not license_key:
            self.ids.reg_status.text = "License key required"
            return
        if not username:
            self.ids.reg_status.text = "Username required"
            return
        if not password or len(password) < 6:
            self.ids.reg_status.text = "Password must be 6+ characters"
            return
        if password != confirm:
            self.ids.reg_status.text = "Passwords don't match"
            return
            
        self.ids.reg_status.text = "Processing..."
        
        # Schedule the registration attempt
        Clock.schedule_once(lambda dt: self._perform_register(license_key, username, password), 0.1)
    
    def _perform_register(self, license_key, username, password):
        valid, msg = auth.check_license_validity(license_key)
        if not valid:
            self.ids.reg_status.text = f"License Error: {msg}"
            return
            
        success, message = auth.register_with_license(license_key, username, password)
        if success:
            self.ids.reg_status.text = ""
            self.manager.current = 'main'
            main_screen = self.manager.get_screen('main')
            main_screen.update_user_info(username)
        else:
            self.ids.reg_status.text = message

class MainScreen(Screen):
    username = StringProperty("")
    ip_address = StringProperty("")
    login_time = StringProperty("")
    
    def update_user_info(self, username):
        self.username = username
        self.ip_address = auth.get_ip_address()
        self.login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def show_subscription(self):
        self.manager.current = 'subscription'
        sub_screen = self.manager.get_screen('subscription')
        sub_screen.username = self.username
    
    def logout(self):
        auth.logout()
        self.manager.current = 'login'
        self.manager.get_screen('login').ids.username.text = ""
        self.manager.get_screen('login').ids.password.text = ""

class SubscriptionScreen(Screen):
    username = StringProperty("")

class AuthApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SubscriptionScreen(name='subscription'))
        
        # Check if already logged in
        if auth.is_authenticated():
            sm.current = 'main'
            sm.get_screen('main').update_user_info(auth.get_username())
        else:
            sm.current = 'login'
            
        return sm

if __name__ == '__main__':
    try:
        # Handle Android permissions
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.INTERNET])
            
        AuthApp().run()
    except Exception as e:
        print(f"Critical error: {str(e)}")
        sys.exit(1)