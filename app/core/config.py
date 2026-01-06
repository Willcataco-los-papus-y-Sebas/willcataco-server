from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    app_name: str = "Willcataco Server"
    debug: bool = False
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: int
    environment: str

    # JWTokens
    token_time_expire: int
    token_algorithm : str
    token_key : str

    # Email

    email_sender: str
    email_sender_password: str
    smtp_server: str
    smtp_port: int

    model_config = SettingsConfigDict(env_file=".env")
    
    # CORS
    allowed_origins: list[str] = []

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
        secrets_dir="/run/secrets"
    )

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

config = Config()