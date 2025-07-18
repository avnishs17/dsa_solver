from langchain_core.tools import tool
from models.llm import get_llm


@tool("generate_test_cases", description="Generate test cases for DSA problems without solving them.")
def generate_test_cases(problem_description: str) -> str:
    """Generate test cases for DSA problems without solving them.
    
    Args:
        problem_description (str): The DSA problem statement.
        
    Returns:
        str: Generated test cases for the problem.
    """
    llm = get_llm()
    
    prompt = f"Create 3 test cases for this DSA problem without solving it: {problem_description}"
    response = llm.invoke(prompt)
    
    return response.content
