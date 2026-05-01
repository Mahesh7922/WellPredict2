import streamlit as st

users_data = {
    "Yatharth Singh": "Y@th@rth@#2005",
    "jane_smith": "securepass456"
}

def authenticate(username, password):
    if username in users_data and users_data[username] == password:
        return True
    return False

st.title("Login Page")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if authenticate(username, password):
        st.success(f"Welcome, {username}!")
    else:
        st.error("Invalid username or password. Please try again.")
