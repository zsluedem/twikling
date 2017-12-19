# coding=utf8
import asyncio

import websockets
import zmq
from JZquantWebsocket.zmqconnector import ZMQConnector


class Wait(object):

    def __init__(self, protocol: websockets.WebSocketCommonProtocol, zmq_connector: ZMQConnector):
        self._protocol = protocol
        self.zmq_connector = zmq_connector
        self._waiting = set()

        self.init()

    def init(self) -> None:
        pass

    @property
    def waiting(self) -> set:
        return self._waiting

    def reorganize(self, dones: set) -> None:
        for done in dones:
            new_fs = self.create_client_fs(done._kind)
            self._waiting.remove(done)
            self._waiting.add(new_fs)

    def decorate(self, future: asyncio.Future, kind: str) -> None:
        future._kind = kind

    def create_client_fs(self, type: str) -> asyncio.Future:
        pass
