# 📄 PDF Download Guide - YouTube Notes Generator

The YouTube Notes Generator now supports PDF download functionality! You can generate beautiful, formatted PDF documents from your YouTube video notes.

## ✨ Features

### 📋 **Professional PDF Formatting**

- **Title Page**: Video title, source URL, and generation timestamp
- **Metadata Table**: Author, duration, publish date, view count
- **Structured Content**: Well-organized sections with headers
- **Rich Formatting**: Bold, italic, bullet points, code blocks
- **Clean Layout**: Professional typography and spacing

### 🎨 **Visual Elements**

- **Headers**: Clear section divisions with proper hierarchy
- **Bullet Points**: Easy-to-scan lists and key points
- **Emphasis**: Bold and italic text for important information
- **Code Blocks**: Technical terms and commands in code format
- **Metadata**: Video information in a clean table format

## 🚀 How to Use

### **Method 1: API Endpoint**

#### **Step 1: Generate Notes**

```bash
curl -X POST "http://localhost:8000/generate-notes" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=your_video_id",
    "style": "comprehensive"
  }'
```

#### **Step 2: Generate PDF**

```bash
curl -X POST "http://localhost:8000/generate-pdf" \
  -H "Content-Type: application/json" \
  -d '{
    "notes": "Your generated notes here...",
    "title": "Video Title",
    "youtube_url": "https://www.youtube.com/watch?v=your_video_id",
    "metadata": {
      "video_author": "Channel Name",
      "video_duration": "10:30",
      "publish_date": "2024-01-15",
      "view_count": "50000"
    }
  }' \
  --output "notes.pdf"
```

### **Method 2: Python Script**

```python
import requests

# Generate notes
notes_response = requests.post(
    "http://localhost:8000/generate-notes",
    json={
        "url": "https://www.youtube.com/watch?v=your_video_id",
        "style": "comprehensive"
    }
)

notes_data = notes_response.json()

# Generate PDF
pdf_response = requests.post(
    "http://localhost:8000/generate-pdf",
    json={
        "notes": notes_data["notes"],
        "title": notes_data["video_title"],
        "youtube_url": "https://www.youtube.com/watch?v=your_video_id",
        "metadata": {
            "video_author": notes_data["video_author"],
            "video_duration": notes_data["video_duration"],
            "publish_date": notes_data["publish_date"],
            "view_count": notes_data["view_count"]
        }
    }
)

# Save PDF
with open("youtube_notes.pdf", "wb") as f:
    f.write(pdf_response.content)
```

### **Method 3: Frontend Integration**

```javascript
// Generate notes first
const notesResponse = await fetch("/generate-notes", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    url: youtubeUrl,
    style: "comprehensive",
  }),
});

const notesData = await notesResponse.json();

// Generate and download PDF
const pdfResponse = await fetch("/generate-pdf", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    notes: notesData.notes,
    title: notesData.video_title,
    youtube_url: youtubeUrl,
    metadata: {
      video_author: notesData.video_author,
      video_duration: notesData.video_duration,
      publish_date: notesData.publish_date,
      view_count: notesData.view_count,
    },
  }),
});

// Download the PDF
const blob = await pdfResponse.blob();
const url = window.URL.createObjectURL(blob);
const a = document.createElement("a");
a.href = url;
a.download = `${notesData.video_title}.pdf`;
a.click();
```

## 📊 API Reference

### **POST /generate-pdf**

**Request Body:**

```json
{
  "notes": "string (required)",
  "title": "string (required)",
  "youtube_url": "string (required)",
  "metadata": {
    "video_author": "string (optional)",
    "video_duration": "string (optional)",
    "publish_date": "string (optional)",
    "view_count": "string (optional)"
  }
}
```

**Response:**

- **Content-Type**: `application/pdf`
- **Body**: PDF file binary data
- **Headers**:
  - `Content-Disposition`: `attachment; filename="notes.pdf"`

## 🧪 Testing

### **Quick Test**

```bash
# Run the simple PDF test
python test_pdf_simple.py
```

### **Full Workflow Test**

```bash
# Test complete workflow (YouTube URL → Notes → PDF)
python test_full_workflow.py
```

### **Frontend Test**

1. Open `test_frontend_pdf.html` in your browser
2. Enter a YouTube URL
3. Click "Generate Notes"
4. Click "Download PDF"

## 📁 Generated Files

The system generates PDF files with descriptive names:

- `test_notes.pdf` - Simple test PDF
- `youtube_notes_{video_id}.pdf` - Full workflow PDF
- `{video_title}.pdf` - Frontend download

## 🎯 PDF Structure

### **Title Page**

- Video title (large, centered)
- Source URL
- Generation timestamp
- Metadata table (if available)

### **Content Sections**

- **Overview & Summary**: Introduction and context
- **Key Concepts**: Main ideas and definitions
- **Detailed Explanations**: In-depth analysis
- **Practical Applications**: Real-world usage
- **Key Takeaways**: Important lessons
- **Additional Notes**: Quotes, references, further reading

### **Formatting Features**

- **Headers**: Clear section divisions (##, ###)
- **Bullet Points**: Easy-to-scan lists (•)
- **Bold Text**: Important terms and concepts
- **Italic Text**: Definitions and emphasis
- **Code Blocks**: Technical terms and commands
- **Metadata Table**: Video information

## 🔧 Configuration

### **PDF Settings** (in `config.py`)

```python
PDF_PAGE_SIZE = "A4"
PDF_MARGIN = 1  # inch
```

### **Styling Options**

- **Page Size**: A4 (default)
- **Margins**: 0.75 inches on all sides
- **Font**: Helvetica family
- **Colors**: Black text, blue headers, gray metadata

## 🚨 Troubleshooting

### **Common Issues**

1. **PDF Generation Fails**

   - Check if `reportlab` is installed: `pip install reportlab`
   - Verify notes content is not empty
   - Check server logs for errors

2. **Large File Size**

   - PDFs are typically 2-10KB for short notes
   - Longer videos generate larger PDFs
   - Check if notes contain excessive formatting

3. **Download Issues**
   - Ensure proper Content-Type headers
   - Check browser download settings
   - Verify file permissions

### **Error Messages**

- `"PDF generation failed"`: Check notes content and metadata
- `"Invalid request"`: Verify JSON format and required fields
- `"Server error"`: Check server logs and dependencies

## 📈 Performance

### **Generation Time**

- **Simple PDF**: < 1 second
- **Full Workflow**: 5-30 seconds (depends on video length)
- **Large Videos**: May take longer for processing

### **File Sizes**

- **Short Notes**: 2-5KB
- **Medium Notes**: 5-15KB
- **Long Notes**: 15-50KB

## 🌟 Best Practices

1. **Use Descriptive Titles**: Make PDFs easy to identify
2. **Include Metadata**: Provides context and source information
3. **Choose Appropriate Style**: Match note style to your needs
4. **Test with Different Videos**: Verify multilingual support
5. **Check PDF Quality**: Ensure formatting looks good

## 🎉 Success!

Your YouTube Notes Generator now supports full PDF download functionality! You can:

✅ Generate notes from any language YouTube video  
✅ Create professionally formatted PDFs  
✅ Download PDFs with one click  
✅ Include video metadata and source information  
✅ Use multiple note styles  
✅ Handle multilingual content

The PDF download feature is fully integrated and ready to use! 📄✨
