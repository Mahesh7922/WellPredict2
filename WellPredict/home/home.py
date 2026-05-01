import streamlit as st
from streamlit_option_menu import option_menu

# Set the page configuration
st.set_page_config(page_title="WellPredict App", layout="centered", page_icon="🩺")

# Sidebar menu for app selection
with st.sidebar:
    selected_app = option_menu("Choose an Application", 
                               ['Disease Prediction', 
                                'Health Care ChatBot'],
                               icons=['activity', 'chat'],
                               menu_icon="cast", 
                               default_index=0)

# Title of the Home Page
st.title("Welcome to WellPredict")

# Home Page description
st.write("""
This platform provides applications to assist with health diagnostics, chatbot services and more in future:
- **Disease Prediction:** Use AI models to predict diabetes, heart disease, and kidney disease.
- **Health Care ChatBot:** Chat with an AI-driven health care assistant for advice and assistance.

Choose an app from the sidebar to get started.
""")

# Redirect to respective app URLs
if selected_app == 'Disease Prediction':
    st.write("You selected the **Disease Prediction** app. [Click here to visit the app](http://192.168.1.5:8503)")
elif selected_app == 'Health Care ChatBot':
    st.write("You selected the **Health Care ChatBot** app. [Click here to visit the app]( http://192.168.1.5:8501)")
