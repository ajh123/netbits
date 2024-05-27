import struct

class Buffer:
    """
    A class to handle reading and writing of binary data with support for integers and strings.
    
    :param buffer: A bytearray to store the binary data.
    :type buffer: bytearray
    """

    def __init__(self, buffer: bytearray):
        """
        Initialize the Buffer instance.

        :param buffer: A bytearray to store the binary data.
        :type buffer: bytearray
        """
        self.buffer = buffer
        self.position = 0

    def write_int(self, value: int):
        """
        Write an integer to the buffer.

        :param value: The integer value to write.
        :type value: int
        """
        self.buffer.extend(struct.pack('!i', value))

    def read_int(self) -> int:
        """
        Read an integer from the buffer.

        :return: The integer value read from the buffer.
        :rtype: int
        """
        int_size = struct.calcsize('!i')
        int_value = struct.unpack('!i', self.buffer[self.position:self.position + int_size])[0]
        self.position += int_size
        return int_value

    def write_string(self, value: str):
        """
        Write a string to the buffer.

        :param value: The string value to write.
        :type value: str
        """
        encoded_string = value.encode('utf-8')
        length = len(encoded_string)
        self.buffer.extend(struct.pack(f'!I{length}s', length, encoded_string))

    def read_string(self) -> str:
        """
        Read a string from the buffer.

        :return: The string value read from the buffer.
        :rtype: str
        """
        length_size = struct.calcsize('!I')
        length = struct.unpack('!I', self.buffer[self.position:self.position + length_size])[0]
        self.position += length_size
        encoded_string = struct.unpack(f'!{length}s', self.buffer[self.position:self.position + length])[0]
        self.position += length
        return encoded_string.decode('utf-8')
