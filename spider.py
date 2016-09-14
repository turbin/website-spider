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
#from DataStructure import JsonMessgePackage
from DataStructure import JsonHelper_FromItems
from Log import Logger
from Listener import ClientWrapper,BaseConnectHandler,TcpServerImp, get_address
from JobQueue import JobQ, JobHandler


import cookielib
from RuleFactory import RuleFactory,BasicRule
from AbstractRule import BasicPageParser,BasicSiteRequest
from time import sleep


log = Logger(__name__)

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


class ItemsKeeper(list):
    def addItems(self, items=None):
        log.info('add items!')
        if not items:
            log.warn('add items failed, items == None!')
            return
        self.extend(items)

def _decode(s):
    log.debug('@here')
    g = s.encode('utf-8')
    log.debug('return decode')
    return g

class crawlPage(JobHandler):
    Rule = None
    keeper = None

    def __init__(self,rule, data_keeper=None):
        self.Rule = rule
        self.keeper = data_keeper

    def run_job(self):
        firstPage = downloaderWithCookie(url=self.Rule.getRequst().Url(),data=self.Rule.getRequst().getData(),timeout=5).getPage()
        #print "page = %s" % page
        #log.info("page %s" % firstPage)
        if(firstPage):
            items = self.Rule.getPaser().getItems(firstPage)
            if not items:
                log.warn("warning not match from this sit, url=%s !" % self.Rule.getRequst().Url())
            else :
                log.info("do crawl success !")
                self.keeper.addItems(items)
                dumpCrawlResultItems(items)
        else:
            log.error("do crawl error!")


class TcpConnectHandler(BaseConnectHandler):

    def handle(self):
        BaseConnectHandler.handle(self)

        data = self.client.recv()
        log.debug('recv =%s'% repr(data))

        json_data= JsonMsg(data)
        kwt = _decode(json_data.extract()['keyword'])


        Rules=\
        [
            RuleFactory.create('SUNING',   kwt),
            RuleFactory.create('JD',       kwt),
            RuleFactory.create('Tmall',    kwt),
            RuleFactory.create('Yhd',      kwt),
            RuleFactory.create('Foodmall', kwt)
        ]

        job_q  = JobQ(len(Rules))
        items  = ItemsKeeper()

        for rule in Rules:
            log.info("create thread for %s" % (rule.forSite))
            job_q.addJob(crawlPage(rule,items))

        log.debug("do Crawll !")

        job_q.startAll()
        job_q.wait_for_done()

        log.debug("CrawAll Down !")
        log.debug('get items num = %s' % len(items))

        json_data = JsonHelper_FromItems(items, JsonMsg())
        self.client.send(json_data.compress())


if __name__ == '__main__':
    tcp_server = TcpServerImp()
    tcp_server.bind(get_address('', 50007),TcpConnectHandler)
    tcp_server.run_forever()




