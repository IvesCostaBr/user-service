from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SendEvent(_message.Message):
    __slots__ = ["consumer", "template_type", "channel", "payload"]
    CONSUMER_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    consumer: str
    template_type: str
    channel: str
    payload: str
    def __init__(self, consumer: _Optional[str] = ..., template_type: _Optional[str] = ..., channel: _Optional[str] = ..., payload: _Optional[str] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ["sended", "message"]
    SENDED_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    sended: bool
    message: str
    def __init__(self, sended: bool = ..., message: _Optional[str] = ...) -> None: ...

class DataReceiver(_message.Message):
    __slots__ = ["data", "isSuccess"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    ISSUCCESS_FIELD_NUMBER: _ClassVar[int]
    data: str
    isSuccess: bool
    def __init__(self, data: _Optional[str] = ..., isSuccess: bool = ...) -> None: ...

class HeathCheck(_message.Message):
    __slots__ = ["status", "version", "service_name", "datetime"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    DATETIME_FIELD_NUMBER: _ClassVar[int]
    status: str
    version: str
    service_name: str
    datetime: str
    def __init__(self, status: _Optional[str] = ..., version: _Optional[str] = ..., service_name: _Optional[str] = ..., datetime: _Optional[str] = ...) -> None: ...

class SendHelthCheck(_message.Message):
    __slots__ = ["ping", "service"]
    PING_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    ping: str
    service: str
    def __init__(self, ping: _Optional[str] = ..., service: _Optional[str] = ...) -> None: ...
