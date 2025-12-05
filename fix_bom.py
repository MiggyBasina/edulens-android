import os
import sys

def remove_bom_from_file(filepath):
    """Remove BOM character from a file"""
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        
        # Check for UTF-8 BOM
        if content.startswith(b'\xef\xbb\xbf'):
            print(f"Fixing BOM in: {filepath}")
            with open(filepath, 'wb') as f:
                f.write(content[3:])  # Remove first 3 bytes (BOM)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

# Fix all Python files in the project
def fix_all_python_files():
    python_files = []
    
    # Walk through all directories
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    print(f"Found {len(python_files)} Python files")
    
    fixed_count = 0
    for filepath in python_files:
        if remove_bom_from_file(filepath):
            fixed_count += 1
    
    print(f"Fixed {fixed_count} files with BOM issues")

if __name__ == "__main__":
    fix_all_python_files()