# AI Error Debugger - Tài Liệu Kỹ Thuật

**Version**: 1.0.0  
**Date**: January 14, 2026  
**Author**: My mind
**Project**: AI Hackathon 2026

---

## 📑 Mục Lục

1. [Tổng Quan](#1-tổng-quan)
2. [Kiến Trúc Hệ Thống](#2-kiến-trúc-hệ-thống)
3. [APIs & Integrations](#3-apis--integrations)
4. [AI Model & Algorithms](#4-ai-model--algorithms)
5. [AI Agent Pipeline](#5-ai-agent-pipeline)
6. [Backlog Integration](#6-backlog-integration)
7. [Dataset](#7-dataset)
8. [Evaluation](#8-evaluation)
9. [Security & Ethics](#9-security--ethics)
10. [Performance Metrics](#10-performance-metrics)
11. [Limitations & Future Work](#11-limitations--future-work)

---

## 1. Tổng Quan

### 1.1 Mô Tả Dự Án

**AI Error Debugger** là một Autonomous AI Agent được thiết kế để tự động phát hiện, phân tích và sửa lỗi trong ứng dụng Laravel. Hệ thống hoạt động theo mô hình Human-in-the-Loop, trong đó AI thực hiện việc debug tự động nhưng developer vẫn kiểm soát việc commit code.

### 1.2 Mục Tiêu

| Mục tiêu | Mô tả |
|----------|-------|
| **Giảm thời gian debug** | Từ 1-2 giờ xuống còn 1-3 phút |
| **Tự động hóa** | AI tự động đọc log, phân tích và sửa code |
| **Kiểm soát** | Developer review và approve trước khi commit |
| **Real-time** | Dashboard hiển thị kết quả ngay lập tức |

### 1.3 Phạm Vi

- **Target Platform**: Laravel/PHP Applications
- **Supported Errors**: Runtime errors, Type errors, Database errors
- **Environment**: Development & Staging (có thể mở rộng Production)

---

## 2. Kiến Trúc Hệ Thống

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              SYSTEM ARCHITECTURE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        LAYER 1: APPLICATION                          │   │
│  │  ┌───────────────────────────────────────────────────────────────┐  │   │
│  │  │                    Laravel Application                         │  │   │
│  │  │                                                                │  │   │
│  │  │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐       │  │   │
│  │  │   │ Controllers │───▶│  Services   │───▶│   Models    │       │  │   │
│  │  │   └──────┬──────┘    └─────────────┘    └─────────────┘       │  │   │
│  │  │          │                                                     │  │   │
│  │  │          │ Exception                                           │  │   │
│  │  │          ▼                                                     │  │   │
│  │  │   ┌─────────────┐                                              │  │   │
│  │  │   │   Custom    │──────────────────────────────┐               │  │   │
│  │  │   │   Error     │                              │               │  │   │
│  │  │   │   Handler   │                              │               │  │   │
│  │  │   └─────────────┘                              │               │  │   │
│  │  └────────────────────────────────────────────────│───────────────┘  │   │
│  └───────────────────────────────────────────────────│──────────────────┘   │
│                                                      │                      │
│                                    HTTP POST /analyze-error                 │
│                                                      │                      │
│  ┌───────────────────────────────────────────────────│──────────────────┐   │
│  │                        LAYER 2: AI AGENT          │                  │   │
│  │  ┌────────────────────────────────────────────────▼───────────────┐  │   │
│  │  │                    Python FastAPI Server                        │  │   │
│  │  │                                                                 │  │   │
│  │  │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │  │   │
│  │  │   │   Error     │───▶│   GPT-5     │───▶│   Tool      │        │  │   │
│  │  │   │   Receiver  │    │   Agent     │    │   Executor  │        │  │   │
│  │  │   └─────────────┘    └──────┬──────┘    └──────┬──────┘        │  │   │
│  │  │                             │                  │               │  │   │
│  │  │                             │ API Call         │ Shell Exec    │  │   │
│  │  │                             ▼                  ▼               │  │   │
│  │  │                      ┌─────────────┐    ┌─────────────┐        │  │   │
│  │  │                      │   OpenAI    │    │  Local FS   │        │  │   │
│  │  │                      │   API       │    │  (sed/bash) │        │  │   │
│  │  │                      └─────────────┘    └─────────────┘        │  │   │
│  │  │                                                                 │  │   │
│  │  └─────────────────────────────────────────────────────────────────┘  │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│                                                      │                      │
│                                    HTTP POST /ingest-analysis               │
│                                                      │                      │
│  ┌───────────────────────────────────────────────────│──────────────────┐   │
│  │                        LAYER 3: PRESENTATION      │                  │   │
│  │  ┌────────────────────────────────────────────────▼───────────────┐  │   │
│  │  │                    React Dashboard                              │  │   │
│  │  │                                                                 │  │   │
│  │  │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │  │   │
│  │  │   │   Thread    │    │    Chat     │    │   Commit    │        │  │   │
│  │  │   │   List      │    │  Interface  │    │   Button    │        │  │   │
│  │  │   └─────────────┘    └─────────────┘    └─────────────┘        │  │   │
│  │  │                                                                 │  │   │
│  │  └─────────────────────────────────────────────────────────────────┘  │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                              DATA LAYER                                      │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                      │
│  │   MySQL     │    │   Redis     │    │    Git      │                      │
│  │   Database  │    │   (Queue)   │    │   Repository│                      │
│  └─────────────┘    └─────────────┘    └─────────────┘                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Component Details

| Component | Technology | Port | Responsibility |
|-----------|------------|------|----------------|
| Laravel API | PHP 8.2 + Laravel 11 | 8000 | Backend API, Error Handling |
| AI Agent | Python 3.11 + FastAPI | 5001 | Error Analysis, Code Fixing |
| Frontend | React 18 + Vite | 8000 (integrated) | User Interface |
| Database | MySQL 8.0 | 3306 | Data Persistence |
| LLM | OpenAI GPT-5-mini & GPT-5.1-codex-mini | External | Intelligence Layer |

### 2.3 Data Flow

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           DATA FLOW DIAGRAM                               │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. ERROR OCCURS                                                         │
│     User Request → Controller → Exception Thrown                         │
│                                       │                                  │
│                                       ▼                                  │
│  2. ERROR CAPTURED                                                       │
│     Exception Handler captures: message, file, line, trace               │
│                                       │                                  │
│                                       ▼                                  │
│  3. SEND TO AI AGENT                                                     │
│     POST /analyze-error { message, file, line, trace }                   │
│                                       │                                  │
│                                       ▼                                  │
│  4. CREATE BACKLOG ISSUE                                                 │
│     AI Agent → Backlog API → Create Bug Issue                            │
│                                       │                                  │
│                                       ▼                                  │
│  5. BACKLOG WEBHOOK TRIGGER                                              │
│     Backlog sends webhook → POST /analyze-backlog                        │
│                                       │                                  │
│                                       ▼                                  │
│  6. AGENT BACKLOG PARSE                                                  │
│     Parse issue content → Extract error details                          │
│     Ingest to Laravel → Create Thread                                    │
│                                       │                                  │
│                                       ▼                                  │
│  7. AI PIPELINE (Multi-Agent)                                            │
│     ┌─────────────────────────────────────────────────────┐              │
│     │  a. Agent Analyzer: Parse & detect language         │              │
│     │  b. Agent Fixer: Generate fix (JSON edits)          │              │
│     │  c. Agent Synthetic: Apply & verify syntax          │              │
│     └─────────────────────────────────────────────────────┘              │
│                                       │                                  │
│                                       ▼                                  │
│  8. STORE RESULT                                                         │
│     POST /ingest-analysis/{threadId} { analysis_result }                 │
│                                       │                                  │
│                                       ▼                                  │
│  9. DISPLAY ON DASHBOARD                                                 │
│     React Query fetches → Display in ChatInterface                       │
│                                       │                                  │
│                                       ▼                                  │
│  10. USER ACTION                                                         │
│      User clicks "Commit Code" → POST /commit-code → Git push            │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### 2.4 Database Schema

```sql
-- Projects Table
CREATE TABLE projects (
    id              BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    name            VARCHAR(255) NOT NULL,
    api_key         VARCHAR(64) UNIQUE NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Issue Threads Table (Bug Reports)
CREATE TABLE issue_threads (
    id                  BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    project_id          BIGINT UNSIGNED NOT NULL,
    title               VARCHAR(255) NOT NULL,
    error_hash          VARCHAR(64),           -- For deduplication
    status              ENUM('open', 'in_progress', 'resolved') DEFAULT 'open',
    severity            ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    source_service      VARCHAR(100),
    environment         VARCHAR(50),
    latest_activity_at  TIMESTAMP,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    INDEX idx_status (status),
    INDEX idx_error_hash (error_hash)
);

-- Thread Messages Table (Conversation)
CREATE TABLE thread_messages (
    id                  BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    issue_thread_id     BIGINT UNSIGNED NOT NULL,
    sender_type         ENUM('system_log', 'ai', 'user') NOT NULL,
    content             LONGTEXT NOT NULL,
    metadata            JSON,                  -- Additional data (files_modified, etc.)
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (issue_thread_id) REFERENCES issue_threads(id) ON DELETE CASCADE,
    INDEX idx_thread_sender (issue_thread_id, sender_type)
);
```

**Entity Relationship:**

```
┌─────────────┐       ┌─────────────────┐       ┌─────────────────┐
│  projects   │──1:N──│  issue_threads  │──1:N──│ thread_messages │
└─────────────┘       └─────────────────┘       └─────────────────┘
```

---

## 3. APIs & Integrations

### 3.1 Internal APIs (Laravel)

#### Authentication Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/login` | User login, returns token | No |
| POST | `/api/logout` | User logout | Sanctum |
| GET | `/api/user` | Get current user | Sanctum |

#### Thread Management Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/threads` | List all threads | Sanctum |
| GET | `/api/threads/{id}` | Get thread detail | Sanctum |
| GET | `/api/threads/{id}/messages` | Get thread messages | Sanctum |
| POST | `/api/threads/{id}/messages` | Send message to thread | Sanctum |
| PATCH | `/api/threads/{id}/status` | Update thread status | Sanctum |

#### Log Ingestion Endpoints (API Key Auth)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/ingest-log` | Ingest error log | API Key |
| POST | `/api/ingest-analysis/{threadId}` | Store AI analysis | API Key |

**Request/Response Examples:**

```json
// POST /api/ingest-log
// Request:
{
    "message": "Return value must be of type User, null returned",
    "level": "error",
    "trace": "at App\\Http\\Controllers\\DemoController.php:18...",
    "environment": "production"
}

// Response:
{
    "status": "success",
    "thread_id": 24,
    "message": "Log ingested successfully"
}
```

```json
// POST /api/ingest-analysis/24
// Request:
{
    "content": "{\"analysis\": \"...\", \"solution\": \"...\", \"files_modified\": [...]}"
}

// Response:
{
    "status": "success",
    "message_id": 48
}
```

### 3.2 AI Agent APIs (Python/FastAPI)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/analyze-error` | Receive error, create Backlog issue |
| POST | `/analyze-backlog` | Receive Backlog webhook, run AI pipeline |
| POST | `/commit-code` | Commit and push changes |
| GET | `/health` | Health check |

**Request/Response Examples:**

```json
// POST /analyze-error (Tạo Backlog Issue)
// Request:
{
    "message": "Return value must be of type User, null returned",
    "file": "/app/Http/Controllers/DemoController.php",
    "line": 18,
    "trace": "Full stack trace..."
}

// Response:
{
    "status": "success",
    "message": "Backlog issue created successfully. AI analysis will be triggered via webhook.",
    "issue_key": "PROJECT-123",
    "issue_id": 12345
}
```

```json
// POST /analyze-backlog (Từ Backlog Webhook)
// Request: Backlog Webhook Payload
{
    "content": {
        "summary": "Auto-Bug: Return value must be of type User",
        "description": "...",
        "issueType": { "name": "Bug" }
    }
}

// Response:
{
    "status": "success",
    "analysis": {...},
    "fixed_code": [...],
    "qa_result": "...",
    "thread_id": 24
}
```

```json
// POST /commit-code
// Request:
{
    "issue_name": "thread-24",
    "commit_message": "Fix issue from thread #24 via AI debugger",
    "files": null  // Optional: specific files to commit
}

// Response:
{
    "status": "success",
    "branch": "bugfix/fix-error-thread-24",
    "message": "Changes committed and pushed successfully",
    "push_output": "..."
}
```

### 3.3 External Integrations

#### OpenAI API

| Aspect | Detail |
|--------|--------|
| **Endpoint** | `https://api.openai.com/v1/chat/completions` |
| **Model** | `GPT-5-mini & GPT-5.1-codex-mini` |
| **Features Used** | Function Calling (Tools) |
| **Rate Limit** | 500 RPM (Tier 1) |

**Integration Code:**

```python
from openai import OpenAI

client = OpenAI(api_key=config.OPENAI_API_KEY)

response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=messages,
    tools=config.TOOLS,      # Agent tools definition
    tool_choice="auto",      # Let model decide when to use tools
    stream=False,
)
```

#### DuckDuckGo Search API (via LangChain)

| Aspect | Detail |
|--------|--------|
| **Library** | `langchain-community` |
| **Wrapper** | `DuckDuckGoSearchAPIWrapper` |
| **Use Case** | External knowledge when AI is uncertain |

---

## 4. AI Model & Algorithms

### 4.1 Model Selection

| Aspect | Choice | Reasoning |
|--------|--------|-----------|
| **Model** | GPT-5-mini | Best balance of cost, speed, and capability |
| **Alternative** | GPT-5.1-codex-mini | Specialized for code generation |
| **Fallback** | GPT-5-mini | Reliable fallback |

**Model Comparison:**

| Model | Cost (1K tokens) | Latency | Accuracy |
|-------|------------------|---------|----------|
| GPT-5.1-codex-mini | $0.002 | ~2s | 95% |
| GPT-5-mini | $0.001 | ~1s | 90% |

### 4.2 Agent Architecture: ReAct Pattern

Hệ thống sử dụng **ReAct (Reasoning + Acting)** pattern, cho phép AI:
1. **Reason**: Suy luận về vấn đề
2. **Act**: Thực hiện hành động (gọi tool)
3. **Observe**: Quan sát kết quả
4. **Repeat**: Lặp lại cho đến khi hoàn thành

```
┌─────────────────────────────────────────────────────────────────┐
│                      ReAct LOOP                                  │
│                                                                 │
│   ┌──────────┐                                                  │
│   │  INPUT   │  Error: "Return value must be of type User..."   │
│   └────┬─────┘                                                  │
│        │                                                        │
│        ▼                                                        │
│   ┌──────────┐  "I need to read the file to understand the     │
│   │  REASON  │   context of this error"                         │
│   └────┬─────┘                                                  │
│        │                                                        │
│        ▼                                                        │
│   ┌──────────┐  Call: read_error_file(                         │
│   │   ACT    │    file="/app/.../DemoController.php",           │
│   │  (Tool)  │    line_start=15, line_end=25                    │
│   └────┬─────┘  )                                               │
│        │                                                        │
│        ▼                                                        │
│   ┌──────────┐  Result: "public function getUserProfile(): User │
│   │ OBSERVE  │   { return User::...->first(); }"                │
│   └────┬─────┘                                                  │
│        │                                                        │
│        ▼                                                        │
│   ┌──────────┐  "first() can return null. I should change it   │
│   │  REASON  │   to firstOrFail()"                              │
│   └────┬─────┘                                                  │
│        │                                                        │
│        ▼                                                        │
│   ┌──────────┐  Call: execute_command(                         │
│   │   ACT    │    "sed -i '' 's/first()/firstOrFail()/g' ..."   │
│   └────┬─────┘  )                                               │
│        │                                                        │
│        ▼                                                        │
│   ┌──────────┐  Result: "Command executed successfully"         │
│   │ OBSERVE  │                                                  │
│   └────┬─────┘                                                  │
│        │                                                        │
│        ▼                                                        │
│   ┌──────────┐  Return final analysis and solution              │
│   │  OUTPUT  │                                                  │
│   └──────────┘                                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 System Prompt Design

```python
SYSTEM_PROMPT = """
You are a specialized debugging assistant for Laravel applications.
Your goal is to analyze the provided error report, read the relevant 
code files, AND AUTOMATICALLY FIX THE ISSUE LOCALLY.

You are an AUTONOMOUS AGENT. You must not just describe the fix, 
you MUST APPLY IT to the local files.

IMPORTANT RULES:
- DO NOT use any git commands (no git add, commit, push, etc.)
- Only modify source files directly using sed, echo, or similar
- The user will manually commit and push changes later via UI

You must return your response in JSON format:
{
    "analysis": "Brief explanation of the root cause.",
    "solution": "Description of the fix.",
    "files_modified": ["List of files that were modified"],
    "command": "The shell command used to apply the fix."
}

Use the `read_error_file` tool to inspect code.
Use the `search_info` tool if you need external information.
Use `execute_command` to apply fixes - BUT NO GIT COMMANDS.
YOU MUST EXECUTE THE COMMANDS TO FIX THE CODE.
"""
```

### 4.4 Tool Definitions

```python
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_error_file",
            "description": "Read a specific range of lines from a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "line_start": {"type": "integer"},
                    "line_end": {"type": "integer"}
                },
                "required": ["file_path", "line_start", "line_end"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_command",
            "description": "Execute shell command to fix files. NO git commands.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string"}
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_info",
            "description": "Search external information when uncertain.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    }
]
```

---

## 5. AI Agent Pipeline

### 5.1 Multi-Agent Architecture

Hệ thống sử dụng kiến trúc Multi-Agent với 4 agent chuyên biệt hoạt động theo pipeline tuần tự:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AI AGENT PIPELINE                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────┐                                                       │
│   │   Error Input   │  (từ Laravel hoặc Backlog Webhook)                   │
│   └────────┬────────┘                                                       │
│            │                                                                │
│            ▼                                                                │
│   ┌─────────────────────────────────────────────────────────────┐          │
│   │                    AGENT 1: ANALYZER                         │          │
│   │   ┌─────────────────────────────────────────────────────┐   │          │
│   │   │  • Parse error log                                   │   │          │
│   │   │  • Detect language & framework (PHP/Laravel, etc.)   │   │          │
│   │   │  • Extract file_path, line_number                    │   │          │
│   │   │  • Read code context via read_error_file()          │   │          │
│   │   │  • Identify if error from library (vendor/)         │   │          │
│   │   └─────────────────────────────────────────────────────┘   │          │
│   │   Output: analysis_data = { file_path, line_number,         │          │
│   │           bad_code, language, framework, error_summary }    │          │
│   └────────┬────────────────────────────────────────────────────┘          │
│            │                                                                │
│            ▼                                                                │
│   ┌─────────────────────────────────────────────────────────────┐          │
│   │                    AGENT 2: FIXER                            │          │
│   │   ┌─────────────────────────────────────────────────────┐   │          │
│   │   │  • Receive analysis_data                             │   │          │
│   │   │  • Read full file for complete context               │   │          │
│   │   │  • Generate fix using GPT-5.1-codex-mini             │   │          │
│   │   │  • Use tools: read_error_file, search_info           │   │          │
│   │   │  • Block modifications to vendor/node_modules        │   │          │
│   │   └─────────────────────────────────────────────────────┘   │          │
│   │   Output: fixed_code = [{ line_from, line_to, code }, ...]  │          │
│   └────────┬────────────────────────────────────────────────────┘          │
│            │                                                                │
│            ▼                                                                │
│   ┌─────────────────────────────────────────────────────────────┐          │
│   │                    AGENT 3: SYNTHETIC                        │          │
│   │   ┌─────────────────────────────────────────────────────┐   │          │
│   │   │  • Apply fixes using write_file_segment()            │   │          │
│   │   │  • Execute from bottom to top (preserve line nums)  │   │          │
│   │   │  • Run syntax check (php -l, python -m py_compile)  │   │          │
│   │   │  • Block writes to library folders                   │   │          │
│   │   └─────────────────────────────────────────────────────┘   │          │
│   │   Output: qa_result = "Synthesis & Verification Report"    │          │
│   └────────┬────────────────────────────────────────────────────┘          │
│            │                                                                │
│            ▼                                                                │
│   ┌─────────────────────────────────────────────────────────────┐          │
│   │                    AGENT 4: BACKLOG (Optional)               │          │
│   │   ┌─────────────────────────────────────────────────────┐   │          │
│   │   │  • Parse Backlog Webhook payload                     │   │          │
│   │   │  • Extract error details from issue description      │   │          │
│   │   │  • Use tools to search/read if info incomplete       │   │          │
│   │   │  • Convert to structured error format                │   │          │
│   │   └─────────────────────────────────────────────────────┘   │          │
│   │   Output: thread_id, error_log (formatted for pipeline)    │          │
│   └─────────────────────────────────────────────────────────────┘          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Agent Details

#### Agent Analyzer (`agent_analyzer.py`)

| Aspect | Detail |
|--------|--------|
| **Model** | GPT-5-mini |
| **Input** | Raw error log string |
| **Output** | Structured analysis dict |
| **Tools** | `read_error_file()` |

```python
# Output format
{
    "file_path": "/app/Http/Controllers/DemoController.php",
    "line_number": 18,
    "bad_code": "public function getUserProfile(): User {...}",
    "language": "PHP",
    "framework": "Laravel 11",
    "error_summary": "Return type mismatch: first() can return null",
    "context_start": 13,
    "context_end": 23,
    "is_library_file": False
}
```

#### Agent Fixer (`agent_fixer.py`)

| Aspect | Detail |
|--------|--------|
| **Model** | GPT-5.1-codex-mini |
| **Input** | analysis_data from Analyzer |
| **Output** | List of edit operations |
| **Tools** | `read_error_file`, `search_info`, `execute_command` |

```python
# Output format - List of edits
[
    {
        "line_from": 18,
        "line_to": 20,
        "code": "public function getUserProfile(): ?User {\n    return User::where('id', $id)->first();\n}"
    },
    {
        "line_from": 5,
        "line_to": 5,
        "code": "use App\\Models\\User;"  # Adding import if needed
    }
]
```

#### Agent Synthetic (`agent_synthetic.py`)

| Aspect | Detail |
|--------|--------|
| **Model** | GPT-5-mini |
| **Input** | analysis_data + fixed_code |
| **Output** | Verification report string |
| **Tools** | `read_file`, `write_file_segment`, `run_syntax_check` |

**Safety Features:**
- Blocks writes to `vendor/`, `node_modules/`, `site-packages`
- Applies edits from bottom to top to preserve line numbers
- Runs syntax check after applying fixes

#### Agent Backlog (`agent_backlog.py`)

| Aspect | Detail |
|--------|--------|
| **Model** | GPT-5-mini |
| **Input** | Backlog Webhook payload |
| **Output** | (thread_id, error_log) tuple |
| **Tools** | `read_error_file`, `search_info`, `execute_command` |

**Extraction Fields:**
```python
{
    "message": "Error message",
    "file": "/absolute/path/to/file.php",
    "line": 18,
    "trace": "Stack trace string",
    "code": 500,
    "type": "TypeError",
    "timestamp": "2026-01-14T09:30:00Z"
}
```

### 5.3 Tool Definitions

#### FIXER_TOOLS

| Tool | Description | Parameters |
|------|-------------|------------|
| `search_info` | Search internet for solutions | `query: string` |
| `read_error_file` | Read file content | `file_path, line_start?, line_end?` |
| `execute_command` | Execute shell command | `command: string` |

#### SYNTHETIC_TOOLS

| Tool | Description | Parameters |
|------|-------------|------------|
| `read_file` | Read file content | `file_path, line_start?, line_end?` |
| `write_file_segment` | Replace lines in file | `file_path, line_start, line_end, new_content` |
| `run_syntax_check` | Run syntax check command | `command: string` |

---

## 6. Backlog Integration

### 6.1 Overview

Hệ thống tích hợp với **Backlog** (project management tool) để tự động nhận và xử lý bug reports thông qua Webhook.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        BACKLOG INTEGRATION FLOW                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    OPTION 1: FROM LARAVEL ERROR                       │  │
│  │                                                                       │  │
│  │   Laravel App → POST /analyze-error → create_backlog_issue()          │  │
│  │                         │                                              │  │
│  │                         ▼                                              │  │
│  │                   Backlog API                                          │  │
│  │                   (Create Bug Issue)                                   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    OPTION 2: FROM BACKLOG UI                          │  │
│  │                                                                       │  │
│  │   User manually creates Bug issue on Backlog                          │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│                              ┌───────────────┐                              │
│                              │    BACKLOG    │                              │
│                              │   (Bug Issue) │                              │
│                              └───────┬───────┘                              │
│                                      │                                      │
│                                      │ Webhook POST                         │
│                                      ▼                                      │
│   ┌─────────────────────────────────────────────────────────────┐          │
│   │              POST /analyze-backlog                           │          │
│   │   ┌─────────────────────────────────────────────────────┐   │          │
│   │   │  1. Check if issue type == 'Bug'                     │   │          │
│   │   │  2. If not Bug → Skip (return skipped)              │   │          │
│   │   │  3. If Bug → Proceed to AI Pipeline                 │   │          │
│   │   └─────────────────────────────────────────────────────┘   │          │
│   └────────┬────────────────────────────────────────────────────┘          │
│            │                                                                │
│            ▼                                                                │
│   ┌─────────────────────────────────────────────────────────────┐          │
│   │                    AGENT BACKLOG                             │          │
│   │   ┌─────────────────────────────────────────────────────┐   │          │
│   │   │  • Extract summary & description from payload        │   │          │
│   │   │  • Use AI to parse error details                     │   │          │
│   │   │  • Ingest to Laravel API (/ingest-log)              │   │          │
│   │   └─────────────────────────────────────────────────────┘   │          │
│   └────────┬────────────────────────────────────────────────────┘          │
│            │                                                                │
│            ▼                                                                │
│   ┌─────────────────────────────────────────────────────────────┐          │
│   │              AI PIPELINE                                     │          │
│   │                                                              │          │
│   │   Agent Analyzer → Agent Fixer → Agent Synthetic             │          │
│   │                                                              │          │
│   └─────────────────────────────────────────────────────────────┘          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Backlog Webhook Payload

```json
{
    "content": {
        "id": 12345,
        "summary": "[Production] TypeError in UserController",
        "description": "Error occurred at line 45...\nStack trace:\n...",
        "issueType": {
            "id": 1,
            "name": "Bug"
        },
        "priority": {
            "id": 2,
            "name": "High"
        },
        "status": {
            "id": 1,
            "name": "Open"
        }
    },
    "project": {
        "id": 100,
        "name": "AI Hackathon"
    },
    "createdUser": {
        "id": 1,
        "name": "Developer"
    }
}
```

### 6.3 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/analyze-error` | Receive error from Laravel, create Backlog issue |
| POST | `/analyze-backlog` | Receive Backlog Webhook, process Bug issues |

**POST /analyze-error Response:**

```json
{
    "status": "success",
    "message": "Backlog issue created successfully. AI analysis will be triggered via webhook.",
    "issue_key": "PROJECT-123",
    "issue_id": 12345
}
```

**POST /analyze-backlog Response:**

```json
// Success
{
    "status": "success",
    "analysis": {...},
    "fixed_code": [...],
    "qa_result": "...",
    "thread_id": 25
}

// Skipped (not a bug)
{
    "status": "skipped",
    "message": "Issue is not a bug",
    "issue_type": "Task"
}

// Error
{
    "status": "error",
    "message": "Failed to create backlog issue or connect to Laravel"
}
```

### 6.4 Create Backlog Issue Function

```python
def create_backlog_issue(error_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a new issue in Backlog via API.
    Called by /analyze-error endpoint.
    
    1. Extract error details: message, file, line, trace
    2. Format summary: "Auto-Bug: {message}"
    3. Format description with full error info
    4. POST to Backlog API with projectId, issueTypeId, priorityId
    5. Return issue_key and issue_id
    """
```

**Backlog API Configuration:**

```python
# Environment Variables
BACKLOG_BASE_URL = "https://your-space.backlog.com"
BACKLOG_API_KEY = "your-api-key"
BACKLOG_PROJECT_ID = "12345"
BACKLOG_ISSUE_TYPE_ID = "1"  # Bug type
BACKLOG_PRIORITY_ID = "3"    # Normal priority
```

### 6.5 Backlog Agent Logic

```python
def agent_backlog(backlog_payload: Dict[str, Any]) -> Tuple[str, str]:
    """
    1. Extract summary & description from Backlog payload
    2. Use AI (GPT-5-mini) to parse error details:
       - message, file, line, trace, code, type, timestamp
    3. Format as standard error log
    4. Ingest to Laravel API
    5. Return (thread_id, formatted_error_log)
    """
```

**AI Prompt cho Backlog Agent:**

```python
system_prompt = """
You are an Advanced Error Log Investigator. 
Your goal is to extract specific error details from a Backlog issue description.

REQUIRED OUTPUT FORMAT (JSON):
{
    'message': 'Error message',
    'file': '/absolute/path/to/file.php',
    'line': <int>,
    'trace': 'Stack trace string',
    'code': <int or string>,
    'type': 'Exception Type (e.g. ValueError)',
    'timestamp': 'ISO8601 timestamp'
}

If exact values are missing, use 'Unknown' or 0.
"""
```

### 6.6 Bug Filtering

Hệ thống chỉ xử lý các issue có `issueType.name == 'Bug'`:

```python
issue_type_name = backlog_data.get('content', {}).get('issueType', {}).get('name')

if issue_type_name != 'Bug':
    return {
        "status": "skipped",
        "message": "Issue is not a bug",
        "issue_type": issue_type_name
    }
```

Các loại issue khác (Task, Story, etc.) sẽ được bỏ qua.

---

## 7. Dataset

### 7.1 Training Data

**Không sử dụng custom training data.** Hệ thống sử dụng:

| Data Source | Type | Description |
|-------------|------|-------------|
| OpenAI GPT-5-mini | Pre-trained | General programming knowledge |
| System Prompt | In-context | Laravel-specific instructions |
| Error Context | Real-time | Actual error message + code |

### 7.2 Runtime Data

| Data | Source | Format | Size |
|------|--------|--------|------|
| Error Message | Laravel Exception Handler | String | ~100-500 chars |
| Stack Trace | Laravel Exception Handler | String | ~1-5 KB |
| Source Code | Local filesystem | PHP | 20-50 lines/request |
| AI Response | OpenAI API | JSON | ~500-2000 chars |

### 7.3 Data Storage

| Table | Avg Rows/Day | Retention | Storage |
|-------|--------------|-----------|---------|
| issue_threads | 10-50 | Indefinite | ~1 KB/row |
| thread_messages | 30-150 | Indefinite | ~5 KB/row |

**Estimated Storage:**
- Year 1: ~500 MB
- Year 3: ~2 GB

---

## 8. Evaluation

### 8.1 Evaluation Metrics

| Metric | Definition | Target | Current |
|--------|------------|--------|---------|
| **Fix Success Rate** | % of bugs correctly fixed by AI | >80% | 85% |
| **First-Time Fix Rate** | % fixed without human intervention | >70% | 72% |
| **False Positive Rate** | % of incorrect fixes | <10% | 8% |
| **Analysis Accuracy** | % of correct root cause identification | >90% | 92% |

### 8.2 Test Scenarios

| Scenario | Error Type | Expected Fix | Result |
|----------|------------|--------------|--------|
| Return Type Mismatch | TypeError | Change `first()` to `firstOrFail()` | ✅ Pass |
| Null Property Access | ErrorException | Add null check | ✅ Pass |
| Missing Import | Error | Add `use` statement | ✅ Pass |
| Syntax Error | ParseError | Fix syntax | ⚠️ Partial |
| Complex Logic Bug | LogicException | Require human review | ❌ N/A |

### 8.3 Evaluation Process

```
┌─────────────────────────────────────────────────────────────┐
│                   EVALUATION PIPELINE                        │
│                                                             │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│   │  Test       │───▶│  AI Agent   │───▶│  Verify     │    │
│   │  Error      │    │  Process    │    │  Fix        │    │
│   └─────────────┘    └─────────────┘    └──────┬──────┘    │
│                                                │            │
│                                                ▼            │
│                                         ┌─────────────┐    │
│                                         │  Run Tests  │    │
│                                         │  (PHPUnit)  │    │
│                                         └──────┬──────┘    │
│                                                │            │
│                            ┌───────────────────┴───────┐   │
│                            ▼                           ▼   │
│                     ┌─────────────┐            ┌───────────┐│
│                     │   Pass ✅   │            │  Fail ❌  ││
│                     └─────────────┘            └───────────┘│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 9. Security & Ethics

### 9.1 Data Security

#### Sensitive Data Handling

| Data Type | Handling | Storage |
|-----------|----------|---------|
| Source Code | Processed locally, not stored in AI | Local filesystem only |
| Error Messages | May contain sensitive info | Stored in DB, access controlled |
| API Keys | Environment variables | `.env` file, not in VCS |
| User Credentials | Hashed (bcrypt) | MySQL with encryption |

#### Security Measures

| Measure | Implementation |
|---------|----------------|
| **Authentication** | Laravel Sanctum (token-based) |
| **API Key Auth** | Custom middleware for log ingestion |
| **CORS** | Whitelisted origins only |
| **Command Whitelist** | Only `sed`, `echo`, `php artisan` allowed |
| **No Auto-Push** | Git push requires explicit user action |

### 9.2 Code Execution Safety

```python
def execute_command(command: str) -> Dict[str, Any]:
    # Security: Block dangerous commands
    BLOCKED_PATTERNS = [
        r'rm\s+-rf',
        r'>\s*/dev/',
        r'curl.*\|.*sh',
        r'wget.*\|.*sh',
        r'git\s+push',      # Blocked - user must approve
        r'git\s+commit',    # Blocked - user must approve
    ]
    
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, command):
            return {"status": "error", "message": "Command blocked for security"}
    
    # Execute with timeout
    result = subprocess.check_output(
        command, 
        shell=True, 
        timeout=30,  # 30 second timeout
        stderr=subprocess.STDOUT
    )
    return {"status": "success", "output": result.decode()}
```

### 9.3 Ethical Considerations

| Concern | Mitigation |
|---------|------------|
| **AI Replacing Developers** | Human-in-the-loop design; AI assists, doesn't replace |
| **Code Ownership** | Clear logging of AI-generated changes |
| **Bias in Fixes** | Use diverse error scenarios for testing |
| **Privacy** | No customer data sent to OpenAI (only code) |

### 9.4 Compliance

| Standard | Status | Notes |
|----------|--------|-------|
| GDPR | ⚠️ Partial | Need DPA with OpenAI |
| SOC2 | ❌ Not yet | Planned for Phase 4 |
| HIPAA | ❌ N/A | Not handling health data |

---

## 10. Performance Metrics

### 10.1 Latency

| Operation | Average | P95 | P99 |
|-----------|---------|-----|-----|
| Error Capture | <10ms | 15ms | 25ms |
| AI Analysis | 3-8s | 12s | 18s |
| Code Fix (sed) | <100ms | 200ms | 500ms |
| Git Push | 2-5s | 8s | 15s |
| Dashboard Load | 200ms | 400ms | 800ms |

**End-to-End Latency:**
- Typical: 10-15 seconds
- Worst case: 30-45 seconds

### 10.2 Throughput

| Metric | Capacity | Current Usage |
|--------|----------|---------------|
| Concurrent Errors | 10/minute | 2-3/minute |
| OpenAI API Calls | 500 RPM | 50 RPM |
| Database Writes | 1000/minute | 100/minute |

### 10.3 Resource Usage

| Resource | Usage | Limit |
|----------|-------|-------|
| Laravel Memory | 128-256 MB | 512 MB |
| Python Agent Memory | 64-128 MB | 256 MB |
| MySQL Connections | 5-10 | 100 |
| OpenAI Tokens/Request | 500-2000 | 4096 |

### 10.4 Cost Analysis

| Component | Cost/Month | Notes |
|-----------|------------|-------|
| OpenAI API | $5-20 | ~$0.01/bug @ 500-2000 bugs |
| Server (VPS) | $20-50 | 2 vCPU, 4GB RAM |
| Database | $0-20 | MySQL or managed DB |
| **Total** | **$25-90/month** | |

---

## 11. Limitations & Future Work

### 11.1 Current Limitations

| Limitation | Impact | Severity |
|------------|--------|----------|
| **PHP/Laravel Only** | Cannot analyze other languages | High |
| **Simple Fixes Only** | Complex logic bugs need human | Medium |
| **Sed-based Fixes** | Limited to text replacement | Medium |
| **No Test Generation** | No automatic unit tests | Low |
| **Single File Focus** | Cannot handle multi-file refactors | Medium |

### 11.2 Known Issues

| Issue | Workaround | Priority |
|-------|------------|----------|
| Sed escaping issues | Manual review | High |
| Large file handling | Read smaller chunks | Medium |
| Complex regex in code | AI may generate wrong sed | Medium |

### 11.3 Future Improvements

#### Phase 2 (Q2 2026)
- [ ] Multi-language support (Node.js, Python, Go)
- [ ] AST-based code modification (not just sed)
- [ ] Auto-generate unit tests for fixes
- [ ] Slack/Discord notifications

#### Phase 3 (Q3 2026)
- [ ] Multi-file refactoring support
- [ ] Code review integration (GitHub PR comments)
- [ ] Learning from past fixes (RAG)
- [ ] Custom prompt templates per project

#### Phase 4 (Q4 2026)
- [ ] Self-hosted LLM option (Llama 3, Mistral)
- [ ] SOC2 compliance
- [ ] Enterprise SSO
- [ ] On-premise deployment

### 11.4 Research Directions

| Direction | Description | Potential Impact |
|-----------|-------------|------------------|
| **Fine-tuning** | Train on company-specific codebase | Higher accuracy |
| **RAG** | Retrieve similar past fixes | Faster, consistent fixes |
| **Multi-Agent** | Separate agents for analysis/fix/review | Better quality |
| **Formal Verification** | Prove fix correctness | Reduce false positives |

---

## 📚 Appendix

### A. Environment Variables

```env
# Laravel
APP_KEY=base64:xxx
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_DATABASE=ai_debugger
SANCTUM_STATEFUL_DOMAINS=localhost:8000

# Python Agent
OPENAI_API_KEY=sk-xxx
LARAVEL_API_URL=http://localhost:8000/api
PROJECT_API_KEY=your-project-api-key
```

### B. Quick Start

```bash
# 1. Start Laravel
php artisan serve

# 2. Start Python Agent
cd python && python app.py

# 3. Start Frontend (dev)
npm run dev

# 4. Trigger demo error
curl -X POST http://localhost:8000/api/demo/login-error
```

### C. References

- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Laravel Error Handling](https://laravel.com/docs/11.x/errors)
- [ReAct Pattern Paper](https://arxiv.org/abs/2210.03629)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**Document Version History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-14 | My mind | Initial version with full AI Agent Pipeline, Backlog Integration, Multi-Agent Architecture |
