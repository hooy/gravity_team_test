import asyncio
import datetime
import logging
import string
import time
from task1.consumer import AbstractAsyncApiConsumer
from task1.websocket import WebSocketBase
from math import inf


class PublicBinance(AbstractAsyncApiConsumer):
    exchange = "binance"

    def __init__(self, uri: string):
        self.uri = uri
        self.highest_bid = {"price": -inf, "time": time.time()}
        self.lowest_ask = {"price": inf, "time": time.time()}
        self.loop = asyncio.new_event_loop()
        self.loop.create_task(self.init())
        self.loop.run_forever()

    async def init(self):
        WebSocketBase("binance_public", self)

    def _ws_connect_public(self):
        logging.info(f"_ws_connect_public {self.exchange}")
        print(f"{'=' * 10}Connected to Binance!{'=' * 10}")

    def _process_prices(self, data):
        best_bid, best_ask = float(data["b"]), float(data["a"])
        self._check_and_update_ask(best_ask)
        self._check_and_update_bid(best_bid)
        self.print_current_best_prices()

    def print_current_best_prices(self):
        # TODO: consider to move bid/ask to own objects and hide all logic there
        bid, bid_time = self.highest_bid["price"], datetime.datetime.fromtimestamp(
            self.highest_bid["time"]
        ).strftime("%Y-%m-%d %H:%M:%S")
        ask, ask_time = self.lowest_ask["price"], datetime.datetime.fromtimestamp(
            self.lowest_ask["time"]
        ).strftime("%Y-%m-%d %H:%M:%S")

        print(f"Highest bid: {bid} at {bid_time}; Lowest ask: {ask} at {ask_time}")

    def _check_and_update_ask(self, best_ask: float):
        if best_ask < self.lowest_ask["price"]:
            self.lowest_ask["price"] = best_ask
            self.lowest_ask["time"] = time.time()

    def _check_and_update_bid(self, best_bid: float):
        if best_bid > self.highest_bid["price"]:
            self.highest_bid["price"] = best_bid
            self.highest_bid["time"] = time.time()

    def get_loop(self):
        return self.loop

    def on_connect(self):
        self._ws_connect_public()

    def on_message(self, data):
        self._process_prices(data)

    def get_connection_uri(self):
        return self.uri


if __name__ == "__main__":
    # logging.getLogger().setLevel(logging.DEBUG)
    # TODO: move this to config
    uri = "wss://stream.binance.com:9443/ws/btcusdt@ticker"
    binance = PublicBinance(uri)
