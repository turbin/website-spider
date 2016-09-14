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

log = Logger(__name__)

class YhdRequst(BasicSiteRequest):
    def __init__(self):
        self.base= 'http://search.yhd.com'
    
    def setKeyword(self, keyword):
        self.keyword = urllib.quote_plus(keyword)
        self.provinceId= '14'
         
    def Url(self):
        req_url = self.base + '/c' + '0' + '-0/k' +self.keyword+'/'\
                + self.provinceId + '/' + '?tp=51.' + self.keyword
        log.debug("req Url = %s" % req_url)
        return req_url
    
class YhdParser(BasicPageParser):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
#         self.page = htmlStream
     
    def getItems(self,page=None):
        log.info("@YhdParser")
        if(page == None):
            log.error("@getItems page == None please check it !")
            pass
        
        #log.info("page =%s" % page)
        tree   = etree.HTML(page)
        items  = tree.xpath(u'//div[@class=\'list_width small spread clearfix\']/div[@class=\'mod_search_pro\']')
        debugDumpTree(tree)
        return self._getGoodItems(items)
 
    '''
        todo add imges donwload 
    '''
    def _extractFromHtmlDoc(self, htmlDoc,attr=[], subNode='', subNodeAttrib='text'):
        nodes = htmlDoc.xpath(u"./div[@class=\'itemBox\']/%s[@class=\'%s\']/%s" % (attr[0],attr[1], subNode))
        if(len(nodes) == 0):
            log.error("attr =%s, subNode=%s, subNodeAttrib=%s not exsit !" % (attr, subNode, subNodeAttrib))
            return ''
        if subNodeAttrib != 'text':
            if not subNodeAttrib in nodes[0].attrib:
                return ' '
            else:
                return nodes[0].attrib[subNodeAttrib]
        else:
            return nodes[0].text
        
    def _extractImage(self,htmlDoc):
        styleOfImage  = self._extractFromHtmlDoc(htmlDoc, ['div','proImg'], 'a/img', 'style')
        #href = ' '
        href = self._extractFromHtmlDoc(htmlDoc, ['div','proImg'], 'a/img', 'src')
        href = href if href != ' ' else \
                self._extractFromHtmlDoc(htmlDoc, ['div','proImg'], 'a/img', 'original')
        
        
        def _extract_from_node(node_str):
            str_list = node_str.split(';')
            _w = str_list[0]
            _h = str_list[1]
            __parser = lambda _s,_k:_s[len(_k):(len(_s)-len('px'))]
            return __parser(_w,'width:'), __parser(_h, 'height:')
                
        width,height = _extract_from_node(styleOfImage)            
        return ImageItem(width, height, href)
        
    def _getItemFromHtmlDoc(self, htmlDoc):        
        hrefPage = self._extractFromHtmlDoc(htmlDoc, ['p','proName clearfix'], 'a', 'href')
        title    = self._extractFromHtmlDoc(htmlDoc, ['p','proName clearfix'], 'a', 'title')
        img   = self._extractImage(htmlDoc)
        price = self._extractFromHtmlDoc(htmlDoc, ['p','proPrice'], 'em', 'yhdprice')
        
        
        return ResultItem.create(price, img, 'Yhd', hrefPage, title)
                     
    def _getGoodItems(self, items, itemPaser=None):
        goodItems=[]
        for good in items:
            #log.debug("good.attrib %s" % good.attrib)
            goodItems.append(self._getItemFromHtmlDoc(good))
        return goodItems

# class JDRule(BasicRule):
#     '''
#     classdocs
#     '''
#     def __init__(self,forSite, keyword):
#         super(JDRule,self).__init__(forSite, keyword)
#         super(JDRule,self).parser = JDParser()
#         super(JDRule,self).request= JDRequst()
#         log.debug("call JDRule init")
    
    
    
