from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_ECHO: bool
    SERVER_HOST: str
    SERVER_PORT: int
    
    api_v1_prefix: str = "/api/v1"
    security_basic: list = [{"basic": []}]
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')    

    def get_db_url(self):
        return (f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

settings = Settings()
