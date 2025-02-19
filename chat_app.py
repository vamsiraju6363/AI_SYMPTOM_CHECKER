import streamlit as st
from openai import OpenAI
import os

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv())
# Function to check if the response is related to the medical field
def is_medical_related(response):
    medical_keywords = ["patient", "treatment", "medicine", "health", "diagnosis", "hospital", "doctor", "therapy", "medical"]
    return any(keyword in response.lower() for keyword in medical_keywords)

# Function to generate specific, meaningful suggestions based on assistant reply
def generate_suggestions(assistant_reply):
    if is_medical_related(assistant_reply):
        prompt = f"Based on the following assistant response, suggest three relevant actions or recommendations related to patient care, medical treatments, healthcare management, or improving health outcomes that the user could take, which are closely related to the context of the response and useful for the user.\n\nResponse: {assistant_reply}\n\nSuggestions (be specific and relevant to the context):"
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": prompt}],
                max_tokens=200,
                n=1,
                temperature=0.7
            )
            
            suggestions_text = response.choices[0].message.content.strip()
            suggestions = suggestions_text.split("\n")
            return [s.strip() for s in suggestions if s.strip()]
        except Exception as e:
            st.error(f"Error generating suggestions: {str(e)}")
            return ["Unable to generate suggestions at this time."]
    else:
        return ["The response is not related to medical or health topics."]

def chat_interface():
    # Add custom CSS for styling "You" and "Assistant" labels in different colors
    st.markdown("""
        <style>
        .assistant {
            color: #00695c; /* Teal color for Assistant */
            font-weight: bold;
        }
        .user {
            color: #d32f2f; /* Red color for You */
            font-weight: bold;
        }
        .output-box {
            padding: 10px;
            margin-bottom: 10px;
            background-color: #f0f0f0;
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Doctor profiles dropdown
    doctor_options = {
        "Dr. A - Cardiologist": "Dr. A",
        "Dr. B - General Practitioner": "Dr. B",
        "Dr. C - Pediatrician": "Dr. C"
    }
    
    selected_doctor = st.selectbox("Select a Doctor", options=list(doctor_options.keys()))
    st.write(f"**Selected Doctor:** {doctor_options[selected_doctor]}")
    
    doctor_id = doctor_options[selected_doctor]

    # Initialize session state for chats for each doctor
    if "chat_sessions" not in st.session_state:
        st.session_state["chat_sessions"] = {}

    if doctor_id not in st.session_state["chat_sessions"]:
        st.session_state["chat_sessions"][doctor_id] = {}  # Initialize empty dict for this doctor

    # Handle new chat creation
    chat_name = st.text_input("Enter Chat Name", key="new_chat_name")
    if st.button("➕ New Chat"):
        if chat_name and chat_name not in st.session_state["chat_sessions"][doctor_id]:
            st.session_state["chat_sessions"][doctor_id][chat_name] = []

    # Select chat to load (chats specific to the selected doctor)
    chat_selection = st.selectbox(
        "Select a Chat", 
        options=list(st.session_state["chat_sessions"][doctor_id].keys())
    )

    if chat_selection:
        st.write(f"**Chat: {chat_selection}**")
        chat_history = st.session_state["chat_sessions"][doctor_id][chat_selection]

        # Input field for user messages or clicked suggestion
        if st.session_state.get("selected_suggestion"):
            # If a suggestion was clicked, use it as the input
            user_input = st.session_state["selected_suggestion"]
            st.session_state["selected_suggestion"] = ""  # Reset after using
        else:
            # Normal input field for the user
            user_input = st.text_input("Type your message here:", key="user_input")

        # Send message if user clicks 'Send' or suggestion is clicked
        if st.button("Send") and user_input:
            # Append user input to chat history
            chat_history.append({"role": "user", "content": user_input})

            try:
                # Call OpenAI API to get assistant's reply
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=chat_history
                )

                # Add assistant's reply to chat history only if it is medically relevant
                reply = response.choices[0].message.content

                if is_medical_related(reply):
                    chat_history.append({"role": "assistant", "content": reply})
                else:
                    chat_history.append({"role": "assistant", "content": "The response is not related to medical or health topics."})

                # Generate suggestions based on assistant's reply
                suggestions = generate_suggestions(reply)

                # Display suggestions
                st.write("**Suggestions:**")
                for suggestion in suggestions:
                    if st.button(suggestion, key=suggestion):
                        # When a suggestion is clicked, set it to session state and trigger rerun
                        st.session_state["selected_suggestion"] = suggestion
                        st.experimental_rerun()

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

        # Display chat history with the most recent message on top
        for message in reversed(chat_history):
            if message["role"] == "user":
                st.markdown(f'<div class="output-box"><span class="user">You:</span> {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="output-box"><span class="assistant">Assistant:</span> {message["content"]}</div>', unsafe_allow_html=True)

        # Clear chat button
        if st.button("Clear Chat"):
            st.session_state["chat_sessions"][doctor_id][chat_selection] = []

        # Delete chat button
        if st.button("❌ Delete Chat"):
            del st.session_state["chat_sessions"][doctor_id][chat_selection]
            st.experimental_rerun()  # Rerun to refresh the state after deletion

# Run the chat interface
if __name__ == "__main__":
    chat_interface()