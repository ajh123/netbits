class Identifier:
    """
    A class to represent an identifier with a namespace and an ID.

    :param namespace: The namespace of the identifier.
    :type namespace: str
    :param id: The ID of the identifier.
    :type id: str
    """

    def __init__(self, namespace: str, id: str):
        """
        Initialize an Identifier instance.

        :param namespace: The namespace of the identifier.
        :type namespace: str
        :param id: The ID of the identifier.
        :type id: str
        """
        self.namespace = namespace
        self.id = id

    @classmethod
    def from_string(cls, namespaced_string: str):
        """
        Create an Identifier instance from a namespaced string.

        :param namespaced_string: A string in the format 'namespace:id'.
        :type namespaced_string: str
        :return: An Identifier instance.
        :rtype: Identifier
        :raises ValueError: If the string is not in the format 'namespace:id'.
        """
        try:
            namespace, id = namespaced_string.split(':')
            return cls(namespace, id)
        except ValueError:
            raise ValueError("String must be in the format 'namespace:id'")

    def __eq__(self, other):
        """
        Check equality with another Identifier instance.

        :param other: Another Identifier instance to compare with.
        :type other: Identifier
        :return: True if both Identifiers are equal, False otherwise.
        :rtype: bool
        """
        if isinstance(other, Identifier):
            return self.namespace == other.namespace and self.id == other.id
        return False

    def __hash__(self):
        """
        Compute the hash value of the Identifier.

        :return: The hash value of the Identifier.
        :rtype: int
        """
        return hash((self.namespace, self.id))

    def __str__(self):
        """
        Return the string representation of the Identifier.

        :return: The string representation in the format 'namespace:id'.
        :rtype: str
        """
        return f"{self.namespace}:{self.id}"
