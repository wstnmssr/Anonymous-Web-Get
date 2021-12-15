import awget
import os
import random
import socket
import struct
import subprocess
import sys

def print_usage(program):
    print('{} usage:'.format(program))
    print('\tusing default port: python3 {}'.format(program))
    print('\tusing given port:   python3 {} -p [port]'.format(program))

def check_argv(args):
    if len(args) == 1:
        return 12358
    elif len(args) == 3:
        try:
            if args[1] == '-p':
                return int(args[2])
            else:
                print('{}: invalid arguments given.'.format(args[0]))
                print_usage(args[0])
                sys.exit(1)
        except:
            print('{}: invalid port given: {}.'.format(args[0], args[2]))
            print_usage(args[0])
            sys.exit(1)
    else:
        print('{}: invalid arguments given: {}.'.format(args[0]))
        print_usage(args[0])
        sys.exit(1)

def decode(request):
    SSnum = int(request[0])
    URLlen = int(request[1])

    data = struct.unpack('>BB{}s{}'.format(URLlen, 'IH' * SSnum), request)

    SSpairs, addr, url = [], '', data[2].decode()
    for i, SSpart in enumerate(data[3:]):
        if i % 2 == 0:
            quad0 = (SSpart & 0xff000000) >> 24
            quad1 = (SSpart & 0x00ff0000) >> 16
            quad2 = (SSpart & 0x0000ff00) >> 8
            quad3 = SSpart & 0x000000ff
            addr = '{}.{}.{}.{}'.format(quad0, quad1, quad2, quad3)
        else:
            SSpairs.append((addr, SSpart))

    return SSnum, SSpairs, url

if __name__ == '__main__':
    #---SETUP---
    port = check_argv(sys.argv)
    #---SETUP---
    print('this host: {}'.format(socket.gethostbyname(socket.gethostname())))

    request, conn, fromSS = awget.recv(port)
    fromSS = (fromSS[0], 12359)
    print('2 recvd from: {}'.format(fromSS))
    SSnum, SSpairs, url = decode(request)

    if SSnum == 0:
        #subprocess.Popen(['wget', '-O', 'file', url])
        #file = open('file', 'r')
        print('6 chain end, send to: {}'.format(fromSS))
        conn.sendall(b'recieved')#file.read().encode())
        #file.close()
        #os.remove('file') 
    else:
        SSnum, SSpair = awget.choose_pair(SSnum, SSpairs)
        print('3 send to: {}'.format(fromSS))
        awget.send(SSpair, awget.encode(SSnum, SSpairs, url))

    reply, conn, fromSS = awget.recv(12359)[0]
    print('4 recvd from: {}'.format(fromSS))
    print('5 send to: {}'.format(fromSS))
    conn.sendall(reply)
    conn.close() 
