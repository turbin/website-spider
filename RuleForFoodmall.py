#coding=utf-8
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
from Log import Logger
from Utility import debugDumpTree
from PIL.ImImagePlugin import MODE

log = Logger(__name__)

class FoodmallRequst(BasicSiteRequest):
    def __init__(self):
        #self.base = 'http://10.6.65.57:8080/imall/search.htm'
        self.base= 'http://www.foodmall.com/search.htm'
    
    def setKeyword(self, keyword):
        self.keyword = urllib.quote(keyword)
        
    def getData(self):
        log.debug('@getData')
        return urllib.urlencode(
                    {'type':'goods',
                     'keyword':self.keyword
                    }
                )
         
    def Url(self):
        return self.base
    
    
class FoodmallParser(BasicPageParser):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
#         self.page = htmlStream
     
    def getItems(self,page=None):
        log.info("@FoodmallParser")
        if(page == None):
            log.error("@getItems page == None please check it !")
            pass
        #log.info("page =%s" % page)
        tree   = etree.HTML(page.decode('utf-8'))
        items  = tree.xpath(u'//div[@class=\'grid-goodsDiv\']/ul[@class=\'itemslist\']/li[@class=\'itemLi\']')
      #  log.debug("dump tree")
      #  debugDumpTree(tree)
        
        return self.getGoodItems(items)
 
    '''
        todo add imges donwload 
    '''
    def _extractFromHtmlDoc(self, htmlDoc,attr, subNode, subNodeAttrib):
        nodes = htmlDoc.xpath(u"./div[@class=\'itemDiv\']/%s[@class=\'%s\']/%s" % (attr[0],attr[1], subNode))
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
        width  = self._extractFromHtmlDoc(htmlDoc, ['div','pic'], 'a/img', 'width')
        height = self._extractFromHtmlDoc(htmlDoc, ['div','pic'], 'a/img', 'height')        
        href = self._extractFromHtmlDoc(htmlDoc,   ['div','pic'], 'a/img', 'original')

            
        return ImageItem(width, height, href)
        
    def getItemFromHtmlDoc(self, htmlDoc):        
        hrefPage = self._extractFromHtmlDoc(htmlDoc, ['div','name'], 'a', 'href')
        img   = self._extractImage(htmlDoc);
        price = self._extractFromHtmlDoc(htmlDoc, ['div','price'], 'span[@class=\'f_red\']', 'text')[1:]
        title = self._extractFromHtmlDoc(htmlDoc, ['div','name'], 'a', 'text')
        
        return ResultItem.create(price, img, 'Foodmall', hrefPage, title)
                     
    def getGoodItems(self, items, itemPaser=None):
        goodItems=[]
        for good in items:
            #log.debug("dump good")
            #debugDumpTree(good)
            goodItems.append(self.getItemFromHtmlDoc(good))
        return goodItems

    
    
