#!/usr/bin/env python3
"""
PDF service for generating formatted PDF documents
"""

import tempfile
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import black, blue, gray, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class PDFService:
    """Service for PDF generation"""
    
    @staticmethod
    def generate_pdf(notes: str, title: str, youtube_url: str, metadata: Dict = None) -> str:
        """Generate PDF from notes with enhanced formatting"""
        try:
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            pdf_path = temp_file.name
            temp_file.close()
            
            # Create PDF document
            doc = SimpleDocTemplate(
                pdf_path, 
                pagesize=A4,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=0.75*inch,
                bottomMargin=0.75*inch
            )
            
            # Build content
            story = PDFService._build_content(notes, title, youtube_url, metadata)
            
            # Build PDF
            doc.build(story)
            
            return pdf_path
            
        except Exception as e:
            raise Exception(f"PDF generation failed: {str(e)}")
    
    @staticmethod
    def _build_content(notes: str, title: str, youtube_url: str, metadata: Dict = None) -> List:
        """Build PDF content with proper formatting"""
        story = []
        styles = getSampleStyleSheet()
        
        # Create custom styles with better formatting
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1,  # Center alignment
            textColor=blue,
            fontName='Helvetica-Bold',
            spaceBefore=20
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=15,
            alignment=1,  # Center alignment
            textColor=gray,
            fontName='Helvetica'
        )
        
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading2'],
            fontSize=18,
            spaceAfter=15,
            spaceBefore=25,
            textColor=blue,
            fontName='Helvetica-Bold',
            leftIndent=0
        )
        
        subheader_style = ParagraphStyle(
            'CustomSubHeader',
            parent=styles['Heading3'],
            fontSize=14,
            spaceAfter=10,
            spaceBefore=18,
            textColor=black,
            fontName='Helvetica-Bold',
            leftIndent=0
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            textColor=black,
            fontName='Helvetica',
            alignment=0,  # Left alignment
            leftIndent=0
        )
        
        bullet_style = ParagraphStyle(
            'CustomBullet',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            leftIndent=20,
            textColor=black,
            fontName='Helvetica',
            bulletIndent=10,
            bulletFontName='Helvetica-Bold',
            bulletFontSize=8
        )
        
        # Add title page
        story.append(Paragraph(title, title_style))
        story.append(Paragraph(f"Generated from: {youtube_url}", subtitle_style))
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", subtitle_style))
        
        # Add metadata if available
        if metadata:
            story.append(Spacer(1, 20))
            story.extend(PDFService._create_metadata_table(metadata, styles))
        
        story.append(PageBreak())
        
        # Process notes content with improved formatting
        lines = notes.split('\n')
        current_text = []
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_text:
                    # Add accumulated text
                    text = ' '.join(current_text)
                    story.append(Paragraph(text, normal_style))
                    story.append(Spacer(1, 8))
                    current_text = []
            elif line.startswith('##'):
                # Add accumulated text before header
                if current_text:
                    text = ' '.join(current_text)
                    story.append(Paragraph(text, normal_style))
                    story.append(Spacer(1, 8))
                    current_text = []
                
                # Clean and format header (remove ## and emojis)
                header_text = line.replace('##', '').strip()
                # Remove emojis and clean up
                header_text = PDFService._clean_text(header_text)
                if header_text:
                    story.append(Paragraph(header_text, header_style))
                    
            elif line.startswith('###'):
                # Add accumulated text before subheader
                if current_text:
                    text = ' '.join(current_text)
                    story.append(Paragraph(text, normal_style))
                    story.append(Spacer(1, 8))
                    current_text = []
                
                # Clean and format subheader (remove ### and emojis)
                subheader_text = line.replace('###', '').strip()
                subheader_text = PDFService._clean_text(subheader_text)
                if subheader_text:
                    story.append(Paragraph(subheader_text, subheader_style))
                    
            elif line.startswith('####'):
                # Add accumulated text before sub-subheader
                if current_text:
                    text = ' '.join(current_text)
                    story.append(Paragraph(text, normal_style))
                    story.append(Spacer(1, 8))
                    current_text = []
                
                # Clean and format sub-subheader
                subsubheader_text = line.replace('####', '').strip()
                subsubheader_text = PDFService._clean_text(subsubheader_text)
                if subsubheader_text:
                    story.append(Paragraph(subsubheader_text, subheader_style))
                    
            elif line.startswith('- ') or line.startswith('• '):
                # Add accumulated text before bullet point
                if current_text:
                    text = ' '.join(current_text)
                    story.append(Paragraph(text, normal_style))
                    story.append(Spacer(1, 8))
                    current_text = []
                
                # Clean and format bullet point
                bullet_text = line.replace('- ', '').replace('• ', '').strip()
                bullet_text = PDFService._clean_text(bullet_text)
                if bullet_text:
                    story.append(Paragraph(f"• {bullet_text}", bullet_style))
                    
            elif line.startswith('**') and line.endswith('**'):
                # Bold text - clean and format
                bold_text = line.replace('**', '').strip()
                bold_text = PDFService._clean_text(bold_text)
                if bold_text:
                    story.append(Paragraph(f"<b>{bold_text}</b>", normal_style))
                    story.append(Spacer(1, 6))
                    
            elif line.startswith('*') and line.endswith('*') and not line.startswith('**'):
                # Italic text - clean and format
                italic_text = line.replace('*', '').strip()
                italic_text = PDFService._clean_text(italic_text)
                if italic_text:
                    story.append(Paragraph(f"<i>{italic_text}</i>", normal_style))
                    story.append(Spacer(1, 6))
                    
            elif line.startswith('```'):
                # Code block - skip for now or handle differently
                if current_text:
                    text = ' '.join(current_text)
                    story.append(Paragraph(text, normal_style))
                    story.append(Spacer(1, 8))
                    current_text = []
                    
            elif line.startswith('`') and line.endswith('`'):
                # Inline code - clean and format
                code_text = line.replace('`', '').strip()
                code_text = PDFService._clean_text(code_text)
                if code_text:
                    story.append(Paragraph(f"<code>{code_text}</code>", normal_style))
                    story.append(Spacer(1, 6))
                    
            else:
                # Regular text - clean and accumulate
                cleaned_line = PDFService._clean_text(line)
                if cleaned_line:
                    current_text.append(cleaned_line)
        
        # Add any remaining text
        if current_text:
            text = ' '.join(current_text)
            story.append(Paragraph(text, normal_style))
        
        return story
    
    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean text by removing emojis and unnecessary symbols"""
        import re
        
        # Remove emojis and special characters
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        
        # Remove emojis
        text = emoji_pattern.sub('', text)
        
        # Remove extra markdown symbols
        text = text.replace('**', '').replace('*', '').replace('`', '')
        
        # Clean up extra spaces and formatting
        text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
        text = text.strip()
        
        return text
    
    @staticmethod
    def _create_metadata_table(metadata: Dict, styles) -> List:
        """Create a metadata table for the PDF"""
        table_data = []
        
        # Add metadata rows
        if metadata.get('video_author'):
            table_data.append(['Author:', metadata['video_author']])
        if metadata.get('video_duration'):
            table_data.append(['Duration:', metadata['video_duration']])
        if metadata.get('publish_date'):
            table_data.append(['Published:', metadata['publish_date']])
        if metadata.get('view_count'):
            table_data.append(['Views:', f"{int(metadata['view_count']):,}"])
        
        if not table_data:
            return []
        
        # Create table
        table = Table(table_data, colWidths=[1.5*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), gray),
            ('TEXTCOLOR', (0, 0), (0, -1), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, black),
        ]))
        
        return [table, Spacer(1, 20)]
    
    @staticmethod
    def generate_simple_pdf(notes: str, title: str) -> str:
        """Generate a simple PDF without metadata"""
        try:
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            pdf_path = temp_file.name
            temp_file.close()
            
            # Create PDF document
            doc = SimpleDocTemplate(pdf_path, pagesize=A4)
            story = []
            
            # Get styles
            styles = getSampleStyleSheet()
            
            # Add title
            story.append(Paragraph(title, styles['Heading1']))
            story.append(Spacer(1, 20))
            
            # Add notes
            story.append(Paragraph(notes, styles['Normal']))
            
            # Build PDF
            doc.build(story)
            
            return pdf_path
            
        except Exception as e:
            raise Exception(f"Simple PDF generation failed: {str(e)}") 