from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS settings to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    user_message: str

@app.post("/chat")
def chat_endpoint(message: Message):
    # Replace this with your AI logic later
    return {"response": f"Legal response to: {message.user_message}"}
