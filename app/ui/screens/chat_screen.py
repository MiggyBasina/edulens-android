from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty
from datetime import datetime
from kivy.clock import Clock
import threading
import time

class ChatScreen(MDScreen):
    chat_history = StringProperty("🤖 **EduLens AI Assistant**\n\nHello! I can analyze your educational data.\n\nAsk me about student performance, attendance, or teaching strategies.")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "chat"
        self.ai_processing = False
    
    def send_message(self):
        """Send message to AI with proper dataset passing"""
        if self.ai_processing:
            return
            
        if hasattr(self, "ids") and "input_field" in self.ids:
            message = self.ids.input_field.text.strip()
            if not message:
                return
            
            # Clear input immediately
            self.ids.input_field.text = ""
            
            # Add user message
            timestamp = datetime.now().strftime("%H:%M")
            new_history = f"{self.chat_history}\n\n**[{timestamp}] You:** {message}"
            self.chat_history = new_history
            
            # Process in background
            self.ai_processing = True
            threading.Thread(
                target=self._process_ai_response,
                args=(message, timestamp),
                daemon=True
            ).start()
    
    def _process_ai_response(self, question, timestamp):
        """Process AI response with proper dataset access"""
        try:
            app = MDApp.get_running_app()
            
            # Wait a moment for better UX
            time.sleep(0.3)
            
            # Get dataset summaries for context
            dataset_summaries = self._get_dataset_summaries()
            
            # Check if AI analyzer exists
            if not hasattr(app, 'ai_analyzer') or not app.ai_analyzer:
                self._add_response("AI service is not available. Please wait for initialization.", timestamp)
                return
            
            # Get AI response WITH actual datasets
            response = app.ai_analyzer.answer_question(
                question=question,
                datasets_dict=app.all_dataframes,  # Pass the actual datasets
                dataset_summaries=dataset_summaries
            )
            
            # Update UI
            Clock.schedule_once(
                lambda dt, resp=response, ts=timestamp: 
                self._add_response(resp, ts)
            )
            
        except Exception as e:
            print(f"❌ AI processing error: {e}")
            import traceback
            traceback.print_exc()
            
            error_msg = "I encountered an error. Please try a simpler question."
            Clock.schedule_once(
                lambda dt: self._add_response(error_msg, timestamp)
            )
        finally:
            self.ai_processing = False
    
    def _get_dataset_summaries(self):
        """Create summaries of all loaded datasets"""
        app = MDApp.get_running_app()
        
        if not hasattr(app, 'all_dataframes') or not app.all_dataframes:
            return "No datasets loaded."
        
        summaries = []
        for name, df in app.all_dataframes.items():
            summary = f"{name}: {len(df)} records, {len(df.columns)} columns"
            summaries.append(summary)
        
        return "; ".join(summaries)
    
    def _add_response(self, response, timestamp):
        """Add AI response to chat"""
        new_history = f"{self.chat_history}\n\n**[{timestamp}] AI:** {response}"
        self.chat_history = new_history
    
    def go_back(self):
        """Return to dashboard"""
        app = MDApp.get_running_app()
        app.sm.current = "dashboard"