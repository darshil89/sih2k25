from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from app.types.response import ChatMessage, ChatResponse

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

@app.post("/api/chat/{report_id}")
async def chat_with_report(report_id: str, chat_message: ChatMessage):
    """
    Chat endpoint for interacting with UFDR reports
    """
    try:
        response = f"Received message for report {report_id}: {chat_message.message}"
        
        if chat_message.image_data:
            response += " (Image received and processed)"
        
        return ChatResponse(
            response=response,
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=port, reload=True)