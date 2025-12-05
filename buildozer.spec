[app]

# App information
title = EduLens
package.name = edulens
package.domain = org.edulens
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json
version = 1.0.0
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pandas,numpy,Pillow,google-generativeai,supabase,protobuf,certifi
p4a.branch = develop
android.p4a_args = --ndk-api=24
android.permissions = INTERNET,ACCESS_NETWORK_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,ACCESS_WIFI_STATE
android.api = 33
android.minapi = 24
# android.sdk = 24  # REMOVE THIS - deprecated
android.ndk = 25b
android.gradle_dependencies = 'com.android.support:multidex:1.0.3'
android.archs = arm64-v8a,armeabi-v7a  # Changed from android.arch to android.archs

# Orientation
orientation = portrait

# Window style (fullscreen is better for mobile)
fullscreen = 0

# Presplash (loading screen)
presplash.filename = %(source.dir)s/assets/presplash.png
icon.filename = %(source.dir)s/assets/icon.png

# Log level (debug for first build)
log_level = 2

# Build modes
# (comment out to test, then uncomment for release)
android.accept_sdk_license = True
# android.release_artifact = .apk

# Python optimizations
# android.prebuild_commands =  # REMOVE or simplify
#    rm -rf venv,
#    rm -rf .git,
#    rm -rf __pycache__,
#    find . -name "*.pyc" -delete,
#    find . -name "__pycache__" -type d -delete

# Blacklist patterns
android.blacklist_src = tests, test, __pycache__, .git, venv, .github

# Presplash color (white background)
presplash.color = #FFFFFF

# Kivy configuration
android.entrypoint = org.kivy.android.PythonActivity

# Touch improvements
# android.meta_data =  # REMOVE or comment out

# Debug options (disable for release)
android.debug = 1
android.allow_backup = true
android.enable_profiler = false

# Packaging options
android.private_storage = true
android.expand_java_src = false
android.expand_assets = false
# android.add_manifest_xml =  # REMOVE or comment out

# Clean builds
android.clean_build = true

# Buildozer optimization
# buildozer.on_build =  # REMOVE or comment out

# Logcat filters
logcat_filters = *:S python:D

# AndroidX (modern Android support)
android.enable_androidx = true

# Multidex support (for larger apps)
android.multidex = true

# App themes and styles
android.apptheme = "@android:style/Theme.Material.Light"

# Disable some features to reduce size
# android.ignore_path =  # REMOVE or comment out
# android.skip_compile =  # REMOVE or comment out

# Python packages to include
# android.include_python_packages =  # REMOVE or comment out

# ========== ONLY FOR RELEASE ==========
# Uncomment these lines for release build:
# android.release_artifact = .apk
# android.accept_sdk_license = true
# log_level = 1
# android.debug = 0
# fullscreen = 1

[buildozer]

# Build directory
build_dir = ./.buildozer

# Log directory  
log_dir = ./.buildozer/logs

# Bin directory
bin_dir = ./.buildozer/bin