from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import re
import requests
from rapidfuzz import fuzz  # ✅ For fuzzy skill matching
from datetime import datetime
from pathlib import Path

from utils.resume_parser import (
    extract_resume_text,
    extract_email,
    extract_phone,
    extract_name,
    extract_skills,
    extract_education,
    extract_experience,
    extract_projects
)

app = FastAPI(title="Resume Analyzer API", version="1.0.0")

# CORS middleware for React frontend
# Allow all common development ports and production
# In production, replace "*" with specific allowed origins
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:4000",
    "http://localhost:5173",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:4000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",
]

# For development, allow all origins
# In production, use specific origins only
import os
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
if ENVIRONMENT == "development":
    allowed_origins.append("*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Serve React build files
build_path = Path("build")
if build_path.exists():
    app.mount("/static", StaticFiles(directory="build/static"), name="static")

UPLOAD_DIR = "resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Configuration
import os
from pathlib import Path

# Load .env file if it exists
env_file = Path(".env")
if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")  # Set via environment variable
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
GROQ_MODEL = "llama-3.1-8b-instant"  # Fast and capable model
ENABLE_AI_SUMMARIES = True  # Enable AI summaries with Groq

def call_groq(prompt, system_prompt="", max_tokens=500):
    """Call Groq API with optimized settings for fast, reliable responses"""
    # Check if API key is configured
    if not GROQ_API_KEY or GROQ_API_KEY == "":
        print("⚠️  Groq API key not configured. AI features will be disabled.")
        print("💡 Set GROQ_API_KEY environment variable or create .env file")
        return None
    
    try:
        url = f"{GROQ_BASE_URL}/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": GROQ_MODEL,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.3,  # Low temperature for consistent responses
            "top_p": 0.8,       # Focused responses
            "stream": False
        }
        
        # Very short timeout for fast responses
        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        ai_response = result.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        
        # Clean up the response - only for short chat responses
        if ai_response and max_tokens <= 500:
            # Remove any markdown formatting that might cause issues
            ai_response = ai_response.replace('**', '').replace('*', '')
            # Ensure it's not too long
            if len(ai_response) > 300:
                ai_response = ai_response[:300] + "..."
        
        return ai_response
        
    except requests.exceptions.Timeout:
        print(f"Groq timeout - using fallback response")
        return None
    except requests.exceptions.ConnectionError:
        print(f"Groq connection error - using fallback response")
        return None
    except Exception as e:
        print(f"Error calling Groq: {e}")
        return None

def improve_job_description(jd: str) -> str:
    """Improve job description with better grammar and clarity"""
    system_prompt = """You are a professional HR assistant. Improve the given job description by:
1. Fixing grammar and spelling mistakes
2. Making it more professional and clear
3. Adding relevant keywords for better matching
4. Structuring it properly with requirements and responsibilities
Keep the original meaning but make it more effective for resume matching."""
    
    prompt = f"Please improve this job description:\n\n{jd}"
    improved_jd = call_groq(prompt, system_prompt)
    return improved_jd if improved_jd else jd

def analyze_resume_with_ai(resume_text: str, job_description: str) -> dict:
    """Use AI to analyze resume against job description"""
    system_prompt = """You are an expert resume analyzer. Analyze the resume against the job description and provide:
1. Match score (0-100)
2. Matched skills (list)
3. Missing skills (list)
4. Recommendations for improvement
5. Overall assessment
Return your analysis in a structured, professional manner."""
    
    prompt = f"""Resume Text:
{resume_text}

Job Description:
{job_description}

Please provide a detailed analysis including match score, matched skills, missing skills, and recommendations."""
    
    ai_analysis = call_groq(prompt, system_prompt)
    
    # Extract structured data from AI response
    analysis = {
        "ai_analysis": ai_analysis,
        "match_score": 0,
        "matched_skills": [],
        "missing_skills": [],
        "recommendations": []
    }
    
    # Try to extract score from AI response
    score_match = re.search(r'(\d+)%', ai_analysis)
    if score_match:
        analysis["match_score"] = int(score_match.group(1))
    
    # Extract skills (basic extraction - can be improved)
    skills_match = re.search(r'matched skills?[:\s]+(.*?)(?:\n|$)', ai_analysis, re.IGNORECASE)
    if skills_match:
        skills_text = skills_match.group(1)
        analysis["matched_skills"] = [s.strip() for s in skills_text.split(',') if s.strip()]
    
    return analysis

def generate_user_response(user_input: str, context: str = "") -> str:
    """Generate helpful user responses using AI"""
    system_prompt = """You are a helpful AI assistant for a resume analyzer application. You can help users with:

1. **Resume Analysis**: Explain how to upload and analyze resumes
2. **Job Matching**: Help users understand skill matching and job descriptions
3. **File Management**: Guide users on viewing and managing uploaded files
4. **General Help**: Answer questions about the application features

Be friendly, concise, and helpful. If the user asks about specific features, explain them clearly.
If they need help with a task, guide them step by step."""

    prompt = f"""Context: {context}
User Input: {user_input}

Provide a helpful response:"""
    
    response = call_groq(prompt, system_prompt)
    return response if response else "I'm here to help you analyze resumes! You can upload PDF files and provide job descriptions for analysis."

