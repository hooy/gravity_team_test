import asyncio
import logging
from typing import Dict, List
from task2.binance_api import BinanceAPI


def printBalances(balances: List[Dict]):
    for b in balances:
        free, asset = float(b["free"]), b["asset"]
        if free != 0:
            print(f"{asset}: {free}")


def pretty_print(account_info: Dict, headers):
    print(f"Date: {headers['Date']}")
    printBalances(account_info["balances"])


async def main():
    binance_api = BinanceAPI(loop)
    # server_time = await binance_api.get_server_time()
    # print(server_time)

    await binance_api.init()
    while True:
        account_info, headers = await binance_api.get_account_info()
        pretty_print(account_info, headers)
        await asyncio.sleep(5)  # TODO: IMplement checking if we are not spaming a lot

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
