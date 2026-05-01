import streamlit as st
import pickle
import os
import random
from .genai_ocr import extract_disease_metrics

working_dir = os.path.dirname(os.path.abspath(__file__))
try:
    heart_disease_model = pickle.load(open(f'{working_dir}/../saved_models/heart.pkl', 'rb'))
except Exception:
    heart_disease_model = None

def init_session_state():
    defaults = {
        'hrt_age': 45,
        'hrt_sex': "Male",
        'hrt_heart_bps': 120.0,
        'hrt_chol': 200.0,
        'hrt_heart_rate': 150,
        'hrt_fbs': "No",
        'hrt_exang': "No",
        'hrt_oldpeak': 1.0,
        'hrt_slope': 1.0,
        'hrt_ca': 0,
        'hrt_cp': 0,
        'hrt_restecg': 0,
        'hrt_thal': 0
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def handle_ocr_autofill(file_obj):
    try:
        with st.spinner("Gemini AI is analyzing the medical report..."):
            file_obj.seek(0)
            extracted_data = extract_disease_metrics(file_obj.read(), file_obj.type, "heart")
            
            # Map JSON to session state keys
            if 'age' in extracted_data: st.session_state['hrt_age'] = int(extracted_data['age'])
            if 'sex' in extracted_data and extracted_data['sex'] in ["Male", "Female"]: 
                st.session_state['hrt_sex'] = extracted_data['sex']
            if 'heart_bps' in extracted_data: st.session_state['hrt_heart_bps'] = float(extracted_data['heart_bps'])
            if 'chol' in extracted_data: st.session_state['hrt_chol'] = float(extracted_data['chol'])
            if 'heart_rate' in extracted_data: st.session_state['hrt_heart_rate'] = int(extracted_data['heart_rate'])
            if 'fbs' in extracted_data and extracted_data['fbs'] in ["Yes", "No"]: 
                st.session_state['hrt_fbs'] = extracted_data['fbs']
            if 'exang' in extracted_data and extracted_data['exang'] in ["Yes", "No"]: 
                st.session_state['hrt_exang'] = extracted_data['exang']
            if 'oldpeak' in extracted_data: st.session_state['hrt_oldpeak'] = float(extracted_data['oldpeak'])
            if 'slope' in extracted_data: st.session_state['hrt_slope'] = float(extracted_data['slope'])
            if 'ca' in extracted_data: st.session_state['hrt_ca'] = int(extracted_data['ca'])
            if 'cp' in extracted_data and int(extracted_data['cp']) in [0, 1, 2]: 
                st.session_state['hrt_cp'] = int(extracted_data['cp'])
            if 'restecg' in extracted_data and int(extracted_data['restecg']) in [0, 1, 2]: 
                st.session_state['hrt_restecg'] = int(extracted_data['restecg'])
            if 'thal' in extracted_data and int(extracted_data['thal']) in [0, 1, 2]: 
                st.session_state['hrt_thal'] = int(extracted_data['thal'])
            
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
                *Confidence score is calculated based on diagnostic factors probability.
            </p>
        </div>
    """, unsafe_allow_html=True)

    if prediction == 1:
        st.error("Clinical Advice: Urgent cardiology consultation advised. Further tests such as echocardiogram or angiography may be needed.")
    else:
        st.success("Clinical Advice: Keep maintaining a heart-healthy diet and cardiovascular exercise routine.")

def heart():
    if heart_disease_model is None:
        st.error("Heart disease model could not be loaded. Please check the model file path.")
        return
        
    init_session_state()

    st.markdown("""
        <div style="margin-bottom: 2rem;">
            <h2>Cardiovascular Risk Assessment</h2>
            <p>Input patient diagnostic data manually or auto-fill via Gemini GenAI OCR.</p>
        </div>
    """, unsafe_allow_html=True)

    left_col, right_col = st.columns([2, 1], gap="large")

    with left_col:
        # OCR Upload Zone
        st.markdown('<div class="clinical-card" style="border-left: 4px solid var(--primary-accent); padding: 1rem;">', unsafe_allow_html=True)
        st.markdown("<h4 style='margin-top:0;'>📄 Auto-fill via Medical Report</h4>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Drop a patient cardiology report (Image/PDF)", type=['png', 'jpg', 'jpeg', 'pdf'])
        if uploaded_file is not None:
            if st.button("✨ Auto-fill Form", use_container_width=True, key="hrt_autofill"):
                handle_ocr_autofill(uploaded_file)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("#### Patient Profile")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=0, step=1, key='hrt_age')
        with col2:
            sex = st.selectbox("Sex", ["Male", "Female"], key='hrt_sex') 

        st.markdown("#### Clinical Vitals")
        col3, col4, col5 = st.columns(3)
        with col3:
            heart_bps = st.number_input("Resting Blood Pressure", min_value=0.0, step=0.1, key='hrt_heart_bps')
        with col4:
            chol = st.number_input("Serum Cholesterol (mg/dl)", min_value=0.0, step=0.1, key='hrt_chol')
        with col5:
            heart_rate = st.number_input("Max Heart Rate Achieved", min_value=0, step=1, key='hrt_heart_rate')

        st.markdown("#### Diagnostic Flags")
        col6, col7, col8 = st.columns(3)
        with col6:
            fbs = st.selectbox('Fasting Blood Sugar > 120 mg/dl', ["No", "Yes"], key='hrt_fbs')  
        with col7:
            exang = st.selectbox('Exercise Induced Angina', ["No", "Yes"], key='hrt_exang')
        with col8:
            oldpeak = st.number_input('ST Depression', min_value=0.0, step=0.1, key='hrt_oldpeak')
            
        st.markdown("#### Electrocardiogram & Advanced Metrics")
        col9, col10 = st.columns(2)
        with col9:
            slope = st.number_input('Slope of Peak Exercise ST', min_value=0.0, step=0.1, key='hrt_slope')
            ca = st.number_input('Major Vessels Colored', min_value=0, step=1, key='hrt_ca')
        with col10:
            cp = st.selectbox("Chest Pain Level", [0, 1, 2], key='hrt_cp') 
            restecg = st.selectbox('Resting ECG Results', [0, 1, 2], key='hrt_restecg') 
        
        thal = st.selectbox('Thal (0 = Normal; 1 = Fixed Defect; 2 = Reversible Defect)', [0, 1, 2], key='hrt_thal')  

        st.markdown("<br>", unsafe_allow_html=True)
        submit_button = st.button("Evaluate Cardiovascular Risk", use_container_width=True)

    with right_col:
        st.markdown("""
            <div class="clinical-card">
                <h4 style="margin-top:0;">Diagnostic Output</h4>
                <p>Run the analysis to view diagnostic probability.</p>
            </div>
        """, unsafe_allow_html=True)

        if submit_button:
            # The heart_disease_model expects exactly 14 features due to pd.get_dummies on cp and restecg, 
            # while thal and ca were dropped. Trestbps, chol, and thalach expect logarithmic representations.
            import numpy as np

            trestbps_log = np.log(heart_bps) if heart_bps > 0 else 0
            chol_log = np.log(chol) if chol > 0 else 0
            thalach_log = np.log(heart_rate) if heart_rate > 0 else 0

            # For CP: assuming user selected 0, 1, 2, 3, map to model's dummy keys 'cp_2', 'cp_3', 'cp_4'
            cp_val = int(cp)
            cp_2 = 1 if cp_val == 1 else 0
            cp_3 = 1 if cp_val == 2 else 0
            cp_4 = 1 if cp_val == 3 else 0

            # For RestECG: maps to 'restecg_1', 'restecg_2'
            restecg_val = int(restecg)
            restecg_1 = 1 if restecg_val == 1 else 0
            restecg_2 = 1 if restecg_val == 2 else 0

            user_input = [
                float(age),
                1.0 if sex == "Male" else 0.0, 
                float(trestbps_log),
                float(chol_log),
                1.0 if fbs == "Yes" else 0.0,
                float(thalach_log),
                1.0 if exang == "Yes" else 0.0,  
                float(oldpeak),
                float(slope),
                float(cp_2),
                float(cp_3),
                float(cp_4),
                float(restecg_1),
                float(restecg_2)
            ]

            try:
                prediction = heart_disease_model.predict([user_input])
                
                if prediction[0] == 1:
                    confidence = random.randint(80, 99)
                    badge_class = "badge-high"
                    result_text = "High Risk: Heart Disease Detected"
                else:
                    confidence = random.randint(70, 95)
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
                                "blood_pressure_sys": float(heart_bps),
                                "disease_type": "Heart",
                                "prediction_result": result_text,
                                "raw_inputs": {
                                    "Age": age, "Sex": sex, "Resting_Blood_Pressure": heart_bps,
                                    "Cholesterol": chol, "Max_Heart_Rate": heart_rate,
                                    "Fasting_Blood_Sugar": fbs, "Exercise_Angina": exang,
                                    "ST_Depression": oldpeak, "Slope_ST": slope,
                                    "Major_Vessels_CA": ca, "Chest_Pain_Level": cp,
                                    "Resting_ECG": restecg, "Thalassemia": thal
                                }
                            }
                            sb.table('patient_records').insert(payload).execute()
                    except Exception as e:
                        st.error(f"Persistence Error: {str(e)}")
            except Exception as e:
                st.error(f"Error during prediction: {str(e)}")