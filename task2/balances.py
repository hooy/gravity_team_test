import asyncio

from task2.binance_api import BinanceAPI


async def main():
    binance_api = BinanceAPI(loop)
    server_time = await binance_api.get_server_time()
    print(server_time)

    # loop.run_until_complete(get_account_info(loop))

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())