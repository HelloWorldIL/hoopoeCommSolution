import hsl_comm
import socket
import time

config =  hsl_comm.Config.from_file()

predict = hsl_comm.PredictSolution(
    config.Satellite,
    config.Station,
    config.Doppler,
    config.Rotator,
    config.tleUrl
)

server_address = ('localhost', 52001)

tcpSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

tcpSocket.connect(server_address)

frame = hsl_comm.Frame(source=b'4X4HSL-1', destination=b'4X4HSC-1', info=bytes([0xFF]))


for I in range(0, 11):
    tcpSocket.send(frame.encode())
    time.sleep(0.01)

# print(frame.encode().hex())