========================
Netbits client Tutorial
========================

This tutorial will guide you through creating a Python program that uses custom structured packets to communicate with a server using the `netbits` library. We will create two types of packets: `ExampleRequest` and `StringMessage`, and implement a client to send and receive these packets.

The complete source code can be `found on GitHub <https://github.com/ajh123/netbits/blob/main/example-client.py/>`_.

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

Client Implementation
=====================

Next, we will implement the client to send and receive these packets.

.. code-block:: python

    import socket
    from netbits.registry import *
    from netbits.sockets import *

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

Explanation
===========

1. **Packet Definition**:
    - `ExampleRequest` and `StringMessage` classes are defined, inheriting from `StructuredPacket`.
    - Both classes implement the `pack` and `unpack` methods to serialize and deserialize packet data.

2. **Client Setup**:
    - A socket connection is established to the server at `127.0.0.1` on port `8888`.

3. **Registry Initialization**:
    - A registry for packet types is created and packet classes are registered with unique identifiers. **The registry must have the same keys and values as the server!**

4. **Packet Sending**:
    - An `ExampleRequest` packet and a `StringMessage` packet are created and sent to the server using the `sendStructuredPacket` function.

5. **Packet Receiving**:
    - The client reads the response packet from the server and prints its content if available.

Conclusion
==========

This tutorial covers the basics of creating and using custom structured packets in Python with the `netbits` library. You can expand this example by adding more packet types and implementing a server to handle the packets.