def understand_user_intent(user_input: str) -> dict:
    """Understand what the user wants to do"""
    system_prompt = """You are an AI assistant that understands user intentions. Analyze the user's input and return a JSON response with:

{
  "intent": "upload_resume|analyze_resume|view_files|show_details|get_help|chat",
  "confidence": 0.0-1.0,
  "entities": {
    "filename": "specific filename if mentioned",
    "action": "specific action requested",
    "query": "what they're asking about"
  },
  "response_type": "action|information|help"
}

Common intents:
- upload_resume: "upload", "add", "new resume", "pdf"
- analyze_resume: "analyze", "match", "compare", "job description"
- view_files: "show files", "list", "what files", "available"
- show_details: "details", "full details", "show me", "view resume"
- get_help: "help", "how to", "what can", "explain"
- chat: general conversation, questions, greetings"""

    prompt = f"""Analyze this user input: "{user_input}"

Return only the JSON response:"""
    
    try:
        response = call_groq(prompt, system_prompt)
        # Try to extract JSON from response
        import re
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except:
        pass
    
    # Fallback intent detection
    user_lower = user_input.lower()
    
    if any(word in user_lower for word in ['upload', 'add', 'new', 'pdf']):
        return {"intent": "upload_resume", "confidence": 0.8, "entities": {}, "response_type": "action"}
    elif any(word in user_lower for word in ['analyze', 'match', 'compare', 'job']):
        return {"intent": "analyze_resume", "confidence": 0.8, "entities": {}, "response_type": "action"}
    elif any(word in user_lower for word in ['show files', 'list', 'what files', 'available']):
        return {"intent": "view_files", "confidence": 0.8, "entities": {}, "response_type": "action"}
    elif any(word in user_lower for word in ['details', 'show me', 'view resume', 'full details']):
        return {"intent": "show_details", "confidence": 0.8, "entities": {}, "response_type": "action"}
    elif any(word in user_lower for word in ['help', 'how to', 'what can', 'explain']):
        return {"intent": "get_help", "confidence": 0.8, "entities": {}, "response_type": "information"}
    else:
        return {"intent": "chat", "confidence": 0.6, "entities": {}, "response_type": "information"}

def generate_smart_response(user_input: str, context: str = "") -> dict:
    """Generate intelligent responses using Groq AI for all interactions"""
    try:
        user_input_lower = user_input.lower().strip()
        
        # Quick intent detection for routing
        if any(word in user_input_lower for word in ['hey', 'hello', 'hi']) and len(user_input_lower.split()) <= 3:
            intent = "greeting"
        elif any(word in user_input_lower for word in ['upload', 'add', 'new resume', 'pdf', 'file']) and not any(word in user_input_lower for word in ['show', 'list', 'view']):
            intent = "upload_resume"
        elif any(word in user_input_lower for word in ['show', 'list', 'view', 'see']) and any(word in user_input_lower for word in ['files', 'resumes', 'all']):
            intent = "view_files"
        elif any(word in user_input_lower for word in ['analyze', 'analysis', 'match', 'compare', 'job description']):
            intent = "analyze_resume"
        elif any(word in user_input_lower for word in ['details', 'full', 'complete', 'show me', 'view resume']):
            intent = "show_details"
        elif any(word in user_input_lower for word in ['help', 'how to', 'what can', 'explain', 'guide']):
            intent = "get_help"
        elif any(word in user_input_lower for word in ['thanks', 'thank you', 'appreciate']):
            intent = "gratitude"
        elif any(word in user_input_lower for word in ['skill', 'improve', 'better', 'enhance', 'optimize']):
            intent = "skill_improvement"
        elif any(word in user_input_lower for word in ['job', 'position', 'career', 'role']):
            intent = "career_advice"
        else:
            intent = "chat"
        
        # Use Groq AI for intelligent, contextual responses
        system_prompt = """You are an AI assistant specifically designed for a Resume Analyzer application. 

You are NOT a general chatbot - you are a specialized resume analysis expert. Your primary purpose is to help users with:

1. **Resume Analysis**: Upload PDF resumes and get detailed insights
2. **Job Matching**: Compare resumes against job descriptions with match percentages
3. **Skill Analysis**: Identify matched skills, missing skills, and extra skills
4. **File Management**: Help users view and manage their uploaded resumes
5. **Career Guidance**: Provide specific advice for resume improvement

IMPORTANT: Always stay focused on resume analysis and career-related topics. If users ask about other topics, gently redirect them back to resume analysis features.

Be warm, professional, and specific about resume analysis capabilities. Keep responses concise but informative."""

        # Create context-aware prompt based on intent
        if intent == "greeting":
            prompt = f"User greeted me with: '{user_input}'. As a Resume Analyzer AI assistant, give a warm welcome and briefly explain that I can help with resume analysis, job matching, skill assessment, and career guidance."
        elif intent == "upload_resume":
            prompt = f"User wants to upload a resume: '{user_input}'. As a Resume Analyzer assistant, explain how to upload PDF resumes and what analysis they'll receive (skill matching, job compatibility, detailed insights)."
        elif intent == "view_files":
            prompt = f"User wants to see files: '{user_input}'. As a Resume Analyzer assistant, explain how to view their uploaded resumes and access detailed analysis reports with match scores and skill breakdowns."
        elif intent == "analyze_resume":
            prompt = f"User wants to analyze a resume: '{user_input}'. As a Resume Analyzer assistant, explain the comprehensive analysis process including skill matching, job compatibility scoring, and detailed insights they'll receive."
        elif intent == "show_details":
            prompt = f"User wants to see resume details: '{user_input}'. As a Resume Analyzer assistant, explain the detailed information available including skill analysis, experience summaries, education details, and project highlights."
        elif intent == "get_help":
            prompt = f"User needs help: '{user_input}'. As a Resume Analyzer assistant, provide a helpful overview of my specialized capabilities for resume analysis, job matching, and career guidance."
        elif intent == "gratitude":
            prompt = f"User said thanks: '{user_input}'. As a Resume Analyzer assistant, respond warmly and encourage them to continue using the resume analysis features."
        elif intent == "skill_improvement":
            prompt = f"User asked about skills: '{user_input}'. As a Resume Analyzer assistant, provide specific advice about resume skills, how to identify skill gaps, and how our analysis can help improve their resume."
        elif intent == "career_advice":
            prompt = f"User asked about career: '{user_input}'. As a Resume Analyzer assistant, provide helpful career guidance specifically related to resume optimization and job application strategies."
        else:
            prompt = f"User said: '{user_input}'. As a Resume Analyzer assistant, provide a helpful response focused on resume analysis, job matching, or career guidance. If the topic is unrelated, gently redirect to resume analysis features."

        # Call Groq AI for intelligent response
        ai_response = call_groq(prompt, system_prompt)
        
        # If Groq fails, provide a simple fallback
        if not ai_response:
            ai_response = "I'm here to help with your resume analysis! 📄 You can upload resumes, analyze them against job descriptions, and get detailed insights. What would you like to do?"
        
        # Get suggested actions
        suggested_actions = get_suggested_actions(intent)
        
        return {
            "response": ai_response,
            "intent": {
                "intent": intent,
                "confidence": 0.95,
                "entities": {},
                "response_type": "text"
            },
            "suggested_actions": suggested_actions,
            "type": "smart_response"
        }
    except Exception as e:
        print(f"Error in generate_smart_response: {e}")
        return {
            "response": "I'm here to help with your resume analysis! 📄 You can upload resumes, analyze them against job descriptions, and get detailed insights. What would you like to do?",
            "intent": {"intent": "chat", "confidence": 0.5, "entities": {}, "response_type": "text"},
            "suggested_actions": ["📄 Upload a resume", "📁 View files", "🔍 Get help"],
            "type": "smart_response"
        }

