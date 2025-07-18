from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import get_settings

def get_llm():
    settings = get_settings()
    return ChatGoogleGenerativeAI(
        model=settings.model_name or "gemini-2.5-flash",
        google_api_key=settings.google_api_key
    )

