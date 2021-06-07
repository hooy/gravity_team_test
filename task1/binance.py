import asyncio
import datetime
import logging
import time
from asyncio import AbstractEventLoop

from task1.consumer import AbstractAsyncApiConsumer
from task1.websocket import WebSocketBase
from math import inf

# TODO: add URI builder
WS_BTCUSDT_TICKER_URL = "wss://stream.binance.com:9443/ws/btcusdt@ticker"

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
INTRO = f"{'=' * 10}Connected to Binance!{'=' * 10}"


class PublicBinance(AbstractAsyncApiConsumer):
    exchange = "binance"

    def __init__(self, uri: str, print_only_updates: bool = False):
        self.uri = uri
        self.print_only_updates = print_only_updates
        self.updated = 0b00  # first bit -- bid updated, second bit -- ask updated
        self.highest_bid = {"price": -inf, "time": time.time()}
        self.lowest_ask = {"price": inf, "time": time.time()}
        self.loop = asyncio.new_event_loop()
        self.loop.create_task(self.init())
        self.loop.run_forever()

    async def init(self):
        WebSocketBase("binance_public", self)

    def _ws_connect_public(self):
        logging.info(f"_ws_connect_public {self.exchange}")
        print(INTRO)

    def _process_prices(self, data: dict):
        best_bid, best_ask = float(data["b"]), float(data["a"])
        self.updated = 0b00
        self._check_and_update_ask(best_ask)
        self._check_and_update_bid(best_bid)
        if not self.print_only_updates:
            self.print_current_best_prices()
        else:
            if self._at_least_one_is_updated():
                self.print_current_best_prices()

    def _at_least_one_is_updated(self) -> bool:
        return self.updated > 0

    def print_current_best_prices(self):
        # TODO: consider to move bid/ask to own objects and hide all logic there
        bid, bid_time = self.highest_bid["price"], datetime.datetime.fromtimestamp(
            self.highest_bid["time"]
        ).strftime(TIME_FORMAT)
        ask, ask_time = self.lowest_ask["price"], datetime.datetime.fromtimestamp(
            self.lowest_ask["time"]
        ).strftime(TIME_FORMAT)

        print(f"Highest bid: {bid} at {bid_time}; Lowest ask: {ask} at {ask_time}")

    def _check_and_update_ask(self, best_ask: float):
        if best_ask < self.lowest_ask["price"]:
            self.updated = self.updated | 0b01
            self.lowest_ask["price"] = best_ask
            self.lowest_ask["time"] = time.time()

    def _check_and_update_bid(self, best_bid: float):
        if best_bid > self.highest_bid["price"]:
            self.updated = self.updated | 0b10
            self.highest_bid["price"] = best_bid
            self.highest_bid["time"] = time.time()

    def get_loop(self) -> AbstractEventLoop:
        return self.loop

    def on_connect(self):
        self._ws_connect_public()

    def on_message(self, data: dict):
        self._process_prices(data)

    def get_connection_uri(self) -> str:
        return self.uri


if __name__ == "__main__":
    # logging.getLogger().setLevel(logging.DEBUG)
    # TODO: move this to config
    btcusdt_uri = WS_BTCUSDT_TICKER_URL
    binance = PublicBinance(btcusdt_uri, print_only_updates=True)