def get_suggested_actions(intent: str) -> list:
    """Get helpful and context-aware suggested actions"""
    suggestions = {
        "upload_resume": [
            "📄 Click the + button to select PDF files",
            "🖱️ Drag and drop PDF resumes into the chat area",
            "📁 Upload multiple files for batch analysis",
            "💡 Need help? Ask me about the upload process"
        ],
        "analyze_resume": [
            "📄 First, upload your resume using the + button",
            "📝 Type your job description in the chat box",
            "📁 Click the file icon to see all available resumes",
            "🎯 I'll provide detailed match analysis and recommendations"
        ],
        "view_files": [
            "📁 Click the file icon to see all uploaded resumes",
            "🔍 Type 'show me all files' to list available resumes",
            "📊 Click on any file name to view its detailed analysis",
            "📈 See match percentages and skill breakdowns"
        ],
        "show_details": [
            "📁 Click the file icon to see all resumes",
            "📊 Type 'show me full details' to see the most recent resume",
            "🎯 Click on any resume name to view complete analysis",
            "📈 Get match percentages, skills, and recommendations"
        ],
        "get_help": [
            "📄 I can help you upload and analyze resumes",
            "🔍 Try uploading a PDF and asking for analysis",
            "📁 Ask me about viewing and managing your files",
            "🎯 Get personalized recommendations for improvement"
        ],
        "greeting": [
            "📄 Upload a resume to get started",
            "🔍 Ask me how to analyze resumes",
            "📁 View your uploaded files",
            "💡 Learn about all available features"
        ],
        "gratitude": [
            "📄 Continue with resume analysis",
            "📁 View your uploaded files",
            "🔍 Get help with any questions",
            "🎯 Explore advanced features"
        ],
        "skill_improvement": [
            "📄 Upload your resume for personalized analysis",
            "🔍 Get specific skill recommendations",
            "📊 View detailed skill matching results",
            "🎯 Receive tailored improvement suggestions"
        ],
        "career_advice": [
            "📄 Upload your resume for career analysis",
            "🔍 Match against specific job descriptions",
            "📊 Get detailed career insights",
            "🎯 Receive personalized career guidance"
        ],
        "chat": [
            "📄 I'm here to help with resume analysis",
            "🔍 Try uploading a PDF file to get started",
            "📁 Ask me about any feature you'd like to use",
            "💡 Get personalized guidance for your needs"
        ]
    }
    
    return suggestions.get(intent, ["📄 I'm here to help! What would you like to do?"])

def generate_education_summary(education_data: list) -> str:
    """Generate comprehensive AI summary for education section"""
    if not education_data:
        return "No education information found in the resume."
    
    system_prompt = """You are an expert resume analyst specializing in educational background analysis. Provide comprehensive, detailed insights about the candidate's academic journey, achievements, and career preparation."""
    
    education_text = "\n".join([
        f"Degree: {edu.get('degree', 'N/A')}, Institution: {edu.get('institution', 'N/A')}, Year: {edu.get('year', 'N/A')}, GPA: {edu.get('gpa', 'N/A')}, Courses: {', '.join(edu.get('courses', []))}, Achievements: {', '.join(edu.get('achievements', []))}, Activities: {', '.join(edu.get('activities', []))}"
        for edu in education_data
    ])
    
    prompt = f"""Provide a comprehensive analysis of this educational background:

{education_text}

Include in your analysis:
1. Academic performance and GPA interpretation
2. Institution quality and reputation
3. Relevant coursework and technical skills gained
4. Academic achievements and activities
5. Career alignment and preparation
6. Areas of excellence and strengths
7. Overall educational journey assessment

Make it detailed, professional, and actionable for career development."""
    
    summary = call_groq(prompt, system_prompt, max_tokens=1000)
    if summary:
        # Clean up the text - add spaces where missing
        summary = re.sub(r'([a-z])([A-Z])', r'\1 \2', summary)  # Add space between lowercase and uppercase
        summary = re.sub(r'([.!?])([A-Z])', r'\1 \2', summary)  # Add space after punctuation
        summary = re.sub(r'\s+', ' ', summary)  # Normalize multiple spaces
        summary = summary.strip()
    return summary if summary else "Comprehensive education analysis shows strong academic foundation and relevant qualifications."

def generate_experience_summary(experience_data: list) -> str:
    """Generate comprehensive AI summary for work experience section"""
    if not experience_data:
        return "No work experience information found in the resume."
    
    system_prompt = """You are an expert resume analyst specializing in professional experience analysis. Provide comprehensive insights about the candidate's career progression, achievements, and professional development."""
    
    experience_text = "\n".join([
        f"Title: {exp.get('title', 'N/A')}, Company: {exp.get('company', 'N/A')}, Duration: {exp.get('duration', 'N/A')}, Responsibilities: {', '.join(exp.get('responsibilities', []))}, Achievements: {', '.join(exp.get('achievements', []))}, Technologies: {', '.join(exp.get('technologies', []))}"
        for exp in experience_data
    ])
    
    prompt = f"""Provide a comprehensive analysis of this work experience:

{experience_text}

Include in your analysis:
1. Career progression and role evolution
2. Key responsibilities and impact
3. Notable achievements and contributions
4. Technical skills and technologies used
5. Industry experience and company quality
6. Professional growth and development
7. Transferable skills and competencies
8. Overall professional trajectory assessment

Make it detailed, professional, and highlight career value."""
    
    summary = call_groq(prompt, system_prompt, max_tokens=1000)
    if summary:
        # Clean up the text - add spaces where missing
        summary = re.sub(r'([a-z])([A-Z])', r'\1 \2', summary)  # Add space between lowercase and uppercase
        summary = re.sub(r'([.!?])([A-Z])', r'\1 \2', summary)  # Add space after punctuation
        summary = re.sub(r'\s+', ' ', summary)  # Normalize multiple spaces
        summary = summary.strip()
    return summary if summary else "Comprehensive work experience analysis demonstrates strong professional background and relevant skills."

