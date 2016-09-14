'''
Created on Nov 2, 2015

@author: turbinyan
'''
import urllib2
from Log import Logger

log = Logger(__name__)

class PageHandler(object):
    '''
    classdocs
    '''
    def __init__(self, url, data=None,timeout=None):
        '''
        Constructor
        '''
        self.url = url
        self.timeout = timeout
        self.data = data
        
    def getPage(self):
        httpHandler = urllib2.HTTPHandler(debuglevel=1)
        httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
        opener = urllib2.build_opener(httpHandler, httpsHandler)
        urllib2.install_opener(opener)
        
        req = urllib2.Request(self.url,
                              headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'})
        #htmlstream = urllib2.urlopen(self.url, timeout=self.timeout).read()
        #htmlstream = urllib2.urlopen(req, timeout=5).read()
        res = urllib2.urlopen(req,timeout=5)
        log.debug('the resp url %s' % res.geturl())
        #print htmlstream
        return res.read()         


# class WorkerQueue(list):
#     def 