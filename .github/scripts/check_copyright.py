#!/usr/bin/env python3
"""
Copyright Header Verification Script

Copyright © 2025 NovaSysErr-X. All rights reserved.

This script verifies that all Python files contain proper copyright headers.
"""

import os
import sys
import re

def check_copyright_header(file_path):
    """Check if a file contains the required copyright header"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for copyright notice
        copyright_patterns = [
            r'Copyright © 2025 NovaSysErr-X',
            r'LEGAL WARNING',
            r'protected by copyright law',
            r'anti-tampering mechanisms'
        ]
        
        missing_patterns = []
        for pattern in copyright_patterns:
            if not re.search(pattern, content, re.IGNORECASE):
                missing_patterns.append(pattern)
                
        if missing_patterns:
            print(f"❌ {file_path}: Missing copyright patterns: {missing_patterns}")
            return False
        else:
            print(f"✅ {file_path}: Copyright header verified")
            return True
            
    except Exception as e:
        print(f"❌ Error checking {file_path}: {e}")
        return False

def main():
    """Main verification function"""
    print("🔍 Verifying copyright headers in all Python files...")
    
    src_dir = "src"
    if not os.path.exists(src_dir):
        print(f"❌ Source directory {src_dir} not found")
        sys.exit(1)
        
    python_files = []
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    if not python_files:
        print("❌ No Python files found in src directory")
        sys.exit(1)
        
    all_valid = True
    for file_path in python_files:
        if not check_copyright_header(file_path):
            all_valid = False
            
    if all_valid:
        print("\n✅ All Python files have valid copyright headers")
        sys.exit(0)
    else:
        print("\n❌ Some files are missing copyright headers")
        sys.exit(1)

if __name__ == "__main__":
    main()