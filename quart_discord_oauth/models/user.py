import json
from quart import current_app


class User(object):
    ROUTE = '/users/@me'

    def __init__(self, json):
        self._json = json
        self.username = json["username"]
        self.discriminator = json["discriminator"]
        self.id = int(json["id"])
        self.locale = json["locale"]
        self.email = json["email"]
        self.avatar_url = f'https://cdn.discordapp.com/avatars/{self.id}/{json["avatar"]}.png'

        self.__dict__ = {
            'id': self.id,
            'username': self.username,
            'discriminator': self.discriminator,
            'locale': self.locale,
            'email': self.email,
            'avatar_url': self.avatar_url
        }

    def json(self):
        return json.dumps(self._json)
