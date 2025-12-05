import os

kv_files = {
    "login_screen.kv": """<LoginScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        padding: "40dp"
        spacing: "20dp"
        
        MDLabel:
            text: "🔐 EduLens Login"
            font_style: "H4"
            halign: "center"
            theme_text_color: "Primary"
            size_hint_y: None
            height: self.texture_size[1]
        
        MDLabel:
            text: "Connect to Google Drive to access your educational datasets"
            font_style: "Body1"
            halign: "center"
            theme_text_color: "Secondary"
            size_hint_y: None
            height: self.texture_size[1]
        
        Widget:
            size_hint_y: 0.3
        
        MDRaisedButton:
            text: "Sign in with Google"
            icon: "google"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.8
            on_release: root.login_with_google()
            md_bg_color: "#4285F4"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
        
        MDFlatButton:
            text: "Skip for now (Test Mode)"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.6
            on_release: root.skip_login()
            theme_text_color: "Secondary"
        
        Widget:
            size_hint_y: 0.4
        
        MDLabel:
            text: "SDG 4: Quality Education"
            font_style: "Caption"
            halign: "center"
            theme_text_color: "Secondary"
            size_hint_y: None
            height: self.texture_size[1]
""",
    
    "dashboard_screen.kv": """<DatasetListItem>:
    text: "Dataset"
    on_release: app.root.get_screen('dashboard').select_dataset(self.text)

<DashboardScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "EduLens Datasets"
            elevation: 4
            right_action_items: [["chat", lambda x: root.open_chat()], ["refresh", lambda x: root.refresh_datasets()]]
        
        MDBoxLayout:
            orientation: 'vertical'
            padding: "10dp"
            spacing: "10dp"
            
            MDLabel:
                text: "📁 Dataset Repository"
                font_style: "H6"
                size_hint_y: None
                height: self.texture_size[1]
                padding: ["10dp", "10dp"]
            
            MDLabel:
                text: root.status_text
                font_style: "Caption"
                theme_text_color: "Secondary"
                size_hint_y: None
                height: self.texture_size[1]
                padding: ["10dp", 0]
            
            ScrollView:
                MDList:
                    id: dataset_list
                    
                    canvas.before:
                        Color:
                            rgba: 0.95, 0.95, 0.95, 1
                        Rectangle:
                            pos: self.pos
                            size: self.size
            
            MDRaisedButton:
                text: "📤 Upload New Dataset"
                icon: "cloud-upload"
                pos_hint: {"center_x": 0.5}
                size_hint_x: 0.8
                md_bg_color: app.theme_cls.primary_color
            
            Widget:
                size_hint_y: None
                height: "10dp"
""",
    
    "analysis_screen.kv": """<AnalysisScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "Data Analysis"
            elevation: 4
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
            right_action_items: [["chart-box", lambda x: print("Generate chart")]]
        
        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: "20dp"
                spacing: "15dp"
                size_hint_y: None
                height: self.minimum_height
                
                MDLabel:
                    text: f"📊 {root.dataset_name}"
                    font_style: "H5"
                    size_hint_y: None
                    height: self.texture_size[1]
                    theme_text_color: "Primary"
                
                MDCard:
                    orientation: 'vertical'
                    padding: "15dp"
                    spacing: "10dp"
                    size_hint_y: None
                    height: "200dp"
                    elevation: 2
                    
                    MDLabel:
                        text: "Dataset Information"
                        font_style: "H6"
                        size_hint_y: None
                        height: self.texture_size[1]
                    
                    ScrollView:
                        MDLabel:
                            text: root.dataset_info
                            font_style: "Body1"
                            size_hint_y: None
                            height: self.texture_size[1]
                            padding: ["10dp", 0]
                
                MDRaisedButton:
                    text: "🤖 Ask AI About This Data"
                    icon: "robot"
                    pos_hint: {"center_x": 0.5}
                    on_release: root.ask_about_data()
                    md_bg_color: app.theme_cls.primary_color
                
                Widget:
                    size_hint_y: None
                    height: "20dp"
""",
    
    "chat_screen.kv": """<ChatScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "EduLens AI Assistant"
            elevation: 4
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
        
        ScrollView:
            do_scroll_x: False
            
            MDLabel:
                text: root.chat_history
                font_style: "Body1"
                size_hint_y: None
                height: self.texture_size[1]
                padding: ["20dp", "20dp"]
                valign: "top"
                halign: "left"
        
        MDBoxLayout:
            size_hint_y: None
            height: "60dp"
            padding: ["10dp", "5dp"]
            spacing: "10dp"
            
            MDTextField:
                id: input_field
                hint_text: "Ask about your educational data..."
                mode: "rectangle"
                size_hint_x: 0.8
                on_text_validate: root.send_message(self.text)
            
            MDRaisedButton:
                text: "Send"
                size_hint_x: 0.2
                on_release: root.send_message(app.root.get_screen('chat').ids.input_field.text)
                md_bg_color: app.theme_cls.primary_color
"""
}

# Create/overwrite KV files
for filename, content in kv_files.items():
    filepath = os.path.join("app", "ui", "screens", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {filepath}")

print("✅ KV files created successfully!")