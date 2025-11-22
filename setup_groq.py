#!/usr/bin/env python3
"""
Setup script for Groq API integration
This script helps you configure your Groq API key for the Resume Analyzer
"""

import os
import re

def setup_groq_api():
    """Setup Groq API key for the Resume Analyzer"""
    print("🚀 Welcome to Resume Analyzer Groq Setup!")
    print("=" * 50)
    print()
    print("To use Groq AI (ultra-fast alternative to Ollama), you need an API key.")
    print()
    print("📋 Steps to get your Groq API key:")
    print("1. Go to https://console.groq.com/")
    print("2. Sign up for a free account")
    print("3. Navigate to API Keys section")
    print("4. Create a new API key")
    print("5. Copy the key (starts with 'gsk_')")
    print()
    
    # Check if API key already exists
    main_py_path = "main.py"
    if os.path.exists(main_py_path):
        with open(main_py_path, 'r') as f:
            content = f.read()
            if 'GROQ_API_KEY = "gsk_' in content:
                print("✅ Groq API key already configured!")
                return
    
    # Get API key from user
    api_key = input("🔑 Enter your Groq API key (starts with 'gsk_'): ").strip()
    
    if not api_key.startswith('gsk_'):
        print("❌ Invalid API key format. Groq API keys start with 'gsk_'")
        return
    
    # Update main.py with the API key
    try:
        with open(main_py_path, 'r') as f:
            content = f.read()
        
        # Replace the placeholder API key
        updated_content = re.sub(
            r'GROQ_API_KEY = "gsk_\.\.\."',
            f'GROQ_API_KEY = "{api_key}"',
            content
        )
        
        with open(main_py_path, 'w') as f:
            f.write(updated_content)
        
        print("✅ Groq API key configured successfully!")
        print("🎉 You can now run the Resume Analyzer with ultra-fast AI responses!")
        print()
        print("To start the server, run: python3 main.py")
        
    except Exception as e:
        print(f"❌ Error configuring API key: {e}")

if __name__ == "__main__":
    setup_groq_api() 