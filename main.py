from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import logging
from app.types.response import ChatMessage, ChatResponse
from app.config import get_neo4j_client, get_chroma_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

port = 8080

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Server is running"}

# Test db 
@app.get("/api/test-db")
async def test_database():
    """Test database connection"""
    try:
        get_neo4j_client()
        get_chroma_client()
        return {"message": "Database connections successful"}
    except Exception as e:
        logger.error(f"Error getting database clients: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat/{report_id}")
async def chat_with_report(report_id: str, chat_message: ChatMessage):
    """
    Chat endpoint for interacting with UFDR reports
    """
    try:        
        return ChatResponse(
            response=f"Response from the server",
            status="success"
        )
    except Exception as e:
        logger.error(f"Chat processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=port, reload=True)