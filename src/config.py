from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_ECHO: bool
    REDIS_HOST: str
    REDIS_PORT: int
    SERVER_HOST: str
    SERVER_PORT: int
    
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

    # Basic Authentication
    basic: dict = {
        "type": "http",
        "scheme": "basic"
    }
    security_schemes: dict = {"basic": basic}
    security_basic: list = [{"basic": []}]

    def get_db_url(self):
        return (f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
    
    def get_redis_url(self):
        return (f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}")

settings = Settings()
