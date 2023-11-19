from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SendEvent(_message.Message):
    __slots__ = ["channel", "payload"]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    channel: str
    payload: str
    def __init__(self, channel: _Optional[str] = ..., payload: _Optional[str] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ["id", "sended"]
    ID_FIELD_NUMBER: _ClassVar[int]
    SENDED_FIELD_NUMBER: _ClassVar[int]
    id: str
    sended: bool
    def __init__(self, id: _Optional[str] = ..., sended: bool = ...) -> None: ...

class DataReceiver(_message.Message):
    __slots__ = ["data", "isSuccess"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    ISSUCCESS_FIELD_NUMBER: _ClassVar[int]
    data: str
    isSuccess: bool
    def __init__(self, data: _Optional[str] = ..., isSuccess: bool = ...) -> None: ...

class HeathCheck(_message.Message):
    __slots__ = ["status", "version"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    status: str
    version: str
    def __init__(self, status: _Optional[str] = ..., version: _Optional[str] = ...) -> None: ...
