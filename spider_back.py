#!/usr/bin/env python
'''
Created on Oct 29, 2015

@author: turbin
'''
import urllib2
import os
from Queue import Queue
from threading import Thread
from __builtin__ import True

from DataStructure import JsonMessgePackage as JsonMsg
from DataStructure import JsonHelper_FromItems
from Log import Logger
from Listener import Listener
from Listener import ConnectWrapper
import cookielib
from RuleFactory import RuleFactory,BasicRule
from AbstractRule import BasicPageParser,BasicSiteRequest
from time import sleep


log = Logger(__name__)



def launchThread(run=None, daemon = False):
    t = Thread(target=run)
    t.daemon = daemon
    t.start()


class AddOnHelperInterface(object):
    def addIttems(self, items=[]):
        pass
    
class ItemsKeeper(AddOnHelperInterface):
    def __init__(self):
        self.items = []
    
    def addItems(self, items=[]):
        self.items.extend(items)

    def clearAll(self):
        self.items = None
        self.items = []

dataKeeper = ItemsKeeper()
    
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
        #print htmlstream

class downloaderWithCookie(downloader):
    
    def getPage(self):
        httpHandler = urllib2.HTTPHandler(debuglevel=1)
        httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj),httpHandler, httpsHandler)
        urllib2.install_opener(opener)
        return downloader.getPage(self)

def dumpCrawlResultItems(item_list=[]):
    pass
#     log.debug("@ dumpCrawlResultItems:")
#     for item in item_list:
#         log.debug("result item type=%s item=%s" % (type(item), repr(item)))

class CrawlSpider(object):
    def __init__(self, keyword, AddOnHelper=AddOnHelperInterface()):
        '''
        Constructor
        '''
        self.keyword = keyword #keyword for searching
        log.debug("keyword =%s " % repr(self.keyword))
        #todo add for later
        self.domain   = None #searching in sites 
        self.extend   = None #Reserved field for the feature
        self.q = Queue()
        self.keeper = AddOnHelper
    
    def doCrawl(self):
        Rule = self.q.get()
        firstPage = downloaderWithCookie(url=Rule.getRequst().Url(),data=Rule.getRequst().getData(),timeout=5).getPage()
        #print "page = %s" % page
        #log.info("page %s" % firstPage)
        if(firstPage):
            items = Rule.getPaser().getItems(firstPage)
            if not items:
                log.warn("warning not match from this sit, url=%s !" % Rule.getRequst().Url())
            else :
                log.info("do crawl success !")
                self.keeper.addItems(items)
                dumpCrawlResultItems(items)
        else:
            log.error("do crawl error!")
        
        self.q.task_done()
                            
    def crawAll(self):
        #url = "http://search.jd.com/Search?keyword=yingpan&enc=utf-8&suggest=1.his.0&wq=yingp&pvid=16kddcgi.rsht58"
        Rules=[ RuleFactory.create('SUNING', self.keyword),
                RuleFactory.create('JD', self.keyword),
                RuleFactory.create('Tmall', self.keyword),
                RuleFactory.create('Yhd', self.keyword),
                RuleFactory.create('Foodmall', self.keyword)
               ]
        
        for i in range(len(Rules)):
            log.info("create thread id=%d" % i)
            launchThread(run=self.doCrawl)
        
        for rule in Rules:
            self.q.put(rule)
        
        self.q.join()


class   CrawlJob(object):
    
    def __init__(self):
        self.connectHandler=None
        self.finishedCall = None
        
    def CrawlAll(self):
        def __decode(s):
            log.debug('@__decode')
            g = s.encode('utf-8')
            log.debug('return decode')
            return g

        try:
            log.debug("@CrawlAll ")
            log.debug('data')
            if len(dataKeeper.items) > 0:
                log.warn('clear all data !')
                dataKeeper.clearAll()

            assert self.connectHandler, \
                        log.fatal("@CrawJob has null connect handler, please take a look!")

            assert  self.finishedCall, \
                        log.fatal("@CrawJob has null finishedCall handler! please take a look!")

            message = self.connectHandler.readFrom()
            kwt = __decode(message.extract()['keyword'])

            spider  = CrawlSpider(keyword     = kwt,
                                  AddOnHelper = dataKeeper)
            log.debug("do Crawll !")
            spider.crawAll()
            log.debug("CrawAll Down !")
            log.debug('get items num = %s' % len(dataKeeper.items))
            self.connectHandler.getDataForSend(JsonHelper_FromItems(dataKeeper.items, JsonMsg()))
            self.connectHandler.close()
            self.finishedCall()
        except:
            return


    @classmethod
    def create(cls, connectHandler, finishedCallBack):
        job = CrawlJob()
        job.connectHandler = connectHandler
        job.finishedCall = finishedCallBack
        assert isinstance(job, CrawlJob)
        return job
        


    
class Dispatcher(object):
    
    def __init__(self):
        self.MaxNumOfConnect = 32
        self.q = Queue(32)
        
    def putHandler(self, connectHandler=ConnectWrapper()):
        self.q.put(CrawlJob.create(connectHandler, self.done))
    
    def done(self):
        log.info("take done !")
        self.q.task_done()
    
    def waitForHandleIt(self):
        while True:            
            job = self.q.get()
            launchThread(run=job.CrawlAll)
    
    def launching(self):
        '''
        lauching self
        '''
        launchThread(run=self.waitForHandleIt, daemon=True)


    
    
    
if __name__ == '__main__':
    listener = Listener()
    listener.bind('', 50007)

    dispatcher = Dispatcher()
    dispatcher.launching()
    while True:
        try:
            connectHandler = listener.listenning()
            dispatcher.putHandler(connectHandler)
            log.info("start next job!")
            # sleep(5)
            # listener.close()
            # exit()#for debug execute once
        except KeyboardInterrupt, e:
            log.info("user cencel")
            listener.close()
            exit()

    log.info("craw all ok")

    
    
    