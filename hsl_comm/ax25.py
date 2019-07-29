AX25_CONTROL_FIELD=b'\x03'
AX25_PROTOCOL_PID = b'\xF0'

class Frame:
    ''' Represents an AX.25 Frame '''

    def __init__(self, source: bytes=b'', destination: bytes=b'', info: bytes=b''):
        self.source = Address(source)
        self.destination = Address(destination)
        self.info = Info(info)

    def encode(self):
        ''' Encodes an AX.25 Frame and returns the encoded Frame (in bytes)'''
        encoded = []
        encoded.append(self.destination.encode())
        encoded.append(self.source.encode(last=True))
        encoded.append(AX25_CONTROL_FIELD)
        encoded.append(AX25_PROTOCOL_PID)
        encoded.append(self.info.encode())
        
        return b''.join(encoded)
    

class Field:
    ''' Represents an AX.25 Field (Parent class)'''

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
        ''' Encodes an AX.25 Field and returns the encoded field (in bytes) '''
        return self.raw
    

class Address(Field):
    ''' Represents an AX.25 Address '''

    def __init__(self, callsign: bytes=b''):
        if b'-' in callsign:
            try:
                self.callsign, self.ssid = callsign.split(b'-')
            except ValueError:
                raise ValueError("Bad callsign format")
        else:
            self.callsign = callsign
            # Defaults to 0
            self.ssid = b'0'

        super().__init__(self.callsign+self.ssid)

    def encode(self, last=False):
        ''' Encodes the Adress and returns the encoded Address field (In bytes) '''

        encoded = []
        # Encode callsign
        for _char in self.callsign:
            toAppend = _char << 1
            encoded.append(bytes([toAppend]))

        # Encode ssid (has to be shifted)
        ssid = self.ssid[0] << 1

        # If last address field make sure last bit is 1
        if last:
            encoded.append(bytes([ssid | 1]))
        else:
            encoded.append(bytes([ssid]))
        return b''.join(encoded)


class Info(Field):
    ''' Represents an AX.25 Info Field (Data) '''
    pass
