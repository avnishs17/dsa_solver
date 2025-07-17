"""
Custom exceptions for DSA Mentor application.
"""


class DSAMentorException(Exception):
    """Base exception for DSA Mentor application."""
    
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ToolInitializationError(DSAMentorException):
    """Raised when tools fail to initialize."""
    
    def __init__(self, message: str = "Failed to initialize tools", missing_dependencies: list = None):
        self.missing_dependencies = missing_dependencies or []
        error_code = "TOOL_INIT_ERROR"
        super().__init__(message, error_code)


class ToolExecutionError(DSAMentorException):
    """Raised when tool execution fails."""
    
    def __init__(self, tool_name: str, message: str = None):
        self.tool_name = tool_name
        message = message or f"Tool '{tool_name}' execution failed"
        error_code = "TOOL_EXEC_ERROR"
        super().__init__(message, error_code)


class LLMConnectionError(DSAMentorException):
    """Raised when LLM connection fails."""
    
    def __init__(self, message: str = "Failed to connect to LLM service"):
        error_code = "LLM_CONNECTION_ERROR"
        super().__init__(message, error_code)


class InvalidConfigurationError(DSAMentorException):
    """Raised when configuration is invalid."""
    
    def __init__(self, message: str = "Invalid configuration", config_key: str = None):
        self.config_key = config_key
        error_code = "INVALID_CONFIG_ERROR"
        super().__init__(message, error_code)


class SessionError(DSAMentorException):
    """Raised when session operations fail."""
    
    def __init__(self, session_id: str, message: str = None):
        self.session_id = session_id
        message = message or f"Session operation failed for session: {session_id}"
        error_code = "SESSION_ERROR"
        super().__init__(message, error_code) 