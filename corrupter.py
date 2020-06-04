from Socket import Socket
import time
import binascii
import os
import configparser
import struct


PORT = 6000
ver = "1.0.0"

def BoolInput(message):
    choices = input(message)
    choice = choices[0].lower()
    if choice == '' or not choice in ['y','n']:
        print("Error invalid input")
        BoolInput(message)
    else:
        return choice == 'y'

def between(val, low, high):
    res = val - low
    if res >= 2.0 or res <= 0.0:
        return False
    else:
        return True

def main():
    print("SysBot Corrupter " + ver + " by rydoginator")
    config = configparser.ConfigParser()
    if os.path.isfile('config.ini'):
        config.read('config.ini')
        ip = config['Server']['host']
        port = config['Server']['port']
        if not config['Misc'].getboolean('SkipMsg'):
            if BoolInput("Would you like to connect to " + ip + ":" +  port + "? y or n:"):
                if BoolInput("Would you like to skip this message in the future? y or n:"):
                    config['Misc']['SkipMsg'] = 'yes'
                else:
                    config['Misc']['SkipMsg'] = 'no'
            else:
                ip = input("Enter switch IP address:")
    else:
        ip = input("Enter switch IP address:")
    s = Socket()
    s.connect(ip, PORT)
    if s.connected:
        if not config['Misc'].getboolean('SkipMsg'):
            if BoolInput("Would you like to skip this message in the future? y or n:"):
                config['Misc']['SkipMsg'] = 'yes'
            else:
                config['Misc']['SkipMsg'] = 'no'
        config['Server']['host'] = ip
        config['Server']['port'] = str(PORT)
        with open('config.ini', 'w') as f:
            config.write(f)
        print("Press Ctrl+C to stop execution")
        print("Executing in...")
        for x in range(0,3):
            print(3 - x)
            time.sleep(1)
        offset = 0
        while True:
            value = s.readFloat(x * 4 + 0x0)
            if between(value, 1.0, 2.0):
                buf = struct.pack("f", value)
                print (offset + "->" + buf)
            print (str(offset) + "->" + str(value))
            offset = offset + 4



    
main()
