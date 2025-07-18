from .hint_tool import generate_hint
from .test_case_tool import generate_test_cases
from .complexity_analyzer import complexity_analyzer
from .persistent_python_repl import python_repl

ALL_TOOLS = [
    generate_hint,
    generate_test_cases,
    complexity_analyzer,
    python_repl,
]

def get_all_tools():
    return ALL_TOOLS
