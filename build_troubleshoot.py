import os
import subprocess
import sys

def check_system():
    """Check system requirements"""
    
    print("🔍 Checking system requirements...")
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    
    # Check buildozer
    try:
        result = subprocess.run(['buildozer', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Buildozer: {result.stdout.strip()}")
        else:
            print("❌ Buildozer not found. Install with: pip install buildozer")
            return False
    except FileNotFoundError:
        print("❌ Buildozer not found. Install with: pip install buildozer")
        return False
    
    # Check disk space
    import shutil
    total, used, free = shutil.disk_usage(".")
    free_gb = free // (2**30)
    print(f"Disk space: {free_gb}GB free")
    
    if free_gb < 10:
        print("⚠️  Low disk space (<10GB). Build may fail.")
    
    # Check memory
    try:
        import psutil
        memory = psutil.virtual_memory()
        memory_gb = memory.total // (2**30)
        print(f"Memory: {memory_gb}GB total")
        
        if memory_gb < 4:
            print("⚠️  Low memory (<4GB). Build may be slow.")
    except ImportError:
        print("Memory: Could not check (install psutil for details)")
    
    return True

def fix_common_issues():
    """Fix common build issues"""
    
    print("\n🔧 Fixing common issues...")
    
    fixes = []
    
    # 1. Fix BOM in Python files
    try:
        import glob
        python_files = glob.glob("**/*.py", recursive=True)
        bom_fixed = 0
        
        for file_path in python_files:
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                if content.startswith(b'\xef\xbb\xbf'):
                    with open(file_path, 'wb') as f:
                        f.write(content[3:])
                    bom_fixed += 1
            except:
                pass
        
        if bom_fixed > 0:
            fixes.append(f"Fixed BOM in {bom_fixed} Python files")
    except:
        pass
    
    # 2. Ensure all __init__.py files exist
    init_dirs = ['app', 'app/core', 'app/ui', 'app/ui/screens', 'app/utils']
    
    for dir_path in init_dirs:
        init_file = os.path.join(dir_path, '__init__.py')
        if os.path.exists(dir_path) and not os.path.exists(init_file):
            try:
                with open(init_file, 'w') as f:
                    f.write('')
                fixes.append(f"Created {init_file}")
            except:
                pass
    
    # 3. Clean build directories
    build_dirs = ['.buildozer', 'bin']
    
    for dir_path in build_dirs:
        if os.path.exists(dir_path):
            try:
                import shutil
                shutil.rmtree(dir_path)
                fixes.append(f"Cleaned {dir_path}")
            except:
                pass
    
    if fixes:
        print("✅ Fixed issues:")
        for fix in fixes:
            print(f"   • {fix}")
    else:
        print("✅ No common issues found")
    
    return fixes

def suggest_optimizations():
    """Suggest optimizations for APK build"""
    
    print("\n💡 Optimization suggestions:")
    
    suggestions = [
        "1. Remove unused imports from Python files",
        "2. Comment out heavy AI features for first build test",
        "3. Reduce dataset sample size in mobile_data_processor.py",
        "4. Disable cloud features temporarily for testing",
        "5. Use smaller test datasets for initial build"
    ]
    
    for suggestion in suggestions:
        print(f"   {suggestion}")

def main():
    """Main troubleshooting function"""
    
    print("=" * 60)
    print("🛠️  APK BUILD TROUBLESHOOTING")
    print("=" * 60)
    
    # Check system
    if not check_system():
        print("\n❌ System requirements not met.")
        return
    
    # Fix issues
    fixes = fix_common_issues()
    
    # Suggestions
    suggest_optimizations()
    
    print("\n" + "=" * 60)
    print("🎯 READY FOR BUILD")
    print("=" * 60)
    print("\nCommands to try:")
    print("\n1. INITIALIZE (do this first):")
    print("   buildozer init")
    
    print("\n2. DEBUG BUILD (test):")
    print("   buildozer -v android debug")
    
    print("\n3. RELEASE BUILD (final):")
    print("   buildozer android release")
    
    print("\n4. CLEAN BUILD (if issues):")
    print("   buildozer android clean")
    
    print("\n📝 Build logs will be in: .buildozer/android/platform/build-*/build_output.txt")
    print("📦 APK will be in: ./bin/")

if __name__ == "__main__":
    main()
