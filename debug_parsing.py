#!/usr/bin/env python3
"""
Debug parsing step by step
"""

import sys
import os
import re
sys.path.append('.')

from utils.resume_parser import extract_resume_text

def debug_parsing():
    """Debug parsing step by step"""
    
    pdf_file = "resumes/Harit (1).pdf"
    
    if not os.path.exists(pdf_file):
        print(f"❌ PDF file not found: {pdf_file}")
        return
    
    print("🔍 Debugging Parsing Step by Step")
    print("=" * 50)
    
    # Extract text
    pdf_text = extract_resume_text(pdf_file)
    print(f"📄 Text length: {len(pdf_text)} characters")
    
    # Test education section extraction
    print("\n📚 Testing Education Extraction:")
    education_section = re.search(r'EDUCATION:(.*?)(?=ACHIEVEMENTS|HOBBIES|LANGUAGES|SKILLS|WORK EXPERIENCE)', pdf_text, re.DOTALL | re.IGNORECASE)
    if education_section:
        print("✅ Education section found")
        education_text = education_section.group(1).strip()
        print(f"Education text: {education_text[:200]}...")
        
        # Look for specific degrees
        if 'B.E in Computer Engineering' in education_text:
            print("✅ Found: B.E in Computer Engineering")
        else:
            print("❌ Missing: B.E in Computer Engineering")
            
        if 'Diploma in Information & Technology' in education_text:
            print("✅ Found: Diploma in Information & Technology")
        else:
            print("❌ Missing: Diploma in Information & Technology")
    else:
        print("❌ Education section not found")
    
    # Test projects section extraction
    print("\n🚀 Testing Projects Extraction:")
    projects_section = re.search(r'PROJECTS:(.*?)(?=ACHIEVEMENTS|HOBBIES|LANGUAGES|SKILLS|EDUCATION|WORK EXPERIENCE)', pdf_text, re.DOTALL | re.IGNORECASE)
    if projects_section:
        print("✅ Projects section found")
        projects_text = projects_section.group(1).strip()
        print(f"Projects text: {projects_text[:200]}...")
        
        # Look for specific projects
        if 'E-bookbargainingandsell' in projects_text:
            print("✅ Found: E-bookbargainingandsell")
        else:
            print("❌ Missing: E-bookbargainingandsell")
            
        if 'HomeAutomation' in projects_text:
            print("✅ Found: HomeAutomation")
        else:
            print("❌ Missing: HomeAutomation")
    else:
        print("❌ Projects section not found")
    
    # Test experience section extraction
    print("\n💼 Testing Experience Extraction:")
    experience_section = re.search(r'WORK EXPERIENCE:(.*?)(?=EDUCATION|PROJECTS|ACHIEVEMENTS|HOBBIES|LANGUAGES|SKILLS)', pdf_text, re.DOTALL | re.IGNORECASE)
    if experience_section:
        print("✅ Experience section found")
        experience_text = experience_section.group(1).strip()
        print(f"Experience text: {experience_text[:200]}...")
        
        if 'Intern-ServiceFurther' in experience_text:
            print("✅ Found: Intern-ServiceFurther")
        else:
            print("❌ Missing: Intern-ServiceFurther")
    else:
        print("❌ Experience section not found")

if __name__ == "__main__":
    debug_parsing() 