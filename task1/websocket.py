import json
import logging

import websockets


class WebSocketBase:
    def __init__(self, name, loop, uri, connect, on_message):
        """

        :type connect: function
        :type uri: string
        :type name: string
        :type loop: AbstractEventLoop
        """
        logging.info(f"WebSocketBase with name: {name}")
        self.name = name
        self.uri = uri
        self.connect = connect
        self.web_socket = None
        self.on_message = on_message
        loop.create_task(self.ws())

    async def ws(self):
        self.web_socket = await websockets.connect(self.uri, extra_headers={"User-Agent": "Mozilla/5.0"})
        self.connect()
        while True:
            try:
                stream_raw_json = await self.web_socket.recv()
                data = json.loads(stream_raw_json)
                self.on_message(data)
            except websockets.ConnectionClosed as error_msg:
                logging.info(f"ConnectionClosed: {error_msg} ")

