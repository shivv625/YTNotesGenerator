#!/usr/bin/env python3
"""
Test script to check OpenRouter API functionality
"""

import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def test_openrouter_api():
    """Test OpenRouter API connection"""
    
    # Get API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        api_key = "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"
        print("⚠️  Using fallback API key")
    
    print(f"🔑 API Key: {api_key[:20]}...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-site.com",
        "X-Title": "YouTube Notes Generator"
    }

    body = {
        "model": "nousresearch/deephermes-3-mistral-24b-preview:free",
        "messages": [{"role": "user", "content": "Hello, this is a test message. Please respond with 'API is working'."}],
        "max_tokens": 50,
        "temperature": 0.7,
        "top_p": 0.9
    }

    try:
        print("🌐 Testing OpenRouter API connection...")
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=body
            )
            
            print(f"📊 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ API is working!")
                print(f"📝 Response: {data['choices'][0]['message']['content']}")
                return True
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"📄 Response: {response.text}")
                return False
                
    except httpx.TimeoutException:
        print("⏰ Request timed out")
        return False
    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP Error: {e.response.status_code}")
        print(f"📄 Response: {e.response.text}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

async def test_note_generation():
    """Test note generation with a sample transcript"""
    print("\n📝 Testing note generation...")
    
    # Get API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        api_key = "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"
    
    sample_transcript = """
    Hello everyone, welcome to this tutorial on Python programming. Today we'll be covering the basics of Python including variables, data types, and control structures. Python is a high-level programming language known for its simplicity and readability. Let's start with variables. In Python, you can create a variable by simply assigning a value to it. For example, x equals 5 creates a variable named x with the value 5. Python supports several data types including integers, floats, strings, and booleans. Control structures like if statements and loops help you control the flow of your program. That's the basics of Python programming.
    """
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-site.com",
        "X-Title": "YouTube Notes Generator"
    }

    prompt = f"""You are an expert note-taker and educator. Generate comprehensive, well-structured study notes from this YouTube video transcript.

Please create notes that include:
1. **Overview/Summary** - Brief introduction to the topic
2. **Key Concepts** - Main ideas and important points
3. **Detailed Explanations** - Important details with examples
4. **Practical Applications** - How to apply the knowledge
5. **Key Takeaways** - Summary of most important points

Use clear markdown formatting with:
- Headers (##, ###) for sections
- Bullet points for lists
- **Bold** for emphasis
- Code blocks for technical terms
- Clear organization and flow

Transcript:
{sample_transcript}

Generate comprehensive, educational notes:"""

    body = {
        "model": "nousresearch/deephermes-3-mistral-24b-preview:free",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000,
        "temperature": 0.7,
        "top_p": 0.9
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            print("📡 Generating notes from sample transcript...")
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=body
            )
            response.raise_for_status()
            data = response.json()
            
            print("✅ Note generation successful!")
            print("📄 Generated notes:")
            print("-" * 50)
            print(data['choices'][0]['message']['content'])
            print("-" * 50)
            
            return True
            
    except Exception as e:
        print(f"❌ Note generation failed: {str(e)}")
        return False

async def main():
    print("🚀 YouTube Notes Generator - API Test")
    print("=" * 50)
    
    # Test basic API connection
    api_success = await test_openrouter_api()
    
    if api_success:
        # Test note generation
        await test_note_generation()
    
    print("\n" + "=" * 50)
    if api_success:
        print("✅ All tests passed! Your API key is working correctly.")
        print("🎉 You can now run the full application.")
    else:
        print("❌ API tests failed. Please check your API key and try again.")

if __name__ == "__main__":
    asyncio.run(test_openrouter_api()) 