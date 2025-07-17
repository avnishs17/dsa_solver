import asyncio
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
import json
import os
from dotenv import load_dotenv
from typing import Dict, Any, AsyncGenerator
from langchain_core.messages import BaseMessage

from app.mentor import DSAMentor
from app.logger import get_logger
from app.config import get_settings
from app.models import ChatMessage

# Load environment variables
load_dotenv()

logger = get_logger(__name__)
settings = get_settings()

# Global mentor instance
mentor = None

class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle LangChain messages."""
    def default(self, o: Any) -> Any:
        if isinstance(o, BaseMessage):
            return o.dict()
        return super().default(o)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global mentor
    
    # Startup
    logger.info("Starting DSA Mentor application...")
    try:
        mentor = DSAMentor()
        logger.info("DSA Mentor initialized successfully")
        yield
    except Exception as e:
        logger.error(f"Failed to initialize DSA Mentor: {e}")
        raise
    finally:
        # Shutdown
        logger.info("Shutting down DSA Mentor application...")

# Create FastAPI app with lifespan
app = FastAPI(
    title="DSA Mentor API",
    description="AI-powered DSA mentoring assistant",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "DSA Mentor API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "mentor_initialized": mentor is not None,
        "version": "1.0.0"
    }

async def stream_generator(chat_request: ChatMessage) -> AsyncGenerator[str, None]:
    """Generator for streaming chat responses."""
    try:
        user_message = chat_request.content
        thread_id = chat_request.session_id or "default_session"
        
        if not user_message.strip():
            yield f"data: {json.dumps({'error': 'Empty message received'})}\n\n"
            return

        if mentor is None:
            yield f"data: {json.dumps({'error': 'Mentor not initialized'})}\n\n"
            return

        async for event in mentor.process_message(user_message, thread_id):
            json_event = json.dumps(event, cls=CustomJSONEncoder)
            yield f"data: {json_event}\n\n"
            await asyncio.sleep(0.01)  # Small delay to prevent overwhelming the client

    except Exception as e:
        logger.error(f"Error in stream_generator: {e}", exc_info=True)
        error_event = json.dumps({"error": f"Error processing message: {str(e)}"})
        yield f"data: {error_event}\n\n"

@app.post("/chat/stream")
async def chat_stream(chat_request: ChatMessage):
    """Endpoint for streaming chat responses."""
    return StreamingResponse(stream_generator(chat_request), media_type="text/event-stream")

if __name__ == "__main__":
    # Check for required environment variables
    required_env_vars = ["GOOGLE_API_KEY"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        print(f"Error: Missing required environment variables: {missing_vars}")
        print("Please set these variables in your .env file")
        exit(1)
    
    logger.info("Starting DSA Mentor server...")
    uvicorn.run(
        "app.main:app", 
        host=settings.host, 
        port=settings.port, 
        reload=settings.debug,
        log_level="info"
    )
