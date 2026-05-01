import streamlit as st

# User data for authentication
users_data = {
    'jog':'j123',
    "Yatharth Singh": "Y@th@rth@#2005",
    "jane_smith": "securepass456"
}

# Function to authenticate users
def authenticate(username, password):
    return username in users_data and users_data[username] == password

# Title of the login page
st.title("Login Page")

# Input fields for username and password
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Login button
if st.button("Login"):
    if authenticate(username, password):
        # Set session state to indicate user is logged in
        st.session_state['logged_in'] = True
        st.session_state['username'] = username  # Store username
        st.success(f"Welcome, {username}!")
        
        # Redirect to main application
        st.experimental_rerun()  # Force a rerun of the script
    else:
        st.error("Invalid Username/Password")
