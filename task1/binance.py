import asyncio
import logging
from task1.websocket import WebSocketBase


class PublicBinance:
    exchange = "binance"

    def __init__(self):
        loop = asyncio.new_event_loop()
        loop.create_task(self.init(loop))
        loop.run_forever()

    async def init(self, loop):
        uri = "wss://stream.binance.com:9443/ws/btcusdt@ticker"
        WebSocketBase("binance_public", loop, uri, self._ws_connect_public, self._ws_on_message)

    def _ws_connect_public(self):
        logging.info(f"_ws_connect_public {self.exchange}")

    def _ws_on_message(self, data):
        print(data)


if __name__ == "__main__":
    # logging.getLogger().setLevel(logging.DEBUG)
    binance = PublicBinance()
