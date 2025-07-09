#!/usr/bin/env python3
"""
AI service for generating notes using OpenRouter API
"""

import httpx
import asyncio
from typing import Dict, Optional
from config import Config
import logging

logger = logging.getLogger(__name__)

class AIService:
    """Service for AI-powered note generation"""
    
    @staticmethod
    async def generate_notes(transcript: str, style: str = "comprehensive", transcript_language: str = "unknown") -> str:
        """Generate notes using OpenRouter API with mistralai model"""
        try:
            # Validate API key
            if not Config.OPENROUTER_API_KEY:
                raise Exception("OpenRouter API key not found. Please set OPENROUTER_API_KEY in your environment.")
            
            # Truncate transcript if too long
            if len(transcript) > Config.MAX_TRANSCRIPT_LENGTH:
                transcript = transcript[:Config.MAX_TRANSCRIPT_LENGTH] + "... [truncated]"
            
            # Prepare the prompt based on style
            prompt = AIService._create_prompt(transcript, style, transcript_language)
            
            # Prepare headers
            headers = {
                "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://youtube-notes-generator.com",
                "X-Title": "YouTube Notes Generator"
            }
            
            # Prepare request body
            body = {
                "model": Config.OPENROUTER_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": Config.MAX_TOKENS,
                "temperature": Config.TEMPERATURE,
                "top_p": Config.TOP_P
            }
            
            # Make API request
            async with httpx.AsyncClient(timeout=Config.REQUEST_TIMEOUT) as client:
                response = await client.post(
                    f"{Config.OPENROUTER_BASE_URL}/chat/completions",
                    headers=headers,
                    json=body
                )
                response.raise_for_status()
                data = response.json()
                
                if 'choices' in data and len(data['choices']) > 0:
                    return data['choices'][0]['message']['content']
                else:
                    raise Exception("No response content received from API")
                
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise Exception("Invalid API key. Please check your OpenRouter API key.")
            elif e.response.status_code == 429:
                raise Exception("Rate limit exceeded. Please try again later.")
            elif e.response.status_code == 400:
                raise Exception(f"Bad request: {e.response.text}")
            else:
                raise Exception(f"API request failed: {e.response.status_code} - {e.response.text}")
        except httpx.TimeoutException:
            raise Exception("Request timed out. Please try again.")
        except Exception as e:
            raise Exception(f"Note generation failed: {str(e)}")
    
    @staticmethod
    def _create_prompt(transcript: str, style: str, transcript_language: str = "unknown") -> str:
        """Create prompt based on the requested style with multilingual support"""
        
        # Language context for the prompt
        language_context = ""
        if transcript_language.lower() not in ["english", "en", "unknown"]:
            language_context = f"\n\nIMPORTANT: The transcript is in {transcript_language}. Please translate the content to English and generate notes in English only."
        
        base_prompt = f"""You are an expert note-taker and educator. Generate {style} study notes from this YouTube video transcript.

{language_context}

Transcript:
{transcript}

Generate {style}, educational notes in English:"""
        
        if style == "comprehensive":
            return base_prompt + """

Please create comprehensive, well-formatted notes that include:

## 📋 **Overview & Summary**
- Brief introduction to the main topic
- Context and background information
- What the video aims to teach

## 🎯 **Key Concepts & Main Ideas**
- **Primary Topics**: Main subjects covered
- **Core Principles**: Fundamental ideas and concepts
- **Important Definitions**: Key terms and their meanings

## 📚 **Detailed Explanations**
- **In-Depth Analysis**: Comprehensive breakdown of topics
- **Examples & Illustrations**: Specific examples mentioned
- **Step-by-Step Processes**: If applicable
- **Technical Details**: Important technical information

## 💡 **Practical Applications**
- **Real-World Usage**: How to apply the knowledge
- **Use Cases**: Specific scenarios where this applies
- **Implementation Tips**: Practical advice for application

## 🔍 **Key Takeaways & Insights**
- **Main Lessons**: Most important points to remember
- **Critical Insights**: Key insights and revelations
- **Action Items**: What to do with this knowledge

## 📝 **Additional Notes**
- **Important Quotes**: Notable statements from the video
- **References**: Any sources or references mentioned
- **Further Reading**: Suggestions for additional learning

**Formatting Guidelines:**
- Use clear markdown formatting with headers (##, ###)
- Use bullet points (•) and numbered lists where appropriate
- Use **bold** for emphasis on important terms
- Use *italic* for definitions and key concepts
- Use `code blocks` for technical terms, commands, or code
- Maintain clear hierarchy and organization
- Ensure all content is in English, regardless of original transcript language"""
        
        elif style == "summary":
            return base_prompt + """

Please create a concise, well-structured summary that includes:

## 🎯 **Main Topic**
- What the video is about in 1-2 sentences

## 📋 **Key Points** (3-5 most important takeaways)
- Point 1: [Brief explanation]
- Point 2: [Brief explanation]
- Point 3: [Brief explanation]
- Point 4: [Brief explanation]
- Point 5: [Brief explanation]

## 📝 **Brief Summary**
- 2-3 sentence overview of the entire content
- Main conclusion or takeaway

**Formatting:**
- Use clear headers and bullet points
- Keep language concise and focused
- Ensure all content is in English"""
        
        elif style == "detailed":
            return base_prompt + """

Please create detailed, comprehensive notes that include:

## 🎯 **Introduction & Context**
- **Background Information**: Context and prerequisites
- **Video Purpose**: What the video aims to achieve
- **Target Audience**: Who this content is for

## 📚 **Main Content Breakdown**
- **Section 1**: [Detailed breakdown]
  - Sub-points and explanations
  - Examples and illustrations
- **Section 2**: [Detailed breakdown]
  - Sub-points and explanations
  - Examples and illustrations
- **Section 3**: [Detailed breakdown]
  - Sub-points and explanations
  - Examples and illustrations

## 🔍 **Examples & Case Studies**
- **Specific Examples**: Real-world applications
- **Case Studies**: Detailed scenarios mentioned
- **Practical Demonstrations**: Step-by-step processes

## ⚙️ **Technical Details**
- **Technical Concepts**: Complex information explained
- **Formulas & Calculations**: If applicable
- **Technical Requirements**: Prerequisites and dependencies

## 📋 **Step-by-Step Instructions**
- **Process 1**: Detailed steps
- **Process 2**: Detailed steps
- **Best Practices**: Recommended approaches

## ⚠️ **Common Mistakes & Pitfalls**
- **Mistake 1**: What to avoid and why
- **Mistake 2**: What to avoid and why
- **Prevention Tips**: How to avoid these mistakes

## 💡 **Advanced Tips & Insights**
- **Pro Tips**: Advanced techniques and insights
- **Optimization Strategies**: How to improve results
- **Expert Advice**: Professional recommendations

## 📝 **Summary & Conclusion**
- **Comprehensive Recap**: Summary of all major points
- **Final Takeaways**: Most important lessons
- **Next Steps**: What to do with this knowledge

**Formatting Guidelines:**
- Use multiple heading levels (##, ###, ####)
- Use numbered and bulleted lists extensively
- Use **bold** and *italic* for emphasis
- Use `code blocks` for technical content
- Include tables if relevant
- Maintain clear hierarchical structure
- Ensure all content is in English"""
        
        elif style == "bullet_points":
            return base_prompt + """

Please create bullet-point style notes that include:

## 📋 **Main Topics**
• **Topic 1**: [Brief description]
  - Key point 1
  - Key point 2
  - Key point 3

• **Topic 2**: [Brief description]
  - Key point 1
  - Key point 2
  - Key point 3

• **Topic 3**: [Brief description]
  - Key point 1
  - Key point 2
  - Key point 3

## 🎯 **Key Concepts**
• **Concept 1**: Definition and explanation
• **Concept 2**: Definition and explanation
• **Concept 3**: Definition and explanation

## 💡 **Important Facts**
• Fact 1: [Brief explanation]
• Fact 2: [Brief explanation]
• Fact 3: [Brief explanation]

## 📝 **Examples**
• **Example 1**: [Description]
• **Example 2**: [Description]
• **Example 3**: [Description]

## ✅ **Takeaways**
• Takeaway 1: [Brief summary]
• Takeaway 2: [Brief summary]
• Takeaway 3: [Brief summary]

**Formatting:**
- Use clear headers for main sections
- Use bullet points (•) for all items
- Use sub-bullets for detailed points
- Keep language concise and scannable
- Ensure all content is in English"""
        
        else:
            # Default to comprehensive
            return base_prompt + """

Please create comprehensive, well-formatted notes that include:

## 📋 **Overview & Summary**
- Brief introduction to the main topic
- Context and background information
- What the video aims to teach

## 🎯 **Key Concepts & Main Ideas**
- **Primary Topics**: Main subjects covered
- **Core Principles**: Fundamental ideas and concepts
- **Important Definitions**: Key terms and their meanings

## 📚 **Detailed Explanations**
- **In-Depth Analysis**: Comprehensive breakdown of topics
- **Examples & Illustrations**: Specific examples mentioned
- **Step-by-Step Processes**: If applicable
- **Technical Details**: Important technical information

## 💡 **Practical Applications**
- **Real-World Usage**: How to apply the knowledge
- **Use Cases**: Specific scenarios where this applies
- **Implementation Tips**: Practical advice for application

## 🔍 **Key Takeaways & Insights**
- **Main Lessons**: Most important points to remember
- **Critical Insights**: Key insights and revelations
- **Action Items**: What to do with this knowledge

**Formatting Guidelines:**
- Use clear markdown formatting with headers (##, ###)
- Use bullet points (•) and numbered lists where appropriate
- Use **bold** for emphasis on important terms
- Use *italic* for definitions and key concepts
- Use `code blocks` for technical terms, commands, or code
- Maintain clear hierarchy and organization
- Ensure all content is in English, regardless of original transcript language"""
    
    @staticmethod
    def generate_simple_notes(transcript: str) -> str:
        """Generate simple notes without API (fallback)"""
        lines = transcript.split('\n')
        notes = []
        
        # Add overview
        notes.append("## 📋 Overview/Summary")
        notes.append("This video covers the following topics:")
        
        # Extract key points (simple approach)
        key_points = []
        for line in lines:
            if len(line.strip()) > 20 and any(word in line.lower() for word in ['important', 'key', 'main', 'primary', 'essential']):
                key_points.append(f"• {line.strip()}")
        
        if key_points:
            notes.extend(key_points[:5])  # Limit to 5 key points
        else:
            notes.append("• Key concepts from the video")
        
        notes.append("")
        notes.append("## 🎯 Key Concepts")
        notes.append("• Main topics discussed in the video")
        notes.append("• Important definitions and explanations")
        notes.append("• Core principles and ideas")
        
        notes.append("")
        notes.append("## 📚 Detailed Explanations")
        notes.append("The video provides detailed explanations of the topics covered.")
        
        notes.append("")
        notes.append("## 💡 Practical Applications")
        notes.append("• How to apply the knowledge in real-world scenarios")
        notes.append("• Examples and use cases")
        
        notes.append("")
        notes.append("## 🔍 Key Takeaways")
        notes.append("• Summary of the most important points")
        notes.append("• Main lessons learned")
        
        return '\n'.join(notes) 