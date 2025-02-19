import streamlit as st
import PyPDF2
from openai import OpenAI

def pdf_interface():
    # Initialize OpenAI client
    client = OpenAI()

    # Initialize session state for PDF text and chat history
    if "pdf_text" not in st.session_state:
        st.session_state["pdf_text"] = ""
    if "pdf_chat_history" not in st.session_state:
        st.session_state["pdf_chat_history"] = []

    st.title("📄 Prescription Files")
    
    # PDF File Upload
    uploaded_file = st.file_uploader("Upload Prescription", type="pdf")

    if uploaded_file:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
        st.session_state["pdf_text"] = pdf_text
        st.write(f"Extracted Text:\n{pdf_text}")

    # Ask questions about the PDF
    pdf_question = st.text_input("Ask something related to the Prescription:")
    if st.button("Ask about Prescription"):
        if pdf_question:
            st.session_state["pdf_chat_history"].append({"role": "user", "content": pdf_question})

            # Call OpenAI API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Here is the content of the PDF: {st.session_state['pdf_text']}"},
                    *st.session_state["pdf_chat_history"]
                ]
            )
            
            # Add assistant's reply to chat history
            reply = response.choices[0].message.content
            st.session_state["pdf_chat_history"].append({"role": "assistant", "content": reply})

    # Display PDF chat history
    for message in st.session_state["pdf_chat_history"]:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        else:
            st.write(f"**Assistant:** {message['content']}")

    # Clear PDF Chat Button
    if st.button("Clear Prescription Chat"):
        st.session_state["pdf_chat_history"] = []