from .buffer import Buffer


class StructuredPacket:
    def __init__(self):
        self.buffer = Buffer(bytearray())

    def pack(self, buffer: Buffer):
        raise NotImplementedError

    @classmethod
    def unpack(cls, buffer: Buffer):
        raise NotImplementedError

