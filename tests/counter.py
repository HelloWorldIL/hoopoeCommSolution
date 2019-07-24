import socket
import collections

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

address = ('localhost', 52002)

sock.connect(address)

def kiss_decode(packet):
    FEND = 0xc0
    FESC = 0xdb
    TFEND = 0xdc
    TFESC = 0xdd

    kiss = collections.deque()
    kiss.extend(packet)
    out = list()
    while kiss:
        c = kiss.popleft()
        if c == FESC:
            print('Excape Detected')
            c = kiss.popleft()
            if c == TFEND:
                out.append(FEND)
            elif c == TFESC:
                out.append(FESC)
        else:
            out.append(c)
    return bytearray(out)

count = 0
prev = -1
missing = ""

while prev < 254:
    packet = sock.recv(4096)
    if packet is not None and len(packet.hex()) < 60:
        # Kiss Decode
        packet = kiss_decode(packet)
        pakcet_hex = packet.hex()

        # Get the Number in the data field
        num = pakcet_hex[-4]+pakcet_hex[-3]
        num = int(num, 16)
        count+=1
        if prev+1 is not num:
            while prev+1 is not num:
                prev += 1
                missing += str(prev) + ', '
        prev = num
        print('Packet: ' + str(pakcet_hex))
        print('Packet no. ' + str(count))
        print('Packet data number: ' + str(num))
        print('\n')

print('Number of packets lost: ' + str(len(missing)))
print(missing)

