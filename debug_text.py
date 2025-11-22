#!/usr/bin/env python3
"""
Debug script to see extracted text
"""

import sys
import os
sys.path.append('.')

from utils.resume_parser import extract_resume_text

def debug_text():
    """Debug the extracted text"""
    
    pdf_file = "resumes/Harit (1).pdf"
    
    if not os.path.exists(pdf_file):
        print(f"❌ PDF file not found: {pdf_file}")
        return
    
    print("🔍 Debugging Extracted Text")
    print("=" * 50)
    
    # Extract text
    pdf_text = extract_resume_text(pdf_file)
    print(f"📄 Text length: {len(pdf_text)} characters")
    print("\n📝 Extracted Text:")
    print("-" * 30)
    print(pdf_text)
    print("-" * 30)
    
    # Look for key sections
    print("\n🔍 Looking for key sections:")
    
    sections = ['EDUCATION', 'PROJECTS', 'EXPERIENCE', 'WORK EXPERIENCE', 'SKILLS']
    for section in sections:
        if section.lower() in pdf_text.lower():
            print(f"✅ Found: {section}")
        else:
            print(f"❌ Missing: {section}")
    
    # Look for specific content
    print("\n🔍 Looking for specific content:")
    
    # Education
    if 'B.E in Computer Engineering' in pdf_text:
        print("✅ Found: B.E in Computer Engineering")
    else:
        print("❌ Missing: B.E in Computer Engineering")
    
    if 'Diploma in Information & Technology' in pdf_text:
        print("✅ Found: Diploma in Information & Technology")
    else:
        print("❌ Missing: Diploma in Information & Technology")
    
    # Projects
    if 'E-book bargaining and sell' in pdf_text:
        print("✅ Found: E-book bargaining and sell")
    else:
        print("❌ Missing: E-book bargaining and sell")
    
    if 'Home Automation' in pdf_text:
        print("✅ Found: Home Automation")
    else:
        print("❌ Missing: Home Automation")

if __name__ == "__main__":
    debug_text() 