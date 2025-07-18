import streamlit as st
from typing import List, Dict, Any
from datetime import datetime


class ChatDisplay:
    """Component for displaying chat messages with proper styling."""
    
    def __init__(self):
        """Initialize the chat display component."""
        self.user_avatar = "👤"
        self.assistant_avatar = "🤖"
        
    def render_messages(self, messages: List[Dict[str, Any]]) -> None:
        """
        Render a list of chat messages with proper styling.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
        """
        if not messages:
            self._render_empty_state()
            return
            
        for message in messages:
            self._render_message(message)
    
    def _render_empty_state(self) -> None:
        """Render the empty chat state."""
        st.info("💬 Start a conversation by typing a message below!")
        
    def _render_message(self, message: Dict[str, Any]) -> None:
        """
        Render a single message with proper styling.
        
        Args:
            message: Message dictionary with 'role' and 'content'
        """
        role = message.get("role", "user")
        content = message.get("content", "")
        timestamp = message.get("timestamp", datetime.now().strftime("%H:%M"))
        
        if role == "user":
            self._render_user_message(content, timestamp)
        elif role == "assistant":
            self._render_assistant_message(content, timestamp)
        else:
            self._render_system_message(content, timestamp)
    
    def _render_user_message(self, content: str, timestamp: str) -> None:
        """Render a user message."""
        st.markdown(
            f"""
            <div style="
                display: flex;
                justify-content: flex-end;
                margin: 12px 0;
            ">
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 12px 16px;
                    border-radius: 18px;
                    max-width: 70%;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                ">
                    <div style="font-size: 14px; line-height: 1.4;">{content}</div>
                    <div style="font-size: 11px; opacity: 0.7; margin-top: 4px; text-align: right;">{timestamp}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    def _render_assistant_message(self, content: str, timestamp: str) -> None:
        """Render an assistant message."""
        # Handle both string and list content types
        if isinstance(content, list):
            content = "\n".join(str(item) for item in content)
        elif not isinstance(content, str):
            content = str(content)
        
        # Check if this is a complexity analysis or structured output
        if "complexity" in content.lower() or "time complexity" in content.lower():
            self._render_structured_message(content, timestamp, "📊 Complexity Analysis")
        else:
            st.markdown(
                f"""
                <div style="
                    display: flex;
                    justify-content: flex-start;
                    margin: 12px 0;
                ">
                    <div style="
                        background-color: #f8f9fa;
                        color: #212529;
                        padding: 12px 16px;
                        border-radius: 18px;
                        max-width: 70%;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                        border: 1px solid #e9ecef;
                    ">
                        <div style="display: flex; align-items: center; margin-bottom: 8px;">
                            <span style="font-size: 16px; margin-right: 8px;">{self.assistant_avatar}</span>
                            <span style="font-weight: 600; color: #495057;">Assistant</span>
                        </div>
                        <div style="font-size: 14px; line-height: 1.5;">{content}</div>
                        <div style="font-size: 11px; color: #6c757d; margin-top: 4px;">{timestamp}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    def _render_structured_message(self, content: str, timestamp: str, title: str) -> None:
        """Render a structured message like complexity analysis with proper formatting."""
        # Format content for better display
        formatted_content = self._format_analysis_content(content)
        
        st.markdown(
            f"""
            <div style="
                display: flex;
                justify-content: flex-start;
                margin: 12px 0;
            ">
                <div style="
                    background-color: #f8f9fa;
                    color: #212529;
                    padding: 16px;
                    border-radius: 12px;
                    max-width: 85%;
                    box-shadow: 0 3px 12px rgba(0,0,0,0.1);
                    border: 1px solid #e9ecef;
                    border-left: 4px solid #007bff;
                ">
                    <div style="display: flex; align-items: center; margin-bottom: 12px;">
                        <span style="font-size: 16px; margin-right: 8px;">{self.assistant_avatar}</span>
                        <span style="font-weight: 600; color: #495057;">{title}</span>
                    </div>
                    <div style="font-size: 14px; line-height: 1.6;">{formatted_content}</div>
                    <div style="font-size: 11px; color: #6c757d; margin-top: 8px;">{timestamp}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    def _format_analysis_content(self, content: str) -> str:
        """Format analysis content for better readability."""
        import re
        import html
        
        # Ensure content is a string
        if isinstance(content, list):
            content = "\n".join(str(item) for item in content)
        elif not isinstance(content, str):
            content = str(content)
        
        # Escape HTML to prevent rendering issues
        content = html.escape(content)
        
        # Convert markdown-style headers to HTML
        content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
        
        # Format bullet points
        content = re.sub(r'^- ', r'• ', content, flags=re.MULTILINE)
        content = re.sub(r'^(\d+)\.\s', r'• ', content, flags=re.MULTILINE)
        
        # Format O() notation with highlighting
        content = re.sub(r'O\(([^)]+)\)', r'<span style="background-color: #e3f2fd; padding: 2px 4px; border-radius: 3px; font-family: monospace; color: #1976d2;"><strong>O(\1)</strong></span>', content)
        
        # Format code blocks
        content = re.sub(r'```(.*?)```', r'<div style="background-color: #f5f5f5; padding: 8px; border-radius: 4px; margin: 4px 0; font-family: monospace; border-left: 3px solid #2196f3;">\1</div>', content, flags=re.DOTALL)
        
        # Add line breaks for better spacing
        content = re.sub(r'\n', '<br>', content)
        
        return content.strip()
    
    def _render_system_message(self, content: str, timestamp: str) -> None:
        """Render a system message."""
        # Different styling for tool usage messages
        if "🔧" in content or "✅" in content and "tool" in content.lower():
            # Tool usage message
            bg_color = "#e8f5e8"
            border_color = "#4caf50"
            icon = "🛠️"
        else:
            # Regular system message
            bg_color = "#fff3e0"
            border_color = "#ff9800"
            icon = "⚡"
            
        st.markdown(
            f"""
            <div style="
                background-color: {bg_color};
                padding: 8px 12px;
                border-radius: 8px;
                margin: 8px 0;
                border-left: 4px solid {border_color};
                text-align: center;
                font-style: italic;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            ">
                <div style="color: #555; font-size: 0.85em; font-weight: 500;">
                    {icon} {content} <span style="font-size: 0.75em; opacity: 0.7;">({timestamp})</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    def render_typing_indicator(self) -> None:
        """Render a typing indicator for the assistant."""
        st.markdown(
            f"""
            <div style="
                background-color: #f3e5f5;
                padding: 10px;
                border-radius: 10px;
                margin: 5px 0;
                border-left: 4px solid #7b1fa2;
            ">
                <div style="font-weight: bold; color: #7b1fa2; margin-bottom: 5px;">
                    {self.assistant_avatar} Assistant
                </div>
                <div style="color: #666; font-style: italic;">
                    <span class="typing-dots">Typing...</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    def render_error_message(self, error_msg: str) -> None:
        """Render an error message."""
        st.error(f"❌ Error: {error_msg}")
    
    def render_success_message(self, success_msg: str) -> None:
        """Render a success message."""
        st.success(f"✅ {success_msg}")
