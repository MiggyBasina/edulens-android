from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.properties import StringProperty
from kivy.clock import Clock
import threading
import json
import hashlib
from datetime import datetime
from pathlib import Path
import pandas as pd

# Simple cache
def get_cache_path():
    cache_dir = Path("dashboard_cache")
    cache_dir.mkdir(exist_ok=True)
    return cache_dir

def cache_key(key):
    return hashlib.md5(str(key).encode()).hexdigest()

def get_cached_insights(datasets_key):
    """Get cached insights"""
    cache_file = get_cache_path() / f"insights_{cache_key(datasets_key)}.json"
    if cache_file.exists():
        try:
            with open(cache_file, 'r') as f:
                data = json.load(f)
                cache_time = datetime.fromisoformat(data.get('timestamp', ''))
                if (datetime.now() - cache_time).total_seconds() < 3600:  # 1 hour
                    return data.get('insights')
        except:
            pass
    return None

def cache_insights(datasets_key, insights):
    """Cache insights"""
    cache_file = get_cache_path() / f"insights_{cache_key(datasets_key)}.json"
    try:
        data = {
            'timestamp': datetime.now().isoformat(),
            'insights': insights
        }
        with open(cache_file, 'w') as f:
            json.dump(data, f)
    except:
        pass

class DatasetListItem(OneLineAvatarIconListItem):
    def __init__(self, dataset_name="", **kwargs):
        super().__init__(**kwargs)
        self.text = dataset_name
        self.add_widget(IconLeftWidget(icon="chart-box"))

