#!/usr/bin/env python3
"""
Test script to verify improved PDF parsing
"""

import sys
import os
sys.path.append('.')

from main import parse_pdf_with_ai, parse_pdf_manually

def test_parsing():
    """Test the improved parsing with sample resume text"""
    
    # Sample resume text based on the image
    sample_resume = """
    HARIT MANDALIYA
    Computer Engineering Student
    
    Email: haritmandaliya@gmail.com
    Phone: +91 7600107607
    
    SUMMARY:
    Motivated and curious Computer Engineering student with hands-on experience in web development, IoT, and ERP solutions. Strong foundational skills in programming, data structures, and real-world project execution. Eager to contribute to dynamic teams and learn emerging technologies.
    
    WORK EXPERIENCE:
    Intern - Service Further
    March 2025 - Present
    • Working on a large-scale enterprise project using Frappe, ERPNext, HRMS, React, and Vite.
    • Contributing to the development and customization of ERP modules, UI enhancements, and API integrations.
    • Gaining real-world experience with scalable backend systems and modular frontend architecture.
    
    EDUCATION:
    B.E in Computer Engineering
    Institution: Gyanmanjari Institute of Technology
    September 2022 - July 2025
    Current CGPA - 7.44
    
    Diploma in Information & Technology
    Institution: Sir Bhavsinhji Polytechnic Institute
    August 2019 - June 2022
    CGPA - 7.39
    
    SKILLS:
    Programming languages: C, Python, Java, JavaScript, PHP, HTML, CSS
    Frameworks: React, Frappe, ERPNext, HRMS
    Database: MySQL
    Miscellaneous: Arduino, Git, Bootstrap
    
    PROJECTS:
    E-book bargaining and sell
    Tech Stack: PHP, JavaScript, HTML, CSS, Bootstrap, MYSQL
    • Designed and developed a sophisticated library management website, enabling efficient cataloging, user management, and streamlined lending processes.
    • User-friendly interfaces and intuitive functionalities enhance the overall library experience for administrators and patrons alike.
    
    Home Automation
    Tech Stack/Equipments: Arduino, Arduino IDE, Arduino UNO R3 Board, 16*2 Characters LCD Display, Robocraze HC05 Bluetooth, XCluma 4 channel 5V relay board
    • I've created a home automation project using IoT technology. Enhancing convenience and efficiency through remote control and automated systems.
    • This could include IoT devices, sensors, microcontrollers (like Arduino), smart home platforms (SmartThings, Home Assistant).
    
    ACHIEVEMENTS:
    Tabla Visharad: Achieved 2nd rank at Bhavnagar district level, demonstrating advanced proficiency and mastery in 'Tabla Visharad' examination. Performed at various cultural events and competitions, earning accolades for exceptional rhythm and technique.
    
    Hobby:
    Electronics Troubleshooting
    Professional Photography
    Watching Movies
    
    LANGUAGES:
    Gujarati
    Hindi
    English
    """
    
    print("🧪 Testing Improved PDF Parsing")
    print("=" * 50)
    
    # Test AI parsing
    print("\n📝 Testing AI Parsing:")
    try:
        ai_result = parse_pdf_with_ai(sample_resume)
        print("✅ AI Parsing completed")
        print(f"📚 Education entries: {len(ai_result.get('education', []))}")
        print(f"💼 Experience entries: {len(ai_result.get('experience', []))}")
        print(f"🚀 Projects entries: {len(ai_result.get('projects', []))}")
        
        # Show education details
        if ai_result.get('education'):
            print("\n📖 Education Details:")
            for i, edu in enumerate(ai_result['education'], 1):
                print(f"  {i}. {edu.get('degree', 'N/A')}")
                print(f"     Institution: {edu.get('institution', 'N/A')}")
                print(f"     Duration: {edu.get('year', 'N/A')}")
                print(f"     GPA: {edu.get('gpa', 'N/A')}")
        
        # Show projects details
        if ai_result.get('projects'):
            print("\n🚀 Projects Details:")
            for i, proj in enumerate(ai_result['projects'], 1):
                print(f"  {i}. {proj.get('name', 'N/A')}")
                print(f"     Technologies: {', '.join(proj.get('technologies', []))}")
                print(f"     Description: {proj.get('description', [])[:2]}")  # First 2 description items
        
    except Exception as e:
        print(f"❌ AI Parsing failed: {e}")
    
    # Test manual parsing
    print("\n📝 Testing Manual Parsing:")
    try:
        manual_result = parse_pdf_manually(sample_resume)
        print("✅ Manual Parsing completed")
        print(f"📚 Education entries: {len(manual_result.get('education', []))}")
        print(f"💼 Experience entries: {len(manual_result.get('experience', []))}")
        print(f"🚀 Projects entries: {len(manual_result.get('projects', []))}")
        
        # Show education details
        if manual_result.get('education'):
            print("\n📖 Education Details:")
            for i, edu in enumerate(manual_result['education'], 1):
                print(f"  {i}. {edu.get('degree', 'N/A')}")
                print(f"     Institution: {edu.get('institution', 'N/A')}")
                print(f"     Duration: {edu.get('year', 'N/A')}")
                print(f"     GPA: {edu.get('gpa', 'N/A')}")
        
        # Show projects details
        if manual_result.get('projects'):
            print("\n🚀 Projects Details:")
            for i, proj in enumerate(manual_result['projects'], 1):
                print(f"  {i}. {proj.get('name', 'N/A')}")
                print(f"     Technologies: {', '.join(proj.get('technologies', []))}")
                print(f"     Description: {proj.get('description', [])[:2]}")  # First 2 description items
        
    except Exception as e:
        print(f"❌ Manual Parsing failed: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Parsing test completed!")

if __name__ == "__main__":
    test_parsing() 