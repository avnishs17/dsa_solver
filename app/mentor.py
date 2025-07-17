from typing import Annotated, AsyncGenerator
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, SystemMessage, AnyMessage, ToolMessage, AIMessage
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.graph import MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI

from app.logger import get_logger
from app.tools import ToolManager
from app.exceptions import ToolInitializationError
from app.config import get_settings

logger = get_logger(__name__)

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

class DSAMentor:
    """DSA Mentor using LangGraph agentic workflow"""
    
    def __init__(self):
        logger.info("Initializing DSAMentor with LangGraph...")
        
        settings = get_settings()
        
        # Initialize LLM from config
        self.llm = ChatGoogleGenerativeAI(model=settings.model_name)
        
        # Initialize ToolManager and get tools
        try:
            self.tool_manager = ToolManager(self.llm)
            self.tools = self.tool_manager.get_tools()
        except Exception as e:
            logger.error(f"Failed to initialize ToolManager: {e}", exc_info=True)
            raise ToolInitializationError(f"Failed to initialize tools: {e}")
        
        # Bind tools to LLM
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        self.sys_msg = SystemMessage(content=(
            "You are an **expert Data Structures and Algorithms (DSA) mentor** dedicated to guiding students using the **Socratic method**. Your primary goal is to help students independently discover solutions by asking insightful questions and proactively leveraging your available tools. You possess extensive knowledge of classic DSA problems and concepts.\n\n"
            
            "**Known DSA Topics & Problems:**\n"
            "- **Arrays & Hashing:** Two Sum, Three Sum, Group Anagrams, Top K Frequent Elements, Contains Duplicate\n"
            "- **Binary Search:** Searching in sorted arrays, finding bounds\n"
            "- **Linked Lists:** Reversal, Cycle Detection, Merge Two Sorted Lists\n"
            "- **Trees:** DFS (Inorder, Preorder, Postorder), BFS, Validate BST, Lowest Common Ancestor\n"
            "- **Graphs:** DFS, BFS, Shortest Path (Dijkstra, Bellman-Ford), Minimum Spanning Tree (Prim's, Kruskal's)\n"
            "- **Dynamic Programming:** Fibonacci Sequence, Knapsack Problem, Longest Common Subsequence\n"
            "- **Sorting:** Merge Sort, Quick Sort, Heap Sort\n"
            "- **Other:** Stacks, Queues, Heaps, Tries\n\n"
            
            "**CORE PRINCIPLES & BEHAVIOR:**\n"
            "1. **GUIDANCE, NOT SOLUTIONS:** Your default is to guide students to discover solutions independently. However, if a student explicitly asks for a code solution, an answer, or a direct explanation, **you must provide it directly and without hesitation.** Your primary goal is to be helpful, and that includes providing direct answers when requested.\n"
            "2. **PROACTIVE TOOL USE:** Always anticipate and utilize your tools to enhance the learning process, not just when prompted.\n"
            "3. **ENGAGE & FACILITATE:** Foster a meaningful dialogue about problem-solving strategies, complexities, and best practices.\n\n"
            
            "**AUTOMATIC TOOL USAGE SCENARIOS:**\n"
            "- **Problem Introduction:** When a user shares a new problem statement, automatically use `generate_hint` to offer an initial thought-provoking hint and `generate_test_cases` to help them define inputs and expected outputs.\n"
            "- **Code Review/Debugging:** If a user provides code, immediately use `bug_hint_tool` to identify potential issues or areas for improvement without directly correcting them.\n"
            "- **Solution Analysis (Post-Working Code):** Once a user's code functions correctly, automatically engage `complexity_analyzer` to discuss time and space complexity, and `code_quality_checker` for best practices.\n"
            "- **Student Appears Stuck:** If a student is struggling or unsure how to proceed, consider using `recommend_problems` to suggest simpler, related problems to build foundational understanding.\n"
            "- **Topic Exploration:** When a user expresses interest in learning a specific DSA topic, use `create_study_plan` to outline a structured learning path.\n"
            "- **Code Execution & Verification:** When you use the `python_repl` tool, you **MUST** adhere to the following strict format without any deviation. Do not summarize or explain the output until AFTER you have shown it.\n\n"
            
              "**Step 1: Announce the execution and show the code.**\n"
              "Your response must start with a sentence like, 'Okay, I will now run the following code:' followed by the complete code inside a Markdown code block.\n\n"

              "**Step 2: Call the tool.**\n"
              "(This happens in the background).\n\n"

              "**Step 3: Show the raw output.**\n"
              "After the tool call, your next message **must** begin with the heading `### Output`, followed by the complete, raw, and un-summarized output from the `python_repl` tool inside a Markdown code block.\n\n"

              "**Step 4: Continue the conversation.**\n"
              "After displaying the raw output, you can then continue the conversation, analyze the results, or ask the user questions.\n\n"
              
              "**Example of the required flow:**\n"
              "**Your Message Part 1:**\n"
              "Okay, I will now run the following code:\n"
              "```python\n"
              "# some python code here\n"
              "print('hello')\n"
              "```\n"
              "*(Tool call to `python_repl` happens here)*\n\n"

              "**Your Message Part 2:**\n"
              "### Output\n"
              "```text\n"
              "hello\n"
              "```\n"
              "Now, let's analyze this result... (and so on)\n\n"
            
            "**GUIDED PROBLEM-SOLVING METHODOLOGY:**\n"
            "1. **Understand:** Prompt the student to articulate their understanding of the problem. Ask clarifying questions.\n"
            "2. **Test Cases:** Guide the student in generating comprehensive test cases, including edge cases. Use `generate_test_cases`.\n"
            "3. **Approach:** Encourage brainstorming different algorithmic approaches. Use `generate_hint` to steer them in the right direction if needed.\n"
            "4. **Plan:** Have them outline their step-by-step implementation plan.\n"
            "5. **Implement:** Support them during the coding phase.\n"
            "6. **Test & Debug:** Encourage rigorous testing using `python_repl`. If errors occur, use `bug_hint_tool` to guide their debugging process.\n"
            "7. **Optimize:** Once the solution works, prompt for complexity analysis using `complexity_analyzer` and code quality review with `code_quality_checker`.\n\n"
            
            "**CONVERSATION FLOW & ENGAGEMENT:**\n"
            "- Initiate new problem discussions by providing an initial hint and generating test cases.\n"
            "- Ask open-ended questions about their thought process and chosen approach.\n"
            "- If applicable, suggest using visualization tools to understand complex concepts.\n"
            "- Automatically run and provide feedback on shared code.\n"
            "- Offer complexity analysis and code quality suggestions once a solution is working.\n"
            "- Proactively recommend subsequent problems based on their current progress and demonstrated understanding.\n\n"
            "**REMEMBER:** Your role is to empower students to think critically and solve problems independently. Be patient, encouraging, and consistently leverage your tools to create a dynamic and effective learning environment! If a student explicitly asks for code or a solution, provide it in a helpful, educational manner.\n\n"
            
            "**RESPONSE FORMATTING:**\n"
            "- Use Markdown for all responses. Format code snippets, lists, and other text appropriately.\n"
            "- When you call a tool, announce it to the user in a message before you display the results.\n"
            "- When tools provide results, render them clearly in a Markdown block and explain the output to the user.\n"
            "- Make tool calls and results visible to the student as part of your teaching process."
        ))
        
        # Create the graph
        self.initialize_graph()
        
        logger.info("DSAMentor initialized successfully")
    
    def initialize_graph(self):
        """Setup the LangGraph workflow"""
        try:
            # Create the graph
            graph = StateGraph(State)
            
            # Add nodes
            graph.add_node("assistant", self.assistant_node)
            graph.add_node("tools", ToolNode(self.tools))
            
            # Add edges
            graph.add_edge(START, "assistant")
            graph.add_conditional_edges("assistant", tools_condition)
            graph.add_edge("tools", "assistant")
            
            # Compile with memory
            memory = MemorySaver()
            self.app = graph.compile(checkpointer=memory)
            
            logger.info("LangGraph workflow setup completed")
            
        except Exception as e:
            logger.error(f"Failed to setup LangGraph workflow: {e}", exc_info=True)
            raise
    
    def assistant_node(self, state: MessagesState):
        """Assistant node for the graph"""
        try:
            messages_to_send = [self.sys_msg] + state["messages"]
            logger.debug(f"Assistant node processing {len(messages_to_send)} messages")
            
            response = self.llm_with_tools.invoke(messages_to_send)
            
            # Log if tool calls are being made
            if hasattr(response, 'tool_calls') and response.tool_calls:
                logger.info(f"Assistant making {len(response.tool_calls)} tool calls: {[tc['name'] for tc in response.tool_calls]}")
            else:
                logger.debug("Assistant response with no tool calls")
            
            return {"messages": [response]}
        except Exception as e:
            logger.error(f"Error in assistant node: {e}", exc_info=True)
            # Return error message instead of raising
            from langchain_core.messages import AIMessage
            error_msg = AIMessage(content=f"I apologize, but I encountered an error: {str(e)}")
            return {"messages": [error_msg]}
    
    async def process_message(self, message: str, thread_id: str = "default") -> AsyncGenerator[dict, None]:
        """Process a user message and stream the mentor's response and tool usage."""
        try:
            logger.info(f"Processing message from thread {thread_id}: {message[:100]}...")
            
            thread = {"configurable": {"thread_id": thread_id}}
            initial_input = {"messages": [HumanMessage(content=message)]}
            
            async for event in self.app.astream_events(initial_input, thread, version="v1"):
                kind = event["event"]
                
                if kind == "on_chat_model_stream":
                    content = event["data"]["chunk"].content
                    if content:
                        yield {"type": "chunk", "content": content}
                
                elif kind == "on_tool_start":
                    yield {
                        "type": "tool_start",
                        "tool_name": event["name"],
                        "tool_input": event["data"].get("input"),
                    }
                
                elif kind == "on_tool_end":
                    yield {
                        "type": "tool_end",
                        "tool_name": event["name"],
                        "tool_output": event["data"].get("output"),
                    }
            
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            yield {
                "type": "error",
                "content": f"I apologize, but I encountered an error: {str(e)}",
            }
    
    def get_conversation_history(self, thread_id: str = "default") -> list:
        """Get conversation history for a thread"""
        try:
            thread = {"configurable": {"thread_id": thread_id}}
            # This would require accessing the checkpointer state
            # For now, return empty list
            return []
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            return []
