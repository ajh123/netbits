from typing import Dict, Generic, TypeVar
from ..registry.identifier import Identifier

T = TypeVar("T")

class Registry(Generic[T]):
    def __init__(self):
        self._registry: Dict[Identifier, T] = {}

    def register(self, identifier: Identifier, value: T):
        if not isinstance(identifier, Identifier):
            raise ValueError("Identifier must be an instance of Identifier class.")
        self._registry[identifier] = value

    def get(self, identifier: Identifier) -> T | None:
        try:
            return self._registry.get(identifier)
        except ValueError:
            return None
        
    def get_id(self, value: T) -> Identifier | None:
        try:
            for key, dvalue in self._registry.items():
                if dvalue == value:
                    return key
        except ValueError:
            return None
        return None