#!/usr/bin/env python3
"""
Test real PDF parsing with existing files
"""

import sys
import os
sys.path.append('.')

from main import parse_pdf_with_ai
from utils.resume_parser import extract_resume_text

def test_real_pdf():
    """Test parsing with a real PDF file"""
    
    # Test with an existing PDF
    pdf_file = "resumes/Harit (1).pdf"
    
    if not os.path.exists(pdf_file):
        print(f"❌ PDF file not found: {pdf_file}")
        return
    
    print("🧪 Testing Real PDF Parsing")
    print("=" * 50)
    
    try:
        # Extract text from PDF
        print(f"📄 Extracting text from: {pdf_file}")
        pdf_text = extract_resume_text(pdf_file)
        print(f"✅ Text extracted ({len(pdf_text)} characters)")
        
        # Parse with AI
        print("\n🤖 Parsing with AI...")
        result = parse_pdf_with_ai(pdf_text)
        
        print(f"✅ Parsing completed")
        print(f"📚 Education entries: {len(result.get('education', []))}")
        print(f"💼 Experience entries: {len(result.get('experience', []))}")
        print(f"🚀 Projects entries: {len(result.get('projects', []))}")
        
        # Show education details
        if result.get('education'):
            print("\n📖 Education Details:")
            for i, edu in enumerate(result['education'], 1):
                print(f"  {i}. {edu.get('degree', 'N/A')}")
                print(f"     Institution: {edu.get('institution', 'N/A')}")
                print(f"     Duration: {edu.get('year', 'N/A')}")
                print(f"     GPA: {edu.get('gpa', 'N/A')}")
        
        # Show projects details
        if result.get('projects'):
            print("\n🚀 Projects Details:")
            for i, proj in enumerate(result['projects'], 1):
                print(f"  {i}. {proj.get('name', 'N/A')}")
                print(f"     Technologies: {', '.join(proj.get('technologies', []))}")
                print(f"     Description: {proj.get('description', [])[:2]}")  # First 2 description items
        
        # Show experience details
        if result.get('experience'):
            print("\n💼 Experience Details:")
            for i, exp in enumerate(result['experience'], 1):
                print(f"  {i}. {exp.get('title', 'N/A')}")
                print(f"     Company: {exp.get('company', 'N/A')}")
                print(f"     Duration: {exp.get('duration', 'N/A')}")
                print(f"     Responsibilities: {exp.get('responsibilities', [])[:2]}")  # First 2 responsibilities
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("✅ Real PDF parsing test completed!")

if __name__ == "__main__":
    test_real_pdf() 