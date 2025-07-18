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
    
    prompt = f"""Analyze the time and space complexity of this code. Format your response clearly with the following structure:

**Time Complexity:** O(n) - Brief explanation of why
- Detailed explanation of the time complexity analysis

**Space Complexity:** O(n) - Brief explanation of why  
- Detailed explanation of the space complexity analysis

**Algorithm Approach:**
- Brief description of the algorithm and how it works

**Optimization Suggestions:**
- Any potential optimizations or alternative approaches
- Trade-offs between different solutions

Code to analyze:
```
{code}
```

Please provide a clear, well-structured analysis that's easy to read."""
    
    response = llm.invoke(prompt)
    
    return response.content
