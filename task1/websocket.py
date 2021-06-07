import json
import logging

import websockets

from task1.consumer import AbstractAsyncApiConsumer

EXTRA_HEADERS = {"User-Agent": "Mozilla/5.0"}


class WebSocketBase:
    def __init__(self, name: str, manager: AbstractAsyncApiConsumer):
        """
        Base class to register socket and map callbacks
        """
        logging.info(f"WebSocketBase with name: {name}")
        self.name = name
        self.manager = manager
        self.web_socket = None
        manager.get_loop().create_task(self.ws())

    async def ws(self):
        self.web_socket = await websockets.connect(
            self.manager.get_connection_uri(),
            extra_headers=EXTRA_HEADERS,
        )
        self.manager.on_connect()
        while True:
            try:
                stream_raw_json = await self.web_socket.recv()
                data = json.loads(stream_raw_json)
                self.manager.on_message(data)
            except websockets.ConnectionClosed as error_msg:
                logging.error(f"ConnectionClosed: {error_msg} ")
