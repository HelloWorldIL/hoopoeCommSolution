AX25_CONTROL_FIELD=b'\x03'
AX25_PROTOCOL_PID = b'\xF0'

class Frame:
    def __init__(self, source: bytes=b'', destination: bytes=b'', info: bytes=b''):
        self.source = Address(source)
        self.destination = Address(destination)
        self.info = Info(info)
    def encode(self):
        encoded = []
        encoded.append(self.destination.encode())
        encoded.append(self.source.encode())
        encoded.append(AX25_CONTROL_FIELD)
        encoded.append(AX25_PROTOCOL_PID)
        encoded.append(self.info.encode())
        
        return b''.join(encoded)
    

class Field:
    def __init__(self, contents: bytes=b''):
        self.raw = contents
    
    def __str__(self):
        return self.raw.decode('ascii')

    @classmethod
    def from_string(cls, raw: str=''):
        return cls(raw.encode('ascii'))
    
    def __len__(self):
        return len(self.raw)

    def encode(self):
        return self.raw
    

class Address(Field):
    def __init__(self, callsign: bytes=b''):
        self.callsign, self.ssid = callsign.split(b'-')
        super().__init__(self.callsign+self.ssid)

    def encode(self):
        encoded = []
        for _char in self.raw:
            encoded.append(bytes([_char << 1]))
        return b''.join(encoded)


class Info(Field):
    pass
