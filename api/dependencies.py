from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from api.settings import Settings
from api.spotify_auth import SpotifyAuthentication


@lru_cache
def get_settings() -> Settings:
    return Settings()

SettingsDependency = Annotated[Settings, Depends(get_settings)]

def get_spotify_auth(settings : SettingsDependency)->SpotifyAuthentication:
    return SpotifyAuthentication(
    client_id = settings.client_id,
    client_secret=settings.client_secret,
    spotify_base_url=settings.spotify_base_url,
    redirect_url=settings.redirect_url,
    auth_scope=settings.auth_scope,
    top_tracks_url=settings.top_tracks_url
    )

SpotifyAuthenticationDependency = Annotated[SpotifyAuthentication, Depends(get_spotify_auth)]