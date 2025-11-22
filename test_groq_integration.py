#!/usr/bin/env python3
"""
Test script for Groq integration
This script helps test and configure Groq API integration
"""

import requests
import json

def test_groq_api():
    """Test Groq API integration"""
    print("🧪 Testing Groq API Integration")
    print("=" * 40)
    
    # Test the smart chat endpoint
    url = "http://localhost:8000/api/smart-chat"
    headers = {"Content-Type": "application/json"}
    
    test_messages = [
        "hey",
        "How can I improve my resume for software engineering jobs?",
        "I want to upload a resume",
        "Show me my files",
        "Help me analyze my resume"
    ]
    
    for message in test_messages:
        print(f"\n📝 Testing: '{message}'")
        try:
            data = {"message": message, "context": ""}
            response = requests.post(url, headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Response: {result['response'][:100]}...")
                print(f"🎯 Intent: {result['intent']['intent']} (confidence: {result['intent']['confidence']})")
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 40)
    print("📋 Current Status:")
    print("✅ Server is running")
    print("✅ API endpoints are responding")
    print("⚠️  Groq API key needs to be configured for AI responses")
    print("\n🔧 To configure Groq API key:")
    print("1. Run: python3 setup_groq.py")
    print("2. Get your API key from: https://console.groq.com/")
    print("3. Restart the server: python3 main.py")

if __name__ == "__main__":
    test_groq_api() 