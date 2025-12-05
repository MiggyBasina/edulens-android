import os

print("📋 Current requirements are too heavy for first build.")
print("They will likely fail with matplotlib, google-api, etc.")
print()

# Read current spec
with open('buildozer.spec', 'r') as f:
    content = f.read()

# Find requirements line
import re
match = re.search(r'requirements\s*=\s*(.+)', content)
if match:
    current_req = match.group(1)
    print(f"Current requirements: {current_req[:100]}...")
    print(f"Total packages: {len(current_req.split(','))}")
else:
    print("Could not find requirements line")

print()
print("🎯 Creating simplified version for first build...")

# Simplified requirements - core only
simple_req = "python3,kivy==2.3.0,kivymd==1.2.0,pandas,numpy,Pillow,google-generativeai,supabase,protobuf,certifi"

# Update the spec
new_content = content.replace(
    'requirements = python3,kivy==2.3.0,kivymd==1.2.0,pandas,numpy,matplotlib,google-api-python-client,google-auth-httplib2,google-auth-oauthlib,google-generativeai,Pillow,chardet,supabase,httpx,postgrest,realtime,gotrue,storage3,certifi,idna,sniffio,httpcore,anyio,h11,proto-plus,protobuf',
    f'requirements = {simple_req}'
)

# Also uncomment the license acceptance
new_content = new_content.replace(
    '# android.accept_sdk_license = True',
    'android.accept_sdk_license = True'
)

# Write back
with open('buildozer.spec', 'w') as f:
    f.write(new_content)

print("✅ Simplified buildozer.spec")
print(f"New requirements: {simple_req}")
print("\n📦 Packages removed for now (will add back later):")
print("  - matplotlib (heavy C++ compilation)")
print("  - google-api-python-client (complex)")
print("  - httpx and related HTTP packages")
print("  - chardet, idna, sniffio, etc.")
print("\n⚡ After successful build, we'll add them back one by one.")
print("\nNow run: buildozer android clean")
print("Then: buildozer -v android debug")
