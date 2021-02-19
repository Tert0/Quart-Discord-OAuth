class Guild(object):
    def __init__(self, json):
        self._json = json
        self.name = json["name"]
        self.discriminator = json["discriminator"]
        self.id = int(json["id"])
        self.locale = json["locale"]
        self.email = json["email"]

    def __str__(self):
        return f'{self._json}'
