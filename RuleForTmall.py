#coding=gbk

'''
Created on Nov 3, 2015

@author: turbinyan
'''

from string import Template
import urllib
from lxml import etree
from DataStructure import ImageItem
from DataStructure import ResultItem
from AbstractRule import  BasicPageParser,BasicSiteRequest
from Utility import debugDumpTree
from Log import Logger
from Utility import  Utility
import chardet

log = Logger(__name__)

class TmallRequst(BasicSiteRequest):
    def __init__(self): 
        self.base= 'https://list.tmall.com/search_product.htm'
    
    def setKeyword(self, keyword):
        self.keyword = keyword
        request ={
                  'q':self.keyword,
                  'type':'p',
                  'vmarket':'',
                  'spm':'875.7789098.a2227oh.d100',
                  'from':'mallfp..pc_1_searchbutton'
                  }
        self.request = urllib.urlencode(request)
         
    def Url(self):
        req_url = self.base + '?' + self.request
        log.debug("req Url = %s" % req_url)
        return req_url
    
class TmallParser(BasicPageParser):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
#         self.page = htmlStream
     
    def getItems(self,page=None):
        log.info("@Tmall Parser")
        if(page == None):
            log.error("@getItems page == None please check it !")
            pass
        
        #log.debug("page coding in %s:" % chardet.detect(page)['encoding'])
        #encoding = chardet.detect(page)['encoding']
        #log.info("page =%s" % page)
        try:
            tree   = etree.HTML(page.decode('gbk'))
            items  = tree.xpath(u'//div[@id=\'J_ItemList\']/div[@class=\'product  \']')
            #log.debug("dump items")
            #debugDumpTree(items[0])
            return self._getGoodItems(items)
        except Exception as e:
            log.error("parser tree error %s" % repr(e))
            return []
    
    '''
        todo add imges donwload 
    '''
    def _extractFromHtmlDoc(self, htmlDoc,attr=[], subNode='', subNodeAttrib='text'):
        nodes = htmlDoc.xpath(u"./div[@class=\'product-iWrap\']/%s[@class=\'%s\']/%s" % (attr[0],attr[1], subNode))
        if(len(nodes) == 0):
            log.error("attr =%s, subNode=%s, subNodeAttrib=%s not exsit !" % (attr, subNode, subNodeAttrib))
            return None
        
        if subNodeAttrib != 'text':
            if not subNodeAttrib in nodes[0].attrib:
                return None
            else:
                return nodes[0].attrib[subNodeAttrib]
        else:
            return nodes[0].text
        
    def _extractImage(self,htmlDoc):
        href  = self._extractFromHtmlDoc(htmlDoc, ['div','productImg-wrap'], 'a/img', 'src')
        href  = href if href else \
                self._extractFromHtmlDoc(htmlDoc, ['div','productImg-wrap'], 'a/img', 'data-ks-lazyload')

        href = Utility.AddPrefixIfNotExsit(href, 'http:')
        return ImageItem('220px', '220px', href)
    
    def _getItemFromHtmlDoc(self, htmlDoc):
                
        hrefPage = Utility.AddPrefixIfNotExsit(self._extractFromHtmlDoc(htmlDoc, ['p','productTitle'], 'a', 'href'),'http:')
        title    = self._extractFromHtmlDoc(htmlDoc, ['p','productTitle'], 'a', 'text')
        img   = self._extractImage(htmlDoc)
        price = self._extractFromHtmlDoc(htmlDoc, ['p','productPrice'], 'em', 'title')
        
        
        return ResultItem.create(price, img, 'Tmall', hrefPage, title)
                     
    def _getGoodItems(self, items, itemPaser=None):
        goodItems=[]
        __exist = lambda n,a:True if a in n.attrib else False
         
        for good in items:
            goodItems.append(self._getItemFromHtmlDoc(good))
        return goodItems

    
    
    