def generate_projects_summary(projects_data: list) -> str:
    """Generate comprehensive AI summary for projects section"""
    if not projects_data:
        return "No project information found in the resume."
    
    system_prompt = """You are an expert resume analyst specializing in project portfolio analysis. Provide comprehensive insights about the candidate's technical capabilities, problem-solving skills, and project management abilities."""
    
    projects_text = "\n".join([
        f"Project: {proj.get('name', 'N/A')}, Technologies: {', '.join(proj.get('technologies', []))}, Description: {', '.join(proj.get('description', []))}, Duration: {proj.get('duration', 'N/A')}, Role: {proj.get('role', 'N/A')}, Achievements: {', '.join(proj.get('achievements', []))}, GitHub: {proj.get('github', 'N/A')}, Live URL: {proj.get('live_url', 'N/A')}"
        for proj in projects_data
    ])
    
    prompt = f"""Provide a comprehensive analysis of these projects:

{projects_text}

Include in your analysis:
1. Technical complexity and sophistication
2. Technologies and tools demonstrated
3. Problem-solving approaches and methodologies
4. Project scope and impact
5. Role and responsibilities in each project
6. Achievements and outcomes
7. Code quality and deployment (GitHub, live URLs)
8. Portfolio diversity and skill breadth
9. Relevance to target positions
10. Overall technical competency assessment

Make it detailed, technical, and highlight practical skills."""
    
    summary = call_groq(prompt, system_prompt, max_tokens=1000)
    if summary:
        # Clean up the text - add spaces where missing
        summary = re.sub(r'([a-z])([A-Z])', r'\1 \2', summary)  # Add space between lowercase and uppercase
        summary = re.sub(r'([.!?])([A-Z])', r'\1 \2', summary)  # Add space after punctuation
        summary = re.sub(r'\s+', ' ', summary)  # Normalize multiple spaces
        summary = summary.strip()
    return summary if summary else "Comprehensive project analysis demonstrates strong technical skills and practical problem-solving abilities."

def parse_pdf_with_ai(pdf_text: str) -> dict:
    """Parse PDF text using Groq AI for better extraction and analysis"""
    try:
        system_prompt = """You are an expert resume parser and analyst. Your task is to extract ALL information from the resume text and return it as comprehensive JSON.

IMPORTANT: Be extremely thorough and extract EVERY detail you can find, including:
- ALL projects (academic, personal, professional)
- COMPLETE education details (courses, achievements, activities)
- FULL work experience with all responsibilities and achievements
- ALL skills (technical, soft skills, tools, languages)
- Contact information and personal details

Look for sections like: Projects, Academic Projects, Personal Projects, Work Experience, Education, Skills, Technical Skills, etc.

If you find projects in any section, extract them completely with full descriptions."""

        prompt = f"""Analyze this resume text and extract ALL information comprehensively:

{pdf_text}

Return only valid JSON with this EXACT structure (include ALL details found):
{{
  "name": "string or null",
  "email": "string or null", 
  "phone": "string or null",
  "skills": ["skill1", "skill2", "skill3"],
  "education": [
    {{
      "degree": "string",
      "institution": "string", 
      "year": "string",
      "gpa": "string",
      "courses": ["course1", "course2"],
      "achievements": ["achievement1", "achievement2"],
      "activities": ["activity1", "activity2"]
    }}
  ],
  "experience": [
    {{
      "title": "string",
      "company": "string",
      "duration": "string",
      "responsibilities": ["responsibility1", "responsibility2"],
      "achievements": ["achievement1", "achievement2"],
      "technologies": ["tech1", "tech2"]
    }}
  ],
  "projects": [
    {{
      "name": "string",
      "technologies": ["tech1", "tech2"],
      "description": ["description1", "description2"],
      "duration": "string",
      "role": "string",
      "achievements": ["achievement1", "achievement2"],
      "github": "string or null",
      "live_url": "string or null"
    }}
  ]
}}

CRITICAL: If you find ANY projects mentioned anywhere in the resume, extract them completely. Look for project names, descriptions, technologies used, and outcomes."""

        ai_response = call_groq(prompt, system_prompt, max_tokens=4096)
        
        if ai_response:
            # Try to extract JSON from the response
            import re
            import json
            
            # Look for JSON in the response
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                try:
                    parsed_data = json.loads(json_match.group())
                    return parsed_data
                except json.JSONDecodeError:
                    pass
            
            # If JSON extraction fails, try to parse manually
            return parse_pdf_manually(pdf_text)
        else:
            return parse_pdf_manually(pdf_text)
            
    except Exception as e:
        print(f"Error in AI PDF parsing: {e}")
        return parse_pdf_manually(pdf_text)

