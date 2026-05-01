import streamlit as st
import pickle
import os

working_dir = os.path.dirname(os.path.abspath(__file__))

liver_disease_model = pickle.load(open(f'{working_dir}/../saved_models/liver.pkl', 'rb'))

def liver():
    st.title("Liver Disease Prediction")
    col1, col2, col3 = st.columns(3)
    # Age,Gender,Total_Bilirubin,Direct_Bilirubin,Alkaline_Phosphotase,
    # Alamine_Aminotransferase,Aspartate_Aminotransferase,Total_Protiens,
    # Albumin,Albumin_and_Globulin_Ratio,Dataset
    
    with col1:
        age = st.number_input("Age: ", step=1, min_value=0)
    with col2:
        sex = st.selectbox("sex: ", ['Male', 'Female'])
    with col3:
        tb = st.number_input('Total Bilirubin: ')
    with col1:
        db = st.number_input('Direct Bilirubin: ')
    with col2:
        ap = st.number_input("Alkaline Phosphotase", step=1, min_value=0)
    with col3:
        ala = st.number_input("Alamine Aminotransferase", step=1)
    with col1:
        asa = st.number_input("Aspartate Aminotransferase", step=1)
    with col2:
        tp = st.number_input("Total Protien")
    with col3:
        alb = st.number_input("Albumin: ")
    with col1:
        agr = st.number_input("Albumin_and_Globulin_Ratio")

    liver_disease_result = ""
    if st.button("Liver Disease Test Result"):
        user_input = [
            age,
            1 if sex == "Male" else 0,
            tb,
            db,
            ap,
            ala,
            asa,
            tp,
            alb,
            agr
        ]
        
        try:
            prediction = liver_disease_model.predict([user_input])
            liver_disease_result = "This person has Liver disease" if prediction[0] == 1 else "This person does not have Liver disease"
            if prediction[0] == 1:
                st.success(liver_disease_result)
            else:
                st.error(liver_disease_result)
        except Exception as e:
            liver_disease_result = f"Error during prediction: {str(e)}"
            st.error(liver_disease_result)