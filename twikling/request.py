# coding=utf8
from urllib.parse import urlparse

from websockets import WebSocketCommonProtocol


class Request(object):
    def __init__(self, host, port, path, localaddress, headers):
        self.remote_host = host
        self.remote_port = port
        self.localaddress = localaddress
        self.fullpath = path

        parseresult = urlparse(path)
        self.path = parseresult.path

        self.query = self._parse_query(parseresult.query)

        self.headers = {}
        for key, value in headers:
            self.headers[key] = value

    @classmethod
    def parse_request(cls, websocketprotocol: WebSocketCommonProtocol):
        return cls(
            host=websocketprotocol.host,
            port=websocketprotocol.port,
            path=websocketprotocol.path,
            localaddress=websocketprotocol.local_address,
            headers=websocketprotocol.raw_request_headers
        )

    def __repr__(self):
        return "path:{}\nquery:{}\nheaders:{}".format(self.path, self.query, self.headers)

    def _parse_query(self, query:str)->dict:
        query_dict = {}
        items = query.split("&")
        for item in items:
            key, value = item.split('=')
            if key in query_dict:
                raise ValueError('duplicate key in query')
            query_dict[key] = value
        return query_dict

    def get_argument(self, name:str)->str or None:
        return self.query.get(name, None)