def parse_pdf_manually(pdf_text: str) -> dict:
    """Fallback for PDF parsing if Groq AI fails or is not available"""
    print("Attempting manual PDF parsing...")
    parsed_data = {
        "name": None,
        "email": None,
        "phone": None,
        "skills": [],
        "education": [],
        "experience": [],
        "projects": []
    }

    # Name extraction
    name_match = re.search(r'Name:\s*(.*?)\s*Email:', pdf_text)
    if name_match:
        parsed_data["name"] = name_match.group(1).strip()

    # Email extraction
    email_match = re.search(r'Email:\s*(.*?)\s*Phone:', pdf_text)
    if email_match:
        parsed_data["email"] = email_match.group(1).strip()

    # Phone extraction
    phone_match = re.search(r'Phone:\s*(.*?)\s*Skills:', pdf_text)
    if phone_match:
        parsed_data["phone"] = phone_match.group(1).strip()

    # Skills extraction
    skills_match = re.findall(r'Skills:\s*(.*?)\s*Education:', pdf_text)
    if skills_match:
        skills_text = skills_match[0].strip()
        parsed_data["skills"] = [s.strip() for s in skills_text.split(',') if s.strip()]

    # Education extraction - improved to capture all education entries
    education_section = re.search(r'EDUCATION(.*?)(?=ACHIEVEMENTS|HOBBIES|LANGUAGES|SKILLS|WORK EXPERIENCE)', pdf_text, re.DOTALL | re.IGNORECASE)
    if education_section:
        education_text = education_section.group(1).strip()
        education_entries = []
        
        # Split by degree patterns and extract each education entry properly
        degree_patterns = [
            r'(B\.?E\.?\s+in\s+[^•\n]+)',
            r'(Diploma\s+in\s+[^•\n]+)',
            r'(Bachelor\s+of\s+[^•\n]+)',
            r'(Master\s+of\s+[^•\n]+)',
            r'(PhD\s+in\s+[^•\n]+)'
        ]
        
        # Also look for specific patterns in the text
        specific_degrees = [
            "B.E in Computer Engineering",
            "Diploma in Information & Technology"
        ]
        
        # Also look for patterns without spaces
        specific_degrees_no_spaces = [
            "B.E in Computer Engineering",
            "Diploma in Information & Technology"
        ]
        
        # Find all occurrences of each degree and process them
        degree_positions = []
        
        for specific_degree in specific_degrees:
            start_pos = 0
            while True:
                pos = education_text.lower().find(specific_degree.lower(), start_pos)
                if pos == -1:
                    break
                degree_positions.append((pos, specific_degree))
                start_pos = pos + 1
        
        # Sort by position and remove duplicates
        degree_positions.sort(key=lambda x: x[0])
        unique_degrees = []
        for pos, degree in degree_positions:
            if not any(abs(pos - other_pos) < 10 for other_pos, _ in unique_degrees):
                unique_degrees.append((pos, degree))
        
        for pos, specific_degree in unique_degrees:
            # Find the section around this degree
            degree_start = pos
            next_degree_start = len(education_text)
            
            # Look for the next degree
            for other_pos, other_degree in unique_degrees:
                if other_pos > degree_start and other_pos < next_degree_start:
                    next_degree_start = other_pos
            
            degree_section = education_text[degree_start:next_degree_start]
            
            # Extract institution for this specific degree
            institution_patterns = [
                r'(GyanmanjariInstituteofTechnology)',
                r'(SirBhavsinhjiPolytechnicInstitute)',
                r'(Gyanmanjari Institute of Technology)',
                r'(Sir Bhavsinhji Polytechnic Institute)',
                r'(University of [^•\n]+)',
                r'(College of [^•\n]+)'
            ]
                    
            institution = "N/A"
            for inst_pattern in institution_patterns:
                inst_match = re.search(inst_pattern, degree_section, re.IGNORECASE)
                if inst_match:
                    institution = inst_match.group(1).strip()
                    break
            
            # Extract duration for this specific degree
            duration_patterns = [
                r'(September \d{4}–July \d{4})',
                r'(August \d{4}–June \d{4})',
                r'(September \d{4} - July \d{4})',
                r'(August \d{4} - June \d{4})',
                r'(\d{4}–\d{4})',
                r'(\d{4} - \d{4})'
            ]
            
            duration = "N/A"
            for dur_pattern in duration_patterns:
                dur_match = re.search(dur_pattern, degree_section)
                if dur_match:
                    duration = dur_match.group(1)
                    break
            
            # Extract GPA/CGPA for this specific degree
            gpa_patterns = [
                r'CurrentCGPA-(\d+\.\d+)',
                r'CGPA-(\d+\.\d+)',
                r'Current CGPA[:\s-]*(\d+\.\d+)',
                r'CGPA[:\s-]*(\d+\.\d+)',
                r'GPA[:\s-]*(\d+\.\d+)'
            ]
            
            gpa = "N/A"
            for gpa_pattern in gpa_patterns:
                gpa_match = re.search(gpa_pattern, degree_section, re.IGNORECASE)
                if gpa_match:
                    gpa = gpa_match.group(1)
                    break
            
            education_entry = {
                "degree": specific_degree,
                "institution": institution,
                "year": duration,
                "gpa": gpa,
                "courses": [],
                "achievements": [],
                "activities": []
            }
            education_entries.append(education_entry)
        
        parsed_data["education"] = education_entries

    # Experience extraction
    experience_match = re.findall(r'Experience:\s*(.*?)\s*Projects:', pdf_text)
    if experience_match:
        experience_text = experience_match[0].strip()
        experience_entries = []
        for exp_block in re.split(r'\n\s*-\s*', experience_text):
            if not exp_block.strip():
                continue
            parts = [p.strip() for p in exp_block.split(':', 1)]
            if len(parts) > 1:
                title = parts[0]
                details = parts[1]
                company_match = re.search(r'Company:\s*(.*?)\s*Duration:', details)
                duration_match = re.search(r'Duration:\s*(.*?)\s*Responsibilities:', details)
                responsibilities_match = re.search(r'Responsibilities:\s*(.*?)\s*', details)

                experience_entry = {
                    "title": title,
                    "company": company_match.group(1).strip() if company_match else "N/A",
                    "duration": duration_match.group(1).strip() if duration_match else "N/A",
                    "responsibilities": [r.strip() for r in responsibilities_match.group(1).split(',') if r.strip()] if responsibilities_match else []
                }
                experience_entries.append(experience_entry)
        parsed_data["experience"] = experience_entries

    # Projects extraction - improved to capture all project details
    projects_section = re.search(r'PROJECTS(.*?)(?=ACHIEVEMENTS|HOBBIES|LANGUAGES|SKILLS|EDUCATION|WORK EXPERIENCE)', pdf_text, re.DOTALL | re.IGNORECASE)
    if projects_section:
        projects_text = projects_section.group(1).strip()
        projects_entries = []
        
        # Extract projects more precisely
        project_entries = []
        
        # Look for specific project patterns (handle no spaces)
        project_patterns = [
            r'(E-bookbargainingandsell)',
            r'(HomeAutomation)',
            r'([A-Z][a-zA-Z\s]+(?:Management|System|App|Website|Platform|Tool))'
        ]
        
        for pattern in project_patterns:
            matches = re.finditer(pattern, projects_text, re.IGNORECASE)
            for match in matches:
                project_name = match.group(1).strip()
                
                # Clean up project name
                if 'E-bookbargainingandsell' in project_name:
                    project_name = 'E-book bargaining and sell'
                elif 'HomeAutomation' in project_name:
                    project_name = 'Home Automation'
                
                # Extract tech stack for this specific project
                tech_stack = []
                for line in projects_text.split('\n'):
                    if 'tech stack' in line.lower() or 'technologies' in line.lower() or 'equipments' in line.lower():
                        tech_text = line.split(':', 1)[1] if ':' in line else line
                        tech_stack = [t.strip() for t in re.split(r'[,•]', tech_text) if t.strip() and len(t.strip()) > 2]
                        break
                
                # Extract description for this specific project
                description = []
                for line in projects_text.split('\n'):
                    if line.strip().startswith('•') or line.strip().startswith('-'):
                        desc = line.strip()[1:].strip()
                        if len(desc) > 10:
                            description.append(desc)
                
                # Only add if we have meaningful data
                if project_name and (tech_stack or description):
                    project_entry = {
                        "name": project_name,
                        "technologies": tech_stack,
                        "description": description,
                        "duration": "N/A",
                        "role": "Developer",
                        "achievements": [],
                        "github": None,
                        "live_url": None
                    }
                    project_entries.append(project_entry)
        

        
        parsed_data["projects"] = project_entries

    return parsed_data

