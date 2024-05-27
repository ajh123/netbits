from .buffer import Buffer

class StructuredPacket:
    """
    A base class for structured packets with packing and unpacking functionality.
    """

    def pack(self, buffer: Buffer):
        """
        Pack data into the provided buffer. This method should be overridden by subclasses.

        :param buffer: The buffer to pack data into.
        :type buffer: Buffer
        :raises NotImplementedError: This method should be implemented by subclasses.
        """
        raise NotImplementedError

    @classmethod
    def unpack(cls, buffer: Buffer):
        """
        Unpack data from the provided buffer. This method should be overridden by subclasses.

        :param buffer: The buffer to unpack data from.
        :type buffer: Buffer
        :raises NotImplementedError: This method should be implemented by subclasses.
        """
        raise NotImplementedError