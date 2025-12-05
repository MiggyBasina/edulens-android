import os
import sys
import threading
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.clock import Clock
from kivy.core.window import Window

# Set window size for mobile
Window.size = (360, 640)

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Import screens FIRST (needed for KV files)
from app.ui.screens.login_screen import LoginScreen
from app.ui.screens.dashboard_screen import DashboardScreen
from app.ui.screens.analysis_screen import AnalysisScreen
from app.ui.screens.chat_screen import ChatScreen

print("🚀 Starting EduLens Mobile...")

# Load KV files in background thread
def load_kv_files_async():
    """Load KV files in background"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        kv_files = [
            'login_screen.kv',
            'dashboard_screen.kv', 
            'analysis_screen.kv',
            'chat_screen.kv'
        ]
        
        loaded_count = 0
        for filename in kv_files:
            kv_path = os.path.join(current_dir, 'app', 'ui', 'screens', filename)
            if os.path.exists(kv_path):
                try:
                    Builder.load_file(kv_path)
                    loaded_count += 1
                except Exception as e:
                    print(f"   ⚠️ Error loading {filename}: {e}")
        
        print(f"   ✅ Loaded {loaded_count}/{len(kv_files)} KV files")
    except Exception as e:
        print(f"❌ KV loading error: {e}")

# Start loading KV files immediately
kv_thread = threading.Thread(target=load_kv_files_async, daemon=True)
kv_thread.start()

class EduLensApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Data storage
        self.current_data = None
        self.all_dataframes = {}  
        self.dataset_info = {}    
        self.current_dataset_name = None
        self.data_type = None
        self.ai_analyzer = None  # Will hold the AI analyzer
        
        # Initialize ALL components in background
        self._init_background_components()
    
    def _init_background_components(self):
        """Initialize all heavy components in background"""
        def init_in_thread():
            try:
                print("🔄 Initializing app components...")
                
                # Import and initialize Supabase
                from app.utils.supabase_client import SupabaseClient
                self.supabase = SupabaseClient()
                print("   ✅ Supabase initialized")
                
                # Import and initialize Data Processor
                from app.core.data_processor import MobileDataProcessor
                self.data_processor = MobileDataProcessor()
                print("   ✅ Data processor initialized")
                
                # Import and initialize AI Analyzer (CRITICAL!)
                from app.core.ai_analyzer import EducationalAnalyst
                self.ai_analyzer = EducationalAnalyst(self.supabase)
                print("   ✅ AI analyzer initialized")
                
                # Load cloud datasets in background
                self.cloud_datasets = []
                threading.Thread(
                    target=self._load_initial_datasets,
                    daemon=True
                ).start()
                
                print("✅ All background components initialized successfully!")
                
            except Exception as e:
                print(f"❌ Background initialization failed: {e}")
                import traceback
                traceback.print_exc()
        
        # Start initialization
        threading.Thread(target=init_in_thread, daemon=True).start()
    
    def _load_initial_datasets(self):
        """Load initial datasets in background"""
        try:
            if hasattr(self, 'supabase') and self.supabase:
                print("🌥️ Loading cloud datasets...")
                self.cloud_datasets = self.supabase.list_datasets()
                print(f"   ✅ Found {len(self.cloud_datasets)} cloud datasets")
        except Exception as e:
            print(f"⚠️ Cloud dataset load failed: {e}")
    
    def build(self):
        """Build app UI"""
        print("🛠️ Building app UI...")
        
        # Wait for KV files to load (max 3 seconds)
        kv_thread.join(timeout=3)
        
        # Set theme
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        
        # Create screen manager
        self.sm = ScreenManager(transition=FadeTransition(duration=0.15))
        
        # Add screens
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(DashboardScreen(name='dashboard'))
        self.sm.add_widget(AnalysisScreen(name='analysis'))
        self.sm.add_widget(ChatScreen(name='chat'))
        
        # Set initial screen
        self.sm.current = 'login'
        
        print(f"✅ App ready. Screen: {self.sm.current}")
        
        # Check if AI is ready
        if self.ai_analyzer and hasattr(self.ai_analyzer, 'gemini_available'):
            print(f"🤖 AI Status: {'Ready' if self.ai_analyzer.gemini_available else 'Not available'}")
        
        return self.sm
    
    def select_dataset(self, dataset_name):
        """Select dataset - optimized version"""
        # Clean name
        clean_name = dataset_name.replace("📊 ", "").strip()
        
        # Set current dataset
        self.current_dataset_name = clean_name
        if clean_name in self.all_dataframes:
            self.current_data = self.all_dataframes[clean_name]
            self.data_type = self.dataset_info.get(clean_name, {}).get('type', 'general')
        
        # Go to analysis screen
        self.sm.current = 'analysis'
        
        # Load dataset in background if not loaded
        if clean_name not in self.all_dataframes and hasattr(self, 'cloud_datasets'):
            threading.Thread(
                target=self._load_dataset_in_background,
                args=(clean_name,),
                daemon=True
            ).start()
    
    def _load_dataset_in_background(self, dataset_name):
        """Load dataset in background thread"""
        try:
            # Find cloud dataset
            for cloud_ds in self.cloud_datasets:
                if cloud_ds['name'] == dataset_name:
                    local_path = self.supabase.download_dataset(cloud_ds['cloud_id'])
                    if local_path:
                        df = self.data_processor.load_file_mobile(local_path, max_rows=5000)
                        if not df.empty:
                            self.all_dataframes[dataset_name] = df
                            self.dataset_info[dataset_name] = {
                                'rows': len(df),
                                'columns': len(df.columns),
                                'type': self.data_processor.detect_data_type(df)
                            }
                            print(f"✅ Background loaded: {dataset_name}")
        except Exception as e:
            print(f"❌ Background load failed: {e}")
    
    def on_start(self):
        """App startup complete"""
        print("🎯 EduLens Mobile is ready!")

def main():
    EduLensApp().run()

if __name__ == "__main__":
    main()