import streamlit as st
from typing import Optional, Callable


class ChatInput:
    """Component for handling user input and message submission."""
    
    def __init__(self, on_submit: Optional[Callable[[str], None]] = None):
        """
        Initialize the chat input component.
        
        Args:
            on_submit: Optional callback function to handle message submission
        """
        self.on_submit = on_submit
        self.placeholder_text = "Type your message here..."
        
    def render(self) -> Optional[str]:
        """
        Render the chat input component.
        
        Returns:
            The submitted message if any, None otherwise
        """
        # Initialize session state if needed
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Create input form
        with st.form(key="chat_input_form", clear_on_submit=True):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                user_input = st.text_input(
                    "Your message:", 
                    placeholder=self.placeholder_text,
                    key="user_message_input",
                    label_visibility="collapsed"
                )
            
            with col2:
                submit_button = st.form_submit_button(
                    "Send", 
                    type="primary",
                    use_container_width=True
                )
        
        # Handle submission
        if submit_button and user_input.strip():
            message = user_input.strip()
            
            # Call the callback if provided
            if self.on_submit:
                self.on_submit(message)
                # Let the parent component handle rerun
            
            return message
        
        return None
    
    def render_with_examples(self, examples: list = None) -> Optional[str]:
        """
        Render the chat input with example prompts.
        
        Args:
            examples: List of example prompts to display
            
        Returns:
            The submitted message if any, None otherwise
        """
        if examples is None:
            examples = [
                "Help me solve a two-sum problem",
                "Explain binary search approach", 
                "How do I optimize this recursive solution?",
                "Generate test cases for my algorithm"
            ]
        
        # Display examples with better styling
        if not st.session_state.get("messages", []):
            st.markdown("<h4 style='margin-bottom: 10px;'>💡 Try these examples:</h4>", unsafe_allow_html=True)
            
            # Use 2x2 grid for better layout
            col1, col2 = st.columns(2)
            for i, example in enumerate(examples):
                with col1 if i % 2 == 0 else col2:
                    if st.button(example, key=f"example_{i}", use_container_width=True):
                        # Call callback if provided (don't add to session state here)
                        if self.on_submit:
                            self.on_submit(example)
                        
                        return example
        
        # Render normal input
        return self.render()
    
    def set_placeholder(self, placeholder: str) -> None:
        """
        Set the placeholder text for the input field.
        
        Args:
            placeholder: The placeholder text to display
        """
        self.placeholder_text = placeholder
    
    def clear_input(self) -> None:
        """
        Clear the input field (for programmatic clearing).
        """
        if "user_message_input" in st.session_state:
            st.session_state.user_message_input = ""
    
    def render_quick_actions(self) -> Optional[str]:
        """
        Render quick action buttons for common operations.
        
        Returns:
            The action taken if any, None otherwise
        """
        st.markdown("<h4 style='margin-bottom: 10px;'>🚀 Quick Actions:</h4>", unsafe_allow_html=True)
        
        # Add custom CSS for better button styling
        st.markdown("""
        <style>
        .stButton > button {
            width: 100%;
            height: 48px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 8px;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .stButton > button:active {
            transform: translateY(0);
        }
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("❓ Get Help", key="quick_help", use_container_width=True):
                return "help"
            if st.button("� Practice Problem", key="quick_practice", use_container_width=True):
                return "practice"
        
        with col2:
            if st.button("💡 Explain More", key="quick_explain", use_container_width=True):
                return "explain"
            if st.button("� Debug Help", key="quick_debug", use_container_width=True):
                return "debug"
        
        return None

