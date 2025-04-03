import secrets
from fastapi import FastAPI, Response, Request
from api.dependencies import SpotifyAuthenticationDependency, SettingsDependency
app = FastAPI()

@app.get("/login")
def get_authentication(spotify: SpotifyAuthenticationDependency):
    state = secrets.token_hex(16)
    url = spotify.get_auth_headers(state=state)
    response = Response(headers={"location": url}, status_code=307)
    response.set_cookie(key="spotify_auth_state", value=state, httponly=True, secure=False)
    return response

@app.get("/callback")
def spotify_callback(
        request : Request,
        spotify: SpotifyAuthenticationDependency,
        settings: SettingsDependency):
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    print(f"code={code}")
    if not code:
        return {"error": "Authorization code not found"}
    access_token = spotify.get_tokens(code)
    response = Response(headers={"location": "http://127.0.0.1:8000"}, status_code=307)
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=False)
    return response

@app.get("/top_tracks")
def top_tracks(
        request: Request,
        spotify: SpotifyAuthenticationDependency
):
    access_token = request.get("access_token")
    print(f"access_token = {access_token}")
    top_track_json = spotify.get_top_tracks(access_token)
    return top_track_json

