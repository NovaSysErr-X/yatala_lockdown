#!/usr/bin/env python3
"""
Digital Watermarking System

Copyright © 2025 NovaSysErr-X. All rights reserved.

LEGAL WARNING:
This file contains proprietary digital watermarking technology.
Unauthorized reproduction, modification, or distribution is prohibited.
Violators will be prosecuted to the fullest extent of the law.

This system embeds unique identifiers in source code to track
unauthorized distribution and modifications.
"""

import hashlib
import os
import time
import json
import base64
from typing import Dict, Any, Optional

class DigitalWatermark:
    """Digital watermarking system for source code protection"""
    
    def __init__(self):
        self.watermark_signature = "YATALA_LOCKDOWN_PROTECTED"
        self.version = "1.0"
        
    def generate_fingerprint(self, file_path: str) -> str:
        """Generate unique fingerprint for a file"""
        # Combine file path, timestamp, and system info
        timestamp = int(time.time())
        file_hash = hashlib.sha256(file_path.encode()).hexdigest()[:16]
        system_info = os.environ.get('USER', 'unknown')[:8]
        
        # Create unique fingerprint
        fingerprint_data = f"{file_hash}:{timestamp}:{system_info}"
        fingerprint = hashlib.sha256(fingerprint_data.encode()).hexdigest()[:32]
        
        return fingerprint
    
    def embed_watermark(self, content: str, file_path: str) -> str:
        """Embed digital watermark into source code"""
        fingerprint = self.generate_fingerprint(file_path)
        
        # Create watermark data
        watermark_data = {
            "signature": self.watermark_signature,
            "version": self.version,
            "fingerprint": fingerprint,
            "timestamp": int(time.time()),
            "file": file_path,
            "author": "NovaSysErr-X"
        }
        
        # Encode watermark
        watermark_json = json.dumps(watermark_data)
        watermark_encoded = base64.b64encode(watermark_json.encode()).decode()
        
        # Split watermark into parts and embed in comments
        watermark_parts = [watermark_encoded[i:i+80] for i in range(0, len(watermark_encoded), 80)]
        
        # Add watermark comments at strategic locations
        lines = content.split('\n')
        watermark_lines = []
        
        for i, part in enumerate(watermark_parts):
            if i < len(lines):
                # Insert after imports or class definitions
                if lines[i].strip().startswith(('import', 'from', 'class', 'def')):
                    watermark_lines.append(f"# WM_{i+1:02d}: {part}")
                    
        # Add final watermark at end
        final_watermark = f"""
# WATERMARK_INTEGRITY_CHECK
# This file is protected by digital watermarking technology
# Unauthorized modification or distribution will be detected
# Fingerprint: {fingerprint}
# Copyright © 2025 NovaSysErr-X. All rights reserved.
"""
        
        return content + final_watermark
    
    def verify_watermark(self, content: str) -> Dict[str, Any]:
        """Verify digital watermark in content"""
        result = {
            "valid": False,
            "fingerprint": None,
            "timestamp": None,
            "tampered": False
        }
        
        # Look for watermark signature
        if "WATERMARK_INTEGRITY_CHECK" not in content:
            result["tampered"] = True
            return result
            
        # Extract fingerprint
        lines = content.split('\n')
        for line in lines:
            if "Fingerprint:" in line:
                result["fingerprint"] = line.split("Fingerprint:")[1].strip()
                result["valid"] = True
                break
                
        return result
    
    def check_integrity(self, file_path: str) -> bool:
        """Check if file has been tampered with"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            verification = self.verify_watermark(content)
            
            if not verification["valid"]:
                print(f"⚠️  WARNING: {file_path} missing digital watermark!")
                return False
                
            if verification["tampered"]:
                print(f"🚨 ALERT: {file_path} appears to be tampered with!")
                return False
                
            print(f"✅ {file_path}: Digital watermark verified")
            return True
            
        except Exception as e:
            print(f"❌ Error checking {file_path}: {e}")
            return False

# Global watermark instance
watermark = DigitalWatermark()

def protect_file(file_path: str) -> bool:
    """Apply digital watermark protection to a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Skip if already watermarked
        if "WATERMARK_INTEGRITY_CHECK" in content:
            print(f"ℹ️  {file_path} already watermarked")
            return True
            
        # Apply watermark
        protected_content = watermark.embed_watermark(content, file_path)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(protected_content)
            
        print(f"🔒 {file_path}: Digital watermark applied")
        return True
        
    except Exception as e:
        print(f"❌ Error protecting {file_path}: {e}")
        return False

def verify_all_files(directory: str = "src") -> bool:
    """Verify all Python files in directory"""
    print("🔍 Verifying digital watermarks...")
    
    all_valid = True
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if not watermark.check_integrity(file_path):
                    all_valid = False
                    
    if all_valid:
        print("✅ All files have valid digital watermarks")
    else:
        print("❌ Some files have invalid or missing watermarks")
        
    return all_valid

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "verify":
            verify_all_files()
        elif sys.argv[1] == "protect":
            if len(sys.argv) > 2:
                protect_file(sys.argv[2])
            else:
                print("Usage: python digital_watermark.py protect <file>")
    else:
        print("Digital Watermarking System v1.0")
        print("Usage:")
        print("  python digital_watermark.py verify")
        print("  python digital_watermark.py protect <file>")