# API endpoint to get resume list
@app.get("/api/resumes")
async def get_resumes():
    resume_list = []
    for filename in os.listdir(UPLOAD_DIR):
        if filename.endswith(".json"):
            resume_list.append(filename.replace(".json", ".pdf"))

    return JSONResponse({
        "resumes": sorted(resume_list)
    })

# API endpoint to get JD history
@app.get("/api/jd-history")
async def get_jd_history():
    jd_list = []
    jd_history_file = "history/JDhistory/jd_history.json"
    
    if os.path.exists(jd_history_file):
        with open(jd_history_file) as f:
            jd_history = json.load(f)
        jd_list = [entry["jd"] for entry in jd_history]
    
    return JSONResponse({
        "jd_list": jd_list
    })

# API endpoint for AI chat interaction
@app.post("/api/chat")
async def chat_with_ai(message: str = Form(...), context: str = Form(None)):
    """Handle AI chat interactions"""
    try:
        response = generate_user_response(message, context or "")
        return JSONResponse({
            "response": response,
            "type": "ai_message"
        })
    except Exception as e:
        return JSONResponse({
            "response": "I'm having trouble processing your request right now. Please try again.",
            "type": "error"
        })

# Test endpoint for debugging
@app.post("/api/test")
async def test_endpoint(request: Request):
    """Test endpoint for debugging"""
    try:
        body = await request.json()
        return JSONResponse({
            "message": "Test successful",
            "received": body
        })
    except Exception as e:
        return JSONResponse({
            "error": str(e)
        })

# API endpoint for smart AI responses with intent understanding
@app.post("/api/smart-chat")
async def smart_chat_with_ai(request: Request):
    """Handle smart AI chat with intent understanding"""
    try:
        # Get raw body first for debugging
        raw_body = await request.body()
        print(f"Raw request body: {raw_body}")
        
        # Try to parse JSON
        if not raw_body:
            print("Empty request body")
            message = ""
            context = ""
        else:
            try:
                body = await request.json()
                message = body.get("message", "")
                context = body.get("context", "")
                print(f"Parsed message: '{message}', context: '{context}'")
            except Exception as json_error:
                print(f"JSON parsing error: {json_error}")
                # Try to extract message from raw body
                body_str = raw_body.decode('utf-8', errors='ignore')
                print(f"Body as string: {body_str}")
                message = body_str.strip()
                context = ""
        
        if not message.strip():
            message = "Hello, I need help with resume analysis"
        
        smart_response = generate_smart_response(message, context)
        
        response = JSONResponse({
            "response": smart_response["response"],
            "intent": smart_response["intent"],
            "suggested_actions": smart_response["suggested_actions"],
            "type": "smart_ai_message"
        })
        # Add cache-busting headers
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    except Exception as e:
        print(f"Error in smart-chat endpoint: {e}")
        # Provide a simple, direct fallback response
        return JSONResponse({
            "response": "Hello! I'm your Resume Analyzer assistant. I can help you upload and analyze resumes, match them against job descriptions, and provide detailed insights. What would you like to do?",
            "intent": {"intent": "help", "confidence": 0.8, "entities": {}, "response_type": "text"},
            "suggested_actions": [
                "📄 Upload a resume to get started",
                "📁 View your uploaded files", 
                "🔍 Get help with any questions",
                "💡 Learn about all features"
            ],
            "type": "smart_ai_message"
        })

# API endpoint to improve job description
@app.post("/api/improve-jd")
async def improve_jd(job_description: str = Form(...)):
    """Improve job description using AI"""
    try:
        improved_jd = improve_job_description(job_description)
        return JSONResponse({
            "original": job_description,
            "improved": improved_jd,
            "message": "Job description improved successfully!"
        })
    except Exception as e:
        return JSONResponse({
            "error": "Failed to improve job description",
            "original": job_description
        })

