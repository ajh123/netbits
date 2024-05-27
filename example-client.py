from netbits.registry import *
from netbits.packet import StructuredPacket
from netbits.sockets import *
import socket


class ExampleRequest(StructuredPacket):
    def __init__(self, title: str, x: int, y: int, width: int, height: int):
        super().__init__()
        self.title = title
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def pack(self, buffer):
        buffer.write_string(self.title)
        buffer.write_int(self.x)
        buffer.write_int(self.y)
        buffer.write_int(self.width)
        buffer.write_int(self.height)

    @classmethod
    def unpack(cls, buffer):
        return cls(buffer.read_string(), buffer.read_int(), buffer.read_int(), buffer.read_int(), buffer.read_int())

class StringMessage(StructuredPacket):
    def __init__(self, string: str):
        super().__init__()
        self.string = string

    def pack(self, buffer):
        buffer.write_string(self.string)

    @classmethod
    def unpack(cls, buffer):
        return cls(buffer.read_string())

def client_main():
    host = '127.0.0.1'  # server IP address
    port = 8888

    s = socket.socket()
    s.connect((host, port))

    reg = Registry[Type[StructuredPacket]]()
    reg.register(Identifier.from_string("example:request"), ExampleRequest)
    reg.register(Identifier.from_string("example:string_message"), StringMessage)

    try:
        # Create an ExampleRequest packet
        example_request = ExampleRequest("TestTitle", 10, 20, 200, 400)
        sendStructuredPacket(s, example_request, reg)

        # Create a StringMessage packet
        string_message = StringMessage("Hello, Server!")
        sendStructuredPacket(s, string_message, reg)

        resp = readStructuredPacket(s, reg)
        if resp is not None:
            print(f"Got String Message: {vars(resp)}")

    finally:
        s.close()

if __name__ == '__main__':
    client_main()
