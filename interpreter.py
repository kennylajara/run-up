from abc import ABC, abstractmethod


class Interpreter(ABC):
    """Interpreters' abstract class."""
        
    @abstractmethod
    def create_backup(self):
        pass
        
    @abstractmethod
    def restore_backup(self):
        pass


class Interpreter_1(Interpreter):
    """Interpreter that implements the rules for YAML version 1."""
    
    def create_backup(self):
        pass

    def restore_backup(self):
        pass
    