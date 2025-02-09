import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
from mistralai import Mistral
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
app = FastAPI()

# Mistral API key
#api_key = os.getenv("MISTRAL_API_KEY")
# fine-tuned model ID
#fine_tuned_model_id = os.getenv("FINE_TUNED_MODEL_ID")

api_key = st.secrets["MISTRAL_API_KEY"]
fine_tuned_model_id = st.secrets["FINE_TUNED_MODEL_ID"]

print("🔍 Debug: FINE_TUNED_MODEL =", fine_tuned_model_id)
print("🔍 Debug: OPENAI_API_KEY =", api_key)

client = Mistral(api_key = api_key)
class Message(BaseModel):
    text: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(message: Message):
    try:
        chat_response = client.chat.complete(
            model=fine_tuned_model_id,
            messages=[
                {
                    "role": "user",
                    "content": message.text,
                },
            ],
            max_tokens=200,
        )
        response_text = chat_response.choices[0].message.content
        return ChatResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        print(detail)

    print(chat_response.choices[0].message.content)
    return ChatResponse(response=response_text)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Chatbot API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

message = Message(text="How are you ?")
response = chat(message)
print(response)