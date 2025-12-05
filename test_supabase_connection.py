import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from supabase import create_client

url = "https://sdmhvwztkikrpelupjbd.supabase.co"
key = "sb_publishable_rI3qZjg9KG2BE2XcaPV19Q_kpO0gdiZ"

print("Testing Supabase connection...")
try:
    client = create_client(url, key)
    print("✅ Client created")
    
    # Test storage
    storage = client.storage.from_("edulens-datasets")
    print("✅ Storage accessed")
    
    # Try to list (might be empty)
    files = storage.list()
    print(f"✅ Files in bucket: {len(files)}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()