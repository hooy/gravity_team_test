from abc import ABC, abstractmethod


class AbstractAsyncApiConsumer:
    @abstractmethod
    def get_loop(self):
        pass

    @abstractmethod
    def on_connect(self):
        pass

    @abstractmethod
    def on_message(self, data):
        pass

    @abstractmethod
    def get_connection_uri(self):
        pass
