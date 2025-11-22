# Resume Analyzer - Single Server Edition

A modern, AI-powered resume analysis application built with React and FastAPI, served from a single server. Upload your resume and paste job descriptions to get intelligent matching insights and recommendations.

## ✨ Features

- **Modern React UI** - Beautiful, responsive interface with smooth animations
- **Single Server Setup** - React frontend served directly from FastAPI backend
- **Drag & Drop Upload** - Easy PDF resume upload with visual feedback
- **AI-Powered Analysis** - Intelligent skill matching and resume parsing
- **Real-time Results** - Instant analysis with detailed breakdowns
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- **Dark Theme** - Eye-friendly dark mode with modern aesthetics
- **File Management** - Organize and view uploaded resumes
- **History Tracking** - Keep track of previous analyses

## 🚀 Quick Start

### Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd resume_analyzer
   ```

2. **Start the single server**
   ```bash
   ./start_server.sh
   ```
   
   This will:
   - Install all dependencies
   - Build the React app
   - Start the FastAPI server
   - Serve everything on `http://localhost:8000`

3. **Access the application**
   - **Main App**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs

## 📁 Project Structure

```
resume_analyzer/
├── src/                    # React source code
│   ├── components/         # React components
│   │   ├── Sidebar.js      # Navigation sidebar
│   │   ├── ChatArea.js     # Main chat interface
│   │   ├── HomeView.js     # Home page with upload
│   │   ├── AnalysisResult.js # Results display
│   │   └── ResumeDetails.js # Resume details view
│   ├── App.js              # Main app component
│   └── index.js            # App entry point
├── build/                  # React production build (generated)
├── public/                 # Static assets
├── utils/                  # Python utilities
├── resumes/                # Uploaded resume storage
├── history/                # Analysis history
├── main.py                 # FastAPI backend (serves React)
├── package.json            # React dependencies
├── start_server.sh         # Single server startup script
└── README.md               # This file
```

## 🎨 UI Components

### Modern Design System
- **Color Palette**: Dark theme with blue accents
- **Typography**: Inter font family for readability
- **Animations**: Smooth transitions with Framer Motion
- **Icons**: Lucide React icons for consistency
- **Responsive**: Mobile-first design approach

### Key Components
- **Sidebar**: Navigation and file management
- **HomeView**: File upload and job description input
- **AnalysisResult**: Detailed matching results
- **ResumeDetails**: Comprehensive resume information

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
REACT_APP_API_URL=http://localhost:8000
```

### Backend Configuration
The FastAPI backend is configured to:
- Accept PDF file uploads
- Parse resume content using PyPDF2
- Perform fuzzy skill matching
- Store analysis history
- Serve React build files

## 📱 Usage

1. **Upload Resume**: Drag and drop or click to upload PDF resumes
2. **Add Job Description**: Paste the job description or requirements
3. **Analyze**: Click "Analyze Resume" to get results
4. **View Results**: See detailed matching scores and skill analysis
5. **Browse History**: Access previous analyses from the sidebar

## 🛠️ Development

### Available Scripts

```bash
# Start single server (production)
./start_server.sh

# Build React app only
npm run build

# Start React development server (for development only)
npm start

# Run tests
npm test
```

### Code Style
- Use functional components with hooks
- Follow React best practices
- Implement proper error handling
- Use TypeScript for better type safety (optional)

## 🚀 Deployment

### Single Server Deployment
```bash
# Build and start production server
./start_server.sh

# Or manually
npm run build
python3 main.py
```

### Docker Deployment (Optional)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y nodejs npm
RUN npm install
RUN npm run build
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "main.py"]
```

## 🔧 API Endpoints

- `GET /` - Serve React app
- `GET /api/resumes` - Get list of uploaded resumes
- `GET /api/jd-history` - Get job description history
- `POST /api/process_input/` - Process resume and job description
- `GET /api/resume/{filename}` - Get specific resume data
- `GET /docs` - API documentation (Swagger UI)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [React](https://reactjs.org/) - Frontend framework
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [Framer Motion](https://www.framer.com/motion/) - Animation library
- [Lucide React](https://lucide.dev/) - Icon library
- [React Dropzone](https://react-dropzone.js.org/) - File upload
- [React Hot Toast](https://react-hot-toast.com/) - Notifications

## 📞 Support

If you have any questions or need help, please open an issue on GitHub or contact the development team.

---

**Made with ❤️ by the Resume Analyzer Team** 