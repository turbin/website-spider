#coding=utf-8
'''
Created on Nov 3, 2015

@author: turbinyan
'''

from string import Template
import urllib
import urllib2
from lxml import etree
from DataStructure import ImageItem
from DataStructure import ResultItem
from Utility import debugDumpDiv, debugDumpTree
from AbstractRule import  BasicPageParser,BasicSiteRequest
from Log import Logger
import json
from json.decoder import JSONObject

log = Logger(__name__)

#
'''
from searchi_result_new.js in site script.suning.com
function cutPrefix(g, k) {
    if (typeof(g) != "undefined") {
        if (g.length == k) {
            return g
        }
        if (g.length > k) {
            var i = /[0-9]+([0-9]{9})/;
            if (i.test(g)) {
                g = g.match(i)[1] + ""
            }
            return g
        }
        var l = k - g.length;
        var h = "";
        for (var j = 0; j < l; j++) {
            h += "0"
        }
        return h + g
    }
}
'''
class SuningHelper(object):
    
    def __int__(self):
        pass
    
    @staticmethod
    def ajax(url='', referer=None, headers=None, data=None):
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
        req.add_header('X-Requested-With','XMLHttpRequest')
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116')
        
        if referer:
            req.add_header('Referer',referer)
        if headers:
            for k in headers.keys():
                req.add_header(k,headers[k])
        
        params = None if not data else urllib.urlencode(data)
        response = urllib2.urlopen(req, params)
        jsonText = response.read()
        log.debug("json response %s" % (repr(jsonText)))
        return jsonText
    
    @staticmethod
    def wrapJsonLoad(stream):
        log.debug("@wrapJsonLoad, stream=%s" % repr(stream))
        return json.loads(stream)
    
    @staticmethod
    def getUrl(forItem='',divWrapNode=None,cityId='9017'):
    
    
        def __for_price(cityId, divWrapNode):
            __test = lambda v, attr:True if attr in v.attrib else False
            
            classHidenInfo = divWrapNode.xpath('.//input[@class=\'hidenInfo\']')
            
#             assert (classHidenInfo==None or len(classHidenInfo)==0), \
#                 log.debug('./input[@class=\'hidenInfo\'] not exsit !');\
#                 return None

            if not classHidenInfo or len(classHidenInfo)==0:
                log.error('./input[@class=\'hidenInfo\'] not exsit !')
                return None
            
            datapro = classHidenInfo[0].attrib['datapro']
            u = datapro.split('||')
            if not (len(u) == 3):
                log.error('./input[@class=\'hidenInfo\'] attr=dataPro has invalid value!') 
                return None
             
            #depend on requires from the site in keyword 'yingpan'
            '''demo:http://ds.suning.cn/ds/general/\
            000000000132452578_29899336-9018-1--1--getDataFromDsServer.jsonp
            '''
    #             q = '1'
    #             r = ''
    #
            cmmdtyCode=''
            catentryId=None
             
            if(__test(classHidenInfo[0], 'multinumberid') and 
               __test(classHidenInfo[0], 'multinumber')):
                catentryId = classHidenInfo[0].attrib['multinumberid']
                cmmdtyCode = classHidenInfo[0].attrib['multinumber']
            else:
                cmmdtyCode = u[1].zfill(18)
                catentryId = u[0]
            
            urlTemplate = ('%s/ds/general/%s_%s-%s-1--1--getDataFromDsServer.jsonp' % 
                            ('http://ds.suning.cn', cmmdtyCode, catentryId, cityId)
                           )
             
            return urlTemplate
         
        if(forItem == 'price'):    
            return __for_price(cityId, divWrapNode)   
        else:
            return None

class SuningResourceDownloader(object):
    '''
    for download resource from suning site,as price,image and on.
    '''
    def __init__(self):
        pass
    
    def getItemPrice(self, url=None):
        if url == None:
            log.warn("getItem Price Faild")
            return None
        
        response =  SuningHelper.ajax(url)
        
        last = len(response)-len(');')
        jsonObj = response[len('getDataFromDsServer('):last]
