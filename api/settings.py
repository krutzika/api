from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    client_id: str
    client_secret: str
    redirect_url : str
    auth_scope :str
    spotify_base_url :str
    top_tracks_url: str
    frontend_url : str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra='ignore')
