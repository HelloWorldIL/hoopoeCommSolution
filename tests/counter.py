import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

address = ('localhost', 52002)

sock.connect(address)

count = 0
prev = -1
missing = ""

while prev < 254:
    packt = sock.recv(4096)
    if packt is not None and len(packt.hex()) > 20:
        print(packt)
        num = packt.hex()[-4]+packt.hex()[-3]
        num = int(num, 16)
        count+=1
        if prev+1 is not num:
            for i in range(prev+1, num):
                missing += str(i)
                missing += ', '
        prev = num
        print(count)
        print(num)
print(missing)