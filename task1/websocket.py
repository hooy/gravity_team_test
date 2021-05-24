from task1.common import loop


class WebSocketBase:
    def __init__(self, name, connect, on_message):
        self.name = name
        self.connect = connect
        self.web_socket = None
        self.on_message = on_message
        loop.create_task(self.ws())

    async def ws(self):
        self.web_socket = await self.connect()
        while True:
            msg = await self.web_socket.recv()
            self.on_message(msg)

