from typing import Dict, Generic, TypeVar
from ..registries.identifier import Identifier

T = TypeVar("T")

class Registry(Generic[T]):
    """
    A generic registry to store and retrieve items by their identifiers.
    """

    def __init__(self):
        """
        Initialize an empty registry.
        """
        self._registry: Dict[Identifier, T] = {}

    def register(self, identifier: Identifier, value: T):
        """
        Register an item with its identifier in the registry.

        :param identifier: The identifier for the item.
        :type identifier: Identifier
        :param value: The item to be registered.
        :type value: T
        :raises ValueError: If the identifier is not an instance of the Identifier class.
        """
        if not isinstance(identifier, Identifier):
            raise ValueError("Identifier must be an instance of Identifier class.")
        self._registry[identifier] = value

    def get(self, identifier: Identifier) -> T | None:
        """
        Retrieve an item from the registry by its identifier.

        :param identifier: The identifier of the item to retrieve.
        :type identifier: Identifier
        :return: The item associated with the identifier, or None if not found.
        :rtype: T | None
        """
        try:
            return self._registry.get(identifier)
        except ValueError:
            return None
        
    def get_id(self, value: T) -> Identifier | None:
        """
        Retrieve the identifier of an item in the registry.

        :param value: The item whose identifier is to be retrieved.
        :type value: T
        :return: The identifier associated with the item, or None if not found.
        :rtype: Identifier | None
        """
        try:
            for key, dvalue in self._registry.items():
                if dvalue == value:
                    return key
        except ValueError:
            return None
        return None
