import os
from supabase import create_client, Client
from .cache_manager import app_cache

class SupabaseClient:
    def __init__(self):
        self.url = "https://sdmhvwztkikrpelupjbd.supabase.co"
        self.key = "sb_publishable_rI3qZjg9KG2BE2XcaPV19Q_kpO0gdiZ"
        self.client: Client = None
        
        try:
            self.client = create_client(self.url, self.key)
            print("✅ Supabase connected")
        except Exception as e:
            print(f"❌ Supabase error: {e}")
    
    def upload_dataset(self, file_path, dataset_name):
        """Upload dataset to Supabase"""
        if not self.client:
            print("❌ No Supabase client")
            return False
        
        try:
            # Read file
            with open(file_path, 'rb') as f:
                file_bytes = f.read()
            
            print(f"📤 Uploading {dataset_name} to cloud...")
            
            # Upload to storage
            result = self.client.storage.from_("edulens-datasets").upload(
                path=f"datasets/{dataset_name}",
                file=file_bytes
            )
            
            # Clear cache since we added new data
            app_cache.delete("datasets_list")
            
            print(f"✅ SUCCESS: Uploaded to cloud: {dataset_name}")
            return True
            
        except Exception as e:
            print(f"❌ FAILED: Upload error: {e}")
            return False
    
    def list_datasets(self, force_refresh=False):
        """Get ALL files with caching"""
        if not self.client:
            print("❌ No Supabase client")
            return []
        
        # Check cache first (unless forced refresh)
        if not force_refresh:
            cached = app_cache.get("datasets_list")
            if cached is not None:
                print("📦 Using cached dataset list")
                return cached
        
        try:
            print("🔄 Fetching fresh dataset list...")
            all_items = self.client.storage.from_("edulens-datasets").list("")
            
            cloud_datasets = []
            for item in all_items:
                name = item.get('name', '')
                
                # Skip empty names or folders
                if not name or name.endswith('/'):
                    continue
                
                # Try to extract filename in multiple ways
                clean_name = name
                if '/' in name:
                    clean_name = name.split('/')[-1]
                
                # Remove extension for display name
                display_name = clean_name
                if '.' in clean_name:
                    display_name = clean_name.rsplit('.', 1)[0]
                
                # Accept ANY file
                cloud_datasets.append({
                    'name': display_name,
                    'cloud_id': name,  # Keep original path
                    'original_name': clean_name,
                    'full_path': name,
                    'is_cloud': True,
                    'size': item.get('metadata', {}).get('size', 0)
                })
            
            # Cache the result
            app_cache.set("datasets_list", cloud_datasets, ttl_hours=6)
            
            print(f"✅ Retrieved {len(cloud_datasets)} datasets")
            return cloud_datasets
            
        except Exception as e:
            print(f"❌ Storage list error: {e}")
            return []
    
    def download_dataset(self, cloud_id, use_cache=True):
        """Download dataset from cloud with caching"""
        if not self.client:
            print("❌ No Supabase client")
            return None
        
        # Check cache first
        cache_key = f"dataset_{cloud_id}"
        if use_cache:
            cached_path = app_cache.get(cache_key)
            if cached_path and os.path.exists(cached_path):
                print(f"📦 Using cached: {cloud_id}")
                return cached_path
        
        try:
            print(f"📥 Downloading from cloud: {cloud_id}")
            
            # Download file
            file_bytes = self.client.storage.from_("edulens-datasets").download(cloud_id)
            
            # Save to temp file
            import tempfile
            
            # Determine file extension
            if cloud_id.lower().endswith('.csv'):
                suffix = '.csv'
            elif cloud_id.lower().endswith('.xlsx'):
                suffix = '.xlsx'
            elif cloud_id.lower().endswith('.xls'):
                suffix = '.xls'
            else:
                suffix = '.csv'  # default
            
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            temp_file.write(file_bytes)
            temp_file.close()
            
            # Cache the file path (cache for 12 hours)
            app_cache.set(cache_key, temp_file.name, ttl_hours=12)
            
            print(f"✅ Downloaded: {cloud_id} → {temp_file.name}")
            return temp_file.name
            
        except Exception as e:
            print(f"❌ Download error for {cloud_id}: {e}")
            return None
    
    def clear_cache(self):
        """Clear Supabase-related cache"""
        app_cache.delete("datasets_list")
        print("🧹 Cleared Supabase cache")