
import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import wave
import io
import base64

def chat_bot():
    # Load environment variables
    load_dotenv()

    # Set up Gemini API key from environment variable
    genai.configure(api_key=os.getenv("API_KEY"))

    st.title("Health Care ChatBot")
    # 🩺
    USER_AVATAR = "👤"
    BOT_AVATAR = "🧑🏻‍⚕️"

    # Initialize or load chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Sidebar with a button to delete chat history
    with st.sidebar:
        if st.button("Delete Chat History"):
            st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Function to call the Gemini API
    def get_gemini_response(prompt):
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.candidates[0].content.parts[0].text

    # Function to record audio in Python
    def record_audio(duration=3, sample_rate=44100):
        import sounddevice as sd
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()  # Wait until recording is finished
        return audio_data

    # Function to convert recorded audio to text using SpeechRecognition
    def audio_to_text(audio_data):
        # Convert numpy array audio to a WAV format in-memory buffer
        audio_io = io.BytesIO()
        wav_file = wave.open(audio_io, 'wb')
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(44100)
        wav_file.writeframes(audio_data)
        wav_file.close()
        audio_io.seek(0)

        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_io) as source:
            audio_content = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_content)
            return text
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand the audio.")
            return None
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service; {e}")
            return None

    # Microphone button to trigger audio recording
    if st.button("🎤 Record Voice"):
        st.write("Recording...")
        audio_data = record_audio()
        st.write("Recording complete.")
        
        # Convert the audio to text
        text_input = audio_to_text(audio_data)
        
        if text_input:
            # Append user input to chat
            st.session_state.messages.append({"role": "user", "content": text_input})
            
            # Display the user input message
            with st.chat_message("user", avatar=USER_AVATAR):
                st.markdown(text_input)

            # Call Gemini API for assistant response
            with st.chat_message("assistant", avatar=BOT_AVATAR):
                message_placeholder = st.empty()
                full_response = get_gemini_response(text_input)
                message_placeholder.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response})


    # Allow users to input text via text box
    if prompt := st.chat_input("How can I help?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(prompt)

        # Call Gemini API for assistant response
        with st.chat_message("assistant", avatar=BOT_AVATAR):
            message_placeholder = st.empty()
            full_response = get_gemini_response(prompt)
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
