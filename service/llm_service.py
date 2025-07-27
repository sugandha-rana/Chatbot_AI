import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()  # Load GOOGLE_API_KEY from .env

class LLMService:
    _instance = None
    _model = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            api_key = os.getenv("GOOGLE_API_KEY")
            genai.configure(api_key=api_key)
            cls._model = genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-2.5-flash-lite"
        return cls._instance

    @property
    def model(self):
        return self._model
