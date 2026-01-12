# Laravel Error Analysis Agent

AI-powered error analysis service for Laravel applications using LangChain and OpenAI.

## 📋 Overview

This service provides intelligent error analysis for Laravel applications by:

-   Indexing your Laravel codebase using vector embeddings
-   Analyzing error traces with GPT-4
-   Searching for similar code patterns
-   Providing actionable debugging suggestions

## 🏗️ Project Structure

```
python/
├── app.py           # Main application entry point
├── api.py           # FastAPI routes and endpoints
├── models.py        # Data models and vector store management
├── tools.py         # LangChain tools and agent setup
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## 🚀 Quick Start

### 1. Create Virtual Environment

#### macOS/Linux:

```bash
cd python
python3 -m venv venv
source venv/bin/activate
```

#### Windows:

```bash
cd python
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

Create a `.env` file in the python directory or export the variable:

```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

Or add to your shell profile (`~/.zshrc`, `~/.bashrc`, etc.):

```bash
echo 'export OPENAI_API_KEY="your-api-key"' >> ~/.zshrc
source ~/.zshrc
```

### 4. Run the Server

```bash
python app.py
```

The server will start on `http://localhost:5001`

## 📦 Dependencies

The application requires the following packages (see [requirements.txt](requirements.txt)):

-   `fastapi` - Web framework
-   `uvicorn` - ASGI server
-   `langchain-openai` - OpenAI integration for LangChain
-   `langchain-community` - Community tools for LangChain
-   `langchain-core` - Core LangChain functionality
-   `faiss-cpu` - Vector similarity search
-   `python-dotenv` - Environment variable management

## 🔧 Configuration

### CORS Configuration

CORS is configured in [api.py](api.py) to allow requests from:

-   `http://127.0.0.1:8000` (Laravel)
-   `http://localhost:8000` (Laravel)
-   `http://localhost:5173` (Vite dev server)

Add more origins as needed in the `allow_origins` list.

## 📡 API Endpoints

### POST `/analyze-error`

Analyze a Laravel error.

**Request body:**

```json
{
    "message": "Error message",
    "file": "/path/to/file.php",
    "line": 123,
    "trace": "Stack trace...",
    "type": "Exception",
    "code": 0,
    "timestamp": "2026-01-12T10:30:00"
}
```

**Response:**

```json
{
  "status": "success",
  "analysis": "Detailed analysis...",
  "error_details": {...},
  "analysis_id": 1
}
```

### GET `/latest-analysis`

Get the most recent error analysis.

### GET `/analysis-history?limit=10`

Get analysis history (default: 10 records, max: 50).

### GET `/`

API information and available endpoints.

### GET `/health`

Health check endpoint.

## 🧩 Module Descriptions

### `app.py`

Main entry point that initializes the FastAPI application and starts the server.

### `api.py`

Contains all FastAPI route definitions and endpoint handlers:

-   Error analysis endpoint
-   History retrieval
-   Health checks

### `models.py`

Manages data models and vector store:

-   `AnalysisRecord` - Data model for error analyses
-   `AnalysisHistory` - In-memory storage manager
-   `index_laravel_codebase()` - Indexes Laravel code using FAISS

### `tools.py`

LangChain tools and agent configuration:

-   `read_code_file` - Tool to read Laravel source files
-   `search_similar_code` - Tool for vector similarity search
-   `create_agent()` - Creates the LangChain agent executor

## 🔍 How It Works

1. **Indexing Phase** (on startup):

    - Scans all PHP files in the Laravel project
    - Chunks code into segments
    - Creates vector embeddings using OpenAI
    - Stores in FAISS vector database

2. **Analysis Phase** (on error):

    - Receives error data from Laravel
    - Formats error information for the agent
    - Agent uses tools to:
        - Read the exact code where error occurred
        - Search for similar code patterns
    - GPT-4 analyzes and provides solutions
    - Results stored in memory

3. **Retrieval Phase**:
    - Frontend fetches latest analysis
    - Displays formatted results to user

## 🛠️ Development

### Running in Development

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Run with auto-reload
uvicorn api:app --reload --port 5001
```

### Adding New Tools

1. Define tool in [tools.py](tools.py) using `@tool` decorator
2. Add tool to the `tools` list in `create_agent()`
3. Update system prompt if needed

### Modifying Analysis History

Edit `AnalysisHistory` class in [models.py](models.py) to:

-   Change max storage size
-   Add persistence (database, file storage)
-   Modify data structure

## 🐛 Troubleshooting

### Vector Store Not Initializing

-   Check Laravel project path is correct
-   Ensure PHP files exist and are readable
-   Check console for indexing errors

### OpenAI API Errors

-   Verify `OPENAI_API_KEY` is set correctly
-   Check API key has sufficient credits
-   Ensure network connectivity

### CORS Issues

-   Add your frontend URL to `allow_origins` in [api.py](api.py)
-   Check browser console for specific CORS errors

### Import Errors

-   Ensure all dependencies are installed: `pip install -r requirements.txt`
-   Verify virtual environment is activated
-   Check Python version (3.8+ required)

## 📝 License

Part of the AI Hackathon project.

## 🤝 Contributing

1. Create feature branch
2. Make changes with clear commit messages
3. Test thoroughly
4. Submit pull request

## 📞 Support

For issues or questions, please open an issue in the repository.
