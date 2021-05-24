from task1.common import loop
from task1.websocket import WebSocketBase


class PublicBinance:
    exchange = 'binance'

    def __init__(self):
        loop.run_until_complete(self.async_init())

    async def async_init(self):
        WebSocketBase('binance_public', self.ws_connect_public, self.ws_on_message)


if __name__ == '__main__':
    binance = PublicBinance()
    loop.run_forever()
