import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import fitz  # PyMuPDF

# Load environment logic
load_dotenv()
API_KEY = os.getenv("API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

def pdf_page_to_image_bytes(pdf_bytes):
    """Converts the first page of a PDF to JPEG bytes."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    page = doc.load_page(0)
    pix = page.get_pixmap(dpi=150)
    return pix.tobytes("jpeg")

def extract_disease_metrics(file_bytes, mime_type, disease_type):
    """
    Calls Gemini-1.5-Flash to extract factors from a medical document 
    and returns a structured JSON dictionary mapping to the Streamlit session state fields.
    """
    if not API_KEY:
        raise Exception("API_KEY not found in .env. Please configure your API key.")
        
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    # Standardize to JPEG bytes
    if mime_type == "application/pdf":
        img_bytes = pdf_page_to_image_bytes(file_bytes)
        upload_mime = "image/jpeg"
    else:
        img_bytes = file_bytes
        upload_mime = mime_type
        
    image_parts = [
        {"mime_type": upload_mime, "data": img_bytes}
    ]
    
    # Prompt Schemas per Disease
    prompts = {
        "diabetes": '''
            You are a medical data extraction assistant. Extract the following metrics from the provided medical report. 
            Return ONLY a valid JSON object with the exact keys below. If a value is missing in the document, use 0 for numbers or standard safe defaults.
            Keys to extract:
            - "Age" (integer)
            - "BMI" (float)
            - "BloodPressure" (integer)
            - "SkinThickness" (integer)
            - "Glucose" (integer)
            - "Insulin" (integer)
            - "Pregnancies" (integer)
            - "DiabetesPedigreeFunction" (float)
        ''',
        "heart": '''
            You are a medical data extraction assistant. Extract the following cardiovascular metrics from the provided document.
            Return ONLY a valid JSON object with the exact keys below. If a value is missing, use 0 for numbers or "No" / "Normal" / "0" where applicable.
            Keys:
            - "age" (integer)
            - "sex" (string: "Male" or "Female")
            - "heart_bps" (float: resting blood pressure)
            - "chol" (float: serum cholesterol mg/dl)
            - "heart_rate" (integer: max heart rate)
            - "fbs" (string: "Yes" or "No", fasting blood sugar > 120)
            - "exang" (string: "Yes" or "No", exercise induced angina)
            - "oldpeak" (float: ST depression)
            - "slope" (float: slope of peak exercise ST segment)
            - "ca" (integer: colored vessels 0-4)
            - "cp" (integer: chest pain level 0, 1, or 2)
            - "restecg" (integer: resting ecg 0, 1, or 2)
            - "thal" (integer: 0, 1, or 2)
        ''',
        "kidney": '''
            You are a medical data extraction assistant. Extract the following nephrology metrics.
            Return ONLY a valid JSON object. If missing, use intelligent 0 or negative/normal string defaults.
            Keys:
            - "age" (integer)
            - "blood_pressure" (float)
            - "haemoglobin" (float)
            - "specific_gravity" (float)
            - "red_blood_cells" ("Normal" or "Abnormal")
            - "albumin" (float)
            - "pus_cell" ("Normal" or "Abnormal")
            - "sugar" (float)
            - "bacteria" ("Present" or "Not Present")
            - "blood_glucose_random" (float)
            - "sodium" (float)
            - "blood_urea" (float)
            - "potassium" (float)
            - "serum_creatinine" (float)
            - "packed_cell_volume" (float)
            - "white_blood_cell_count" (float)
            - "red_blood_cell_count" (float)
            - "pus_cell_clumps" ("Yes" or "No")
            - "hypertension" ("Yes" or "No")
            - "diabetes_mellitus" ("Yes" or "No")
            - "cad" ("Yes" or "No")
            - "appet" ("Good" or "Poor")
            - "pe" ("Yes" or "No")
            - "aane" ("Yes" or "No")
        '''
    }
    
    prompt = prompts.get(disease_type, "")
    
    # Generate content
    response = model.generate_content([prompt, image_parts[0]])
    
    # Parse json strictly from markdown block if Gemini wraps it
    text_content = response.candidates[0].content.parts[0].text.strip()
    if text_content.startswith("```json"):
        text_content = text_content[7:-3].strip()
    elif text_content.startswith("```"):
        text_content = text_content[3:-3].strip()
        
    try:
        data = json.loads(text_content)
        return data
    except Exception as e:
        raise Exception(f"Failed to parse Gemini output into JSON. Raw output: {text_content}")
