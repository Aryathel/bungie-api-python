import abc


class ClientBase(abc.ABC):
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    @abc.abstractmethod
    def get(self, response_):
        pass
