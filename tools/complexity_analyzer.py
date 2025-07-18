from langchain_core.tools import tool
from models.llm import get_llm


@tool("complexity_analyzer", description="Analyze time and space complexity of code")
def complexity_analyzer(code: str) -> str:
    """Analyze the time and space complexity of the given code.
    
    Args:
        code (str): The code to analyze for complexity.
        
    Returns:
        str: Analysis of time and space complexity with optimization suggestions.
    """
    llm = get_llm()
    
    prompt = f"""Analyze the time and space complexity of this code. Provide:
    1. Time complexity with explanation
    2. Space complexity with explanation
    3. Suggestions for optimization if any
    
    Code: {code}"""
    
    response = llm.invoke(prompt)
    
    return response.content
