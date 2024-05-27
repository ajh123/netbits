========================
Netbits server Tutorial
========================

This tutorial will guide you through creating a Python server that uses custom structured packets to communicate with clients using the `netbits` library. We will define two types of packets: `ExampleRequest` and `StringMessage`, and implement a server to handle these packets.

The complete source code can be `found on GitHub <https://github.com/ajh123/netbits/blob/main/example-server.py/>`_.

Requirements
============

Before you start, ensure you have the `netbits` library installed. You can install it using pip:

.. code-block:: bash

    pip install netbits

Packet Classes
==============

We will define two packet classes: `ExampleRequest` and `StringMessage`.

ExampleRequest Packet
---------------------

The `ExampleRequest` packet contains the following fields:

- `title` (string)
- `x` (integer)
- `y` (integer)
- `width` (integer)
- `height` (integer)

.. code-block:: python

    from netbits.packet import StructuredPacket

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

StringMessage Packet
--------------------

The `StringMessage` packet contains a single field:

- `string` (string)

.. code-block:: python

    class StringMessage(StructuredPacket):
        def __init__(self, string: str):
            super().__init__()
            self.string = string

        def pack(self, buffer):
            buffer.write_string(self.string)

        @classmethod
        def unpack(cls, buffer):
            return cls(buffer.read_string())

Registry and Message Handler
=============================

Next, we will set up a registry and a message handler to process the incoming packets.

Registry Setup
--------------

.. code-block:: python

    from netbits.registry import *
    from typing import Type

    reg = Registry[Type[StructuredPacket]]()
    reg.register(Identifier.from_string("example:request"), ExampleRequest)
    reg.register(Identifier.from_string("example:string_message"), StringMessage)

Message Handler
---------------

.. code-block:: python

    from netbits.handler import MessageHandler, handlesMessage

    class ServerMessageHandler(MessageHandler):
        def __init__(self):
            super().__init__()

        @handlesMessage(ExampleRequest)
        def handle_example_request(self, message: StructuredPacket, user_data):
            print(f"Got Example Request: {vars(message)} with user data: {user_data}")

        @handlesMessage(StringMessage)
        def handle_string_message(self, message: StructuredPacket, user_data):
            global reg
            print(f"Got String Message: {vars(message)} with user data: {user_data}")
            sendStructuredPacket(user_data[0], StringMessage("I'm sorry"), reg)

Client Handler
==============

We will create a function to handle new client connections.

.. code-block:: python

    import socket
    from netbits.sockets import *

    def on_new_client(client_socket: socket.socket, addr: str):
        global reg
        sh = ServerMessageHandler()
        while True:
            message = readStructuredPacket(client_socket, reg)
            if message is None:
                break
            sh.handle(message, (client_socket, addr))

Server Implementation
=====================

Finally, we will implement the server to accept connections and handle client messages in separate threads.

.. code-block:: python

    from threading import Thread

    def socket_main():
        host = '0.0.0.0'
        port = 8888

        s = socket.socket()
        s.bind((host, port))
        s.listen(5)

        print(f"Listening on {host}:{port}")

        while True:
            c, addr = s.accept()
            print(f"New connection from: {addr}")
            thread = Thread(target=on_new_client, args=(c, addr), daemon=True)
            thread.start()

    if __name__ == '__main__':
        socket_main()

Explanation
===========

1. **Packet Definition**:
    - `ExampleRequest` and `StringMessage` classes are defined, inheriting from `StructuredPacket`.
    - Both classes implement the `pack` and `unpack` methods to serialize and deserialize packet data.

2. **Registry Initialization**:
    - A registry for packet types is created and packet classes are registered with unique identifiers. **The registry must have the same keys and values as the client!**

3. **Message Handler**:
    - `ServerMessageHandler` class is defined to handle incoming packets using the `handle_example_request` and `handle_string_message` methods.

4. **Client Handler**:
    - The `on_new_client` function reads incoming packets from the client and passes them to the message handler.

5. **Server Setup**:
    - A socket is created to listen for incoming connections on port `8888`.
    - For each new connection, a new thread is spawned to handle client messages.

Conclusion
==========

This tutorial covers the basics of creating and using custom structured packets in Python with the `netbits` library. You can expand this example by adding more packet types and handling additional message types.