class DashboardScreen(MDScreen):
    status_text = StringProperty("Loading educational insights...")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'dashboard'
        self.dialog = None
        self.loading_datasets = False
        self.cached_cloud_list = None

    def on_pre_enter(self):
        """Called before screen becomes visible - start loading early"""
        if not self.loading_datasets:
            self.loading_datasets = True
            Clock.schedule_once(self._start_loading, 0.1)
    
    def _start_loading(self, dt):
        """Start background loading"""
        threading.Thread(target=self._load_datasets_background, daemon=True).start()
    
    def _load_datasets_background(self):
        """Load datasets in background"""
        try:
            app = MDApp.get_running_app()
            
            # Get cloud datasets (cached)
            if self.cached_cloud_list is None and hasattr(app, 'supabase'):
                print("📡 Loading cloud datasets...")
                self.cached_cloud_list = app.supabase.list_datasets()
            
            cloud_datasets = self.cached_cloud_list or []
            
            # Load datasets (max 3 for speed)
            loaded = 0
            for cloud_ds in cloud_datasets[:3]:
                if loaded >= 3:  # Limit to 3
                    break
                    
                if self._load_single_dataset(cloud_ds):
                    loaded += 1
            
            # Update UI
            Clock.schedule_once(lambda dt: self._update_ui_after_loading(loaded, len(cloud_datasets)))
            
        except Exception as e:
            print(f"❌ Background load error: {e}")
        finally:
            self.loading_datasets = False
    
    def _load_single_dataset(self, cloud_ds):
        """Load single dataset - returns True if successful"""
        try:
            app = MDApp.get_running_app()
            dataset_name = cloud_ds['name']
            
            # Skip if already loaded
            if dataset_name in app.all_dataframes:
                return True
            
            # Download
            local_path = app.supabase.download_dataset(cloud_ds['cloud_id'])
            if not local_path:
                return False
            
            # Load with limited rows
            df = app.data_processor.load_file_mobile(local_path, max_rows=2000)
            if df.empty:
                return False
            
            # Store
            app.all_dataframes[dataset_name] = df
            app.dataset_info[dataset_name] = {
                'rows': len(df),
                'columns': len(df.columns),
                'type': app.data_processor.detect_data_type(df)
            }
            
            # Add to UI list
            Clock.schedule_once(
                lambda dt, name=dataset_name: self._add_to_list(name)
            )
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to load {cloud_ds.get('name')}: {e}")
            return False
    
    def _add_to_list(self, dataset_name):
        """Add dataset to UI list"""
        if hasattr(self, 'ids') and 'dataset_list' in self.ids:
            item = DatasetListItem(dataset_name=f"📊 {dataset_name}")
            self.ids.dataset_list.add_widget(item)
    
    def _update_ui_after_loading(self, loaded, total):
        """Update UI after loading"""
        if loaded > 0:
            self.status_text = f"Ready! {loaded} datasets loaded"
        else:
            self.status_text = "Connect to load datasets"
        
        # Generate insights in background
        threading.Thread(target=self._generate_insights_background, daemon=True).start()
    
    def _generate_insights_background(self):
        """Generate insights in background"""
        try:
            app = MDApp.get_running_app()
            
            if not app.all_dataframes:
                return
            
            # Simple insights (fast, no AI)
            insights = self._generate_quick_insights(app.all_dataframes)
            
            # Update UI
            Clock.schedule_once(lambda dt, i=insights: self._update_insights(i))
            
        except Exception as e:
            print(f"❌ Insight generation error: {e}")
    
    def _generate_quick_insights(self, datasets):
        """Generate quick insights without AI"""
        if not datasets:
            return "• No datasets loaded\n• Upload or connect to cloud"
        
        total_rows = sum(len(df) for df in datasets.values())
        total_cols = sum(len(df.columns) for df in datasets.values())
        
        insights = [
            f"📊 **{len(datasets)} Datasets Loaded**",
            f"• {total_rows:,} total records",
            f"• {total_cols} metrics available",
            f"• Tap any dataset for analysis",
            f"• Ask AI for detailed insights"
        ]
        
        # Add dataset-specific info
        for name, df in datasets.items():
            insights.append(f"\n**{name}**: {len(df):,} records")
        
        return "\n".join(insights)
    
    def _update_insights(self, insights):
        """Update insights display"""
        if hasattr(self, 'ids') and 'insights_label' in self.ids:
            self.ids.insights_label.text = insights
    
    def refresh_datasets(self):
        """Force refresh datasets"""
        self.cached_cloud_list = None
        app = MDApp.get_running_app()
        app.all_dataframes.clear()
        app.dataset_info.clear()
        
        if hasattr(self, 'ids') and 'dataset_list' in self.ids:
            self.ids.dataset_list.clear_widgets()
        
        self.on_pre_enter()
        print("🔄 Refreshed datasets")
    
    def open_chat(self):
        """Open chat screen"""
        app = MDApp.get_running_app()
        app.sm.current = 'chat'
    
    def select_dataset(self, dataset_name):
        """Handle dataset selection"""
        clean_name = dataset_name.replace("📊 ", "").strip()
        app = MDApp.get_running_app()
        app.select_dataset(clean_name)
    
    def show_trends(self):
        """Show quick trends"""
        app = MDApp.get_running_app()
        
        if not app.all_dataframes:
            self._show_message("No data available yet", "📈 Trends")
            return
        
        # Show loading
        self._show_message("Analyzing trends...", "📈 Analyzing")
        
        # Analyze in background
        threading.Thread(target=self._analyze_trends_background, daemon=True).start()
    
    def _analyze_trends_background(self):
        """Analyze trends in background"""
        try:
            app = MDApp.get_running_app()
            trends = self._simple_trend_analysis(app.all_dataframes)
            
            Clock.schedule_once(
                lambda dt, t=trends: self._show_trends_result(t)
            )
            
        except Exception as e:
            print(f"❌ Trend analysis error: {e}")
    
    def _simple_trend_analysis(self, datasets):
        """Fast trend analysis"""
        if not datasets:
            return "No data available."
        
        trends = ["📊 **Quick Trends Analysis**", ""]
        
        for name, df in datasets.items():
            trends.append(f"**{name}**")
            trends.append(f"• Records: {len(df):,}")
            trends.append(f"• Columns: {len(df.columns)}")
            
            # Check for common educational metrics
            cols_lower = ' '.join(df.columns).lower()
            if any(word in cols_lower for word in ['grade', 'score', 'mark']):
                trends.append("• Contains performance data")
            if any(word in cols_lower for word in ['attendance', 'present']):
                trends.append("• Contains attendance data")
            if any(word in cols_lower for word in ['survey', 'response']):
                trends.append("• Contains survey data")
            
            trends.append("")  # Empty line
        
        trends.append("💡 **Suggestions**")
        trends.append("• Ask AI for detailed analysis")
        trends.append("• Look for performance patterns")
        trends.append("• Check student engagement")
        
        return "\n".join(trends)
    
    def _show_trends_result(self, trends):
        """Show trends result"""
        self._show_scrollable_message(trends, "📈 Trends Analysis")
    
    def _show_message(self, message, title="Info"):
        """Show simple message"""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton
        
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title=title,
            text=message,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
        )
        self.dialog.open()
    
    def _show_scrollable_message(self, message, title):
        """Show scrollable message"""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.scrollview import MDScrollView
        from kivymd.uix.label import MDLabel
        from kivymd.uix.button import MDFlatButton
        
        if self.dialog:
            self.dialog.dismiss()
        
        scroll = MDScrollView(size_hint=(1, None), size=("350dp", "300dp"))
        label = MDLabel(
            text=message,
            size_hint_y=None,
            height=max(300, len(message.split('\n')) * 20),
            padding=("10dp", "10dp"),
            markup=True
        )
        scroll.add_widget(label)
        
        self.dialog = MDDialog(
            title=title,
            type="custom",
            content_cls=scroll,
            buttons=[MDFlatButton(text="CLOSE", on_release=lambda x: self.dialog.dismiss())]
        )
        self.dialog.open()