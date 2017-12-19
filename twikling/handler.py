# coding=utf8
import asyncio
import json
import logging
import time
from urllib.parse import urlparse

import websockets


logger = logging.getLogger('websockets')


class Handler(object):
    def __init__(self, protocol: websockets.WebSocketCommonProtocol, path: str):
        self.protocol = protocol
        self.path = path


    async def on_open(self, request: Request):
        pass

    async def _init(self, user_state):
        pass

    async def run_once(self):
        dones, pendings = await asyncio.wait(self.wait.waiting,
                                             timeout=PING_INTERVAL,
                                             return_when=asyncio.FIRST_COMPLETED)

        # do something with msg
        for done in dones:
            self.ping_action = False
            assert isinstance(done, asyncio.Future)
            if getattr(done, '_kind') == 'client':
                msg = done.result()
                await self.processor.process_from_client(msg)
            elif getattr(done, '_kind') == 'zmq':
                message = done.result()
                print(message)
                for i in message[1:]:
                    await self.protocol.send(i.decode('utf8'))

        if self.ping_action:
            raise PingNoReplyError

        self.wait.reorganize(dones)

        if not dones and not self.ping_action:
            logger.info("")
            self.ping_action = True
            ping_msg = Message.create(PING, {}, int(time.time()))
            await self.protocol.send(ping_msg.to_json())

    async def handle(self):
        request = Request.parse_request(self.protocol)
        user_state = await self.on_open(request)

        await self._init(user_state)

        try:
            while True:
                await self.run_once()
        except PingNoReplyError:
            logger.debug("client don't reply to pong ")
        except Exception:
            logger.error(catch_traceback())
        finally:
            try:
                await self.etc_client.delete_user()
            except asyncio.TimeoutError:
                logger.error("etcd not reply, please check the etcd is up or down")
            self.zmq_connector.clean_up()
