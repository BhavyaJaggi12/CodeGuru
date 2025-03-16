import streamlit as st

st.set_page_config(page_title="Home - CODEGURU: YOUR PERSONAL CODING PARTNER", page_icon="🏠")

st.title("🏠 Welcome to the CODEGURU: YOUR PERSONAL CODING PARTNER")
st.subheader("Choose a service to assist you:")

st.markdown("""
### 🔗 Navigation:
- 📄 [Summarize YouTube/Website](./pages/summarize.py)
- 🤖 [Chat with CodeGuru](./pages/chatbot.py)
""")
