import pyttsx3
import openai
from google.cloud import speech_v1p1beta1 as speech

# Initialize TTS engine
tts_engine = pyttsx3.init()

# Speech-to-Text using Google Speech API
def voice_to_text(audio_file_path: str) -> str:
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=open(audio_file_path, "rb").read())
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    response = client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript

# Text-to-Speech
def speak_text(text: str):
    tts_engine.say(text)
    tts_engine.runAndWait()
