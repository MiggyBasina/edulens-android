from kivymd.app import MDApp
from kivymd.uix.label import MDLabel

class TestApp(MDApp):
    def build(self):
        return MDLabel(text="✅ EduLens Mobile is working!", halign="center")

if __name__ == "__main__":
    TestApp().run()