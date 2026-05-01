import streamlit as st

def kidney_gen():
    def calculate_bmi(weight_kg, height_cm):
        height_m = height_cm / 100 
        return round(weight_kg / (height_m ** 2), 2)

    weights = {
        'bmi': {
            'Underweight': 1,
            'Normal': 0,
            'Overweight': 3,
            'Obese': 4
        },
        'age': {
            '0-30': 0,
            '31-50': 2,
            '51-70': 3,
            '71+': 4
        },
        'diabetes_status': {
            'Select': None,
            'Yes': 5,
            'No': 0
        },
        'blood_pressure': {
            'Select': None,
            'Normal': 0,
            'Slight Swelled': 2,
            'High Swelled': 3
        },
        'physical_activity': {
            'Select': None,
            'No Urination': 4,
            'Frequent': 3,
            'Normal': 0
        },
        'unhealthy_foods': {
            'Select': None,
            'Heavy Cramps': 4,
            'Slight Cramps': 1,
            'Never': 0
        }
    }

    def kidney_prediction(bmi_category, age_group, diabetes_status,
                        blood_pressure_category, physical_activity, unhealthy_foods):
        
        risk_score = (
            weights['bmi'][bmi_category] +
            weights['age'][age_group] +
            weights['diabetes_status'][diabetes_status] +
            weights['blood_pressure'][blood_pressure_category] +
            weights['physical_activity'][physical_activity] +
            weights['unhealthy_foods'][unhealthy_foods]
        )
        
        if risk_score <= 8:
            risk_category = "Safe"
            message = "You are at low risk for kidney disease. Keep maintaining a healthy lifestyle."
            return risk_category, message, "safe"
        elif 9 <= risk_score <= 17:
            risk_category = "Moderate Risk"
            message = "You have a moderate risk of kidney disease. Consider consulting a healthcare professional."
            return risk_category, message, "moderate"
        else:
            risk_category = "High Risk"
            message = "You are at high risk for kidney disease. It's advisable to seek medical attention."
            return risk_category, message, "high"

    st.title("Kidney Disease Prediction Model")
    st.header("Enter Your Details Below:")

    col1, col2, col3 = st.columns(3)

    with col1:
        height_cm = st.number_input(
            "Height (cm)", 
            min_value=100, 
            max_value=250, 
            value=170, 
            step=1
        )
    with col2:
        weight_kg = st.number_input(
            "Weight (kg)", 
            min_value=30, 
            max_value=200, 
            value=70, 
            step=1
        )
    with col3:
        age = st.number_input(
            "Age", 
            min_value=0, 
            max_value=120, 
            value=30, 
            step=1
        )

    col4, col5, col6 = st.columns(3)

    with col4:
        diabetes_status = st.selectbox(
            "Diabetes Status", 
            options=list(weights['diabetes_status'].keys()), 
            index=0
        )
    with col5:
        blood_pressure_category = st.selectbox(
            "Pedaledema (swelling in foot)", 
            options=list(weights['blood_pressure'].keys()), 
            index=0
        )
    with col6:
        physical_activity = st.selectbox(
            "Urination", 
            options=list(weights['physical_activity'].keys()), 
            index=0
        )

    col7, col8, col9 = st.columns(3)

    with col7:
        unhealthy_foods = st.selectbox(
            "Muscle cramps", 
            options=list(weights['unhealthy_foods'].keys()), 
            index=0
        )
    with col8:
        st.empty()
    with col9:
        st.empty()

    bmi = calculate_bmi(weight_kg, height_cm)

    if bmi < 18.5:
        bmi_category = 'Underweight'
    elif 18.5 <= bmi < 24.9:
        bmi_category = 'Normal'
    elif 25 <= bmi < 29.9:
        bmi_category = 'Overweight'
    else:
        bmi_category = 'Obese'

    st.write(f"**Your BMI:** {bmi} ({bmi_category})")

    if st.button("Predict Kidney Disease Risk"):
        selections = [
            diabetes_status, 
            blood_pressure_category, 
            physical_activity, 
            unhealthy_foods
        ]
        if all(selection != 'Select' for selection in selections):
            if age <= 30:
                age_group = '0-30'
            elif 31 <= age <= 50:
                age_group = '31-50'
            elif 51 <= age <= 70:
                age_group = '51-70'
            else:
                age_group = '71+'
            
            risk_category, message, risk_level = kidney_prediction(
                bmi_category,
                age_group,
                diabetes_status,
                blood_pressure_category,
                physical_activity,
                unhealthy_foods
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
            st.warning("Please make a selection for all dropdown fields before predicting the risk.")
