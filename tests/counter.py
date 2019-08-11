import socket
import multiprocessing
import time
import collections
import argparse

# Command Line Arguments
parser = argparse.ArgumentParser(
    description='Counts number and indices of recieved packets (expected AX.25 packet kiss encoded).')
parser.add_argument('--len', action='store', dest='len', type=int,
                    help='Expected Length of a packet (Used to ignore ack packet).', default=23)
parser.add_argument('--num', action='store', dest='num', type=int,
                    help='Number of packets (0 to detect burst end automaticly).', default=0)
parser.add_argument('--time', action='store', dest='time', type=int,
                    help='(seconds) Timeout used to detect burst end (only if num is 0).', default=3)
parser.add_argument('--simple', action='store', dest='simple',
                    type=bool, help='Only count the number of packets', default=False)
parser.add_argument('--size', action='store', dest='size',
                    type=int, help='Size of counter (number of bytes)', default=2)
# Network arguments
parser.add_argument('--host', action='store', dest='host', type=str,
                    help='Packet source connection host', default='localhost')
parser.add_argument('--port', action='store', dest='port',
                    type=int, help='Packet source connection port', default=52002)

args = parser.parse_args()


def kiss_decode(packet):
    ''' Packet kiss decode (https://en.wikipedia.org/wiki/KISS_(TNC)) '''
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


def getPacketIndex(packet):
    ''' Get the packet index (Expected in the last positions in the data field) '''
    size = args.size
    field = packet[-size:-1]
    return int.from_bytes(field, 'little')


# Global variables
count = 0
missing = []

index = 0
prev = 0

def receivePacket():
    global sock
    global count
    global missing
    global prev
    global index

    packet = sock.recv(4096)
    # Check if packet is at correct size
    if len(packet) is args.len:
        count += 1
        # Kiss Decode
        packet = kiss_decode(packet)
        # Get packet index
        index = getPacketIndex(packet)

        # Add missing packets indices to missing list
        while prev is not index:
            prev += 1
            missing.append(prev)
        prev = index

        # Print information
        print(f'Packet: {packet.hex()}')
        print(f'Packet count is {count}')
        print(f'Packet index is {index}')
        print(f'Packet loss rate is {1-len(missing)/count}')
        print('\n')

if __name__ == '__main__':

    # Setup socket connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = (args.host, args.port)
    sock.connect(address)


    while True:
        if args.num is 0:
            p = multiprocessing.Process(target=receivePacket)
            p.start()
            if count >= 1:
                p.join(args.time)
                if p.is_alive():
                    p.terminate()
                    p.join()
        else:
            receivePacket()
            if args.len is index:
                # Packet index is number of packets
                break

    # Print information
    print(f'Number of packets lost is {len(missing)} (received {count})')
    print(f'Packet loss rate is {1-len(missing)/count}')

    for lostPacket in missing:
        print(f'{lostPacket}, ', end='')
    print()
