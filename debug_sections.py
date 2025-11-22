#!/usr/bin/env python3
"""
Debug section boundaries
"""

import sys
import os
import re
sys.path.append('.')

from utils.resume_parser import extract_resume_text

def debug_sections():
    """Debug section boundaries"""
    
    pdf_file = "resumes/Harit (1).pdf"
    
    if not os.path.exists(pdf_file):
        print(f"❌ PDF file not found: {pdf_file}")
        return
    
    print("🔍 Debugging Section Boundaries")
    print("=" * 50)
    
    # Extract text
    pdf_text = extract_resume_text(pdf_file)
    
    # Find all section headers
    print("📋 Looking for section headers:")
    
    # Look for common section patterns
    section_patterns = [
        r'EDUCATION',
        r'PROJECTS', 
        r'WORK EXPERIENCE',
        r'EXPERIENCE',
        r'ACHIEVEMENTS',
        r'HOBBIES',
        r'LANGUAGES',
        r'SKILLS'
    ]
    
    for pattern in section_patterns:
        matches = list(re.finditer(pattern, pdf_text, re.IGNORECASE))
        if matches:
            print(f"✅ Found '{pattern}' at positions: {[m.start() for m in matches]}")
            for match in matches:
                start = max(0, match.start() - 20)
                end = min(len(pdf_text), match.end() + 20)
                context = pdf_text[start:end]
                print(f"   Context: ...{context}...")
        else:
            print(f"❌ Not found: '{pattern}'")
    
    # Look for the exact text around EDUCATION
    print("\n📚 Looking for EDUCATION section:")
    edu_pos = pdf_text.find('EDUCATION')
    if edu_pos != -1:
        print(f"✅ EDUCATION found at position {edu_pos}")
        start = max(0, edu_pos - 50)
        end = min(len(pdf_text), edu_pos + 200)
        context = pdf_text[start:end]
        print(f"Context: ...{context}...")
    else:
        print("❌ EDUCATION not found")
    
    # Look for the exact text around PROJECTS
    print("\n🚀 Looking for PROJECTS section:")
    proj_pos = pdf_text.find('PROJECTS')
    if proj_pos != -1:
        print(f"✅ PROJECTS found at position {proj_pos}")
        start = max(0, proj_pos - 50)
        end = min(len(pdf_text), proj_pos + 200)
        context = pdf_text[start:end]
        print(f"Context: ...{context}...")
    else:
        print("❌ PROJECTS not found")

if __name__ == "__main__":
    debug_sections() 