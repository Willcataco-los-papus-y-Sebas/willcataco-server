from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    app_name: str = "Willcataco Server"
    debug: bool = False
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: int

    model_config = SettingsConfigDict(env_file=".env")

config = Config()