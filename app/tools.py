import sys
from io import StringIO
from typing import Dict

from .logger import get_logger
from .exceptions import ToolInitializationError, ToolExecutionError

logger = get_logger(__name__)

try:
    from langchain_core.tools import tool, Tool
    from langchain_experimental.utilities import PythonREPL
    from langchain_core.language_models.chat_models import BaseChatModel
    LANGCHAIN_AVAILABLE = True
    logger.info("Successfully imported all LangChain dependencies")
except ImportError as e:
    LANGCHAIN_AVAILABLE = False
    logger.error(f"Failed to import LangChain dependencies: {e}")
    logger.error("Tools will not be available until dependencies are installed")


class PersistentPythonREPLToolPythonREPL(PythonREPL):
    """Enhanced Python REPL with persistent state."""
    
    def __init__(self):
        super().__init__()
        self._globals = {}

    def run(self, command: str) -> str:
        """Execute Python code with persistent state."""
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        try:
            # First try eval (single expression)
            result = eval(command, self._globals)
            output = captured_output.getvalue()
            if output:
                return output + str(result)
            return str(result)
        except SyntaxError:
            # If it's a statement block, use exec
            try:
                exec(command, self._globals)
                output = captured_output.getvalue()
                return output if output else "Executed successfully with no output."
            except Exception as e:
                output = captured_output.getvalue()
                return output + repr(e) if output else repr(e)
        except Exception as e:
            output = captured_output.getvalue()
            return output + repr(e) if output else repr(e)
        finally:
            # Restore stdout
            sys.stdout = old_stdout

class ToolManager:
    """Manages all DSA mentoring tools."""
    
    def __init__(self, llm: BaseChatModel):
        logger.info("Initializing ToolManager...")
        self.llm = llm
        
        try:
            self.python_repl = PersistentPythonREPLToolPythonREPL()
            self.initialize_tools()
            logger.info("Successfully initialized all tools")
        except Exception as e:
            logger.error(f"Failed to initialize tools: {e}", exc_info=True)
            raise ToolInitializationError(f"Failed to initialize tools: {e}")
    
    def initialize_tools(self):
        """Initialize all tools."""
        self.repl_tool = Tool(
            name="python_repl",
            description="A Python shell. Use this to execute python commands. " \
                        "Input should be a valid python command. If you want to see " \
                        "the output of a value, you should print it out with `print(...)`.",
            func=self.python_repl.run,
        )
        
        self.generate_hint = Tool(
            name="generate_hint",
            description="Generate a helpful hint for a DSA problem without solving it.",
            func=self.generate_hint_handler
        )
        
        self.generate_test_cases = Tool(
            name="generate_test_cases", 
            description="Generate test cases for DSA problems without solving them.",
            func=self.generate_test_cases_handler
        )
        
        self.bug_hint_tool = Tool(
            name="bug_hint_tool",
            description="Analyze code for logic issues and provide a subtle hint.",
            func=self.analyze_code_bugs
        )
        
        self.complexity_analyzer = Tool(
            name="complexity_analyzer",
            description="Analyze time and space complexity of code",
            func=self.analyze_complexity
        )
        
        self.code_quality_checker = Tool(
            name="code_quality_checker",
            description="Check code quality and suggest improvements",
            func=self.check_code_quality
        )
        
        self.recommend_problems = Tool(
            name="recommend_problems",
            description="Recommend next problems based on progress",
            func=self.recommend_problems_handler
        )
    
    def generate_hint_handler(self, question: str) -> str:
        """Generate a helpful hint for a DSA problem without solving it."""
        try:
            logger.info(f"Generating hint for question: {question}")
            response = self.llm.invoke(f"Give a helpful hint for this DSA problem without solving it: {question}")
            return response.content
        except Exception as e:
            logger.error(f"Error generating hint: {e}")
            raise ToolExecutionError("generate_hint", f"Failed to generate hint: {str(e)}")
    
    def generate_test_cases_handler(self, problem_description: str) -> str:
        """Generate test cases for DSA problems."""
        try:
            logger.info(f"Generating test cases for problem: {problem_description}")
            response = self.llm.invoke(f"Create 3 test cases for this DSA problem without solving it: {problem_description}")
            return response.content
        except Exception as e:
            logger.error(f"Error generating test cases: {e}")
            raise ToolExecutionError("generate_test_cases", f"Failed to generate test cases: {str(e)}")
    
    def analyze_code_bugs(self, code: str) -> str:
        """Analyze code for logic issues and provide a subtle hint."""
        try:
            logger.info(f"Analyzing code for bugs: {code[:100]}...")
            response = self.llm.invoke(f"Analyze this code for logic issues and give a subtle hint: {code}")
            return response.content
        except Exception as e:
            logger.error(f"Error analyzing code: {e}")
            raise ToolExecutionError("bug_hint_tool", f"Failed to analyze code for bugs: {str(e)}")
    
    def analyze_complexity(self, code: str) -> str:
        """Analyze the time and space complexity of the given code."""
        try:
            logger.info(f"Analyzing complexity for code: {code[:100]}...")
            prompt = f"""Analyze the time and space complexity of this code. Provide:
            1. Time complexity with explanation
            2. Space complexity with explanation
            3. Suggestions for optimization if any
            
            Code: {code}"""
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            logger.error(f"Error analyzing complexity: {e}")
            raise ToolExecutionError("complexity_analyzer", f"Failed to analyze complexity: {str(e)}")
    
    def check_code_quality(self, code: str) -> str:
        """Check code quality and suggest improvements."""
        try:
            logger.info(f"Checking code quality for: {code[:100]}...")
            prompt = f"""Review this code for:
            1. Readability and style
            2. Edge case handling
            3. Variable naming
            4. Code structure
            
            Code: {code}"""
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            logger.error(f"Error checking code quality: {e}")
            raise ToolExecutionError("code_quality_checker", f"Failed to check code quality: {str(e)}")
    
    def recommend_problems_handler(self, current_topic: str = "", difficulty: str = "medium") -> str:
        """Recommend problems based on learning progression."""
        try:
            logger.info(f"Recommending problems for topic: {current_topic}, difficulty: {difficulty}")
            prompt = f"""Based on the current topic '{current_topic}' and difficulty '{difficulty}', 
            recommend 3 specific DSA problems that would be good next steps for learning. 
            Include problem names and brief descriptions."""
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            logger.error(f"Error recommending problems: {e}")
            raise ToolExecutionError("recommend_problems", f"Failed to recommend problems: {str(e)}")
    
    def get_tools(self):
        """Return all available tools"""
        tools = [
            self.repl_tool, 
            self.generate_hint, 
            self.generate_test_cases, 
            self.bug_hint_tool,
            self.complexity_analyzer,
            self.code_quality_checker,
            self.recommend_problems
        ]
        logger.info(f"Initialized {len(tools)} tools")
        return tools
