import streamlit as st
import pickle
import os
from streamlit_option_menu import option_menu

# Set page config MUST be the first Streamlit command
st.set_page_config(page_title="WellPredict", layout="wide", page_icon="⚕️")

# Import other files
from disease_main import kidney_main, heart_main, diabetes_main, Diabetes_general, Heart_general, Kidney_general, standalone_ocr
from Profile import user_profile
from chatbot_folder.streamlit_chatbot_interface_main import chatbot

def apply_custom_css():
    """Applies the custom clinical health-tech CSS theme."""
    st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Nunito:wght@400;600;700&display=swap');

        /* Global Theme Variables */
        :root {
            --bg-color: #0b132b;          /* Deep Navy Background */
            --glass-bg: rgba(28, 37, 65, 0.6); /* Glassmorphism Panel */
            --glass-border: rgba(255, 255, 255, 0.1);
            --primary-accent: #00e5ff;    /* Electric Blue */
            --secondary-accent: #00c49a;  /* Emerald Green */
            --text-main: #f8f9fa;         /* Sharp White */
            --text-muted: #cad2c5;        /* Muted Text */
        }

        /* App Background and Pulse Pattern */
        .stApp {
            background-color: var(--bg-color) !important;
            background-image: 
                linear-gradient(rgba(11, 19, 43, 0.9), rgba(11, 19, 43, 0.9)),
                radial-gradient(circle at 50% 50%, rgba(0, 229, 255, 0.05) 0%, transparent 60%);
            background-size: cover;
            background-attachment: fixed;
            font-family: 'Nunito', sans-serif !important;
            color: var(--text-main) !important;
        }

        /* Base Typography */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'DM Sans', sans-serif !important;
            color: var(--text-main) !important;
            font-weight: 700;
        }
        
        p, span, div, label {
            color: var(--text-muted);
            font-family: 'Nunito', sans-serif;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: rgba(11, 19, 43, 0.95) !important;
            border-right: 1px solid var(--glass-border);
            box-shadow: 2px 0 10px rgba(0,0,0,0.5);
        }

        /* Form / Input Container Styling */
        .stNumberInput > div > div > input, 
        .stTextInput > div > div > input, 
        .stSelectbox > div > div {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid var(--glass-border) !important;
            color: var(--text-main) !important;
            border-radius: 8px !important;
            font-family: 'Numito', monospace;
        }
        .stNumberInput > div > div > input:focus, 
        .stTextInput > div > div > input:focus, 
        .stSelectbox > div > div:focus {
            border-color: var(--primary-accent) !important;
            box-shadow: 0 0 5px rgba(0, 229, 255, 0.5) !important;
        }

        /* Custom Buttons */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary-accent) 0%, #00b4d8 100%) !important;
            color: #000000 !important;
            font-weight: 700 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.5rem 2rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
            width: 100%;
        }
        .stButton > button p, .stButton > button div {
            color: #000000 !important;
            font-weight: 700 !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0, 229, 255, 0.4) !important;
        }

        /* Custom Cards for Layout */
        .css-element-container .stMarkdown div[data-testid="stMarkdownContainer"] .clinical-card {
            background: var(--glass-bg);
            backdrop-filter: blur(10px);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }

        /* Hero Banner */
        .hero-section {
            background: linear-gradient(90deg, rgba(28,37,65,0.8) 0%, rgba(0,229,255,0.1) 100%);
            padding: 2rem 3rem;
            border-radius: 16px;
            border-left: 4px solid var(--primary-accent);
            margin-bottom: 2rem;
            backdrop-filter: blur(8px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            display: flex;
            align-items: center;
        }
        .hero-title {
            font-family: 'DM Sans', sans-serif;
            font-size: 2.5rem;
            font-weight: 700;
            color: #ffffff;
            margin: 0;
            line-height: 1.2;
        }
        .hero-subtitle {
            font-family: 'Nunito', sans-serif;
            font-size: 1.2rem;
            color: var(--primary-accent);
            margin-top: 0.5rem;
        }

        /* Animated Badge */
        @keyframes pulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.05); opacity: 0.8; }
            100% { transform: scale(1); opacity: 1; }
        }
        .badge {
            padding: 1rem 2rem;
            border-radius: 50px;
            font-weight: 700;
            font-size: 1.5rem;
            text-align: center;
            width: fit-content;
            margin: 2rem auto;
            animation: pulse 2s infinite;
            color: #0b132b;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
        }
        .badge-low { background-color: var(--secondary-accent); box-shadow: 0 0 20px var(--secondary-accent); }
        .badge-high { background-color: #ff4d4d; box-shadow: 0 0 20px #ff4d4d; color: white; }
        
        /* Progress Bar (Confidence) */
        .confidence-bar-bg {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            height: 12px;
            width: 100%;
            margin-top: 0.5rem;
            overflow: hidden;
        }
        .confidence-bar-fill {
            height: 100%;
            border-radius: 10px;
            background: linear-gradient(90deg, var(--primary-accent), var(--secondary-accent));
            transition: width 1s ease-in-out;
        }
        </style>
    """, unsafe_allow_html=True)

def show_hero():
    st.markdown("""
        <div class="hero-section">
            <div>
                <h1 class="hero-title"><span style="font-size: 3rem;">⚕️</span> WellPredict</h1>
                <p class="hero-subtitle">AI-powered early detection for a healthier life.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

working_dir = os.path.dirname(os.path.abspath(__file__))

# Load model
try:
    diabetes_model = pickle.load(open(f'{working_dir}/saved_models/diabetes.pkl', 'rb'))
except Exception:
    diabetes_model = None

# Apply CSS Globally
apply_custom_css()

# Mock user for static dashboard
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = True
    st.session_state['email'] = 'Harsh Yadav'
    st.session_state['user_id'] = 'harsh_123'

# Main application structure
with st.sidebar:
    st.markdown("<h3 style='text-align: center; color: var(--primary-accent); margin-bottom: 1rem;'>⚕️ WellPredict</h3>", unsafe_allow_html=True)
    selected = option_menu("", 
                            ['Profile',
                            'Diabetes Prediction',
                            'Heart Disease Prediction',
                            'Kidney Disease Prediction',
                            'Chat Bot'
                            ],
                            menu_icon='',
                            icons=['person', 'activity', 'heart-pulse', 'droplet', 'chat-dots'],
                            default_index=0,
                            styles={
                                "container": {"padding": "0!important", "background-color": "transparent"},
                                "icon": {"color": "#00e5ff", "font-size": "18px"}, 
                                "nav-link": {"font-family": "Nunito", "font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "rgba(255,255,255,0.1)", "color": "#f8f9fa"},
                                "nav-link-selected": {"background-color": "rgba(0, 229, 255, 0.2)", "border-left": "4px solid #00e5ff"},
                            })

# Only show hero on the main landing/profile/welcome screen to avoid clutter on prediction pages (optional)
if selected in ['Profile', 'Chat Bot']:
    show_hero()

# Handle selected option
if selected == 'Profile':
    user_profile()

elif selected == 'Diabetes Prediction':
    Diabetes_general.diabetes_general()
    with st.expander('Clinical Analysis & Prediction Tool'):
        diabetes_main.diabetes()

elif selected == 'Heart Disease Prediction':
    Heart_general.heart_gen()
    with st.expander('Clinical Analysis & Prediction Tool'):
        heart_main.heart()

elif selected == 'Kidney Disease Prediction':
    Kidney_general.kidney_gen()
    with st.expander('Clinical Analysis & Prediction Tool'):
        kidney_main.kidney()


elif selected == 'Chat Bot':
    chatbot.chat_bot()
