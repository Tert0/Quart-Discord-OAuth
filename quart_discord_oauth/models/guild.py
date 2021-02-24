from .base import DiscordBaseModel


class Guild(DiscordBaseModel):
    def __init__(self, json):
        self._json = json
        self.name = json["name"]
        self.icon = json["icon"]
        self.id = int(json["id"])
        self.owner = bool(json["owner"])
        self.permissions = json["permissions"]
        self.permissions_new = json["permissions_new"]
        self.features = list(json["features"])

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'owner': self.owner,
            'permissions': self.permissions,
            'permissions_new': self.permissions_new,
            'features': self.features
        }
