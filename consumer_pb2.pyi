from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class Consumer(_message.Message):
    __slots__ = [
        "id",
        "name",
        "created_at",
        "client_id",
        "client_secret",
        "logo",
        "credentials",
        "document",
        "treasury_vault",
        "default_asset",
    ]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    LOGO_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    TREASURY_VAULT_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_ASSET_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    created_at: str
    client_id: str
    client_secret: str
    logo: str
    credentials: _containers.RepeatedScalarFieldContainer[str]
    document: str
    treasury_vault: str
    default_asset: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        created_at: _Optional[str] = ...,
        client_id: _Optional[str] = ...,
        client_secret: _Optional[str] = ...,
        logo: _Optional[str] = ...,
        credentials: _Optional[_Iterable[str]] = ...,
        document: _Optional[str] = ...,
        treasury_vault: _Optional[str] = ...,
        default_asset: _Optional[str] = ...,
    ) -> None: ...

class FindConsumers(_message.Message):
    __slots__ = ["ids"]
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class FindCredentials(_message.Message):
    __slots__ = ["ids"]
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class FindProviders(_message.Message):
    __slots__ = ["ids"]
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class FindJouneys(_message.Message):
    __slots__ = ["ids", "filter"]
    IDS_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    filter: str
    def __init__(
        self, ids: _Optional[_Iterable[str]] = ..., filter: _Optional[str] = ...
    ) -> None: ...

class ListJourneys(_message.Message):
    __slots__ = ["data", "error"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    data: str
    error: bool
    def __init__(self, data: _Optional[str] = ..., error: bool = ...) -> None: ...

class ListProviders(_message.Message):
    __slots__ = ["providers", "error"]
    PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    providers: _containers.RepeatedCompositeFieldContainer[Provider]
    error: bool
    def __init__(
        self,
        providers: _Optional[_Iterable[_Union[Provider, _Mapping]]] = ...,
        error: bool = ...,
    ) -> None: ...

class ListCredentials(_message.Message):
    __slots__ = ["credentials", "error"]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    credentials: _containers.RepeatedCompositeFieldContainer[Credential]
    error: bool
    def __init__(
        self,
        credentials: _Optional[_Iterable[_Union[Credential, _Mapping]]] = ...,
        error: bool = ...,
    ) -> None: ...

class ListConsumers(_message.Message):
    __slots__ = ["consumers", "error"]
    CONSUMERS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    consumers: _containers.RepeatedCompositeFieldContainer[Consumer]
    error: bool
    def __init__(
        self,
        consumers: _Optional[_Iterable[_Union[Consumer, _Mapping]]] = ...,
        error: bool = ...,
    ) -> None: ...

class Credential(_message.Message):
    __slots__ = ["id", "provider", "keys", "created_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    provider: str
    keys: str
    created_at: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        provider: _Optional[str] = ...,
        keys: _Optional[str] = ...,
        created_at: _Optional[str] = ...,
    ) -> None: ...

class Provider(_message.Message):
    __slots__ = ["created_at", "name", "type", "required_keys"]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_KEYS_FIELD_NUMBER: _ClassVar[int]
    created_at: str
    name: str
    type: str
    required_keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        created_at: _Optional[str] = ...,
        name: _Optional[str] = ...,
        type: _Optional[str] = ...,
        required_keys: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

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
    def __init__(
        self,
        status: _Optional[str] = ...,
        version: _Optional[str] = ...,
        service_name: _Optional[str] = ...,
        datetime: _Optional[str] = ...,
    ) -> None: ...

class SendHelthCheck(_message.Message):
    __slots__ = ["ping", "service"]
    PING_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    ping: str
    service: str
    def __init__(
        self, ping: _Optional[str] = ..., service: _Optional[str] = ...
    ) -> None: ...

class Journey(_message.Message):
    __slots__ = [
        "cash_out_credential_id",
        "between_credential_id",
        "cash_in_credential_id",
        "consumer_id",
        "id",
    ]
    CASH_OUT_CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    BETWEEN_CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    CASH_IN_CREDENTIAL_ID_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    cash_out_credential_id: str
    between_credential_id: str
    cash_in_credential_id: str
    consumer_id: str
    id: str
    def __init__(
        self,
        cash_out_credential_id: _Optional[str] = ...,
        between_credential_id: _Optional[str] = ...,
        cash_in_credential_id: _Optional[str] = ...,
        consumer_id: _Optional[str] = ...,
        id: _Optional[str] = ...,
    ) -> None: ...
