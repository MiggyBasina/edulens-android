import os
import shutil
import sys

def clean_project():
    """Clean project for APK build"""
    
    print("🧹 Cleaning project for APK build...")
    
    # Remove unnecessary directories
    dirs_to_remove = [
        '.buildozer',
        'bin',
        '__pycache__',
        'venv',
        '.git',
        '.pytest_cache',
        '.mypy_cache',
        '.ruff_cache'
    ]
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"  ✅ Removed: {dir_name}")
            except Exception as e:
                print(f"  ⚠️ Could not remove {dir_name}: {e}")
    
    # Remove cache files
    cache_patterns = ['*.pyc', '*.pyo', '*.pyd', '.DS_Store', 'Thumbs.db']
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            if any(file.endswith(pattern.replace('*', '')) for pattern in cache_patterns):
                try:
                    os.remove(os.path.join(root, file))
                except:
                    pass
    
    print("✅ Project cleaned!")

def check_requirements():
    """Check if all requirements are properly formatted"""
    
    print("\n📋 Checking requirements...")
    
    # Read current requirements from requirements.txt
    try:
        with open('requirements.txt', 'r') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        print(f"Found {len(requirements)} requirements")
        
        # Check for problematic packages
        problematic = ['kivy', 'kivymd', 'matplotlib', 'pandas']
        for pkg in problematic:
            if any(pkg in req for req in requirements):
                print(f"  ⚠️  {pkg} may need special handling")
        
        return requirements
        
    except Exception as e:
        print(f"❌ Error reading requirements: {e}")
        return []

def create_minimal_requirements():
    """Create minimal requirements for Android"""
    
    minimal_req = """python3
kivy==2.3.0
kivymd==1.2.0
pandas
numpy
matplotlib
Pillow
google-generativeai
supabase
httpx
protobuf
certifi
"""
    
    with open('requirements_android.txt', 'w') as f:
        f.write(minimal_req)
    
    print("✅ Created minimal requirements for Android")
    return minimal_req

def check_directory_structure():
    """Check if directory structure is correct"""
    
    print("\n📁 Checking directory structure...")
    
    required_dirs = [
        'app',
        'app/core',
        'app/ui/screens', 
        'app/utils',
        'assets'
    ]
    
    all_good = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"  ✅ {dir_path}/")
        else:
            print(f"  ❌ Missing: {dir_path}/")
            all_good = False
    
    # Check essential files
    essential_files = [
        'main.py',
        'buildozer.spec',
        'app/__init__.py',
        'app/core/__init__.py',
        'app/ui/screens/login_screen.py',
        'app/ui/screens/dashboard_screen.py',
        'app/ui/screens/analysis_screen.py', 
        'app/ui/screens/chat_screen.py',
        'assets/icon.png'
    ]
    
    for file_path in essential_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ⚠️  Missing: {file_path}")
            all_good = False
    
    return all_good

def main():
    """Main preparation function"""
    
    print("=" * 60)
    print("📱 APK BUILD PREPARATION")
    print("=" * 60)
    
    # Step 1: Clean project
    clean_project()
    
    # Step 2: Check structure
    if not check_directory_structure():
        print("\n⚠️  Some files/directories are missing!")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Build preparation cancelled.")
            return
    
    # Step 3: Check requirements
    requirements = check_requirements()
    
    # Step 4: Create minimal requirements
    create_minimal_requirements()
    
    print("\n" + "=" * 60)
    print("✅ PREPARATION COMPLETE!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Make sure you have Buildozer installed:")
    print("   pip install buildozer")
    print("\n2. Test the build (DEBUG mode):")
    print("   buildozer android debug")
    print("\n3. For release build (after testing):")
    print("   buildozer android release")
    print("\n4. Find your APK in:")
    print("   ./bin/edulens-1.0.0-armeabi-v7a-debug.apk")
    print("\n⚠️  First build will take 20-40 minutes!")
    print("   It downloads Android SDK, NDK, and compiles everything.")

if __name__ == "__main__":
    main()