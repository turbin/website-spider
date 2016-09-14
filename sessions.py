
import urllib2
import os
from Log import Logger

log = Logger(__name__)


headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
    'X-Requested-With':'XMLHttpRequest'
}


class downloader(object):
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
        #httpHandler = urllib2.HTTPHandler(debuglevel=1)
        #httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
        #opener = urllib2.build_opener(httpHandler, httpsHandler)
        #urllib2.install_opener(opener)
        log.info('data =%s ' % self.data)
        req = urllib2.Request(self.url,
                              data=self.data,
                              headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'})
        #htmlstream = urllib2.urlopen(self.url, timeout=self.timeout).read()
        #htmlstream = urllib2.urlopen(req, timeout=5).read()
        try:
            res = urllib2.urlopen(req,timeout=5)
            log.debug('the resp url %s' % res.geturl())
            return res.read()

        except urllib2.HTTPError as e:
            log.error('require site =%s failed, http error code =%s' % (self.url,e.code))
            return None
        except urllib2.URLError as url_e:
            log.error('require site =%s failed, http error code =%s' % (self.url,url_e.reason))
            return None
        #todo add throw





class session(object):

    def __init__(self):
        pass

#    def ajax_request(self, request):



