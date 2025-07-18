import streamlit as st
from typing import Dict, Any, Optional
from config.settings import Settings


class Sidebar:
    """Sidebar component for application settings and configuration."""
    
    def __init__(self, settings: Settings):
        """
        Initialize the sidebar component.
        
        Args:
            settings: Application settings instance
        """
        self.settings = settings
    
    def render(self) -> Dict[str, Any]:
        """
        Render the sidebar with UI configuration options only.
        
        Returns:
            Dictionary containing the current configuration values
        """
        st.sidebar.title("⚙️ Settings")
        
        # Display backend configuration (read-only)
        self._render_backend_info()
        
        # Chat UI Settings
        self._render_chat_section()
        
        # Thread Management Section
        self._render_thread_section()
        
        # Advanced UI Settings Section
        self._render_advanced_section()
        
        # Export current settings
        return self._export_settings()
    
    def _render_backend_info(self) -> None:
        """Render backend configuration info (read-only)."""
        st.sidebar.subheader("🔧 Backend Configuration")
        
        # Display current backend settings (read-only)
        with st.sidebar.container():
            st.markdown("**Provider:** Google Gemini")
            st.markdown(f"**Model:** {self.settings.model_name}")
            st.markdown(f"**App:** {self.settings.app_title}")
            
            # Show API key status (without revealing the key)
            if hasattr(self.settings, 'google_api_key') and self.settings.google_api_key:
                st.markdown("**API Key:** ✅ Configured")
            else:
                st.markdown("**API Key:** ❌ Not configured")
    
    def _render_chat_section(self) -> None:
        """Render chat configuration section."""
        st.sidebar.subheader("💬 Chat Settings")
        
        # Auto-scroll
        auto_scroll = st.sidebar.checkbox(
            "Auto-scroll to bottom",
            value=True,
            help="Automatically scroll to the latest message"
        )
        
        # Show timestamps
        show_timestamps = st.sidebar.checkbox(
            "Show timestamps",
            value=True,
            help="Display timestamps for each message"
        )
        
        # Message limit
        message_limit = st.sidebar.number_input(
            "Message History Limit",
            min_value=10,
            max_value=1000,
            value=100,
            step=10,
            help="Maximum number of messages to keep in history"
        )
        
        # Store chat settings
        st.session_state.auto_scroll = auto_scroll
        st.session_state.show_timestamps = show_timestamps
        st.session_state.message_limit = message_limit
    
    def _render_thread_section(self) -> None:
        """Render thread management section."""
        st.sidebar.subheader("🧵 Thread Management")
        
        # Current thread info
        current_thread = st.session_state.get("current_thread_id", "default")
        st.sidebar.info(f"Current Thread: {current_thread}")
        
        # Thread actions
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            if st.button("🆕 New Thread", help="Start a new conversation thread"):
                self._create_new_thread()
        
        with col2:
            if st.button("🗑️ Clear Chat", help="Clear current conversation"):
                self._clear_current_chat()
        
        # Thread list (if available)
        if "thread_list" in st.session_state and st.session_state.thread_list:
            selected_thread = st.sidebar.selectbox(
                "Switch Thread",
                options=st.session_state.thread_list,
                help="Switch to a different conversation thread"
            )
            
            if selected_thread != current_thread:
                self._switch_thread(selected_thread)
    
    def _render_advanced_section(self) -> None:
        """Render advanced settings section."""
        with st.sidebar.expander("🔧 Advanced Settings"):
            # Streaming
            enable_streaming = st.checkbox(
                "Enable Streaming",
                value=True,
                help="Stream responses as they are generated"
            )
            
            # Debug mode
            debug_mode = st.checkbox(
                "Debug Mode",
                value=False,
                help="Show debug information and logs"
            )
            
            # System prompt override
            system_prompt = st.text_area(
                "System Prompt Override",
                placeholder="Enter custom system prompt...",
                height=100,
                help="Override the default system prompt"
            )
            
            # Store advanced settings
            st.session_state.enable_streaming = enable_streaming
            st.session_state.debug_mode = debug_mode
            if system_prompt:
                st.session_state.system_prompt_override = system_prompt
    
    def _create_new_thread(self) -> None:
        """Create a new conversation thread."""
        import uuid
        new_thread_id = str(uuid.uuid4())[:8]
        st.session_state.current_thread_id = new_thread_id
        st.session_state.messages = []
        
        # Add to thread list
        if "thread_list" not in st.session_state:
            st.session_state.thread_list = []
        
        if new_thread_id not in st.session_state.thread_list:
            st.session_state.thread_list.append(new_thread_id)
        
        st.success(f"Created new thread: {new_thread_id}")
        st.rerun()
    
    def _clear_current_chat(self) -> None:
        """Clear the current conversation."""
        st.session_state.messages = []
        st.success("Chat cleared!")
        st.rerun()
    
    def _switch_thread(self, thread_id: str) -> None:
        """Switch to a different thread."""
        st.session_state.current_thread_id = thread_id
        # Load thread messages (implement as needed)
        st.session_state.messages = []
        st.success(f"Switched to thread: {thread_id}")
        st.rerun()
    
    def _export_settings(self) -> Dict[str, Any]:
        """Export current UI settings as a dictionary."""
        return {
            "auto_scroll": st.session_state.get("auto_scroll", True),
            "show_timestamps": st.session_state.get("show_timestamps", True),
            "message_limit": st.session_state.get("message_limit", 100),
            "enable_streaming": st.session_state.get("enable_streaming", True),
            "debug_mode": st.session_state.get("debug_mode", False),
            "current_thread_id": st.session_state.get("current_thread_id", "default"),
        }
    
    def render_model_status(self) -> None:
        """Render model status indicator using backend configuration."""
        status_color = "🟢"
        st.sidebar.markdown(f"{status_color} **Google Gemini** - {self.settings.model_name}")
    
    def render_usage_stats(self) -> None:
        """Render usage statistics."""
        if st.session_state.get("debug_mode", False):
            with st.sidebar.expander("📊 Usage Stats"):
                messages_count = len(st.session_state.get("messages", []))
                st.metric("Messages", messages_count)
                
                tokens_used = st.session_state.get("total_tokens_used", 0)
                st.metric("Tokens Used", tokens_used)
                
                current_thread = st.session_state.get("current_thread_id", "default")
                st.metric("Current Thread", current_thread)
