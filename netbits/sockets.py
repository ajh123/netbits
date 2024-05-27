import socket
import struct
from typing import Type

from .packet import *
from .registries import *


def _send_msg(sock: socket.socket, msg: bytearray):
    """
    Send a message through the socket, prefixed with its length.

    :param sock: The socket to send the message through.
    :type sock: socket.socket
    :param msg: The message to send.
    :type msg: bytearray
    """
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)


def _recv_msg(sock: socket.socket):
    """
    Receive a message from the socket.

    :param sock: The socket to receive the message from.
    :type sock: socket.socket
    :return: The received message data.
    :rtype: bytearray or None
    """
    raw_msglen = _recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    return _recvall(sock, msglen)


def _recvall(sock: socket.socket, n):
    """
    Helper function to receive n bytes or return None if EOF is hit.

    :param sock: The socket to receive data from.
    :type sock: socket.socket
    :param n: The number of bytes to receive.
    :type n: int
    :return: The received data.
    :rtype: bytearray or None
    """
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
    """
    Read a structured packet from the socket.

    :param sock: The socket to read from.
    :type sock: socket.socket
    :param registry: The registry of structured packet types.
    :type registry: registry.Registry[Type[StructuredPacket]]
    :return: The structured packet read from the socket.
    :rtype: StructuredPacket or None
    """
    msg_type_data = _recv_msg(sock)
    if msg_type_data is None:
        return None
    buff = Buffer(msg_type_data)

    msg_type = Identifier.from_string(buff.read_string())
    msg_class = registry.get(msg_type)
    if msg_class is not None:
        return msg_class.unpack(buff)
    else:
        return None


def sendStructuredPacket(sock: socket.socket, packet: StructuredPacket, registry: registry.Registry[Type[StructuredPacket]]):
    """
    Send a structured packet through the socket.

    :param sock: The socket to send through.
    :type sock: socket.socket
    :param packet: The structured packet to send.
    :type packet: StructuredPacket
    :param registry: The registry of structured packet types.
    :type registry: registry.Registry[Type[StructuredPacket]]
    :raises ValueError: If the packet type is not registered in the registry.
    """
    packet_id = registry.get_id(type(packet))
    if packet_id is None:
        raise ValueError(f"Packet({packet}) must be registered in the registry!")

    buff = Buffer(bytearray())
    buff.write_string(str(packet_id))
    packet.pack(buff)

    _send_msg(sock, buff.buffer)
