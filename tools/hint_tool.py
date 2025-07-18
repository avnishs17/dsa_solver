from langchain_core.tools import tool
from models.llm import get_llm


@tool("generate_hint", description="Generate a helpful hint for a DSA problem without solving it.")
def generate_hint(question: str) -> str:
    """Generate a helpful hint for a DSA problem without solving it.
    
    Args:
        question (str): The DSA problem to generate a hint for.
        
    Returns:
        str: A helpful hint for the DSA problem.
    """
    llm = get_llm()
    
    prompt = f"Give a helpful hint for this DSA problem without solving it: {question}"
    response = llm.invoke(prompt)
    
    return response.content
