from urllib.parse import urlencode
import base64
import requests

class SpotifyAuthentication:

    def __init__(self, client_id: str, client_secret: str, redirect_url:str, auth_scope:str, spotify_base_url:str, top_tracks_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.spotify_base_url = spotify_base_url
        self.redirect_url = redirect_url
        self.auth_scope = auth_scope
        self.top_tracks_url = top_tracks_url

    def get_auth_headers(self, state):
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_url,
            "scope": self.auth_scope,
            "state":state
        }
        print(f"{self.spotify_base_url}/authorize?"+urlencode(params))
        return f"{self.spotify_base_url}/authorize?"+urlencode(params)

    def get_tokens(self, code):
        data = {"code": code, "redirect_uri": self.redirect_url, "grant_type": "authorization_code"}
        token_url = f"{self.spotify_base_url}/api/token"
        encoded_credentials = base64.b64encode(self.client_id.encode() + b':' + self.client_secret.encode()).decode("utf-8")
        headers = {
            "Authorization": "Basic " + encoded_credentials,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = requests.post(url=token_url, headers= headers,  data=data)
        response = response.json()
        access_tokens = response.get("access_token")
        # #refresh_token = response.get("refresh_token", refresh_token)
        print(access_tokens)
        return access_tokens

    def get_top_tracks(self, access_tokens):

        user_headers = {
            "Authorization": f"Bearer {access_tokens}",
            "Content-Type": "application/json"
        }
        user_params = {
            "limit": 50,
            "time_range": "long_term"
        }
        url = f"{self.top_tracks_url}/me/top/tracks?"+ urlencode(user_params)
        user_tracks_response = requests.get(url=url, headers=user_headers)
        return user_tracks_response.json()