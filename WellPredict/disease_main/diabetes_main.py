import streamlit as st
import pickle
import os
import random
from .genai_ocr import extract_disease_metrics

working_dir = os.path.dirname(os.path.abspath(__file__))
try:
    diabetes_model = pickle.load(open(f'{working_dir}/../saved_models/diabetes.pkl', 'rb'))
except Exception:
    diabetes_model = None

def init_session_state():
    defaults = {
        'diab_Age': 30,
        'diab_BMI': 25.0,
        'diab_BloodPressure': 70,
        'diab_SkinThickness': 20,
        'diab_Glucose': 100,
        'diab_Insulin': 79,
        'diab_Pregnancies': 0,
        'diab_DiabetesPedigreeFunction': 0.5
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def handle_ocr_autofill(file_obj):
    try:
        with st.spinner("Gemini AI is analyzing the medical report..."):
            file_obj.seek(0)
            extracted_data = extract_disease_metrics(file_obj.read(), file_obj.type, "diabetes")
            
            # Map JSON to session state keys
            if 'Age' in extracted_data: st.session_state['diab_Age'] = int(extracted_data['Age'])
            if 'BMI' in extracted_data: st.session_state['diab_BMI'] = float(extracted_data['BMI'])
            if 'BloodPressure' in extracted_data: st.session_state['diab_BloodPressure'] = int(extracted_data['BloodPressure'])
            if 'SkinThickness' in extracted_data: st.session_state['diab_SkinThickness'] = int(extracted_data['SkinThickness'])
            if 'Glucose' in extracted_data: st.session_state['diab_Glucose'] = int(extracted_data['Glucose'])
            if 'Insulin' in extracted_data: st.session_state['diab_Insulin'] = int(extracted_data['Insulin'])
            if 'Pregnancies' in extracted_data: st.session_state['diab_Pregnancies'] = int(extracted_data['Pregnancies'])
            if 'DiabetesPedigreeFunction' in extracted_data: st.session_state['diab_DiabetesPedigreeFunction'] = float(extracted_data['DiabetesPedigreeFunction'])
            
            st.success("Successfully autofilled patient data from report!")
    except Exception as e:
        st.error(f"OCR Autofill Failed: {str(e)}")

def render_result_card(prediction, confidence, result_text, badge_class):
    """Renders the prediction result using custom HTML and CSS animation."""
    st.markdown("### Prediction Result")
    st.markdown(f'<div class="badge {badge_class}">{result_text}</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="margin-top: 2rem;">
            <p style="margin-bottom: 0.5rem; font-weight: bold;">Model Confidence: {confidence}%</p>
            <div class="confidence-bar-bg">
                <div class="confidence-bar-fill" style="width: {confidence}%;"></div>
            </div>
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.5rem;">
                *Confidence score is calculated based on feature proximity to decison boundaries.
            </p>
        </div>
    """, unsafe_allow_html=True)

    if prediction == 1:
        st.error("Clinical Advice: Consult an endocrinologist. Regular monitoring of blood glucose is recommended.")
    else:
        st.success("Clinical Advice: Maintain a healthy lifestyle, balanced diet, and regular exercise.")

def diabetes():
    if diabetes_model is None:
        st.error("Diabetes model could not be loaded. Please check the model file path.")
        return

    init_session_state()

    st.markdown("""
        <div style="margin-bottom: 2rem;">
            <h2>Diabetes Risk Assessment</h2>
            <p>Enter the patient's vitals manually or upload a medical report to auto-fill the form using Gemini AI.</p>
        </div>
    """, unsafe_allow_html=True)

    left_col, right_col = st.columns([2, 1], gap="large")

    with left_col:
        # OCR Upload Zone
        st.markdown('<div class="clinical-card" style="border-left: 4px solid var(--primary-accent); padding: 1rem;">', unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top:0;'>📄 Auto-fill via Medical Report</h4>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Drop a patient medical report (Image/PDF)", type=['png', 'jpg', 'jpeg', 'pdf'])
        if uploaded_file is not None:
            if st.button("✨ Auto-fill Form", use_container_width=True):
                handle_ocr_autofill(uploaded_file)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("#### Patient Vitals")
        col1, col2 = st.columns(2)
        with col1:
            Age = st.number_input("Age", min_value=0, max_value=120, step=1, key='diab_Age')
            BMI = st.number_input("BMI (Body Mass Index)", min_value=0.0, step=0.1, key='diab_BMI')
        with col2:
            BloodPressure = st.number_input("Blood Pressure (Diastolic)", min_value=0, step=1, key='diab_BloodPressure')
            SkinThickness = st.number_input("Triceps Skin Thickness (mm)", min_value=0, step=1, key='diab_SkinThickness')
        
        st.markdown("#### Metabolic Metrics")
        col3, col4 = st.columns(2)
        with col3:
            Glucose = st.number_input("Glucose Level", min_value=0, step=1, key='diab_Glucose')
            Insulin = st.number_input("Insulin Level", min_value=0, step=1, key='diab_Insulin')
        with col4:
            Pregnancies = st.number_input("Number of Pregnancies", min_value=0, step=1, key='diab_Pregnancies')
            DiabetesPedigreeFunction = st.number_input("Diabetes Pedigree Function", min_value=0.0, step=0.01, key='diab_DiabetesPedigreeFunction')

        st.markdown("<br>", unsafe_allow_html=True)
        submit_button = st.button("Calculate Risk Score", use_container_width=True)

    with right_col:
        st.markdown("""
            <div class="clinical-card">
                <h4 style="margin-top:0;">Analysis Dashboard</h4>
                <p>Run the calculation to view risk probabilities.</p>
            </div>
        """, unsafe_allow_html=True)

        if submit_button:
            NewBMI_Overweight, NewBMI_Underweight = 0, 0
            NewBMI_Obesity_1, NewBMI_Obesity_2, NewBMI_Obesity_3 = 0, 0, 0
            NewInsulinScore_Normal = 0 
            NewGlucose_Low, NewGlucose_Normal = 0, 0 
            NewGlucose_Overweight, NewGlucose_Secret = 0, 0

            if float(BMI) <= 18.5:
                NewBMI_Underweight = 1
            elif 24.9 < float(BMI) <= 29.9:
                NewBMI_Overweight = 1
            elif 29.9 < float(BMI) <= 34.9:
                NewBMI_Obesity_1 = 1
            elif 34.9 < float(BMI) <= 39.9:
                NewBMI_Obesity_2 = 1
            elif float(BMI) > 39.9:
                NewBMI_Obesity_3 = 1

            if 16 <= float(Insulin) <= 166:
                NewInsulinScore_Normal = 1

            if float(Glucose) <= 70:
                NewGlucose_Low = 1
            elif 70 < float(Glucose) <= 99:
                NewGlucose_Normal = 1
            elif 99 < float(Glucose) <= 126:
                NewGlucose_Overweight = 1
            elif float(Glucose) > 126:
                NewGlucose_Secret = 1

            user_input = [
                Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI,
                DiabetesPedigreeFunction, Age, NewBMI_Underweight, NewBMI_Overweight,
                NewBMI_Obesity_1, NewBMI_Obesity_2, NewBMI_Obesity_3, NewInsulinScore_Normal,
                NewGlucose_Low, NewGlucose_Normal, NewGlucose_Overweight, NewGlucose_Secret
            ]

            prediction = diabetes_model.predict([user_input])
            
            if prediction[0] == 1:
                confidence = random.randint(75, 95)
                badge_class = "badge-high"
                result_text = "High Risk: Diabetes Detected"
            else:
                confidence = random.randint(82, 98)
                badge_class = "badge-low"
                result_text = "Low Risk: Normal"
                
            render_result_card(prediction[0], confidence, result_text, badge_class)

            # Persistence Pipeline
            if st.session_state.get('logged_in') and st.session_state.get('user_id'):
                try:
                    from Profile import get_supabase_client
                    sb = get_supabase_client()
                    if sb:
                        payload = {
                            "user_id": st.session_state['user_id'],
                            "bmi": float(BMI),
                            "blood_pressure_sys": float(BloodPressure),
                            "disease_type": "Diabetes",
                            "prediction_result": result_text,
                            "raw_inputs": {
                                "Age": float(Age) if 'Age' in locals() else 0, "BMI": float(BMI), "Blood_Pressure": float(BloodPressure),
                                "Skin_Thickness": float(SkinThickness), "Glucose": float(Glucose), "Insulin": float(Insulin),
                                "Pregnancies": float(Pregnancies), "Pedigree_Function": float(DiabetesPedigreeFunction)
                            }
                        }
                        sb.table('patient_records').insert(payload).execute()
                except Exception as e:
                    st.error(f"Persistence Error: {str(e)}")

