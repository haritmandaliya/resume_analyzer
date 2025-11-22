import pdfplumber
import re

def extract_resume_text(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_email(text):
    match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    return match.group() if match else None

def extract_phone(text):
    match = re.search(r'(\+91)?\s?[6-9]\d{9}', text)
    return match.group().strip() if match else None

def extract_name(text):
    lines = text.strip().split("\n")
    return lines[0].strip() if lines else None

def extract_skills(text, skill_set=None):
    if not skill_set:
        skill_set = ['python', 'html', 'css', 'javascript', 'java', 'php', 'mysql', 'frappe', 'react', 'vite', 'arduino']
    found_skills = []
    for skill in skill_set:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            found_skills.append(skill)
    return found_skills

def extract_education(text):
    """Extract education information from resume text"""
    education_sections = []
    
    # Split text into lines and clean up
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Look for education section
    education_start = -1
    for i, line in enumerate(lines):
        if re.search(r'\b(education|academic|qualification)\b', line, re.IGNORECASE):
            education_start = i
            break
    
    if education_start == -1:
        # If no explicit education section, look for degree patterns
        for i, line in enumerate(lines):
            if re.search(r'\b(bachelor|master|phd|diploma|b\.e|m\.e|b\.tech|m\.tech)\b', line, re.IGNORECASE):
                education_start = i
                break
    
    if education_start != -1:
        current_education = {}
        
        # Process lines starting from education section
        for i in range(education_start, min(education_start + 15, len(lines))):
            line = lines[i]
            
            # Look for degree patterns
            degree_patterns = [
                r'\b(bachelor|master|phd|diploma)\s+(of|in)\s+[a-zA-Z\s]+',
                r'\b(b\.e|m\.e|b\.tech|m\.tech)\s+(in|of)\s+[a-zA-Z\s]+',
                r'[A-Za-z\s]+(Engineering|Science|Arts|Commerce|Technology)',
                r'\b(bachelor|master|phd|diploma)\b'
            ]
            
            for pattern in degree_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    # Clean up the degree text
                    degree_text = line.strip()
                    # Remove extra text that's not part of the degree
                    if 'in"' in degree_text:
                        degree_text = degree_text.split('in"')[0] + ' in Information & Technology'
                    elif 'examination' in degree_text.lower():
                        degree_text = degree_text.split('examination')[0].strip()
                    elif 'performed' in degree_text.lower():
                        degree_text = degree_text.split('performed')[0].strip()
                    
                    # Remove duplication
                    if ' in Information & Technology  in Information & Technology' in degree_text:
                        degree_text = degree_text.replace(' in Information & Technology  in Information & Technology', ' in Information & Technology')
                    
                    current_education['degree'] = degree_text
                    break
            
            # Look for institution names
            institution_patterns = [
                r'[A-Z][a-zA-Z\s&]+(University|College|Institute|School|Polytechnic)',
                r'[A-Z][a-zA-Z\s]+(University|College|Institute)'
            ]
            
            for pattern in institution_patterns:
                if re.search(pattern, line):
                    current_education['institution'] = line
                    break
            
            # Look for years/dates
            year_pattern = r'(19|20)\d{2}'
            if re.search(year_pattern, line):
                current_education['year'] = line
            
            # Look for GPA/CGPA
            gpa_pattern = r'(GPA|CGPA|Grade)[:\s]*(\d+\.?\d*)'
            gpa_match = re.search(gpa_pattern, line, re.IGNORECASE)
            if gpa_match:
                current_education['gpa'] = gpa_match.group(2)
            
            # Look for CGPA in different format
            cgpa_pattern = r'CGPA[:\s-]*(\d+\.?\d*)'
            cgpa_match = re.search(cgpa_pattern, line, re.IGNORECASE)
            if cgpa_match:
                current_education['gpa'] = cgpa_match.group(1)
        
        if current_education:
            education_sections.append(current_education)
    
    # Sort education by level (higher to lower)
    def get_education_level(edu):
        degree_text = edu.get('degree', '').lower()
        
        # PhD/Doctorate (highest)
        if any(word in degree_text for word in ['phd', 'doctorate', 'doctor']):
            return 7
        
        # Masters level
        elif any(word in degree_text for word in ['master', 'm.tech', 'm.e', 'ms', 'mba', 'mca']):
            return 6
        
        # Bachelors level
        elif any(word in degree_text for word in ['bachelor', 'b.tech', 'b.e', 'b.sc', 'b.com', 'b.arts', 'bca']):
            return 5
        
        # Diploma level
        elif any(word in degree_text for word in ['diploma']):
            return 4
        
        # 12th/Higher Secondary
        elif any(word in degree_text for word in ['12th', 'twelfth', 'higher secondary', 'hsc', 'intermediate']):
            return 3
        
        # 10th/Secondary
        elif any(word in degree_text for word in ['10th', 'tenth', 'secondary', 'ssc', 'matric']):
            return 2
        
        # Extra education (music, sports, etc.)
        elif any(word in degree_text for word in ['visharad', 'tabla', 'music', 'game', 'sport', 'certificate', 'hobby']):
            return 1
        
        else:
            return 0
    
    # Sort by education level (highest first)
    education_sections.sort(key=get_education_level, reverse=True)
    
    return education_sections

def extract_experience(text):
    """Extract work experience information from resume text"""
    experience_sections = []
    
    # Split text into lines and clean up
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Look for experience section
    experience_start = -1
    for i, line in enumerate(lines):
        if re.search(r'\b(experience|work|employment|intern|job)\b', line, re.IGNORECASE):
            experience_start = i
            break
    
    if experience_start != -1:
        current_experience = {}
        
        # Process lines starting from experience section
        for i in range(experience_start, min(experience_start + 15, len(lines))):
            line = lines[i]
            
            # Look for job titles
            title_patterns = [
                r'\b(intern|developer|engineer|manager|analyst|designer|consultant|specialist)\b',
                r'\b(senior|junior|lead|principal|associate)?\s*(developer|engineer|manager|analyst|designer)',
                r'[A-Z][a-zA-Z\s]+(Developer|Engineer|Manager|Analyst|Designer)'
            ]
            
            for pattern in title_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    current_experience['title'] = line
                    break
            
            # Look for company names
            company_patterns = [
                r'[A-Z][a-zA-Z\s&]+(Inc|Corp|Ltd|LLC|Company|Technologies|Solutions)',
                r'[A-Z][a-zA-Z\s]+(Inc|Corp|Ltd|LLC)',
                r'[A-Z][a-zA-Z\s]+(Institute|University|College)'
            ]
            
            for pattern in company_patterns:
                if re.search(pattern, line):
                    current_experience['company'] = line
                    break
            
            # Look for dates
            date_pattern = r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(19|20)\d{2}'
            if re.search(date_pattern, line, re.IGNORECASE):
                current_experience['duration'] = line
            
            # Look for responsibilities (bullet points or descriptions)
            if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                if 'responsibilities' not in current_experience:
                    current_experience['responsibilities'] = []
                current_experience['responsibilities'].append(line[1:].strip())
            elif len(line) > 20 and 'responsibilities' in current_experience:
                # Might be a continuation of responsibilities
                current_experience['responsibilities'].append(line)
        
        if current_experience:
            experience_sections.append(current_experience)
    
    return experience_sections

def extract_projects(text):
    """Extract project information from resume text with improved accuracy"""
    project_sections = []
    
    # Split text into lines and clean up
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Look for projects section
    project_start = -1
    for i, line in enumerate(lines):
        if re.search(r'\b(projects|project|portfolio|achievements)\b', line, re.IGNORECASE):
            project_start = i
            break
    
    if project_start != -1:
        current_project = {}
        
        # Process lines starting from projects section
        for i in range(project_start, min(project_start + 30, len(lines))):
            line = lines[i]
            
            # Skip lines that are clearly not projects
            skip_patterns = [
                r'\b(summary|motivated|curious|student|eager|contribute|learn|emerging)\b',
                r'\b(hands-on|experience|foundational|skills|real-world|execution)\b',
                r'\b(dynamic|teams|technologies|programming|data structures)\b',
                r'\b(education|languages|hobby|certifications|achievements)\b',
                r'\b(gujarati|hindi|english|mysql|project|projects)\b',
                r'\b(sirbhavsinhji|polytechnic|institute|university|college)\b',
                r'\b(academic|qualification|degree|diploma|bachelor|master)\b'
            ]
            
            if any(re.search(pattern, line, re.IGNORECASE) for pattern in skip_patterns):
                continue
            
            # Look for actual project names (more specific patterns)
            # Real projects usually have descriptive names
            project_name_patterns = [
                r'\b(e-commerce|ecommerce|library|management|website|platform|system)\b',
                r'\b(automation|home|smart|iot|mobile|web|app|application)\b',
                r'\b(chat|messaging|social|media|blog|forum|shop|store)\b',
                r'\b(calculator|game|tool|dashboard|analytics|report|tracker)\b',
                r'\b(weather|news|todo|notes|calendar|scheduler)\b',
                r'\b(portfolio|personal|blog|resume|cv)\b',
                r'\b(restaurant|hospital|school|college|university)\b',
                r'\b(banking|finance|inventory|order|booking)\b'
            ]
            
            # Check if line looks like a real project name
            is_real_project = any(re.search(pattern, line, re.IGNORECASE) for pattern in project_name_patterns)
            
            # Look for project names (usually in caps or with special formatting)
            if (re.match(r'^[A-Z][A-Za-z\s]+$', line) and 
                len(line) > 3 and len(line) < 60 and
                is_real_project and
                not any(word in line.lower() for word in ['summary', 'motivated', 'curious', 'student', 'eager', 'contribute', 'learn', 'emerging', 'hands-on', 'experience', 'foundational', 'skills', 'real-world', 'execution', 'dynamic', 'teams', 'technologies', 'programming', 'data structures', 'education', 'languages', 'hobby', 'certifications', 'achievements', 'gujarati', 'hindi', 'english', 'mysql', 'project', 'projects', 'sirbhavsinhji', 'polytechnic', 'institute', 'university', 'college', 'academic', 'qualification', 'degree', 'diploma', 'bachelor', 'master'])):
                
                if current_project and 'name' in current_project:
                    # Save previous project and start new one
                    project_sections.append(current_project)
                    current_project = {}
                current_project['name'] = line
                continue
            
            # Look for technologies used
            tech_patterns = [
                r'\b(Python|Java|JavaScript|React|Node|Angular|Vue|HTML|CSS|SQL|MongoDB|AWS|Docker|Kubernetes|PHP|MySQL|Arduino|Bootstrap|Git)\b',
                r'\b(Machine Learning|AI|Data Science|Web Development|Mobile Development|IoT|ERP)\b'
            ]
            
            for pattern in tech_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    if 'technologies' not in current_project:
                        current_project['technologies'] = []
                    # Extract the technology from the line
                    tech_match = re.search(pattern, line, re.IGNORECASE)
                    if tech_match:
                        tech = tech_match.group(1)
                        if tech not in current_project['technologies']:
                            current_project['technologies'].append(tech)
                    break
            
            # Look for project descriptions (bullet points or longer text)
            if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                if 'description' not in current_project:
                    current_project['description'] = []
                current_project['description'].append(line[1:].strip())
            elif len(line) > 20 and not current_project.get('name'):
                # Might be a description, but filter out non-project content
                if not any(word in line.lower() for word in ['summary', 'motivated', 'curious', 'student', 'eager', 'contribute', 'learn', 'emerging', 'hands-on', 'experience', 'foundational', 'skills', 'real-world', 'execution', 'dynamic', 'teams', 'technologies', 'programming', 'data structures', 'education', 'languages', 'hobby', 'certifications', 'achievements', 'gujarati', 'hindi', 'english', 'mysql', 'project', 'projects', 'sirbhavsinhji', 'polytechnic', 'institute', 'university', 'college', 'academic', 'qualification', 'degree', 'diploma', 'bachelor', 'master']):
                    if 'description' not in current_project:
                        current_project['description'] = []
                    current_project['description'].append(line)
        
        # Add the last project
        if current_project:
            project_sections.append(current_project)
    
    # Filter out projects that seem to be just descriptions or summaries
    filtered_projects = []
    for project in project_sections:
        name = project.get('name', '').lower()
        # Skip if it looks like a description rather than a project name
        if not any(word in name for word in ['summary', 'motivated', 'curious', 'student', 'eager', 'contribute', 'learn', 'emerging', 'hands-on', 'experience', 'foundational', 'skills', 'real-world', 'execution', 'dynamic', 'teams', 'technologies', 'programming', 'data structures', 'education', 'languages', 'hobby', 'certifications', 'achievements', 'gujarati', 'hindi', 'english', 'mysql', 'project', 'projects', 'sirbhavsinhji', 'polytechnic', 'institute', 'university', 'college', 'academic', 'qualification', 'degree', 'diploma', 'bachelor', 'master']):
            # Additional check for real project names
            if any(word in name for word in ['e-commerce', 'ecommerce', 'library', 'management', 'website', 'platform', 'system', 'automation', 'home', 'smart', 'iot', 'mobile', 'web', 'app', 'application', 'chat', 'messaging', 'social', 'media', 'blog', 'forum', 'shop', 'store', 'calculator', 'game', 'tool', 'dashboard', 'analytics', 'report', 'tracker', 'weather', 'news', 'todo', 'notes', 'calendar', 'scheduler', 'portfolio', 'personal', 'blog', 'resume', 'cv', 'restaurant', 'hospital', 'school', 'college', 'university', 'banking', 'finance', 'inventory', 'order', 'booking']):
                filtered_projects.append(project)
    
    return filtered_projects
