import streamlit as st

def diabetes_general():
    def calculate_bmi(height_cm, weight_kg):
        height_m = height_cm / 100
        return round(weight_kg / (height_m ** 2), 2)

    weights = {
        'smoking_status': {
            'Sensations': 5,
            'More infections': 3,
            'Non': 0
        },
        'physical_activity': {
            'Blurred': 4,
            'Moderate': 1,
            'Clear': 0
        },
        'unhealthy_foods': {
            'Excessive  ': 4,
            'More than Normal': 3,
            'Normal': 0
        },
        'alcohol_consumption': {
            'Never': 0,
            'Excessive Urination': 4,
            'Frequent Urination': 2
        },
        'family_history': {
            'Yes': 3,
            'No': 0
        }
    }

    def predict_disease_risk(smoking_status, physical_activity, unhealthy_foods, height_cm, weight_kg, alcohol_consumption, family_history):
        bmi = calculate_bmi(height_cm, weight_kg)
        
        if bmi < 18.5:
            bmi_weight = 1
        elif 18.5 <= bmi < 24.9:
            bmi_weight = 0
        elif 25 <= bmi < 29.9:
            bmi_weight = 2
        else:
            bmi_weight = 3
        
        risk_score = (
            weights['smoking_status'][smoking_status] +
            weights['physical_activity'][physical_activity] +
            weights['unhealthy_foods'][unhealthy_foods] +
            bmi_weight +
            weights['alcohol_consumption'][alcohol_consumption] +
            weights['family_history'][family_history]
        )
        
        if risk_score <= 7:
            risk_category = "Safe"
            message = "You are fit! Keep up the good work."
            return risk_category, message, "safe"
        elif 8 <= risk_score <= 13:
            risk_category = "Moderate Risk"
            message = "Consult a healthcare professional for personalized advice."
            return risk_category, message, "moderate"
        else:
            risk_category = "High Risk"
            message = "It's advisable to consult a doctor for further evaluation."
            return risk_category, message, "high"

    st.title("Diabetes Prediction Model")

    col1, col2, col3 = st.columns(3)

    with col1:
        height_cm = st.number_input('Height (cm)', min_value=50, max_value=250, value=175)

    with col2:
        weight_kg = st.number_input('Weight (kg)', min_value=10, max_value=200, value=75)

    with col3:
        alcohol_consumption = st.selectbox('Urination', options=['Select', 'Excessive Urination', 'Frequent Urination'], index=0)

    col4, col5, col6 = st.columns(3)

    with col4:
        smoking_status = st.selectbox('Non healing wound', options=['Select', 'Sensations', 'More infections', 'Non'], index=0)

    with col5:
        physical_activity = st.selectbox('Blurred vision ', options=['Select', 'Clear', 'Moderate', 'Blurred'], index=0)

    with col6:
        unhealthy_foods = st.selectbox('Hunger', options=['Select', 'Normal', 'More than Normal', 'Excessive'], index=0)

    family_history = st.selectbox('Family History of Heart Disease', options=['Select', 'Yes', 'No'], index=0)

    if st.button("Predict Risk"):
        if all(input != 'Select' for input in [smoking_status, physical_activity, unhealthy_foods, alcohol_consumption, family_history]):
            risk_category, message, risk_level = predict_disease_risk(
                smoking_status,
                physical_activity,
                unhealthy_foods,
                height_cm,
                weight_kg,
                alcohol_consumption,
                family_history
            )
            
            if risk_level == "safe":
                st.success(f"**Risk Category:** {risk_category}")
                st.info(message)
            elif risk_level == "moderate":
                st.warning(f"**Risk Category:** {risk_category}")
                st.info(message)
            elif risk_level == "high":
                st.error(f"**Risk Category:** {risk_category}")
                st.info(message)
        else:
            st.warning("Please select all options before predicting the risk.")
diabetes_general()
