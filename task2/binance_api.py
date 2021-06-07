import logging
from asyncio import AbstractEventLoop
from typing import Dict, AnyStr

import hashlib
import hmac
import time
import aiohttp

API_VERSION = "v3"
API_BASE_URL = "https://api.binance.com/api"
ACCOUNT_URL = f"{API_BASE_URL}/{API_VERSION}/account"
TIME_URL = f"{API_BASE_URL}/{API_VERSION}/time"
SECRET = "OQ8JbgsHNd4Nq8MmLIHfsPkzQWgUajLwwSV4w3cD59EG72diAlLdTCkv1mrG6Maw"


class BinanceAPI:
    def __init__(self, loop: AbstractEventLoop):
        self.offset = 0
        self.SECRET = SECRET
        self.loop = loop
        self.aio_session = self._init_aio_session()

    async def init(self):
        """

        TODO: consider make this as classmethod to explicitly create API with initialization
        """
        await self._get_time_diff()

    def _init_aio_session(self) -> aiohttp.ClientSession:
        session = aiohttp.ClientSession(loop=self.loop, headers=self._get_headers())
        return session

    async def get_server_time(self):
        return await self._get(uri=TIME_URL, data={})

    async def get_account_info(self):
        params = {
            "timestamp": self.__get_time() + self.offset,
        }
        return await self._get(uri=ACCOUNT_URL, data=params)

    def _generate_signature(self, data: Dict) -> AnyStr:
        query_string = "&".join([f"{d[0]}={d[1]}" for d in data])
        m = hmac.new(
            self.SECRET.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
        )
        return m.hexdigest()

    def _append_signature(self, data: Dict) -> Dict:
        data["signature"] = self._generate_signature(data)
        return data

    def __get_time(self) -> int:
        return int(time.time() * 1000)

    async def _get(self, uri: AnyStr, data: Dict, signature_needed=False):
        if signature_needed:
            data = self._append_signature(data)
        async with self.aio_session.get(uri, params=data) as resp:
            try:
                json_response = await resp.json()
                print(resp.headers)
                return json_response
            except ValueError:
                msg = await resp.text()
                logging.critical(f"Invalid Response: {msg}")

    def _calculate_offset(self, server_time) -> int:
        return server_time - self.__get_time()

    async def _get_time_diff(self):
        server_time = (await self.get_server_time())["serverTime"]
        self.offset = self._calculate_offset(server_time)
        logging.info(f"Binance server time: {server_time}; Time offset: {self.offset}")

    @staticmethod
    def _get_headers() -> Dict:
        return {
            "X-MBX-APIKEY": "9QC75c7IzdwU1w23EMPMIB4X1JCFf5v3VDSArXXmc8jSIHyuGbbxyoLpaLviMs39",
        }
