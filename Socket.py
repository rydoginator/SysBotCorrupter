import socket
import time
import os
import struct
class Socket:
    """Socket class to communicate with sysbot's server
    """
    connected = False
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        try:
            self.sock.connect((host, port))
            self.connected = True
        except socket.gaierror:
            print ("Error!\nConnect actively refused!")
            return
        except socket.error:
            print ("Error!\nConnect actively refused!")
            return

    def send(self, msg):
        msg += '\r\n' #important for the parser on the switch side
        sent = self.sock.sendall(msg.encode())
        if sent == 0:
            raise RuntimeError("socket connection broken")

    def push_button(self, button):
        self.send("click " + button)

    def write(self, address, value):
        self.send("poke 0x" + address + " 0x" + value)


    def read(self, address, size):
        self.send("peek " + hex(address) + " " + str(size))
        # give some time to respond
        #time.sleep(0.0001)
        return self.sock.recv(8000)

    def readFloat(self, address):
        buf = self.read(address, 4)
        # remove the \n
        buf = buf[0:-1]
        x = struct.unpack('f', buf[0:4])
        return float(x[0])
