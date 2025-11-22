# 🔑 Setting Up Groq API Key

## Quick Setup

### Option 1: Using the Setup Script (Easiest)

```bash
./setup_api_key.sh
```

This will prompt you for your API key and create a `.env` file.

### Option 2: Manual Setup

1. **Get your API key:**
   - Visit: https://console.groq.com/
   - Sign in or create a free account
   - Go to "API Keys" section
   - Click "Create API Key"
   - Copy your key (starts with `gsk_`)

2. **Create .env file:**
   ```bash
   echo "GROQ_API_KEY=your_key_here" > .env
   ```

3. **Or export it:**
   ```bash
   export GROQ_API_KEY=your_key_here
   ```

## Verify Setup

Test your API key:
```bash
python3 test_groq_key.py
```

## Running the Application

After setting up the API key:

```bash
# If using .env file, it will be loaded automatically
python3 main.py

# Or export it first
export GROQ_API_KEY=your_key_here
python3 main.py
```

## Troubleshooting

**"API key not configured" warning:**
- Make sure `.env` file exists in the project root
- Or export `GROQ_API_KEY` environment variable
- Check that the key starts with `gsk_`

**API errors:**
- Verify your key is valid at https://console.groq.com/
- Check your API quota/limits
- Ensure you have internet connection

**Application works without API key:**
- Basic resume parsing will work
- AI-powered features will be disabled
- Job matching will use fallback methods

