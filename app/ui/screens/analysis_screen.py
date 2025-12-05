from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty
from kivy.clock import Clock
import threading

class AnalysisScreen(MDScreen):
    dataset_name = StringProperty("No dataset selected")
    dataset_info = StringProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'analysis'
    
    def on_enter(self):
        """Update display - run in background"""
        threading.Thread(target=self._update_display_background, daemon=True).start()
    
    def _update_display_background(self):
        """Update display in background"""
        try:
            app = MDApp.get_running_app()
            
            if not app.current_dataset_name:
                Clock.schedule_once(lambda dt: self._set_empty_state())
                return
            
            if app.current_dataset_name not in app.all_dataframes:
                Clock.schedule_once(lambda dt: self._set_not_found_state(app.current_dataset_name))
                return
            
            # Dataset exists - prepare info
            df = app.all_dataframes[app.current_dataset_name]
            info = app.dataset_info.get(app.current_dataset_name, {})
            
            # Create simple info (fast)
            analysis = f"📊 **{app.current_dataset_name}**\n\n"
            analysis += f"**Records:** {len(df):,}\n"
            analysis += f"**Metrics:** {len(df.columns)}\n"
            analysis += f"**Type:** {info.get('type', 'Educational Data')}\n\n"
            
            # Add columns preview
            analysis += "**Columns:**\n"
            for i, col in enumerate(df.columns[:8], 1):
                analysis += f"{i}. {col}\n"
            if len(df.columns) > 8:
                analysis += f"... and {len(df.columns)-8} more\n\n"
            
            # Update UI on main thread
            Clock.schedule_once(
                lambda dt, name=app.current_dataset_name, text=analysis: 
                self._update_ui(name, text)
            )
            
        except Exception as e:
            print(f"❌ Analysis update error: {e}")
    
    def _set_empty_state(self):
        """Set empty state"""
        self.dataset_name = "No dataset selected"
        self.dataset_info = "Please select a dataset from the dashboard."
    
    def _set_not_found_state(self, dataset_name):
        """Set not found state"""
        self.dataset_name = dataset_name
        self.dataset_info = f"Dataset '{dataset_name}' not found or still loading.\n\nPlease wait or try again."
    
    def _update_ui(self, name, text):
        """Update UI on main thread"""
        self.dataset_name = name
        self.dataset_info = text
    
    def ask_about_data(self):
        """Go to chat screen"""
        app = MDApp.get_running_app()
        app.sm.current = 'chat'
    
    def go_back(self):
        """Return to dashboard"""
        app = MDApp.get_running_app()
        app.sm.current = 'dashboard'
    
    def show_visualization(self):
        """Placeholder for visualization"""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton
        
        dialog = MDDialog(
            title="Visualization",
            text="Chart generation coming soon!\n\nFor now, ask AI to describe trends.",
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()
    
    def export_data(self):
        """Placeholder for export"""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton
        
        dialog = MDDialog(
            title="Export",
            text="Export functionality coming soon!",
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()