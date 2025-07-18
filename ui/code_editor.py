import streamlit as st
from typing import Optional, Callable


class CodeEditor:
    """Component for code input, execution, and analysis."""
    
    def __init__(self, on_run_code: Optional[Callable[[str], None]] = None):
        """
        Initialize the code editor component.
        
        Args:
            on_run_code: Optional callback function to handle code execution
        """
        self.on_run_code = on_run_code
        self.default_code = '''def two_sum(nums, target):
    """
    Given an array of integers nums and an integer target,
    return indices of the two numbers such that they add up to target.
    """
    # Your solution here
    pass

# Test the function
nums = [2, 7, 11, 15]
target = 9
result = two_sum(nums, target)
print(f"Result: {result}")'''
    
    def render(self) -> Optional[str]:
        """
        Render the code editor with run button.
        
        Returns:
            The code to execute if run button was clicked, None otherwise
        """
        # Initialize session state for code
        if "current_code" not in st.session_state:
            st.session_state.current_code = self.default_code
        
        # Code input area (full width) - good readability height
        code = st.text_area(
            "Write your algorithm here:",
            value=st.session_state.current_code,
            height=400,  # Fixed height for better readability
            key="code_editor",
            help="Write your Python code here. Click 'Run & Analyze' to execute and get AI feedback.",
            placeholder="def solution():\n    # Your code here\n    pass"
        )
        
        # Update session state
        st.session_state.current_code = code
        
        # Action buttons row
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            # Check if already processing to prevent double clicks
            if st.session_state.get("processing", False):
                st.button(
                    "⏳ Processing...", 
                    disabled=True,
                    use_container_width=True,
                    help="Code analysis in progress..."
                )
            else:
                if st.button(
                    "▶️ Run & Analyze", 
                    type="primary",
                    use_container_width=True,
                    help="Execute code, analyze complexity, and get AI feedback",
                    key="run_analyze_btn"
                ):
                    if code.strip():
                        # Call the callback if provided
                        if self.on_run_code:
                            self.on_run_code(code.strip())
                        return code.strip()
        
        with col2:
            if st.button("🗑️ Clear", use_container_width=True, help="Clear the editor"):
                st.session_state.current_code = ""
                st.rerun()
        
        with col3:
            if st.button("📝 Example", use_container_width=True, help="Load example"):
                st.session_state.current_code = self.default_code
                st.rerun()
        
        with col4:
            # Template dropdown
            template_options = ["Select Template", "Two Sum", "Binary Search", "DFS", "BFS", "Dynamic Programming"]
            selected_template = st.selectbox(
                "Templates",
                template_options,
                key="code_template_select",
                label_visibility="collapsed"
            )
            
            if selected_template != "Select Template":
                template_code = self._get_template_code(selected_template)
                if template_code:
                    st.session_state.current_code = template_code
                    st.rerun()
        
        return None
    
    def _get_template_code(self, template_name: str) -> str:
        """Get code template by name."""
        templates = {
            "Two Sum": '''def two_sum(nums, target):
    """
    Given an array of integers nums and an integer target,
    return indices of the two numbers such that they add up to target.
    """
    # Your solution here
    pass''',
            
            "Binary Search": '''def binary_search(arr, target):
    """
    Search for target in a sorted array.
    Returns the index if found, -1 otherwise.
    """
    # Your solution here
    pass''',
            
            "DFS": '''def dfs(graph, start, visited=None):
    """
    Perform depth-first search on a graph.
    """
    if visited is None:
        visited = set()
    
    # Your solution here
    pass''',
            
            "BFS": '''from collections import deque

def bfs(graph, start):
    """
    Perform breadth-first search on a graph.
    """
    visited = set()
    queue = deque([start])
    
    # Your solution here
    pass''',
            
            "Dynamic Programming": '''def fibonacci(n):
    """
    Calculate the nth Fibonacci number using dynamic programming.
    """
    # Your solution here
    pass'''
        }
        
        return templates.get(template_name, "")
    
    def set_code(self, code: str) -> None:
        """
        Set the code in the editor.
        
        Args:
            code: The code to set in the editor
        """
        st.session_state.current_code = code
    
    def get_code(self) -> str:
        """
        Get the current code from the editor.
        
        Returns:
            The current code in the editor
        """
        return st.session_state.get("current_code", "")
    
    def render_results_area(self) -> None:
        """Render an area to show code execution results."""
        if "last_code_result" in st.session_state:
            st.subheader("📊 Execution Results")
            
            result = st.session_state.last_code_result
            
            # Show execution output
            if "output" in result:
                st.markdown("**Output:**")
                st.code(result["output"], language="text")
            
            # Show any errors
            if "error" in result:
                st.error(f"Error: {result['error']}")
            
            # Show complexity analysis
            if "complexity" in result:
                st.markdown("**Complexity Analysis:**")
                st.info(result["complexity"])
            
            # Show test cases
            if "test_cases" in result:
                st.markdown("**Generated Test Cases:**")
                st.json(result["test_cases"])
