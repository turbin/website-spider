'''
Created on Nov 2, 2015

@author: turbinyan
'''

from DataStructure import JsonMessgePackage
from time import sleep
from Log import Logger
import  socket
from  SocketServer import TCPServer, StreamRequestHandler, ThreadingTCPServer, BaseRequestHandler


log=Logger(__name__)


MAXDATA_NUM = 1024

class ConnectWrapper(object):
    ''' 
    classdocs
    '''
    def __init__(self,conn=None):
        self.conn = conn
    
    def readFrom(self):
        # stream = []
        # while True:
        #     log.debug("wait for recv")
        #     data = self.conn.recv(MAXDATA_NUM)
        #     log.debug('recv =%s'% repr(data))
        #     if not data : break
        #     stream.append(data)
        log.debug('wait for data !')
        data = self.conn.recv(MAXDATA_NUM)
        log.debug('recv =%s'% repr(data))
        return JsonMessgePackage(data)
        

    def sendTo(self, message=None):
        log.debug("result num : %s" % len(message.data))
        stream = message.compress()
        #log.debug("json stream : %s" % stream)
        log.debug('send result to host')
        self.conn.send(stream)
        log.debug('send finished')
        return True

    def close(self):
        self.conn.close()


class Listener(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def bind(self, IpAddr, port):
        self.sk.bind((IpAddr,port))
        self.sk.listen(1)

        return True
        
    def listenning(self):
        log.debug("@lisenning socket !")
        conn, addr = self.sk.accept()
        log.debug("@lisenning socket new client arrived!")
        return ConnectWrapper(conn)
    
    def close(self):
        self.sk.close()
        self.sk = None
        # pass

#======================================


def get_address(host='',port=0):
    return (host,port)

def get_handler():
    pass



class ClientWrapper(object):
    request=None
    client_address = None

    def __init__(self, request=None, client_address=None):
        self.request = request
        self.client_address = client_address

    def send(self, stream=None):
        assert stream, 'stream is invalid !'
        self.request.send(stream)

    def recv(self, max_bytes=1024):
        return self.request.recv(max_bytes)

    def address(self):
        return self.client_address


# class BaseConnectHandler(object):
#     client = None
#     def __init__(self):
#         pass
#
#     def setClient(self, client):
#         self.client = client
#         pass
#
#     def handle_connect(self):
#         raise NotImplementedError
#         pass



class BaseConnectHandler(StreamRequestHandler):

    client=None

    def handle(self):
        self.client = ClientWrapper(self.request, self.client_address)
        log.info('new client arrived, address =%s' % str(self.client_address))
        pass

class TcpServerImp(object):

    port  = 0
    server = None
    HOST  = ''

    def bind(self, Addr=None, handler_class=None):
        self.server = ThreadingTCPServer(Addr,handler_class)
        return True

    def run_forever(self):
        self.server.serve_forever()

