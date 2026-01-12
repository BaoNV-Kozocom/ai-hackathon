import os
import glob
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.document import Document
import uvicorn

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

# Initialize FastAPI app
app = FastAPI()

# Configure CORS to allow requests from Laravel server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://localhost:5173",  # Vite dev server
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Laravel project path
LARAVEL_PROJECT_PATH = os.path.join(os.path.dirname(__file__), '../my-laravel-app')

# Initialize embeddings and vector store (will be loaded on startup)
embeddings = OpenAIEmbeddings(api_key=os.environ.get("OPENAI_API_KEY"))
vector_store = None

# In-memory storage for analysis results
# Structure: list of dicts with analysis data
analysis_history = []
latest_analysis = None


def index_laravel_codebase():
    """
    Index the Laravel codebase using FAISS for vector search.
    This creates embeddings for all PHP files in the project.
    """
    global vector_store
    
    print("🔍 Indexing Laravel codebase...")
    
    # Find all PHP files
    php_files = glob.glob(f"{LARAVEL_PROJECT_PATH}/**/*.php", recursive=True)
    
    documents = []
    for file_path in php_files:
        try:
            # Skip vendor and node_modules
            if 'vendor' in file_path or 'node_modules' in file_path:
                continue
                
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Create relative path
            rel_path = os.path.relpath(file_path, LARAVEL_PROJECT_PATH)
            
            # Split large files into chunks (by function/class)
            # For simplicity, we'll chunk by lines
            lines = content.split('\n')
            chunk_size = 50
            
            for i in range(0, len(lines), chunk_size):
                chunk = '\n'.join(lines[i:i+chunk_size])
                if chunk.strip():
                    doc = Document(
                        page_content=chunk,
                        metadata={
                            'file': rel_path,
                            'start_line': i + 1,
                            'end_line': min(i + chunk_size, len(lines))
                        }
                    )
                    documents.append(doc)
        except Exception as e:
            print(f"Error indexing {file_path}: {e}")
    
    print(f"📚 Indexed {len(documents)} code chunks from {len(php_files)} files")
    
    # Create FAISS vector store
    if documents:
        vector_store = FAISS.from_documents(documents, embeddings)
        print("✅ Vector store created successfully")
    else:
        print("⚠️  No documents to index")


@app.on_event("startup")
async def startup_event():
    """Initialize vector store on startup"""
    index_laravel_codebase()


# Tool to read code segments from Laravel project
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
    global vector_store
    
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


# Initialize ChatOpenAI model
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    api_key=os.environ.get("OPENAI_API_KEY")
)

# Define the system prompt for debugging Laravel errors
system_prompt = """You are an expert Laravel debugging assistant. Your role is to analyze error reports from Laravel applications and provide detailed, actionable solutions.

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

# Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
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


@app.post("/analyze-error")
async def analyze_error(request: Request):
    """
    Endpoint to receive error data from Laravel and analyze it using the AI agent.
    """
    global latest_analysis, analysis_history
    
    # Parse error data from request
    error_data = await request.json()
    
    # Extract error details
    message = error_data.get('message', 'No message')
    file = error_data.get('file', 'Unknown file')
    line = error_data.get('line', 'Unknown line')
    trace = error_data.get('trace', 'No trace available')
    error_type = error_data.get('type', 'Unknown error type')
    code = error_data.get('code', 'No code')
    timestamp = error_data.get('timestamp', 'Unknown time')
    
    # Format the error information for the agent
    error_input = f"""
Laravel Error Report:
====================
Type: {error_type}
Message: {message}
File: {file}
Line: {line}
Code: {code}
Timestamp: {timestamp}

Stack Trace:
{trace}

Please analyze this error, read the relevant code, and provide a detailed explanation with suggested fixes.
"""
    
    print("\n" + "="*80)
    print("RECEIVED ERROR FROM LARAVEL")
    print("="*80)
    print(error_input)
    print("="*80 + "\n")
    
    # Invoke the agent
    try:
        result = agent_executor.invoke({"input": error_input})
        analysis = result.get("output", "No analysis generated")
        
        print("\n" + "="*80)
        print("AGENT ANALYSIS")
        print("="*80)
        print(analysis)
        print("="*80 + "\n")
        
        # Store the analysis in memory
        analysis_record = {
            "id": len(analysis_history) + 1,
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "error_message": message,
            "file": file,
            "line": line,
            "analysis": analysis,
            "error_details": error_data,
            "status": "success"
        }
        
        # Add to history
        analysis_history.append(analysis_record)
        
        # Keep only last 50 analyses to prevent memory overflow
        if len(analysis_history) > 50:
            analysis_history.pop(0)
        
        # Update latest analysis
        latest_analysis = analysis_record
        
        return {
            "status": "success",
            "analysis": analysis,
            "error_details": error_data,
            "analysis_id": analysis_record["id"]
        }
    
    except Exception as e:
        error_message = f"Error during analysis: {str(e)}"
        print(f"\n{error_message}\n")
        
        # Store failed analysis
        analysis_record = {
            "id": len(analysis_history) + 1,
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "error_message": message,
            "file": file,
            "line": line,
            "analysis": error_message,
            "error_details": error_data,
            "status": "error"
        }
        
        analysis_history.append(analysis_record)
        if len(analysis_history) > 50:
            analysis_history.pop(0)
        
        latest_analysis = analysis_record
        
        return {
            "status": "error",
            "message": error_message,
            "error_details": error_data
        }


@app.get("/latest-analysis")
async def get_latest_analysis():
    """
    Endpoint to retrieve the latest error analysis.
    Used by the React frontend to display analysis results.
    """
    if latest_analysis is None:
        return {
            "status": "no_data",
            "message": "No analysis has been performed yet"
        }
    
    return {
        "status": "success",
        "data": latest_analysis
    }


@app.get("/analysis-history")
async def get_analysis_history(limit: int = 10):
    """
    Endpoint to retrieve analysis history.
    Optionally specify a limit (default: 10, max: 50).
    """
    limited_history = analysis_history[-min(limit, 50):]
    
    return {
        "status": "success",
        "count": len(limited_history),
        "data": limited_history
    }


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "message": "Laravel Error Analysis Agent is ready",
        "endpoints": {
            "analyze_error": "POST /analyze-error",
            "latest_analysis": "GET /latest-analysis",
            "analysis_history": "GET /analysis-history?limit=10"
        }
    }


if __name__ == "__main__":
    # Run the FastAPI server on port 5000
    print("Starting Laravel Error Analysis Agent on http://localhost:5001")
    print("Make sure to set OPENAI_API_KEY environment variable")
    uvicorn.run(app, host="0.0.0.0", port=5001)