#         jsonObj = Util_extractJsonFromResponse(response, 
#                                      Util_pattern_generate(depth=1))
        if not jsonObj:
            log.warn("extract from response json value error!")
            return None
        
        respJson =  SuningHelper.wrapJsonLoad(jsonObj)
        price = respJson['rs'][0]['price']
        log.debug('price =%s' % price)
        #todo for test
        return price
            
class SuningRequst(BasicSiteRequest):
    def __init__(self):
        self.base= 'http://search.suning.com'
        self.locationCodes={
                            'beijing':'9017',
                            'xiamen': '9019',
                            'fuzhou': '9018',
                            'guangzhou': '9041',
                            'shanghai' : '9264'}
    
    def setKeyword(self, keyword):
        self.keyword = urllib.quote(keyword) #todo fix the encode in CH char
         
    def Url(self):
        return self.base +'/'+self.keyword+'/cityid='+self.locationCodes['beijing']
    
    
class SuningParser(BasicPageParser):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
#         self.page = htmlStream

    def getItems(self,page=None):
        log.info("@Suning")
        if(page == None):
            log.error("@getItems page == None please check it !")
            pass
        
        tree   = etree.HTML(page)
        items  = tree.xpath(u'//div[@class=\'grid\']/ul[@class=\'items   clearfix \']/li/div[@class=\'wrap\']')
        return self._getGoodItems(items)
 
    '''
        todo add imges donwload
    '''
    def _extractFromHtmlDoc(self, htmlDoc,div1=None,nodeName=None,subNodeAttrib=None):
        nodes = htmlDoc.xpath(u".//div[@class=\'%s\']/%s"
                              % (div1, nodeName))
        if(len(nodes) == 0):
            log.error("div1 =%s,subNode=%s, not exsit !" % (div1, nodeName))
            return ''
        
        return nodes[0].attrib[subNodeAttrib]
    
    def _extractFromHtmlDocWithText(self, htmlDoc,div1=None,nodeName=None):
        nodes = htmlDoc.xpath(u".//div[@class=\'%s\']/%s"
                              % (div1, nodeName))
        if(len(nodes) == 0):
            log.error("div1 =%s,subNode=%s, not exsit !" % (div1, nodeName))
            return ''
        
        return nodes[0].text
    
    def _extractImage(self,htmlDoc):
#         format = Template("./div[@class=\'wrap\']/div[@class='\${attr1}\']/")
        width  = self._extractFromHtmlDoc(htmlDoc, 'i-pic limit clearfix','a/img', 'width')
        height = self._extractFromHtmlDoc(htmlDoc, 'i-pic limit clearfix','a/img', 'height')
        href   = self._extractFromHtmlDoc(htmlDoc, 'i-pic limit clearfix','a/img', 'src2')
        
        return ImageItem(width, height, href)
        
    def _getItemFromHtmlDoc(self, htmlDoc):
        debugDumpDiv(htmlDoc)

        hrefPage = self._extractFromHtmlDoc(htmlDoc, 'i-name limit clearfix', 'a', 'href')
        img      = self._extractImage(htmlDoc)
        url = SuningHelper.getUrl(forItem='price',
                                  divWrapNode=htmlDoc
                                  #divWrapNode=htmlDoc.xpath(u'./div[@class=\'wrap\']')[0]
                                 )
        
        price    = SuningResourceDownloader().getItemPrice(url)
        
        title = self._extractFromHtmlDoc(htmlDoc, 'i-name limit clearfix', 'a','title')
        
        return ResultItem.create(price, img, 'SUNING', hrefPage, title)
                     
    def _getGoodItems(self, items, itemPaser=None):
        goodItems=[]
        for good in items:
            goodItems.append(self._getItemFromHtmlDoc(good))
        return goodItems


    
    
    
