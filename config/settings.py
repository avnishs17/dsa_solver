from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    google_api_key: str
    model_name: str = "gemini-1.5-flash"
    app_title: str = "DSA Solver"

    class Config:
        env_file = ".env"
        extra = "allow"

_settings = None

def get_settings():
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
