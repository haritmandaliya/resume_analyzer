#!/bin/bash

# Script to set up Groq API key

echo "🔑 Groq API Key Setup"
echo "===================="
echo ""
echo "To get your Groq API key:"
echo "1. Visit: https://console.groq.com/"
echo "2. Sign in or create a free account"
echo "3. Go to API Keys section"
echo "4. Click 'Create API Key'"
echo "5. Copy your key (starts with 'gsk_')"
echo ""
read -p "Enter your Groq API key: " api_key

if [ -z "$api_key" ]; then
    echo "❌ No API key provided"
    exit 1
fi

# Create .env file
echo "GROQ_API_KEY=$api_key" > .env
echo ""
echo "✅ API key saved to .env file"
echo ""
echo "📝 To use it, run:"
echo "   source .env"
echo "   python3 main.py"
echo ""
echo "Or export it:"
echo "   export GROQ_API_KEY=$api_key"

