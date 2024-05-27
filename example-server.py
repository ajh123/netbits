from netbits.registries import *
from netbits.packet import StructuredPacket
from netbits.handler import MessageHandler, handlesMessage
from netbits.sockets import *
from typing import Type
from threading import Thread
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

reg = Registry[Type[StructuredPacket]]()
reg.register(Identifier.from_string("example:request"), ExampleRequest)
reg.register(Identifier.from_string("example:string_message"), StringMessage)

class ServerMessageHandler(MessageHandler):
    def __init__(self):
        super().__init__()

    @handlesMessage(ExampleRequest)
    def handle_example_request(self, message: StructuredPacket, user_data):
        # The user_data is what we sent when we called ServerMessageHandler.handle!
        print(f"Got Example Request: {vars(message)} with user data: {user_data}")

    @handlesMessage(StringMessage)
    def handle_string_message(self, message: StructuredPacket, user_data):
        global reg
        # The user_data is what we sent when we called ServerMessageHandler.handle!
        print(f"Got String Message: {vars(message)} with user data: {user_data}")
        sendStructuredPacket(user_data[0], StringMessage("I'm sorry"), reg)


def on_new_client(client_socket:socket.socket, addr:str):
    global reg
    sh = ServerMessageHandler()
    while True:
        message = readStructuredPacket(client_socket, reg) # Read any incoming StructuredPackets
        
        if message == None:
            break # if we did not get valid data, break

        sh.handle(message, (client_socket, addr)) # Pass the message to handler. The second parameter is the user data that will be given to the handle method!

def socket_main():
    host = '0.0.0.0'  # allow any incoming connections
    port = 8888

    s = socket.socket()
    s.bind((host, port))  # bind the socket to the port and ip address

    s.listen(5)  # wait for new connections

    print(f"listening on {host}:{port}")

    while True:
        c, addr = s.accept()  # Establish connection with client.
        # this returns a new socket object and the IP address of the client
        print(f"New connection from: {addr}")
        thread = Thread(target=on_new_client, args=(c, addr), daemon=True)  # create the thread
        thread.start()  # start the thread

if __name__ == '__main__':
    socket_main()
