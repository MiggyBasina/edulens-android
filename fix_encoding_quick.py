# Fix main.py KV indentation
import re

def fix_kv_string(kv_string):
    """Fix KV string indentation"""
    lines = kv_string.split('\n')
    fixed_lines = []
    
    for line in lines:
        # Count leading spaces
        leading_spaces = len(line) - len(line.lstrip())
        
        # Ensure indentation is multiple of 4
        if leading_spaces % 4 != 0:
            # Round to nearest multiple of 4
            fixed_spaces = (leading_spaces // 4) * 4
            line = ' ' * fixed_spaces + line.lstrip()
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

# Read main.py
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and fix KV strings
kv_pattern = r'(\w+_kv = """.*?""")'
matches = re.findall(kv_pattern, content, re.DOTALL)

for match in matches:
    # Extract KV string name and content
    lines = match.split('\n')
    kv_name = lines[0].split('_kv')[0]
    
    # Fix indentation
    fixed_kv = fix_kv_string(match)
    
    # Replace in content
    content = content.replace(match, fixed_kv)
    
    print(f"Fixed {kv_name}_kv")

# Write back
with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed all KV string indentations")