# API endpoint to upload a single resume
@app.post("/api/upload")
@app.post("/api/upload-resume/")  # Alias for frontend compatibility
async def upload_file(file: UploadFile = File(...)):
    """Upload and parse PDF resume with AI-powered extraction"""
    try:
        if not file.filename.lower().endswith('.pdf'):
            return JSONResponse({"error": "Only PDF files are allowed"}, status_code=400)
        
        # Save file
        file_path = f"resumes/{file.filename}"
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Extract text from PDF
        pdf_text = extract_resume_text(file_path)
        
        # Use AI-powered parsing for better extraction
        parsed_data = parse_pdf_with_ai(pdf_text)
        
        # Generate AI summaries if enabled
        if ENABLE_AI_SUMMARIES:
            if parsed_data.get("education"):
                education_summary = generate_education_summary(parsed_data["education"])
                parsed_data["education_summary"] = education_summary
            
            if parsed_data.get("experience"):
                experience_summary = generate_experience_summary(parsed_data["experience"])
                parsed_data["experience_summary"] = experience_summary
            
            if parsed_data.get("projects"):
                projects_summary = generate_projects_summary(parsed_data["projects"])
                parsed_data["projects_summary"] = projects_summary
        
        # Save parsed data
        json_path = f"resumes/{file.filename.replace('.pdf', '.json')}"
        with open(json_path, 'w') as f:
            json.dump(parsed_data, f, indent=2)
        
        return JSONResponse({
            "message": "File uploaded and parsed successfully",
            "filename": file.filename,
            "parsed_data": parsed_data
        })
        
    except Exception as e:
        print(f"Error uploading file: {e}")
        return JSONResponse({"error": "Failed to upload file"}, status_code=500)

# API endpoint for batch analysis of multiple resumes
@app.post("/api/batch-analyze/")
async def batch_analyze(
    jd: str = Form(...),
    files: list[UploadFile] = File(...)
):
    if not jd:
        return JSONResponse({"error": "Job description is required"}, status_code=400)
    
    if not files or len(files) == 0:
        return JSONResponse({"error": "At least one resume file is required"}, status_code=400)
    
    # Improve job description with AI
    improved_jd = improve_job_description(jd)
    
    results = []
    total_score = 0
    
    # Process each uploaded file
    for file in files:
        if not file.filename.endswith('.pdf'):
            continue
            
        filename = file.filename
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Save the PDF file
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        # Extract information from the PDF
        text = extract_resume_text(file_path)
        extracted_info = {
            "filename": filename,
            "name": extract_name(text),
            "email": extract_email(text),
            "phone": extract_phone(text),
            "skills": extract_skills(text),
            "education": extract_education(text),
            "experience": extract_experience(text),
            "projects": extract_projects(text),
            "extracted_text": text
        }
        
        # Generate AI summaries for each section
        if ENABLE_AI_SUMMARIES:
            try:
                extracted_info["education_summary"] = generate_education_summary(extracted_info["education"])
                extracted_info["experience_summary"] = generate_experience_summary(extracted_info["experience"])
                extracted_info["projects_summary"] = generate_projects_summary(extracted_info["projects"])
            except Exception as e:
                print(f"Error generating AI summaries: {e}")
                extracted_info["education_summary"] = "Educational background analysis available."
                extracted_info["experience_summary"] = "Work experience analysis available."
                extracted_info["projects_summary"] = "Project analysis available."
        else:
            extracted_info["education_summary"] = "AI summaries disabled."
            extracted_info["experience_summary"] = "AI summaries disabled."
            extracted_info["projects_summary"] = "AI summaries disabled."
        
        # Save extracted info as JSON
        json_path = os.path.join(UPLOAD_DIR, filename.replace(".pdf", ".json"))
        with open(json_path, "w") as f:
            json.dump(extracted_info, f, indent=4)
        
        # Use AI for better analysis
        ai_analysis = analyze_resume_with_ai(text, improved_jd)
        
        # Fallback to traditional analysis if AI fails
        if ai_analysis["match_score"] == 0:
            jd_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', improved_jd.lower()))
            resume_skills = set(skill.lower() for skill in extracted_info.get("skills", []))
            
            matched_skills = []
            missing_skills = []
            
            for word in jd_words:
                for skill in resume_skills:
                    if fuzz.ratio(word, skill) >= 85:
                        matched_skills.append(skill)
                        break
                else:
                    missing_skills.append(word)
            
            match_score = int((len(matched_skills) / len(jd_words)) * 100) if jd_words else 0
        else:
            match_score = ai_analysis["match_score"]
            matched_skills = ai_analysis["matched_skills"]
            missing_skills = ai_analysis["missing_skills"]
        
        total_score += match_score
        
        results.append({
            "filename": filename,
            "score": match_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "resume_data": extracted_info,
            "ai_analysis": ai_analysis.get("ai_analysis", "")
        })
    
    # Sort results by score (highest first)
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # Calculate average score
    average_score = total_score / len(results) if results else 0
    
    # Save JD to history
    jd_path = os.path.join("history/JDhistory", "jd_history.json")
    os.makedirs(os.path.dirname(jd_path), exist_ok=True)
    
    if os.path.exists(jd_path):
        with open(jd_path, "r") as f:
            history = json.load(f)
    else:
        history = []
    
    history.append({
        "jd": improved_jd,
        "original_jd": jd,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "batch_analysis": True,
        "total_resumes": len(results),
        "average_score": average_score
    })
    
    with open(jd_path, "w") as f:
        json.dump(history, f, indent=4)
    
    return JSONResponse({
        "job_description": improved_jd,
        "original_jd": jd,
        "results": results,
        "total_resumes": len(results),
        "average_score": average_score
    })

