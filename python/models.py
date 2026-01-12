"""
Data models and vector store management for Laravel Error Analysis Agent.
"""
import os
import glob
from datetime import datetime
from typing import Optional, List, Dict, Any
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.document import Document


# Laravel project path
LARAVEL_PROJECT_PATH = os.path.join(os.path.dirname(__file__), '../my-laravel-app')

# Initialize embeddings
embeddings = OpenAIEmbeddings(api_key=os.environ.get("OPENAI_API_KEY"))

# Global vector store
vector_store: Optional[FAISS] = None


class AnalysisRecord:
    """Data model for analysis records."""
    
    def __init__(self, 
                 error_type: str, 
                 error_message: str, 
                 file: str, 
                 line: str,
                 analysis: str,
                 error_details: Dict[str, Any],
                 status: str = "success"):
        self.id = None  # Will be set when added to history
        self.timestamp = datetime.now().isoformat()
        self.error_type = error_type
        self.error_message = error_message
        self.file = file
        self.line = line
        self.analysis = analysis
        self.error_details = error_details
        self.status = status
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "error_type": self.error_type,
            "error_message": self.error_message,
            "file": self.file,
            "line": self.line,
            "analysis": self.analysis,
            "error_details": self.error_details,
            "status": self.status
        }


class AnalysisHistory:
    """Manages analysis history in memory."""
    
    def __init__(self, max_size: int = 50):
        self.history: List[AnalysisRecord] = []
        self.max_size = max_size
        self.latest: Optional[AnalysisRecord] = None
    
    def add(self, record: AnalysisRecord) -> AnalysisRecord:
        """Add a new analysis record."""
        record.id = len(self.history) + 1
        self.history.append(record)
        
        # Keep only last max_size analyses
        if len(self.history) > self.max_size:
            self.history.pop(0)
        
        self.latest = record
        return record
    
    def get_latest(self) -> Optional[Dict[str, Any]]:
        """Get the latest analysis."""
        if self.latest is None:
            return None
        return self.latest.to_dict()
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get analysis history with limit."""
        limited = self.history[-min(limit, self.max_size):]
        return [record.to_dict() for record in limited]


# Global analysis history instance
analysis_history = AnalysisHistory()


def index_laravel_codebase() -> None:
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


def get_vector_store() -> Optional[FAISS]:
    """Get the global vector store instance."""
    return vector_store
