# Resume Analyzer - AI-Powered HR Tool

A comprehensive, AI-powered resume analysis application that helps HR professionals and recruiters efficiently analyze resumes, match candidates against job descriptions, and make data-driven hiring decisions. Built with modern technologies including React, TypeScript, FastAPI, and Groq AI.

## 🎯 Overview

Resume Analyzer is a full-stack web application that combines intelligent PDF parsing, AI-powered analysis, and an intuitive user interface to streamline the resume screening process. The application extracts key information from resumes, matches candidates against job descriptions, and provides detailed insights including skill matching, experience analysis, and personalized recommendations.

## ✨ Key Features

- **🤖 AI-Powered Analysis** - Leverages Groq AI for intelligent resume parsing and job matching
- **📄 PDF Resume Parsing** - Automatically extracts contact info, skills, education, experience, and projects
- **🎯 Job Description Matching** - Smart skill matching with match percentage scores
- **💬 Interactive Chat Interface** - AI assistant for guidance and support
- **📊 Batch Analysis** - Analyze multiple resumes simultaneously against a job description
- **📈 Detailed Insights** - Comprehensive analysis with education, experience, and project summaries
- **🎨 Modern UI** - Beautiful, responsive React interface with dark theme
- **📱 Responsive Design** - Works seamlessly on desktop, tablet, and mobile devices
- **📚 History Tracking** - Maintains analysis history for future reference
- **🔍 Advanced Search** - Fuzzy matching for skills and keywords

## 🛠️ Technology Stack

### Frontend
- **React 18** - Modern UI framework
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Smooth animations
- **Lucide React** - Icon library
- **React Dropzone** - File upload component
- **Axios** - HTTP client

