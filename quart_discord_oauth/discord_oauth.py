import requests
import urllib.parse

from . import exeptions
from .models.user import User
from quart import request
from functools import wraps
from quart import current_app
from cachetools import LRUCache, TTLCache, cached

api_cache = TTLCache(maxsize=50, ttl=550)


class DiscordOAuth2:
    DISCORD_TOKEN_URL = "https://discord.com/api/oauth2/token"
    DISCORD_API_URL = "https://discord.com/api"

    def __init__(self, app, client_id, client_secret, redirect_uri, scope):
        self.app = app
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope
        redirect_url = urllib.parse.quote(redirect_uri)
        self.DISCORD_LOGIN_URL = f'https://discord.com/api/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_url}&response_type=code&scope={scope}'
        app.discord_oauth = self

    def get_access_token(self, code):
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "scope": self.scope
        }
        access_token = requests.post(url=DiscordOAuth2.DISCORD_TOKEN_URL, data=payload).json()
        return access_token.get("access_token")

    def get_refresh_token(self, code):
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "scope": self.scope
        }
        access_token = requests.post(url=DiscordOAuth2.DISCORD_TOKEN_URL, data=payload).json()
        return access_token.get("refresh_token")

    def refresh_token(self, refresh_token):
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            'refresh_token': refresh_token,
            "redirect_uri": self.redirect_uri,
            "scope": self.scope
        }
        access_token = requests.post(url=DiscordOAuth2.DISCORD_TOKEN_URL, data=payload).json()
        return access_token

    @cached(cache=api_cache)
    def fetch_from_api(self, route, token=None, method='GET'):
        print("Fetching from Api")
        print(api_cache.items())

        headers = {}
        if token:
            headers = {
                "Authorization": f'Bearer {token}'
            }
        if method == 'GET':
            response = requests.get(url=f'{self.DISCORD_API_URL}{route}', headers=headers)
            data = response.json()
            if response.status_code == 401:
                raise exeptions.Unauthorized
            if response.status_code == 429:
                raise exeptions.RateLimited(data, response.headers)
            return data

    async def fetch_user(self):
        data = await request.json
        try:
            token = data['token']
        except TypeError:
            raise exeptions.InvalidRequest
        user = self.fetch_from_api("/users/@me", token)
        return User(user)

    async def fetch_guilds(self):
        data = await request.json
        try:
            token = data['token']
        except TypeError:
            raise exeptions.InvalidRequest
        return self.fetch_from_api("/users/@me/guilds", token)

    async def get_auth_status(self):
        data = await request.json
        try:
            token = data['token']
        except TypeError:
            raise exeptions.InvalidRequest
        return self.fetch_from_api("/oauth2/@me", token)

    async def is_authenticated(self):
        data = await request.json
        try:
            token = data['token']
        except TypeError:
            return False
        try:
            return not 'code' in await self.get_auth_status()
        except:
            return False


def requires_authorization(view):
    @wraps(view)
    async def wrapper(*args, **kwargs):
        data = await request.json
        try:
            token = data['token']
        except TypeError:
            raise exeptions.InvalidRequest
        if not await current_app.discord_oauth.is_authenticated():
            raise exeptions.Unauthorized
        return await view(*args, **kwargs)

    return wrapper
