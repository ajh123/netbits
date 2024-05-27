class Identifier:
    def __init__(self, namespace: str, id: str):
        self.namespace = namespace
        self.id = id

    @classmethod
    def from_string(cls, namespaced_string: str):
        try:
            namespace, id = namespaced_string.split(':')
            return cls(namespace, id)
        except ValueError:
            raise ValueError("String must be in the format 'namespace:id'")

    def __eq__(self, other):
        if isinstance(other, Identifier):
            return self.namespace == other.namespace and self.id == other.id
        return False

    def __hash__(self):
        return hash((self.namespace, self.id))

    def __str__(self):
        return f"{self.namespace}:{self.id}"