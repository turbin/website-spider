#!/usr/bin/env python
#coding=utf-8
'''
Created on Nov 12, 2015

@author: turbinyan
'''
import urllib2
import urllib
import requests

def exchangeTohost(url):
    #         httpHandler = urllib2.HTTPHandler(debuglevel=1)
#         httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
#         opener = urllib2.build_opener(httpHandler, httpsHandler)
#         urllib2.install_opener(opener)
    form = urllib.urlencode(query={
                                'type':'goods',
                                'keyword':urllib.quote('陕西红富士'),
                                'kwt':'陕西红富士'
                            })
    req = urllib2.Request(url,
                          headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
                                    #'contentType':'application/json',
                                   },
                          data = form
                          )
    try:
        #res =requests.post(url, form)
        res = urllib2.urlopen(req,timeout=5)
        #print 'the resp url %s' % res.geturl()
        print 'response data %s' % res.read()
    
    except urllib2.HTTPError, e:
        print ('require site =%s failed, http error code ' % url,e.code)
   
    #todo add throw
    #print htmlstream

if __name__ == '__main__':
    exchangeTohost(url='http://10.6.65.57:8080/imall/search.htm')
    pass
    
    
    
