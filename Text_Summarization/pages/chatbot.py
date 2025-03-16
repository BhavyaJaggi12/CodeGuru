import requests
import json
import streamlit as st

# API Endpoint
URL = "http://localhost:11434/api/generate"
HEADERS = {'Content-Type': 'application/json'}

# Initialize session state for chat history
if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🤖 CodeGuru Chatbot")
st.subheader("Powered by Streamlit")

# User Input
user_input = st.text_area("Enter your Prompt", height=150)

if st.button("Generate Response"):
    if user_input.strip():
        st.session_state.history.append(user_input)
        final_prompt = "\n".join(st.session_state.history)

        data = {
            "model": "codeguru",
            "prompt": final_prompt,
            "stream": False
        }

        response = requests.post(URL, headers=HEADERS, data=json.dumps(data))

        if response.status_code == 200:
            response_json = response.json()
            actual_response = response_json.get('response', 'No response received.')
            st.session_state.history.append(actual_response)  # Append response to history
            st.success(actual_response)
        else:
            st.error(f"Error: {response.text}")
    else:
        st.warning("Please enter a prompt before submitting.")

# Display chat history
if st.session_state.history:
    st.subheader("Chat History")
    for i, entry in enumerate(st.session_state.history):
        if i % 2 == 0:
            st.write(f"**You:** {entry}")
        else:
            st.write(f"**CodeGuru:** {entry}")
