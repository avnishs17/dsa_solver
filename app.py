import streamlit as st
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# Import application components
from config.settings import get_settings
from models.llm import get_llm
from graph.graph_builder import build_state_graph
from tools.tools_registry import get_all_tools
from ui.sidebar import Sidebar
from ui.chat_display import ChatDisplay
from ui.chat_input import ChatInput
from ui.code_editor import CodeEditor


class DSASolverApp:
    """Main DSA Solver application class."""
    
    def __init__(self):
        """Initialize the DSA Solver application."""
        self.settings = get_settings()
        self.llm_service = get_llm()
        self.tools = get_all_tools()
        self.app = build_state_graph(self.tools)
        
        # Initialize UI components
        self.sidebar = Sidebar(self.settings)
        self.chat_display = ChatDisplay()
        self.chat_input = ChatInput(on_submit=self.handle_user_input)
        self.code_editor = CodeEditor(on_run_code=self.handle_code_execution)
        
        # Initialize session state
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize session state variables."""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        if "current_thread_id" not in st.session_state:
            st.session_state.current_thread_id = "default"
        
        if "app_state" not in st.session_state:
            st.session_state.app_state = {"messages": []}
        
        if "processing" not in st.session_state:
            st.session_state.processing = False
        
        if "last_execution_time" not in st.session_state:
            st.session_state.last_execution_time = 0
    
    def handle_user_input(self, user_message: str):
        """Handle user input and process through the LangGraph app."""
        if st.session_state.processing:
            return
        
        try:
            st.session_state.processing = True
            
            # Debug output
            print(f"🔍 Processing message: '{user_message}'")
            print(f"📊 Current messages count: {len(st.session_state.messages)}")
            
            # Add user message to session state first (with timestamp)
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state.messages.append({
                "role": "user",
                "content": user_message,
                "timestamp": timestamp
            })
            
            # Create HumanMessage for LangGraph
            human_message = HumanMessage(content=user_message)
            
            # Update app state with new message
            st.session_state.app_state["messages"].append(human_message)
            
            # Store the count of messages before processing to identify new ones
            messages_before_count = len(st.session_state.app_state["messages"])
            print(f"📝 LangGraph messages before: {messages_before_count}")
            
            # Show thinking indicator
            with st.spinner("🤔 Thinking..."):
                # Process the message through the LangGraph app
                result = self.app.invoke(
                    st.session_state.app_state,
                    config={"configurable": {"thread_id": st.session_state.current_thread_id}}
                )
                
                print(f"🧠 LangGraph result messages: {len(result.get('messages', []))}")
                
                # Extract only the NEW assistant's response and tool calls
                if "messages" in result and len(result["messages"]) > messages_before_count:
                    # Get only the new messages after our input
                    new_messages = result["messages"][messages_before_count:]
                    print(f"🆕 New messages from LangGraph: {len(new_messages)}")
                    
                    for message in new_messages:
                        print(f"🔍 Processing message type: {type(message)}")
                        print(f"🔍 Message content preview: {getattr(message, 'content', 'No content')[:100]}...")
                        
                        if isinstance(message, AIMessage):
                            print(f"📝 AI Message found with content: {bool(message.content)}")
                            print(f"📝 AI Message has tool calls: {bool(hasattr(message, 'tool_calls') and message.tool_calls)}")
                            
                            # Check if this message has tool calls
                            if hasattr(message, 'tool_calls') and message.tool_calls:
                                for tool_call in message.tool_calls:
                                    tool_name = tool_call.get('name', 'Unknown Tool')
                                    
                                    # Map internal tool names to user-friendly names
                                    tool_display_names = {
                                        'python_repl': 'Code Executor',
                                        'generate_hint': 'Hint Generator',
                                        'complexity_analyzer': 'Complexity Analyzer',
                                        'generate_test_cases': 'Test Case Generator',
                                        'persistent_python_repl': 'Code Executor'
                                    }
                                    
                                    display_name = tool_display_names.get(tool_name, tool_name)
                                    
                                    # Add a tool usage indicator to the chat
                                    tool_timestamp = datetime.now().strftime("%H:%M:%S")
                                    st.session_state.messages.append({
                                        "role": "system",
                                        "content": f"🔧 Using {display_name}...",
                                        "timestamp": tool_timestamp
                                    })
                                    print(f"🔧 Tool used: {tool_name} (displayed as: {display_name})")
                            
                            # Add the actual AI response if it has content
                            if message.content:
                                print(f"✅ Adding AI response: '{message.content[:50]}...'")
                                # Add assistant response to session state
                                assistant_timestamp = datetime.now().strftime("%H:%M:%S")
                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": message.content,
                                    "timestamp": assistant_timestamp
                                })
                            else:
                                print("⚠️ AI Message has no content to display")
                        
                        elif isinstance(message, ToolMessage):
                            # This is the result of a tool call - let the LLM handle the display
                            tool_name = getattr(message, 'name', 'Tool')
                            print(f"🔧 ToolMessage: {tool_name}")
                            print(f"🔧 ToolMessage content length: {len(message.content) if message.content else 0}")
                            print(f"🔧 ToolMessage content preview: {message.content[:200] if message.content else 'None'}...")
                            
                            # Don't display tool results directly - the assistant will synthesize them
                            print("🔧 Tool result received, letting LLM synthesize...")
                            
                    # Update app state with the complete result
                    st.session_state.app_state = result
                else:
                    print("⚠️ No new messages received from LangGraph")
        
        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            st.error(error_msg)
            # Add error message to chat
            error_timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Sorry, I encountered an error: {str(e)}",
                "timestamp": error_timestamp
            })
        
        finally:
            st.session_state.processing = False
            # Force UI update after processing is complete
            st.rerun()
    
    def handle_code_execution(self, code: str):
        """Handle code execution and analysis."""
        if st.session_state.processing:
            return
        
        # Debounce rapid clicks (prevent double execution within 2 seconds)
        current_time = datetime.now().timestamp()
        if current_time - st.session_state.get("last_execution_time", 0) < 2:
            return
        
        st.session_state.last_execution_time = current_time
        
        try:
            # Simple, clean message for code analysis
            analysis_message = f"""
