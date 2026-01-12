"""
LangChain tools and agent setup for Laravel Error Analysis Agent.
"""
import os
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from models import LARAVEL_PROJECT_PATH, get_vector_store


@tool
def read_code_file(file_path: str, line_start: int, line_end: int) -> str:
    """
    Read a segment of a code file from the Laravel project.
    
    Args:
        file_path: Relative path to the file in the Laravel project (e.g., 'app/Http/Controllers/UserController.php')
        line_start: Starting line number (1-indexed)
        line_end: Ending line number (1-indexed)
    
    Returns:
        The content of the specified lines from the file
    """
    try:
        # Construct full path to Laravel project
        full_path = os.path.join(LARAVEL_PROJECT_PATH, file_path)
        
        # Read the file
        with open(full_path, 'r') as f:
            lines = f.readlines()
        
        # Validate line numbers
        if line_start < 1 or line_end > len(lines):
            return f"Error: Invalid line range. File has {len(lines)} lines."
        
        # Extract the specified lines
        code_segment = ''.join(lines[line_start-1:line_end])
        
        return f"File: {file_path}\nLines {line_start}-{line_end}:\n\n{code_segment}"
    
    except FileNotFoundError:
        return f"Error: File not found at {file_path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def search_similar_code(query: str, k: int = 5) -> str:
    """
    Search for similar code segments in the Laravel codebase using vector similarity.
    Useful for finding related code patterns, similar error handlers, or relevant implementations.
    
    Args:
        query: Description of the code you're looking for (e.g., "exception handling in controllers", "database query methods")
        k: Number of similar code segments to return (default: 5)
    
    Returns:
        Similar code segments with file paths and line numbers
    """
    vector_store = get_vector_store()
    
    if vector_store is None:
        return "Error: Vector store not initialized. Please wait for indexing to complete."
    
    try:
        # Search for similar documents
        results = vector_store.similarity_search(query, k=k)
        
        if not results:
            return "No similar code segments found."
        
        # Format results
        output = f"Found {len(results)} similar code segments:\n\n"
        
        for idx, doc in enumerate(results, 1):
            file = doc.metadata.get('file', 'Unknown')
            start_line = doc.metadata.get('start_line', '?')
            end_line = doc.metadata.get('end_line', '?')
            
            output += f"--- Result {idx} ---\n"
            output += f"File: {file}\n"
            output += f"Lines: {start_line}-{end_line}\n"
            output += f"Code:\n{doc.page_content[:300]}...\n\n"
        
        return output
    
    except Exception as e:
        return f"Error searching codebase: {str(e)}"


# Define the system prompt for debugging Laravel errors
SYSTEM_PROMPT = """You are an expert Laravel debugging assistant. Your role is to analyze error reports from Laravel applications and provide detailed, actionable solutions.

When you receive an error report, follow these steps:
1. Analyze the stack trace to understand the error flow
2. Identify the file and line number where the error occurred
3. Use the read_code_file tool to examine the relevant code segment
4. Use the search_similar_code tool to find similar patterns or error handling in the codebase
5. Analyze the code to determine the root cause of the error
6. Provide a clear explanation of what went wrong
7. Suggest specific fixes with code examples
8. Recommend best practices to prevent similar errors

You have access to two powerful tools:
- read_code_file: Read specific lines from a file
- search_similar_code: Find similar code patterns using vector search

Be thorough, precise, and provide Laravel-specific solutions. Always read the actual code before making conclusions."""


def create_agent() -> AgentExecutor:
    """
    Create and configure the LangChain agent executor.
    
    Returns:
        Configured AgentExecutor instance
    """
    # Initialize ChatOpenAI model
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    
    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Create tools list
    tools = [read_code_file, search_similar_code]
    
    # Create the tool-calling agent
    agent = create_openai_tools_agent(llm, tools, prompt)
    
    # Create the agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )
    
    return agent_executor
