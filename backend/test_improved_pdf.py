#!/usr/bin/env python3
"""
Test improved PDF formatting
"""

import requests
import json

def test_improved_pdf():
    """Test the improved PDF formatting"""
    
    print("🧪 Testing Improved PDF Formatting...")
    print("=" * 50)
    
    # Sample notes with emojis and markdown
    sample_notes = """# 📋 Overview & Summary

This video covers the fundamentals of machine learning and artificial intelligence.

## 🎯 Key Concepts & Main Ideas

- **Machine Learning**: A subset of AI that enables computers to learn without being explicitly programmed
- **Deep Learning**: A subset of ML using neural networks with multiple layers
- **Supervised Learning**: Learning from labeled training data

## 📚 Detailed Explanations

Machine learning algorithms can be categorized into three main types:

1. **Supervised Learning**: Uses labeled data to train models
2. **Unsupervised Learning**: Finds patterns in unlabeled data
3. **Reinforcement Learning**: Learns through interaction with environment

## 💡 Practical Applications

- **Image Recognition**: Identifying objects in photos
- **Natural Language Processing**: Understanding and generating human language
- **Recommendation Systems**: Suggesting products or content

## 🔍 Key Takeaways & Insights

- ML is transforming industries across the board
- Data quality is crucial for successful ML projects
- Continuous learning and adaptation are key principles

*This is italic text for emphasis*

**This is bold text for important concepts**

`This is inline code for technical terms`"""

    # Test data
    data = {
        "notes": sample_notes,
        "title": "Improved Formatting Test",
        "youtube_url": "https://www.youtube.com/watch?v=test",
        "metadata": {
            "video_author": "Test Author",
            "video_duration": "15:30",
            "publish_date": "2024-01-15",
            "view_count": "50000"
        }
    }
    
    try:
        print("📝 Testing improved PDF generation...")
        response = requests.post(
            "http://localhost:8000/generate-pdf",
            json=data,
            timeout=60
        )
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📄 Content-Type: {response.headers.get('content-type', 'Unknown')}")
        print(f"📏 Content-Length: {response.headers.get('content-length', 'Unknown')}")
        
        if response.status_code == 200:
            print("✅ Improved PDF Generated Successfully!")
            print(f"📏 Size: {len(response.content)} bytes")
            
            # Save PDF
            filename = "improved_formatting_test.pdf"
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"💾 PDF saved as: {filename}")
            
            # Check if file exists and has content
            import os
            if os.path.exists(filename):
                file_size = os.path.getsize(filename)
                print(f"📁 File exists, size: {file_size} bytes")
                if file_size > 0:
                    print("✅ File download successful!")
                    print("🎨 PDF should now have:")
                    print("   • Clean headers without ## symbols")
                    print("   • No emojis in the content")
                    print("   • Professional bullet points")
                    print("   • Better spacing and typography")
                    print("   • Proper bold and italic formatting")
                else:
                    print("❌ File is empty!")
            else:
                print("❌ File was not created!")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Server is not running")
        print("Please start the server with: uvicorn main:app --reload")
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: Request took too long")
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_multilingual_improved_pdf():
    """Test improved PDF with multilingual content"""
    
    print("\n🌍 Testing Multilingual Improved PDF...")
    print("=" * 50)
    
    # Sample notes with emojis and different languages
    sample_notes = """# 📋 Resumen General

Este video cubre los fundamentos del aprendizaje automático.

## 🎯 Conceptos Clave

- **Machine Learning**: Subconjunto de IA que permite a las computadoras aprender
- **Deep Learning**: Redes neuronales con múltiples capas
- **Supervised Learning**: Aprendizaje con datos etiquetados

## 📚 Explicaciones Detalladas

Los algoritmos de machine learning se pueden categorizar en tres tipos principales:

1. **Aprendizaje Supervisado**: Usa datos etiquetados
2. **Aprendizaje No Supervisado**: Encuentra patrones en datos no etiquetados
3. **Aprendizaje por Refuerzo**: Aprende a través de interacción

## 💡 Aplicaciones Prácticas

- **Reconocimiento de Imágenes**: Identificar objetos en fotos
- **Procesamiento de Lenguaje Natural**: Entender y generar lenguaje humano
- **Sistemas de Recomendación**: Sugerir productos o contenido

*Este es texto en cursiva para énfasis*

**Este es texto en negrita para conceptos importantes**"""

    # Test data
    data = {
        "notes": sample_notes,
        "title": "Multilingual Formatting Test",
        "youtube_url": "https://www.youtube.com/watch?v=test",
        "metadata": {
            "video_author": "Spanish Channel",
            "video_duration": "12:45",
            "publish_date": "2024-01-20",
            "view_count": "25000"
        }
    }
    
    try:
        print("📝 Testing multilingual improved PDF...")
        response = requests.post(
            "http://localhost:8000/generate-pdf",
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            print("✅ Multilingual PDF Generated Successfully!")
            
            # Save PDF
            filename = "multilingual_improved_test.pdf"
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"💾 PDF saved as: {filename}")
            print(f"📏 Size: {len(response.content)} bytes")
            
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    print("🚀 Improved PDF Formatting Test")
    print("=" * 60)
    
    test_improved_pdf()
    test_multilingual_improved_pdf()
    
    print("\n✨ Testing completed!")
    print("📄 Check the generated PDF files for improved formatting!") 