I'd like you to analyze this code:

```python
{code}
```

Please execute it and provide feedback on the implementation. If you notice any issues or if it runs successfully, let me know about the approach and any suggestions for improvement.
"""
            
            # Process through the regular chat flow (don't add duplicate user message)
            self.handle_user_input(analysis_message)
            
        except Exception as e:
            st.error(f"Error executing code: {str(e)}")
            st.session_state.processing = False
    
    def render(self):
        """Render the main application interface."""
        # Render sidebar
        self.sidebar.render()
        
        # Main title (compact)
        st.title("🧮 DSA Solver")
        
        # Create side-by-side layout: Code Editor (left) | Chat Mentor (right)
        col1, col2 = st.columns([1.2, 1])
        
        with col1:
            # Code editor interface  
            self._render_code_interface()
        
        with col2:
            # Chat mentor interface
            self._render_chat_interface()
    
    def _render_chat_interface(self):
        """Render the chat interface."""
        # Chat area
        st.subheader("🤖 DSA Mentor")
        
        # Display chat messages in a more compact container
        if st.session_state.get("debug_mode", False):
            st.write(f"Debug: Total messages in session: {len(st.session_state.messages)}")
        
        # Chat container that grows with content
        self.chat_display.render_messages(st.session_state.messages)
        
        # Use the dedicated ChatInput component instead of duplicating logic
        self.chat_input.set_placeholder("Ask about algorithms, get hints...")
        self.chat_input.render()
        
        # Only 2 compact example prompts when no messages
        if not st.session_state.get("messages", []):
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💡 Get hints", key="example_hints", use_container_width=True):
                    self.handle_user_input("Can you give me a hint?")
                    st.rerun()
            with col2:
                if st.button("📊 Analyze complexity", key="example_complexity", use_container_width=True):
                    self.handle_user_input("What's the time complexity?")
                    st.rerun()
    
    def _render_code_interface(self):
        """Render the code editor interface."""
        # Code editor
        st.subheader("📝 Code Editor")
        st.markdown("*Write, test, and analyze your algorithms*")
        
        # Always render the editor, but control execution
        code_to_run = self.code_editor.render()
        
        # Only handle execution if not already processing and we have code to run
        if code_to_run and not st.session_state.get("processing", False):
            self.handle_code_execution(code_to_run)


def main():
    """Main application entry point."""
    # Set page configuration FIRST - before any other Streamlit commands
    st.set_page_config(
        page_title="DSA Solver",
        page_icon="🧮",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    app = DSASolverApp()
    app.render()


if __name__ == "__main__":
    main()
