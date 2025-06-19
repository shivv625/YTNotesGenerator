#!/usr/bin/env python3
"""
Test simple note generation without API
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import generate_simple_notes, extract_transcript

async def test_simple_generation():
    """Test simple note generation"""
    
    print("🧪 Testing simple note generation...")
    
    # Test with a sample transcript
    sample_transcript = """
    Hello everyone, welcome to this tutorial on Python programming. Today we'll be covering the basics of Python including variables, data types, and control structures. Python is a high-level programming language known for its simplicity and readability. Let's start with variables. In Python, you can create a variable by simply assigning a value to it. For example, x equals 5 creates a variable named x with the value 5. Python supports several data types including integers, floats, strings, and booleans. Control structures like if statements and loops help you control the flow of your program. That's the basics of Python programming.
    """
    
    try:
        # Test simple note generation
        notes = generate_simple_notes(sample_transcript)
        
        print("✅ Simple note generation successful!")
        print(f"📝 Notes length: {len(notes)} characters")
        print("📄 Generated notes:")
        print("-" * 50)
        print(notes)
        print("-" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(test_simple_generation()) 