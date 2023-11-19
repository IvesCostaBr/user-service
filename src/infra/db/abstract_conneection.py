from abc import ABC, abstractmethod


class AbstractConnection(ABC):
    @abstractmethod
    def create_connection():
        raise NotImplementedError()

    @abstractmethod
    def get(self, entity: str, id: str, use_cache: bool = True):
        raise NotImplementedError()

    @abstractmethod
    def get_all(self, entity: str):
        raise NotImplementedError()

    @abstractmethod
    def create(self, entity: str, data: dict):
        raise NotImplementedError()

    @abstractmethod
    def update(self, entity: str, id: str, data: dict):
        raise NotImplementedError()

    @abstractmethod
    def exists(self, entity: str, query: dict):
        raise NotImplementedError()
    
    @abstractmethod
    def filter_query(self, entity: str, query: dict):
        raise NotImplementedError()