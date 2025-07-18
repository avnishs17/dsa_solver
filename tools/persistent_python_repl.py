import sys
import io
import traceback
from contextlib import redirect_stdout, redirect_stderr
from typing import Dict, Any
from langchain_core.tools import tool


class PersistentPythonREPLTool:
    """A persistent Python REPL that maintains state across executions."""
    
    def __init__(self):
        """Initialize the persistent Python REPL with a global namespace."""
        self.global_namespace: Dict[str, Any] = {
            "__name__": "__main__",
            "__doc__": None,
            "__builtins__": __builtins__,
        }
        # Import commonly used modules into the namespace
        exec("import sys, os, math, random, json, datetime", self.global_namespace)
    
    def execute(self, code: str) -> str:
        """Execute Python code in the persistent namespace.
        
        Args:
            code (str): Python code to execute.
            
        Returns:
            str: Output from the code execution including any errors.
        """
        # Capture stdout and stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        try:
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                # Execute the code in the persistent namespace
                exec(code, self.global_namespace)
        except Exception as e:
            # Capture the full traceback
            error_output = traceback.format_exc()
            stderr_capture.write(error_output)
        
        # Get the captured output
        stdout_output = stdout_capture.getvalue()
        stderr_output = stderr_capture.getvalue()
        
        # Combine outputs
        output = ""
        if stdout_output:
            output += stdout_output
        if stderr_output:
            if output:
                output += "\n"
            output += stderr_output
        
        return output if output else "Code executed successfully (no output)"
    
    def reset(self) -> str:
        """Reset the persistent namespace to initial state.
        
        Returns:
            str: Confirmation message.
        """
        self.__init__()
        return "Python REPL namespace has been reset."
    
    def get_namespace_info(self) -> str:
        """Get information about the current namespace.
        
        Returns:
            str: Information about variables and functions in the namespace.
        """
        user_vars = {k: v for k, v in self.global_namespace.items() 
                    if not k.startswith('_') and k not in ['sys', 'os', 'math', 'random', 'json', 'datetime']}
        
        if not user_vars:
            return "No user-defined variables in namespace."
        
        info = "Current namespace variables:\n"
        for name, value in user_vars.items():
            value_type = type(value).__name__
            if callable(value):
                info += f"  {name}: {value_type}\n"
            else:
                # Truncate long values
                value_str = str(value)
                if len(value_str) > 50:
                    value_str = value_str[:50] + "..."
                info += f"  {name}: {value_type} = {value_str}\n"
        
        return info


# Create a global instance for persistence
_persistent_repl = PersistentPythonREPLTool()


@tool("python_repl", description="Execute Python code in a persistent REPL environment")
def python_repl(code: str) -> str:
    """Execute Python code in a persistent REPL environment.
    
    This tool maintains state across multiple executions, allowing for
    interactive programming sessions. Variables and functions defined
    in previous executions remain available.
    
    Args:
        code (str): Python code to execute.
        
    Returns:
        str: Output from the code execution including any errors.
    """
    return _persistent_repl.execute(code)


@tool("python_repl_reset", description="Reset the Python REPL environment")
def python_repl_reset() -> str:
    """Reset the Python REPL environment to initial state.
    
    Returns:
        str: Confirmation message.
    """
    return _persistent_repl.reset()


@tool("python_repl_info", description="Get information about the current Python REPL namespace")
def python_repl_info() -> str:
    """Get information about the current Python REPL namespace.
    
    Returns:
        str: Information about variables and functions in the namespace.
    """
    return _persistent_repl.get_namespace_info()
