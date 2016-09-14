'''
Created on Nov 9, 2015

@author: turbinyan
'''

import urllib2
import urllib
import json

def request_ajax_data(url,data,referer=None,**headers):
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    req.add_header('X-Requested-With','XMLHttpRequest')
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116')
    if referer:
        req.add_header('Referer',referer)
    if headers:
        for k in headers.keys():
            req.add_header(k,headers[k])

    params = urllib.urlencode(data)
    response = urllib2.urlopen(req, params)
    jsonText = response.read()
    print("json response %s" % (repr(jsonText)))
    return jsonText


if __name__ == '__main__':
    site = 'http://www.suning.com/emall/priceService_9018_123742276_1_priceServiceCallBack_.html'
    data_type = 'jsonp'
    jsonp='false'
    cache_control = 'Yes'
    jsonpCallback='priceServiceCallBack'
    cache='true'
    req_data={
              "dataType":data_type,
              "jsonp":jsonp,
    }
    res=request_ajax_data(url=site, data=req_data)
    print "json responce %s " % repr(res)
    pass





