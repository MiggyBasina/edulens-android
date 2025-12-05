import os
from supabase import create_client

url = "https://sdmhvwztkikrpelupjbd.supabase.co"
key = "sb_publishable_rI3qZjg9KG2BE2XcaPV19Q_kpO0gdiZ"

client = create_client(url, key)

# Create a test file
test_content = b"student,grade\nAlice,85\nBob,92\n"
with open("test_debug.csv", "wb") as f:
    f.write(test_content)

print("Testing upload...")
try:
    with open("test_debug.csv", "rb") as f:
        file_bytes = f.read()
    
    result = client.storage.from_("edulens-datasets").upload(
        path="datasets/test_debug",
        file=file_bytes
    )
    print(f"Upload result: {result}")
    print("✅ Manual upload successful")
    
except Exception as e:
    print(f"❌ Manual upload failed: {e}")
    import traceback
    traceback.print_exc()