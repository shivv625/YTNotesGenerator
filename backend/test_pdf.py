#!/usr/bin/env python3
"""
Test script to verify PDF generation functionality
"""

import sys
import os
from utils import generate_pdf

def test_pdf_generation():
    """Test PDF generation with sample content"""
    print("📄 Testing PDF generation...")
    
    # Sample notes content
    sample_notes = """## Overview/Summary
This is a sample educational video about Python programming.

## Key Concepts
- Variables and data types
- Control structures
- Functions and modules

## Detailed Explanations
Python is a high-level programming language known for its simplicity and readability.

## Practical Applications
- Web development
- Data analysis
- Automation scripts

## Key Takeaways
- Python is beginner-friendly
- Large ecosystem of libraries
- Great for rapid prototyping"""

    # Sample Hindi notes
    hindi_notes = """## सारांश/अवलोकन
यह पायथन प्रोग्रामिंग के बारे में एक नमूना शैक्षिक वीडियो है।

## मुख्य अवधारणाएं
- वेरिएबल्स और डेटा टाइप्स
- कंट्रोल स्ट्रक्चर्स
- फंक्शंस और मॉड्यूल्स

## विस्तृत व्याख्या
पायथन एक उच्च-स्तरीय प्रोग्रामिंग भाषा है जो अपनी सरलता और पठनीयता के लिए जानी जाती है।

## व्यावहारिक अनुप्रयोग
- वेब डेवलपमेंट
- डेटा विश्लेषण
- ऑटोमेशन स्क्रिप्ट्स

## मुख्य सीख
- पायथन शुरुआती के लिए अनुकूल है
- लाइब्रेरीज का बड़ा इकोसिस्टम
- तेज प्रोटोटाइपिंग के लिए बेहतरीन"""

    try:
        # Test English PDF
        print("📝 Generating English PDF...")
        english_pdf_path = generate_pdf(
            sample_notes, 
            "Python Programming Tutorial", 
            "https://www.youtube.com/watch?v=example"
        )
        
        if os.path.exists(english_pdf_path):
            print(f"✅ English PDF generated successfully: {english_pdf_path}")
            print(f"📊 File size: {os.path.getsize(english_pdf_path)} bytes")
        else:
            print("❌ English PDF file not found")
            return False
        
        # Test Hindi PDF
        print("\n📝 Generating Hindi PDF...")
        hindi_pdf_path = generate_pdf(
            hindi_notes, 
            "पायथन प्रोग्रामिंग ट्यूटोरियल", 
            "https://www.youtube.com/watch?v=example"
        )
        
        if os.path.exists(hindi_pdf_path):
            print(f"✅ Hindi PDF generated successfully: {hindi_pdf_path}")
            print(f"📊 File size: {os.path.getsize(hindi_pdf_path)} bytes")
        else:
            print("❌ Hindi PDF file not found")
            return False
        
        # Clean up test files
        try:
            os.remove(english_pdf_path)
            os.remove(hindi_pdf_path)
            print("\n🧹 Test files cleaned up")
        except:
            pass
        
        return True
        
    except Exception as e:
        print(f"❌ PDF generation failed: {str(e)}")
        return False

def main():
    print("🚀 YouTube Notes Generator - PDF Test")
    print("=" * 50)
    
    success = test_pdf_generation()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ PDF generation test passed!")
        print("🎉 Your PDF functionality is working correctly.")
    else:
        print("❌ PDF generation test failed.")
        print("🔧 Check the error messages above for troubleshooting.")

if __name__ == "__main__":
    main() 