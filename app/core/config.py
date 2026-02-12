import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field

load_dotenv()

# pydantic을 사용하면 .env에 해당 변수가 없는 경우 에러를 발생, 단순 f string의 경우 해당 환경 변수가 없을 때 None으로 들어가기 때문에 이를 방지할 수 있음
class Settings(BaseSettings):
   POSTGRES_USER: str
   POSTGRES_PASSWORD: str
   POSTGRES_SERVER: str
   POSTGRES_PORT: str
   POSTGRES_DB: str
   GEMINI_API_KEY: str

   @property
   def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
   model_config = SettingsConfigDict(env_file=".env") 

settings = Settings()