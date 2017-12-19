# codint=utf8

class BaseException(Exception):
    pass

class AuthenticateError(BaseException):
    pass

class PingNoReplyError(BaseException):
    pass

class SubscribeItemError(BaseException):
    pass