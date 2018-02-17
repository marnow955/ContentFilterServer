from abc import ABC, abstractmethod


class DbManagerABC(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def select_from_table(self, table_name: str, columns: tuple = ('*',),
                          condition: str = None, join_transaction: bool = False) -> list:
        pass

    @abstractmethod
    def update_columns(self, table_name: str, names_and_values: dict,
                       condition: str = None, join_transaction: bool = False):
        pass
