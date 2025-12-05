from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'login'
        
        # TEST: Add a simple colored background
        from kivy.graphics import Color, Rectangle
        
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Light gray background
            self.rect = Rectangle(pos=self.pos, size=self.size)
        
        # Bind to update rectangle when size changes
        self.bind(pos=self._update_rect, size=self._update_rect)
    
    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    # ... rest of your methods ...
    
    def on_enter(self):
        """Called when screen becomes active"""
        print("Login screen loaded")
    
    def login_with_google(self):
        """Handle Google login"""
        app = MDApp.get_running_app()
        print("Attempting Google login...")
        
        # For now, just go to dashboard
        app.sm.current = 'dashboard'
    
    def skip_login(self):
        """Skip login for testing"""
        app = MDApp.get_running_app()
        app.sm.current = 'dashboard'