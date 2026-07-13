from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # instructs pydantic to read from a loacl .env file
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    # server name
    APP_NAME: str = 'PulseAIController'
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = '0.0.0.0'

    #Databases
    DATABASE_URL: str = Field(
        default='postgresql://postgres:postgres@localhost:5432/pulseai',
        validation_alias='DATABASE_URL',
    )
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        validation_alias="REDIS_URL"
    )

    # Upstream LLM Provider API Keys
    OPENAI_API_KEY: str = Field(default="", validation_alias="OPENAI_API_KEY")
    GEMINI_API_KEY: str = Field(default="", validation_alias="GEMINI_API_KEY")
    GROQ_API_KEY: str = Field(default="", validation_alias="GROQ_API_KEY")
    ANTHROPIC_API_KEY: str = Field(default="", validation_alias="ANTHROPIC_API_KEY")

settings = Settings()
    