### Backend
- **FastAPI** - High-performance Python web framework
- **Uvicorn** - ASGI server
- **pdfplumber** - PDF text extraction
- **rapidfuzz** - Fuzzy string matching
- **Groq AI** - AI-powered analysis and summaries
- **Python 3.8+** - Backend runtime

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Node.js** (v16 or higher) - [Download](https://nodejs.org/)
- **Python** (v3.8 or higher) - [Download](https://www.python.org/downloads/)
- **npm** (comes with Node.js) or **yarn**
- **pip** (Python package manager)
- **Git** - For version control

### Verify Installation

```bash
# Check Node.js version
node --version  # Should be v16 or higher

# Check Python version
python3 --version  # Should be 3.8 or higher

# Check npm version
npm --version

# Check pip version
pip --version
```

## 🚀 Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/haritmandaliya/resume_analyzer.git
cd resume_analyzer
```

### Step 2: Install Dependencies

#### Install Python Dependencies

```bash
# Using pip
pip install -r requirements.txt

# Or using pip3
pip3 install -r requirements.txt

# If you encounter permission issues, use:
pip install --user -r requirements.txt
```

#### Install Node.js Dependencies

```bash
npm install
```

### Step 3: Configure Groq API Key

The application uses Groq AI for intelligent analysis. You need to obtain a Groq API key:

1. Visit [Groq Console](https://console.groq.com/)
2. Sign up or log in
3. Create an API key
4. Update the API key in `main.py`:

```python
# In main.py, line 44
GROQ_API_KEY = "your_groq_api_key_here"
```

**Note:** For production, consider using environment variables:

```bash
# Create a .env file
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

Then update `main.py` to read from environment:

```python
import os
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your_default_key")
```

### Step 4: Create Required Directories

The application will create these automatically, but you can create them manually:

```bash
mkdir -p resumes
mkdir -p history/JDhistory
```

## 🏃 Running the Application

### Option 1: Using the Startup Script (Recommended)

The easiest way to run the application:

```bash
# Make the script executable (first time only)
chmod +x start_server.sh

# Run the startup script
./start_server.sh
```

This script will:
- ✅ Check prerequisites (Node.js, Python, npm)
- ✅ Install dependencies if needed
- ✅ Build the React application
- ✅ Start the FastAPI server
- ✅ Serve everything on `http://localhost:8000`

### Option 2: Manual Setup

If you prefer to run steps manually:

```bash
# 1. Install dependencies (if not already done)
npm install
pip install -r requirements.txt

# 2. Build the React app
npm run build

# 3. Start the FastAPI server
python3 main.py
```

### Option 3: Development Mode

For development with hot-reload:

```bash
# Terminal 1: Start React dev server
npm run dev

# Terminal 2: Start FastAPI server
python3 main.py
```

**Note:** In development mode, React runs on `http://localhost:5173` and FastAPI on `http://localhost:8000`. You'll need to configure CORS or use a proxy.

## 🌐 Accessing the Application

Once the server is running, access the application at:

- **Main Application**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

## 📖 Usage Guide

### 1. Upload a Resume

- Click the **"+"** button or drag and drop a PDF file
- Supported format: PDF only
- The system will automatically parse the resume

### 2. Analyze Against Job Description

- Paste the job description in the chat area
- Click **"Analyze"** or send the message
- View match percentage and detailed analysis

### 3. Batch Analysis

- Upload multiple resumes
- Provide a job description
- Get ranked results with match scores

### 4. View Resume Details

- Click on any resume from the sidebar
- View extracted information:
  - Contact details
  - Skills
  - Education history
  - Work experience
  - Projects
  - AI-generated summaries

### 5. Chat with AI Assistant

- Use the chat interface for help
- Ask questions about features
- Get guidance on using the application

## 📁 Project Structure

```
resume_analyzer/
├── src/                          # React frontend source
│   ├── components/               # React components
│   │   ├── Header.tsx           # Application header
│   │   ├── Sidebar.tsx          # Navigation sidebar
│   │   ├── ChatArea.tsx         # Main chat interface
│   │   ├── FileUpload.tsx       # File upload component
│   │   └── BatchAnalysisView.tsx # Batch analysis view
│   ├── types/                   # TypeScript type definitions
│   │   └── index.ts
│   ├── App.tsx                  # Main app component
│   ├── main.tsx                 # React entry point
│   └── index.css                # Global styles
├── utils/                        # Python utilities
│   └── resume_parser.py         # PDF parsing functions
├── resumes/                      # Uploaded resume storage
├── history/                      # Analysis history
│   └── JDhistory/               # Job description history
├── build/                        # React production build (generated)
├── public/                       # Static assets
├── main.py                      # FastAPI backend server
├── requirements.txt             # Python dependencies
├── package.json                 # Node.js dependencies
├── start_server.sh              # Startup script
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory (optional):

```env
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Application Settings
ENABLE_AI_SUMMARIES=true
```

### Backend Configuration

Key settings in `main.py`:

```python
# API Configuration
GROQ_API_KEY = "your_api_key"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
GROQ_MODEL = "llama-3.1-8b-instant"
ENABLE_AI_SUMMARIES = True

# Server Configuration
HOST = "0.0.0.0"
PORT = 8000
```

## 🧪 Testing

### Test PDF Parsing

```bash
python3 test_parsing.py
```

### Test Groq Integration

```bash
python3 test_groq_integration.py
```

### Test Real Resume Parsing

```bash
python3 test_real_parsing.py
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Port Already in Use

```bash
# Error: Address already in use
# Solution: Change port in main.py or kill the process
lsof -ti:8000 | xargs kill -9
```

#### 2. Module Not Found Error

```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --force-reinstall
npm install
```

#### 3. Build Errors

```bash
# Clear cache and rebuild
rm -rf node_modules build
npm install
npm run build
```

#### 4. PDF Parsing Issues

- Ensure PDFs are not password-protected
- Check that PDFs contain selectable text (not just images)
- Verify pdfplumber is installed: `pip install pdfplumber`

#### 5. Groq API Errors

- Verify API key is correct
- Check API quota/limits
- Ensure internet connection is active
- Review error logs in terminal

### Getting Help

If you encounter issues:

1. Check the [Issues](https://github.com/haritmandaliya/resume_analyzer/issues) page
2. Review error messages in the terminal
3. Check API documentation at `/docs`
4. Verify all prerequisites are installed

## 🔄 Git Workflow

This project uses a **Git Flow** workflow:

### Branches

- **`main`** - Production-ready code
- **`develop`** - Development branch for integration

### Contributing

1. **Clone the repository**
   ```bash
   git clone https://github.com/haritmandaliya/resume_analyzer.git
   cd resume_analyzer
   ```

2. **Create a feature branch**
   ```bash
   git checkout develop
   git checkout -b feature/your-feature-name
   ```

3. **Make changes and commit**
   ```bash
   git add .
   git commit -m "Add: Description of your changes"
   ```

4. **Push to remote**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request** on GitHub

### Pushing to GitHub

If you encounter authentication issues:

```bash
# Option 1: Use SSH (recommended)
git remote set-url origin git@github.com:haritmandaliya/resume_analyzer.git

# Option 2: Use Personal Access Token
# Generate token at: https://github.com/settings/tokens
git remote set-url origin https://YOUR_TOKEN@github.com/haritmandaliya/resume_analyzer.git

# Then push
git push -u origin develop
git push -u origin main
```

## 🚀 Deployment

### Production Deployment

1. **Build the application**
   ```bash
   npm run build
   ```

2. **Set environment variables**
   ```bash
   export GROQ_API_KEY=your_production_key
   ```

3. **Run with production server**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

### Docker Deployment (Optional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install Node.js
RUN apt-get update && apt-get install -y nodejs npm

# Copy files
COPY . .

# Install dependencies
RUN npm install
RUN pip install -r requirements.txt

# Build React app
RUN npm run build

# Expose port
EXPOSE 8000

# Run server
CMD ["python3", "main.py"]
```

Build and run:

```bash
docker build -t resume-analyzer .
docker run -p 8000:8000 -e GROQ_API_KEY=your_key resume-analyzer
```

## 📡 API Endpoints

### Resume Management

- `GET /api/resumes` - Get list of uploaded resumes
- `GET /api/resume/{filename}` - Get specific resume data
- `GET /api/resume-analysis/{filename}` - Get resume analysis with match scores
- `POST /api/upload` - Upload a single resume

### Analysis

- `POST /api/process_input/` - Process resume and job description
- `POST /api/batch-analyze/` - Batch analyze multiple resumes

### Job Description

- `GET /api/jd-history` - Get job description history
- `POST /api/improve-jd` - Improve job description with AI

### Chat & AI

- `POST /api/chat` - Basic AI chat
- `POST /api/smart-chat` - Smart AI chat with intent understanding

### Documentation

- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use ESLint/Prettier for JavaScript/TypeScript
- Write meaningful commit messages
- Add comments for complex logic

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [React](https://reactjs.org/) - Frontend framework
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [Groq AI](https://groq.com/) - AI-powered analysis
- [Framer Motion](https://www.framer.com/motion/) - Animation library
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework
- [pdfplumber](https://github.com/jsvine/pdfplumber) - PDF parsing
- [Lucide React](https://lucide.dev/) - Icon library

## 📞 Support & Contact

- **GitHub Issues**: [Report Issues](https://github.com/haritmandaliya/resume_analyzer/issues)
- **Repository**: https://github.com/haritmandaliya/resume_analyzer

## 📝 Changelog

### Version 1.0.0
- Initial release
- AI-powered resume parsing
- Job description matching
- Batch analysis support
- Interactive chat interface
- Modern React UI

---

**Made with ❤️ by the Resume Analyzer Team**

For questions, suggestions, or contributions, please open an issue on GitHub.
