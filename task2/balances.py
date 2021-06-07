import asyncio
import logging

from task2.binance_api import BinanceAPI


async def main():
    binance_api = BinanceAPI(loop)
    # server_time = await binance_api.get_server_time()
    # print(server_time)

    await binance_api.init()

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
