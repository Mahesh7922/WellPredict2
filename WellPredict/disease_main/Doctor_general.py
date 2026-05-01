import streamlit as st

def doctor_general():
    # Sample data for doctors
    doctors = [
        {"name": "Dr. Jogendra", "specialization": "Cardiologist"},
        {"name": "Dr. Bob Johnson", "specialization": "Dermatologist"},
        {"name": "Dr. Charlie", "specialization": "Neurologist"},
        {"name": "Dr. Dana White", "specialization": "Pediatrician"},
        {"name": "Dr. Eve Davis", "specialization": "General Practitioner"},
        {"name": "Dr. Frank Green", "specialization": "Oncologist"},
        {"name": "Dr. Grace Lee", "specialization": "Orthopedic Surgeon"}
    ]

    # Adding custom CSS for card styling
    card_style = """
        <style>
        .card {
            height: 120px;
            background-color: #f0f0f5;
            border-radius: 10px;
            padding: 15px;
            margin: 10px;
            box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center; /* Center all content horizontally */
        }
        .card:hover {
            transform: scale(1.02);
            box-shadow: 4px 4px 20px rgba(0, 0, 0, 0.2);
        }
        .doctor-name {
            font-size: 1.5em;
            font-weight: bold;
            color: #333;
        }
        .specialization {
            font-size: 1.2em;
            color: #666;
            margin-bottom: 10px;
        }
        .button-container {
            display: flex;
            justify-content: center; /* Center the button */
            width: 100%; /* Ensure the button container spans the full width of the card */
        }
        </style>
    """

    st.markdown(card_style, unsafe_allow_html=True)

    # Title of the app
    st.title("Doctor Appointment Booking")

    # Initialize session state for booking details and chat message
    if 'booking_details' not in st.session_state:
        st.session_state.booking_details = {}

    if 'chat_message' not in st.session_state:
        st.session_state.chat_message = ""

    if 'selected_doctor' not in st.session_state:
        st.session_state.selected_doctor = None

    # Display doctor cards in a 3-column layout using Streamlit's st.columns()
    columns = st.columns(3)  # Create 3 columns

    for index, doctor in enumerate(doctors):
        col = columns[index % 3]  # Assign doctor cards in 3 columns, wrapping to new row after 3rd doctor
        
        with col:
            # Card content for each doctor
            st.markdown(f"""
                <div class="card">
                    <div class="doctor-name">{doctor['name']}</div>
                    <div class="specialization"><strong>Specialization:</strong> {doctor['specialization']}</div>
                </div>
            """, unsafe_allow_html=True)

            # Use Streamlit's button for functionality (hidden visually, handled via custom button style)
            if st.button(f"Book Appointment", key=f"btn_{doctor['name']}"):
                st.session_state.selected_doctor = doctor
                st.session_state.booking_details = {}

            # If "Chat" is clicked, open a text input to send a message
            if st.button(f"Chat", key=f"chat_{doctor['name']}"):
                st.session_state.selected_doctor = doctor
                st.session_state.chat_message = st.text_input(f"Message to {doctor['name']}", key=f"chat_input_{doctor['name']}")
                
                if st.button("Send Message", key=f"send_{doctor['name']}"):
                    st.success(f"Message sent to {doctor['name']}: {st.session_state.chat_message}")
                    st.session_state.chat_message = ""  # Reset message after sending

    # If a doctor is selected, show the booking form
    if st.session_state.selected_doctor and 'booking_details' in st.session_state:
        doctor = st.session_state.selected_doctor
        st.header(f"Booking for {doctor['name']} ({doctor['specialization']})")

        # Collect user details
        with st.form(key='booking_form'):
            st.header("User Information")
            name = st.text_input("Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")

            # Appointment Details
            st.header("Appointment Details")
            appointment_date = st.date_input("Select Appointment Date")
            appointment_time = st.time_input("Select Appointment Time")
            
            # Submit button for the form
            submit_button = st.form_submit_button(label="Confirm Booking")
            
            if submit_button:
                if name and email and phone and appointment_date and appointment_time:
                    st.session_state.booking_details = {
                        "doctor": doctor["name"],
                        "specialization": doctor["specialization"],
                        "date": appointment_date,
                        "time": appointment_time,
                        "name": name,
                        "email": email,
                        "phone": phone
                    }
                    st.success("Your appointment has been booked successfully!")
                else:
                    st.error("Please fill out all fields.")

    # Display booking confirmation if available
    if st.session_state.booking_details:
        st.header("Booking Confirmation")
        booking = st.session_state.booking_details
        st.write(f"**Doctor:** {booking['doctor']}")
        st.write(f"**Specialization:** {booking['specialization']}")
        st.write(f"**Date:** {booking['date']}")
        st.write(f"**Time:** {booking['time']}")
        st.write(f"**Name:** {booking['name']}")
        st.write(f"**Email:** {booking['email']}")
        st.write(f"**Phone:** {booking['phone']}")
