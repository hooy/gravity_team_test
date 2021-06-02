import asyncio
import datetime
import logging
import time

from task1.websocket import WebSocketBase
from math import inf


class PublicBinance:
    exchange = "binance"

    def __init__(self):
        self.highest_bid = {"price": -inf, "time": time.time()}
        self.lowest_ask = {"price": inf, "time": time.time()}
        loop = asyncio.new_event_loop()
        loop.create_task(self.init(loop))
        loop.run_forever()

    async def init(self, loop):
        uri = "wss://stream.binance.com:9443/ws/btcusdt@ticker"
        WebSocketBase(
            "binance_public", loop, uri, self._ws_connect_public, self._process_prices
        )

    def _ws_connect_public(self):
        logging.info(f"_ws_connect_public {self.exchange}")

    def _process_prices(self, data):
        best_bid, best_ask = data["b"], data["a"]
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

        print(
            f"Highest bid: {bid} at {bid_time}; Lowest ask: {ask} at {ask_time}"
        )

    def _check_and_update_ask(self, best_ask):
        ask = float(best_ask)
        if ask < self.lowest_ask["price"]:
            self.lowest_ask["price"] = ask
            self.lowest_ask["time"] = time.time()

    def _check_and_update_bid(self, best_bid):
        bid = float(best_bid)
        if bid > self.highest_bid["price"]:
            self.highest_bid["price"] = bid
            self.highest_bid["time"] = time.time()


if __name__ == "__main__":
    # logging.getLogger().setLevel(logging.DEBUG)
    binance = PublicBinance()
