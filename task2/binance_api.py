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
    def __init__(self, loop):
        self.offset = 0
        self.SECRET = SECRET
        self.loop = loop
        self.aio_session = self._init_aio_session()

    def _init_aio_session(self) -> aiohttp.ClientSession:
        session = aiohttp.ClientSession(loop=self.loop, headers=self._get_headers())
        return session

    def get_server_time(self):
        return await self._get(uri=TIME_URL, data={})

    def _generate_signature(self, data: Dict) -> AnyStr:
        query_string = "&".join([f"{d[0]}={d[1]}" for d in data])
        m = hmac.new(
            self.SECRET.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
        )
        return m.hexdigest()

    def _append_signature(self, data: Dict) -> Dict:
        data["signature"] = self._generate_signature(data)
        return data

    async def _get_account_info(self):
        params = {
            "recvWindow": 5000,
            "timestamp": int(time.time() * 1000 + self.offset),
        }
        pass

    async def _get(self, uri: AnyStr, data: Dict):
        signature = self._append_signature(data)
        async with self.aio_session as session:
            async with session.get(uri) as resp:
                await resp.json()

    @staticmethod
    def _get_headers() -> Dict:
        return {
            "X-MBX-APIKEY": "9QC75c7IzdwU1w23EMPMIB4X1JCFf5v3VDSArXXmc8jSIHyuGbbxyoLpaLviMs39",
        }
