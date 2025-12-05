from supabase import create_client

url = "https://sdmhvwztkikrpelupjbd.supabase.co"
key = "sb_publishable_rI3qZjg9KG2BE2XcaPV19Q_kpO0gdiZ"

client = create_client(url, key)

print("Checking cloud storage...")
try:
    # List all files in bucket
    files = client.storage.from_("edulens-datasets").list()
    print(f"Total files in bucket: {len(files)}")
    
    for file in files:
        print(f"  - {file['name']} ({file.get('metadata', {}).get('size', 0)} bytes)")
        
    if len(files) == 0:
        print("❌ No files in cloud. Upload failed.")
    else:
        print("✅ Files found in cloud.")
        
except Exception as e:
    print(f"Error: {e}")