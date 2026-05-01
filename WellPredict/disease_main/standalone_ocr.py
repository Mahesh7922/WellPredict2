import streamlit as st
from .genai_ocr import extract_disease_metrics
import google.generativeai as genai
import os
from .genai_ocr import pdf_page_to_image_bytes

def report_uploader():
    st.markdown("""
        <div style="margin-bottom: 2rem;">
            <h2>General Medical Report OCR Analyzer</h2>
            <p>Upload any medical document (PDF or Image) to extract general clinical text instantly using Vision AI.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="clinical-card">', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload Medical Report (Image or PDF)", type=['png', 'jpg', 'jpeg', 'pdf'])
    
    if uploaded_file is not None:
        if st.button("Extract Data & Text", use_container_width=True):
            with st.spinner("Reading your document..."):
                try:
                    API_KEY = st.secrets["API_KEY"]
                    model = genai.GenerativeModel("gemini-2.5-flash")
                    
                    uploaded_file.seek(0)
                    if uploaded_file.type == "application/pdf":
                        img_bytes = pdf_page_to_image_bytes(uploaded_file.read())
                        upload_mime = "image/jpeg"
                    else:
                        img_bytes = uploaded_file.read()
                        upload_mime = uploaded_file.type
                        
                    image_parts = [{"mime_type": upload_mime, "data": img_bytes}]
                    
                    prompt = '''
                    Act as an expert medical document parser. 
                    First, provide a structured summary of the report including Patient Name, Age, Type of Report, and the most critical findings.
                    Second, provide the complete exact transcribed text from the document.
                    Format the entire output as clean Markdown.
                    '''
                    
                    response = model.generate_content([prompt, image_parts[0]])
                    
                    st.success("Extraction Complete!")
                    st.markdown("### Document Findings")
                    st.markdown(response.candidates[0].content.parts[0].text)
                    
                except Exception as e:
                    st.error(f"Error during OCR extraction: {str(e)}")
                    
    st.markdown('</div>', unsafe_allow_html=True)
