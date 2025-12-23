import asyncio
import logging

_LOGGER = logging.getLogger(__name__)

class PioneerTelnet:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.callbacks = []
        self.reader = None
        self.writer = None

    async def connect(self):
        while True:
            try:
                self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
                _LOGGER.info("Connected to SC-85")
                asyncio.create_task(self._listen())
                break
            except Exception as e:
                _LOGGER.warning("Reconnect failed: %s", e)
                await asyncio.sleep(5)

    async def _listen(self):
        while True:
            data = await self.reader.readline()
            if not data:
                break
            msg = data.decode().strip()
            for cb in self.callbacks:
                cb(msg)

    def register(self, cb):
        self.callbacks.append(cb)

    async def send(self, cmd):
        if self.writer:
            self.writer.write(f"{cmd}\r".encode())
            await self.writer.drain()
