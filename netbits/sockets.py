import socket
import struct
from typing import Type

from .packet import *
from .registry import *

    
def _send_msg(sock: socket.socket, msg: bytearray):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def _recv_msg(sock: socket.socket):
    # Read message length and unpack it into an integer
    raw_msglen = _recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return _recvall(sock, msglen)

def _recvall(sock: socket.socket, n):
    # Helper function to recv n bytes or return None if EOF is hit
    try:
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data
    except ConnectionAbortedError:
        return None
    

def readStructuredPacket(sock: socket.socket, registry: registry.Registry[Type[StructuredPacket]]) -> StructuredPacket | None:
    # Read the message
    msg_type_data = _recv_msg(sock)
    if msg_type_data == None:
        return None
    buff = Buffer(msg_type_data)

    msg_type = Identifier.from_string(buff.read_string())
    msg_class = registry.get(msg_type)
    if msg_class is not None:
        return msg_class.unpack(buff)
    else:
        return None
    
def sendStructuredPacket(sock: socket.socket, packet: StructuredPacket, registry: registry.Registry[Type[StructuredPacket]]):
    packet_id = registry.get_id(type(packet))
    if packet_id == None:
        raise ValueError(f"Packet({packet}) must be registered in the registry!")

    buff = Buffer(bytearray())
    buff.write_string(str(packet_id))
    packet.pack(buff)

    _send_msg(sock, buff.buffer)