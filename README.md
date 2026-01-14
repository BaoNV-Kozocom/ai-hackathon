# AI Error Debugger

**AI Error Debugger** is an Autonomous AI Agent designed to automatically detect, analyze, and fix errors in applications. The system operates on a Human-in-the-Loop model, where AI performs automatic debugging while developers maintain control over code commits.

## 🎯 Features

-   **Auto Error Detection**: Automatically capture errors from Laravel applications
-   **Backlog Integration**: Automatically create Bug issues on Backlog
-   **Multi-Agent Pipeline**: 4 specialized AI agents (Analyzer, Fixer, Synthetic, Backlog)
-   **Auto Fix**: AI automatically reads code, analyzes, and fixes errors
-   **Syntax Verification**: Verify syntax before completion
-   **Human-in-the-Loop**: Developers review and approve before committing
-   **Real-time Dashboard**: View logs & AI responses instantly

## 🔄 How It Works

```
1. Error occurs in Laravel App
         ↓
2. POST /analyze-error → Python Agent
         ↓
3. Create Bug issue on Backlog
         ↓
4. Backlog sends Webhook → POST /analyze-backlog
         ↓
5. AI Pipeline runs:
   • Agent Analyzer: Parse & detect language/framework
   • Agent Fixer: Generate fix code
   • Agent Synthetic: Apply & verify syntax
         ↓
6. Results displayed on Dashboard
         ↓
7. Developer reviews → Click "Commit Code"
```

## 🛠️ Tech Stack

### Backend

-   **Framework**: Laravel 11
-   **Language**: PHP 8.2+
-   **Authentication**: Laravel Sanctum
-   **Database**: MySQL 8.0

### Frontend

-   **Library**: React 18
-   **Build Tool**: Vite
-   **Styling**: TailwindCSS
-   **State Management**: Zustand
-   **Data Fetching**: React Query (@tanstack/react-query)

### AI Agent (Python)

-   **Framework**: FastAPI
-   **Language**: Python 3.11+
-   **LLM**: OpenAI GPT-5-mini & GPT-5.1-codex-mini
-   **Tools**: LangChain, DuckDuckGo Search

### External Services

-   **Backlog**: Project management & Bug tracking
-   **OpenAI API**: AI-powered analysis & code generation

## 📋 Prerequisites

Ensure you have the following installed on your local machine:

-   [PHP](https://www.php.net/downloads) (8.2 or higher)
-   [Composer](https://getcomposer.org/)
-   [Node.js](https://nodejs.org/) & [npm](https://www.npmjs.com/)
-   [Python](https://www.python.org/) (3.11 or higher)
-   MySQL 8.0
-   Backlog account with API key

## 🚀 Installation

1.  **Clone the repository**

    ```bash
    git clone https://github.com/yourusername/ai-error-debugger.git
    cd ai-error-debugger
    ```

2.  **Install Backend Dependencies**

    ```bash
    composer install
    ```

3.  **Install Frontend Dependencies**

    ```bash
    npm install
    ```

4.  **Install Python Dependencies**

    ```bash
    cd python
    pip install -r requirements.txt
    cd ..
    ```

5.  **Environment Setup**
    
    Copy the example environment files:

    ```bash
    cp .env.example .env
    cp python/.env.example python/.env
    ```

    Configure your settings in `.env`:
    ```env
    # Laravel
    DB_CONNECTION=mysql
    DB_DATABASE=ai_debugger
    
    # Python Agent URL
    AI_AGENT_URL=http://localhost:5001
    ```

    Configure Python agent in `python/.env`:
    ```env
    OPENAI_API_KEY=sk-xxx
    LARAVEL_API_URL=http://localhost:8000/api
    PROJECT_API_KEY=your-project-api-key
    
    # Backlog
    BACKLOG_BASE_URL=https://your-space.backlog.com
    BACKLOG_API_KEY=your-backlog-api-key
    BACKLOG_PROJECT_ID=12345
    BACKLOG_ISSUE_TYPE_ID=1
    ```

    Generate the application key:

    ```bash
    php artisan key:generate
    ```

6.  **Database Migration**
    ```bash
    php artisan migrate
    ```

## 🏃 Running the Application

Run each service in a separate terminal:

```bash
# Terminal 1: Laravel Backend (port 8000)
php artisan serve

# Terminal 2: Laravel Reverb WebSocket (port 8080)
php artisan reverb:start

# Terminal 3: Python AI Agent (port 5001)
cd python && python app.py

# Terminal 4: React Frontend
npm run dev
```

## 📡 API Documentation

### Laravel APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/login` | Authenticate user |
| POST | `/api/logout` | End session |
| GET | `/api/user` | Get authenticated user |
| GET | `/api/threads` | List all threads |
| GET | `/api/threads/{id}/messages` | Get messages for a thread |
| POST | `/api/ingest-log` | Ingest error log (API Key auth) |
| POST | `/api/ingest-analysis/{id}` | Store AI analysis (API Key auth) |

### Python AI Agent APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/analyze-error` | Receive error, create Backlog issue |
| POST | `/analyze-backlog` | Process Backlog webhook, run AI pipeline |
| POST | `/commit-code` | Commit and push code changes |
| GET | `/health` | Health check |

## 📖 Documentation

For detailed technical documentation, see [TECHNICAL_DOCUMENT.md](TECHNICAL_DOCUMENT.md).

## 📄 License

This project is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).
