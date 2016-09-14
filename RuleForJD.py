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
from PIL.ImImagePlugin import MODE
from Utility import Utility

log = Logger(__name__)

class JDRequst(BasicSiteRequest):
    def __init__(self):
        self.enc = 'utf-8'
        self.suggest = '1.his.0'
        self.pivd='16kddcgi.rsht58'
        self.base= 'http://search.jd.com/Search'
    
    def setKeyword(self, keyword):
        self.keyword = keyword
        self.wq = keyword
        
    def toRequstData(self):
        return urllib.urlencode(
                    {'keyword': self.keyword,
                     'enc':'utf-8'}
                    )
         
    def Url(self):
        return self.base +'?'+self.toRequstData()
    
    
class JDParser(BasicPageParser):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
#         self.page = htmlStream
     
    def getItems(self,page=None):
        log.info("@JDParser")
        if(page == None):
            log.error("@getItems page == None please check it !")
            pass
        #log.info("page =%s" % page)
        tree   = etree.HTML(page)
        items  = tree.xpath(u'//ul[@class=\'gl-warp clearfix\']/li[@data-sku]')
        #log.debug("items %s" % repr(items))
        #log.debug('item nums %s' % (len(items)))
        return self.getGoodItems(items)
 
    '''
        todo add imges donwload 
    '''
    def _extractFromHtmlDoc(self, htmlDoc,attr, subNode, subNodeAttrib):
        nodes = htmlDoc.xpath(u"./div[@class=\'gl-i-wrap\']/div[@class=\'%s\']/%s" % (attr, subNode))
        if(len(nodes) == 0):
            log.error("attr =%s, subNode=%s, not exsit !" % (attr, subNode))
            return ''
        
        return nodes[0].attrib[subNodeAttrib]
    
    def _extractImage(self,htmlDoc):
        width  = self._extractFromHtmlDoc(htmlDoc, 'p-img', 'a/img', 'width')
        height = self._extractFromHtmlDoc(htmlDoc, 'p-img', 'a/img', 'height')
        #todo implement later
        #href   = self._extractFromHtmlDoc(htmlDoc, 'p-img', 'a/img',  'src')
        
        href = ''
        
        nodes = htmlDoc.xpath(u"./div[@class=\'gl-i-wrap\']/div[@class=\'p-img\']/a/img")
        if(len(nodes) == 0):
            log.error("attr =%s, subNode=%s, not exsit !" % ('p-img', 'a/img'))
            return ''
        
        #log.debug('nodes type=%s nodes[0].attrib = %s' % (type(nodes[0].attrib),nodes[0].attrib))
        #todo find out why the node extract as src or data-lazy-img
        
        if 'src' in nodes[0].attrib:
            href = nodes[0].attrib['src']
        elif 'data-lazy-img' in nodes[0].attrib:
            href = nodes[0].attrib['data-lazy-img']
        else :
            log.warn("src/data-lazy-img not exist !")
            href = ''

        href = Utility.AddPrefixIfNotExsit(href, 'http:')
        return ImageItem(width, height, href)
        
    def getItemFromHtmlDoc(self, htmlDoc):        
        hrefPage = Utility.AddPrefixIfNotExsit(self._extractFromHtmlDoc(htmlDoc, 'p-img', 'a', 'href'),'http:')
        img   = self._extractImage(htmlDoc)
        price = self._extractFromHtmlDoc(htmlDoc,'p-price', 'strong', 'data-price')
        
        #subPath = Template(u"./div[@class=\'gl-i-wrap\']/div[@class=\'${attr}\']/${subNode}")
        nodes = htmlDoc.xpath(u"./div[@class=\'gl-i-wrap\']/div[@class=\'p-name p-name-type-2\']/a/em")
#         debugDumpDiv(nodes)
        title = '' if len(nodes)==0 else nodes[0].text
        
        return ResultItem.create(price, img, 'JD', hrefPage, title)
                     
    def getGoodItems(self, items, itemPaser=None):
        goodItems=[]
        for good in items:
            #log.debug("good.attrib %s" % good.attrib)
            goodItems.append(self.getItemFromHtmlDoc(good))
        return goodItems

def debugDumpDiv(div_list):
    for div in div_list:
        log.debug('div = %s' % (div.tag))
# class JDRule(BasicRule):
#     '''
#     classdocs
#     '''
#     def __init__(self,forSite, keyword):
#         super(JDRule,self).__init__(forSite, keyword)
#         super(JDRule,self).parser = JDParser()
#         super(JDRule,self).request= JDRequst()
#         log.debug("call JDRule init")
    
    
    