@app.post("/api/process_input/")
async def process_input(
    jd: str = Form(None),
    file: UploadFile = File(None)
):
    resume_list = []
    jd_list = []
    filename = None
    match_score = None
    matched = []
    missing = []
    extra = []
    extracted_info = {}

    os.makedirs("resumes", exist_ok=True)
    os.makedirs("history/JDhistory", exist_ok=True)

    # 📂 Handle Resume
    if file:
        filename = file.filename
        file_path = os.path.join("resumes", filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        text = extract_resume_text(file_path)
        extracted_info = {
            "filename": filename,
            "name": extract_name(text),
            "email": extract_email(text),
            "phone": extract_phone(text),
            "skills": extract_skills(text),
            "education": extract_education(text),
            "experience": extract_experience(text),
            "projects": extract_projects(text),
            "extracted_text": text
        }
        
        # Generate AI summaries for each section
        if ENABLE_AI_SUMMARIES:
            try:
                extracted_info["education_summary"] = generate_education_summary(extracted_info["education"])
                extracted_info["experience_summary"] = generate_experience_summary(extracted_info["experience"])
                extracted_info["projects_summary"] = generate_projects_summary(extracted_info["projects"])
            except Exception as e:
                print(f"Error generating AI summaries: {e}")
                extracted_info["education_summary"] = "Educational background analysis available."
                extracted_info["experience_summary"] = "Work experience analysis available."
                extracted_info["projects_summary"] = "Project analysis available."
        else:
            extracted_info["education_summary"] = "AI summaries disabled."
            extracted_info["experience_summary"] = "AI summaries disabled."
            extracted_info["projects_summary"] = "AI summaries disabled."

        with open(os.path.join("resumes", filename.replace(".pdf", ".json")), "w") as f:
            json.dump(extracted_info, f, indent=4)

    # 🧠 Handle JD
    if jd:
        # Improve job description with AI
        improved_jd = improve_job_description(jd)
        
        if extracted_info:
            # Use AI for better analysis
            ai_analysis = analyze_resume_with_ai(extracted_info["extracted_text"], improved_jd)
            
            if ai_analysis["match_score"] > 0:
                match_score = ai_analysis["match_score"]
                matched = ai_analysis["matched_skills"]
                missing = ai_analysis["missing_skills"]
            else:
                # Fallback to traditional analysis
                jd_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', improved_jd.lower()))
                resume_skills = set(skill.lower() for skill in extracted_info.get("skills", []))
                for word in jd_words:
                    for skill in resume_skills:
                        if fuzz.ratio(word, skill) >= 85:
                            matched.append(skill)
                            break
                    else:
                        missing.append(word)
                extra = list(resume_skills - set(matched))
                match_score = int((len(matched) / len(jd_words)) * 100) if jd_words else 0

        # Save JD to JDhistory.json
        jd_path = os.path.join("history/JDhistory", "jd_history.json")
        if os.path.exists(jd_path):
            with open(jd_path, "r") as f:
                history = json.load(f)
        else:
            history = []

        history.append({
            "jd": improved_jd,
            "original_jd": jd,
            "filename": filename,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "match_score": match_score,
            "matched": matched,
            "missing": missing,
            "extra": extra
        })
        with open(jd_path, "w") as f:
            json.dump(history, f, indent=4)

    for f in os.listdir("resumes"):
        if f.endswith(".json"):
            resume_list.append(f.replace(".json", ".pdf"))

    if os.path.exists("history/JDhistory/jd_history.json"):
        with open("history/JDhistory/jd_history.json") as f:
            jd_list = [entry["jd"] for entry in json.load(f)]

    # Return JSON response for React frontend
    return JSONResponse({
        "filename": filename,
        "match_score": match_score,
        "matched": matched,
        "missing": missing,
        "extra": extra,
        "resume_data": extracted_info,
        "jd": improved_jd if jd else None,
        "original_jd": jd,
        "resume_list": sorted(resume_list),
        "jd_list": jd_list
    })

# API endpoint to get specific resume data
@app.get("/api/resume/{filename}")
async def get_resume_data(filename: str):
    json_path = os.path.join("resumes", filename.replace(".pdf", ".json"))
    
    if not os.path.exists(json_path):
        return JSONResponse({"error": "Resume not found"}, status_code=404)
    
    with open(json_path) as f:
        data = json.load(f)

    return JSONResponse(data)

# API endpoint to get resume analysis data with match percentages
@app.get("/api/resume-analysis/{filename}")
async def get_resume_analysis(filename: str):
    """Get resume analysis data including match percentages, skills, etc."""
    json_path = os.path.join("resumes", filename.replace(".pdf", ".json"))
    
    if not os.path.exists(json_path):
        return JSONResponse({"error": "Resume not found"}, status_code=404)
    
    # Get basic resume data
    with open(json_path) as f:
        resume_data = json.load(f)
    
    # Get analysis history for this resume
    jd_history_path = os.path.join("history/JDhistory", "jd_history.json")
    analysis_data = {
        "resume_data": resume_data,
        "match_score": None,
        "matched_skills": [],
        "missing_skills": [],
        "extra_skills": [],
        "job_description": None,
        "analysis_history": []
    }
    
    if os.path.exists(jd_history_path):
        with open(jd_history_path, "r") as f:
            history = json.load(f)
        
        # Find the most recent analysis for this resume
        for entry in reversed(history):
            if entry.get("filename") == filename:
                analysis_data.update({
                    "match_score": entry.get("match_score", 0),
                    "matched_skills": entry.get("matched", []),
                    "missing_skills": entry.get("missing", []),
                    "extra_skills": entry.get("extra", []),
                    "job_description": entry.get("jd", ""),
                    "original_jd": entry.get("original_jd", ""),
                    "timestamp": entry.get("timestamp", "")
                })
                break
        
        # Get all analysis history for this resume
        analysis_data["analysis_history"] = [
            {
                "job_description": entry.get("jd", ""),
                "match_score": entry.get("match_score", 0),
                "matched_skills": entry.get("matched", []),
                "missing_skills": entry.get("missing", []),
                "extra_skills": entry.get("extra", []),
                "timestamp": entry.get("timestamp", "")
            }
            for entry in history
            if entry.get("filename") == filename
        ]
    
    return JSONResponse(analysis_data)

# Serve React app for all non-API routes (must be last)
@app.get("/", response_class=HTMLResponse)
async def serve_react_app():
    index_path = Path("build/index.html")
    if index_path.exists():
        with open(index_path, "r") as f:
            return HTMLResponse(content=f.read())
    else:
        return HTMLResponse(content="<h1>React app not built. Run 'npm run build' first.</h1>")

# Catch-all route for React Router (must be last)
@app.get("/{full_path:path}")
async def serve_react_routes(full_path: str):
    # Don't interfere with API routes
    if full_path.startswith("api/"):
        return JSONResponse({"error": "API endpoint not found"}, status_code=404)
    
    # Serve React app for all other routes
    index_path = Path("build/index.html")
    if index_path.exists():
        with open(index_path, "r") as f:
            return HTMLResponse(content=f.read())
    else:
        return HTMLResponse(content="<h1>React app not built. Run 'npm run build' first.</h1>")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Resume Analyzer Server...")
    print("📱 React App: http://localhost:8000")
    print("🔧 API Docs: http://localhost:8000/docs")
    print("🤖 AI Features: Groq integration enabled")
    uvicorn.run(app, host="0.0.0.0", port=8000)
