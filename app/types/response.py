from pydantic import BaseModel


class ChatMessage(BaseModel):
    message: str
    report_id: str
    image_data: str = None  # Base64 encoded image

class ChatResponse(BaseModel):
    response: str
    status: str