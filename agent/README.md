# Agent Service

This directory contains the Python-based AI agent service for the project.

## Overview
- **app.py**: Main FastAPI application. Provides endpoints for AI-powered code analysis and error reporting.
- **requirements.txt**: Python dependencies for the agent service.

## Features
- Receives error reports from the Laravel backend and analyzes them using OpenAI models.
- Indexes the Laravel codebase for semantic search and code analysis.
- Provides REST API endpoints for integration with other services.

## Setup
1. **Create and activate virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set environment variables:**
   - `OPENAI_API_KEY`: Your OpenAI API key (required).
4. **Run the service:**
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 5001
   ```

## Notes
- Make sure the Laravel project path in `app.py` is correct.
- The agent expects error reports at `/analyze-error` endpoint.
- CORS is enabled for local development with Laravel and Vite.

---

Feel free to expand this README with more usage and development details as needed.
