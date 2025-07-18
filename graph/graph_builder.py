from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode
from models.llm import get_llm

def build_state_graph(tools: list):
    sys_msg = SystemMessage(content=(
        "You are a Socratic DSA mentor. Your primary goal is to guide users to a solution through questions and hints, not to provide the answer directly. "
        "Engage in a conversation. Ask clarifying questions to understand the user's thought process. "
        "You have access to tools for code execution, hints, test cases, and analysis. "
        "Only provide the full code solution if the user explicitly asks for it or is completely stuck after several hints. "
        "Your role is to foster learning by encouraging the user to think for themselves.\n\n"
        
        "IMPORTANT: When analyzing code:\n"
        "1. ALWAYS check if the code has test cases (look for print statements, assert statements, test functions, or example usage)\n"
        "2. If NO test cases exist, automatically generate and add appropriate test cases to the code before executing\n"
        "3. Use the python_repl tool to execute the complete code with test cases\n"
        "4. Use the complexity_analyzer tool to analyze time/space complexity\n"
        "5. Provide clear, educational feedback about the algorithm\n\n"
        
        "Test case indicators: print(), assert, test_, if __name__, example usage, result = function_call\n"
        "If none of these are present, ADD test cases before execution."
    ))
    
    llm = get_llm()
    llm_with_tools = llm.bind_tools(tools)
    
    def assistant(state: MessagesState):
        return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}
    
    graph = StateGraph(MessagesState)
    graph.add_node("assistant", assistant)
    graph.add_node("tools", ToolNode(tools))
    graph.add_edge(START, "assistant")
    graph.add_conditional_edges("assistant", tools_condition)
    graph.add_edge("tools", "assistant")
    
    return graph.compile()

