import abc


class DiscordBaseModel(abc.ABC, object):
    @abc.abstractmethod
    def __init__(self, json):
        self._json = json
