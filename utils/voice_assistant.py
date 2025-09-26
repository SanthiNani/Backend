# backend/utils/voice_assistant.py
import speech_recognition as sr
from gtts import gTTS
from tempfile import NamedTemporaryFile
import os
from models.health_llm import HealthLLM  # Your LLM class

# Initialize LLM
llm = HealthLLM()

def transcribe_audio_file(file_path: str) -> str:
    """
    Convert an uploaded audio file into text using speech recognition.
    """
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"Transcribed text: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return ""
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return ""

def summarize_medical_query(audio_path: str) -> str:
    """
    Transcribe audio and generate a medical summary using the LLM.
    """
    text = transcribe_audio_file(audio_path)
    if not text:
        return "Sorry, the audio could not be understood."
    
    # Use LLM to generate medical response/summary
    summary = llm.generate_text(text)
    print(f"Medical summary: {summary}")
    return summary

def audio_response(text: str):
    """
    Convert text response into audio (optional for sending back to patient).
    """
    if not text:
        text = "Sorry, no response available."
    tts = gTTS(text=text, lang='en')
    with NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
        tts.save(fp.name)
        os.system(f"start {fp.name}")  # Windows
        # Linux: os.system(f"mpg123 {fp.name}")
        # Mac: os.system(f"afplay {fp.name}")
