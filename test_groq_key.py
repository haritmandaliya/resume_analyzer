#!/usr/bin/env python3
"""
Test script to verify Groq API key configuration
"""

import requests
import json

def test_groq_key():
    """Test if Groq API key is properly configured"""
    print("🔑 Testing Groq API Key Configuration")
    print("=" * 40)
    
    # Read the API key from main.py
    try:
        with open('main.py', 'r') as f:
            content = f.read()
            lines = content.split('\n')
            api_key_line = None
            for line in lines:
                if 'GROQ_API_KEY = ' in line:
                    api_key_line = line
                    break
            
            if api_key_line:
                # Extract the API key
                api_key = api_key_line.split('"')[1]
                print(f"📋 Found API key: {api_key[:10]}...")
                
                if api_key == "gsk_...":
                    print("❌ API key is still set to placeholder!")
                    print("🔧 Please configure your actual Groq API key:")
                    print("1. Get your key from: https://console.groq.com/")
                    print("2. Update main.py line 43 with your actual key")
                    return False
                else:
                    print("✅ API key appears to be configured")
                    
                    # Test the API key
                    print("\n🧪 Testing API key with Groq...")
                    url = "https://api.groq.com/openai/v1/chat/completions"
                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }
                    data = {
                        "model": "llama3-8b-8192",
                        "messages": [{"role": "user", "content": "Hello! Just testing the API key."}],
                        "max_tokens": 50,
                        "temperature": 0.3
                    }
                    
                    try:
                        response = requests.post(url, headers=headers, json=data, timeout=10)
                        if response.status_code == 200:
                            result = response.json()
                            ai_response = result['choices'][0]['message']['content']
                            print(f"✅ API key works! Response: {ai_response}")
                            return True
                        else:
                            print(f"❌ API key test failed: {response.status_code}")
                            print(f"Error: {response.text}")
                            return False
                    except Exception as e:
                        print(f"❌ Error testing API key: {e}")
                        return False
            else:
                print("❌ Could not find GROQ_API_KEY in main.py")
                return False
                
    except Exception as e:
        print(f"❌ Error reading main.py: {e}")
        return False

if __name__ == "__main__":
    success = test_groq_key()
    if success:
        print("\n🎉 Groq API key is working! You can now restart the server:")
        print("python3 main.py")
    else:
        print("\n🔧 Please configure your Groq API key first!") 