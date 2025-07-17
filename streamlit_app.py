import streamlit as st
import requests
import json
import uuid

# --- Page Configuration ---
st.set_page_config(
    page_title="DSA Mentor",
    page_icon="🤖",
    layout="wide"
)

# --- API Endpoint ---
# Make sure your FastAPI server is running at this address
API_ENDPOINT = "http://localhost:8000/chat/stream"

# --- Helper Functions ---
def get_session_id():
    """Get or create a unique session ID."""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    return st.session_state.session_id

def send_message_and_get_response(message: str, thread_id: str):
    """Send a message to the API and stream the response."""
    try:
        payload = {"content": message, "session_id": thread_id}
        with requests.post(API_ENDPOINT, json=payload, stream=True) as r:
            r.raise_for_status()
            
            full_response = ""
            assistant_message_placeholder = st.chat_message("assistant").empty()

            for line in r.iter_lines():
                if line:
                    # Decode the line and strip the "data: " prefix
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith('data: '):
                        json_str = decoded_line[len('data: '):]
                        try:
                            response_data = json.loads(json_str)
                            
                            if response_data.get("type") == "chunk":
                                full_response += response_data.get("content", "")
                                assistant_message_placeholder.markdown(full_response + "▌")
                            
                            elif response_data.get("type") in ["tool_start", "tool_end"]:
                                # Tool interactions are handled by the assistant's response, not shown directly.
                                pass

                            elif response_data.get("error"):
                                st.error(f"An error occurred: {response_data['error']}")
                                break
                        except json.JSONDecodeError:
                            st.error(f"Failed to decode JSON from stream: {json_str}")

            # Update the placeholder with the final response
            assistant_message_placeholder.markdown(full_response)
            
            # Add the final assistant message to history
            if full_response:
                st.session_state.messages.append({"role": "assistant", "content": full_response})

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to the DSA Mentor. Please ensure the backend is running. Error: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# --- Main Application ---
st.title("🤖 DSA Mentor Chat")
st.caption("Your personal AI-powered guide to mastering Data Structures and Algorithms.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("Ask me about any DSA problem..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get session ID
    thread_id = get_session_id()
    
    # Send message and get response from backend
    send_message_and_get_response(prompt, thread_id)
