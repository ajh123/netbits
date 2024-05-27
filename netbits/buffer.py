import struct

class Buffer:
    def __init__(self, buffer: bytearray):
        self.buffer = buffer
        self.position = 0

    def write_int(self, value: int):
        # Pack the integer into bytes and append to the buffer
        self.buffer.extend(struct.pack('!i', value))

    def read_int(self) -> int:
        # Unpack the integer from the buffer starting from the current position
        int_size = struct.calcsize('!i')
        int_value = struct.unpack('!i', self.buffer[self.position:self.position + int_size])[0]
        self.position += int_size
        return int_value

    def write_string(self, value: str):
        # Encode the string to bytes using utf-8
        encoded_string = value.encode('utf-8')
        length = len(encoded_string)
        # Pack the length and the string into bytes and append to the buffer
        self.buffer.extend(struct.pack(f'!I{length}s', length, encoded_string))

    def read_string(self) -> str:
        # Unpack the length of the string from the buffer
        length_size = struct.calcsize('!I')
        length = struct.unpack('!I', self.buffer[self.position:self.position + length_size])[0]
        self.position += length_size
        # Unpack the string bytes based on the length
        encoded_string = struct.unpack(f'!{length}s', self.buffer[self.position:self.position + length])[0]
        self.position += length
        # Decode the byte string back to a string using utf-8
        return encoded_string.decode('utf-8')