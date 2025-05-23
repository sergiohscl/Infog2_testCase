from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    database_url: str
    environment: str
    whatsapp_api_url: str
    whatsapp_api_url_send: str
    apikey: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
