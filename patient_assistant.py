# backend/patient_assistant.py
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Form
import whisper
import openai
from config import settings

router = APIRouter()

# Load Whisper model for audio transcription
whisper_model = whisper.load_model("small")

# Set Gemini API key
openai.api_key = settings.GEMINI_API_KEY

async def get_gemini_response(user_input: str) -> str:
    """
    Send user query (text) to Google Gemini Pro and get response.
    """
    response = openai.ChatCompletion.create(
        model="gemini-pro-1",
        messages=[
            {"role": "system", "content": "You are a helpful medical assistant."},
            {"role": "user", "content": user_input}
        ],
        temperature=0.3,
        max_tokens=300
    )
    return response["choices"][0]["message"]["content"]

@router.websocket("/assistant/stream")
async def assistant_stream(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            message = await ws.receive_json()
            
            # Determine if it's text or voice
            if message.get("type") == "text":
                user_input = message["content"]
            elif message.get("type") == "voice":
                audio_bytes = message["content"].encode("latin1")  # send audio as bytes
                temp_file = "temp_audio.wav"
                with open(temp_file, "wb") as f:
                    f.write(audio_bytes)

                # Transcribe audio
                transcription_result = whisper_model.transcribe(temp_file)
                user_input = transcription_result["text"]
            else:
                await ws.send_json({"error": "Invalid message type"})
                continue

            # Send to Gemini
            assistant_response = await get_gemini_response(user_input)

            # Send back transcription (for voice) and assistant reply
            await ws.send_json({
                "user_input": user_input,
                "assistant_response": assistant_response
            })

    except WebSocketDisconnect:
        print("Assistant WebSocket disconnected")
