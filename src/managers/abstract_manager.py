from abc import ABC, abstractmethod


class AbstractManager(ABC):
    @abstractmethod
    def send(self, id):
        raise NotImplementedError()

    @abstractmethod
    def heath_check(self):
        raise NotImplementedError()
