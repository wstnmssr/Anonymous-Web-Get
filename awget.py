import random
import socket
import sys

def print_usage(program):
    print('{} usage:'.format(program))
    print('\tusing default chainfile: python3 {} [url]'.format(program))
    print('\tusing given chainfile:   python3 {} -c [chainfile] [url]'.format(program))

def check_argv(args):
    if len(args) == 2:
        return (args[1], 'chaingang.txt')
    elif len(args) == 4:
        if args[1] == '-c':
            return (args[3], args[2])
        elif args[2] == '-c':
            return (args[1], args[3])
        else:
            print('{}: invalid arguments given.'.format(args[0]))
            print_usage(args[0])
            sys.exit(1)
    else:
        print('{}: invalid arguments given.'.format(args[0]))
        print_usage(args[0])
        sys.exit(1)

def read_chainfile(chainfilename):
    SSnum, SSpairs, chainfile = None, [], open(chainfilename, 'r')

    for i, line in enumerate(chainfile):
        if i == 0:
            SSnum = int(line[:-1])
            print('  <{}>'.format(SSnum))
        else:
            SSpair = line[:-1].split(', ')
            SSpair = (SSpair[0], int(SSpair[1]))
            SSpairs.append(SSpair)
            print('  <{}>, <{}>'.format(SSpair[0], SSpair[1]))

    return SSnum, SSpairs

def choose_pair(SSnum, SSpairs):
    SSpair = SSpairs.pop(random.randint(0, SSnum - 1))
    SSnum -= 1
    return SSnum, SSpair

def get_normal_url(url):
    if url[:8] == 'https://':
        url = url[8:]
    if url[:7] == 'http://':
        url = url[7:]

    uri = url.split('/')
    filename = ''

    if len(uri) == 1:
        seperator = '/'
        filename = 'index.html'
    else:
        if uri[-1] == '':
            seperator = ''
            filename = 'index.html'
        elif len(uri[-1].split('.')) == 1:
            seperator = '/'
            filename = 'index.html'
        else:
            filename = uri[-2] + uri[-1]
            return url, filename
    url += seperator + filename
    return url, filename

def encode(SSnum, SSpairs, url):
    """
        packet structure:
        |========|========|========|========|
        |SSnum   |len(url)|   url (0-256)   |
        |-----------------------------------|
        |            SSaddress 1 (4)        |
        |    SSport 1 (2)   |       ...     |
        |===================================|
    """
    output = bytearray()

    output.append(SSnum)
    output.append(len(url))

    output.extend(bytearray(url.encode('utf-8')))
    for SSpair in SSpairs:
        addr = SSpair[0].split('.')
        output.append(int(addr[0]))
        output.append(int(addr[1]))
        output.append(int(addr[2]))
        output.append(int(addr[3]))
        output.extend(SSpair[1].to_bytes(2, 'big'))

    return output

def send(SSpair, request):
    toSS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    toSS.connect_ex(SSpair)
    toSS.sendall(request)
    toSS.close() 

def recv(port):
    this = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    this.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    this.bind(('0.0.0.0', port))
    this.listen(10)
    conn, fromSS = this.accept()

    recvd = conn.recv(1024)
    reply = recvd
    while recvd:
        recvd = conn.recv(1024)
        reply += recvd
    this.close()

    return reply, conn, fromSS

def write(data, filename):
    file = open(filename, 'w')
    file.write(reply)
    file.close()

if __name__ == '__main__':
    #---SETUP---
    url, chainfilename = check_argv(sys.argv)
    url, filename = get_normal_url(url)
    SSnum, SSpairs = read_chainfile(chainfilename)
    #---SETUP---
    print('this host: {}'.format(socket.gethostbyname(socket.gethostname())))

    SSnum, SSpair = choose_pair(SSnum, SSpairs)
    print('1 send to: {}'.format(SSpair))
    send(SSpair, encode(SSnum, SSpairs, url))

    reply = recv(12359)[0]
