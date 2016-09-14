#coding=utf-8
__author__ = 'turbinyan'

import socket
import json
import sys


HOST='127.0.0.1'
PORT='50007'
keyword = '大米'
def client_send():
    # Echo client program
    HOST = '127.0.0.1'    # The remote host
    PORT = 50007              # The same port as used by the server
    s = None
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            s = None
            continue
        try:
            s.connect(sa)
        except socket.error as msg:
            s.close()
            s = None
            continue
        break
    if s is None:
        print 'could not open socket'
        sys.exit(1)

    print 'send keyword'
    s.sendall(json.dumps({'keyword':unicode(keyword,'utf-8')}))
    data = s.recv(1024*1024)
    s.close()

    json_data=json.loads(data)
    resultItemList = json_data['result']
    print 'Received', repr(data), 'resultItemList num= ',len(resultItemList)


if __name__ == '__main__':
    client_send()