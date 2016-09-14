#coding=utf-8
'''
Created on Nov 2, 2015

@author: turbinyan
'''

from Log import Logger
import json

log = Logger(__name__)

KeywordForSearching = '硬盘'

class ImageItem(object):
    def __init__(self, width=None, height=None, hRef=None):
        self.width=width
        self.height=height
        self.hRef=hRef
        self.byteCode=None
        self.fileName = ''
        #log.debug("width=%s height=%s hRef=%s" % (self.width, self.height, self.hRef))
    # pull the image from site, depend on href
    def pullFromSite(self):
        #todo add donwloader
        pass

# def ResultItemBuilder(resultItem, 
#                       price         = None,
#                       image         = ImageItem(),
#                       site          = None,
#                       itemRefPage   = None,
#                       title         = None
#                       ):
#     
#     resultItem.price = price
#     resultItem.image = image
#     resultItem.site  = site
#     resultItem.RefPage = itemRefPage
#     resultItem.title = title


class ResultItem(object):
    def __init__(self):
        self.price = ''
        self.image = ImageItem()
        self.SourceSite=''
        self.title = ''
        self.RefPage = ''
        self.title = ''
        
    @classmethod
    def create(cls, 
                      price         = None,
                      image         = ImageItem(),
                      site          = None,
                      itemRefPage   = None,
                      title         = None):
        result = ResultItem()
        result.price = price
        result.image = image
        result.SourceSite  = site
        result.RefPage = itemRefPage
        result.title = title
#         log.debug("result price=%s site=%s RefPage=%s title=%s" % (price, site, itemRefPage, title))
        return result
    
    
    def getPrice(self):
        return self.price
    
    def getImageInfo(self):
        return {'width':self.image.width, 'height':self.image.height, 'href':self.image.hRef}
    
    def getSourceSite(self):
        return self.SourceSite
    
    def getTitle(self):
        return self.title
    
    def getRefPage(self):
        return self.RefPage
    

class JsonMessgePackage(object):
    '''
    jsons object
    '''
    def __init__(self, data=None):
        #$self.msg={'keyword':KeywordForSearching}
        self.data = data or []
        
    def extract(self):
        #return self.msg #for test
        #log.debug("@extract ")
        return json.loads(self.data)
    
    def compress(self):
        return json.dumps({'result': self.data})

def __helper_item2dic(resultItem, message=[]):
    #log.debug('resultItem typeOf=%s resultItem=%s' %(type(resultItem), repr(resultItem)))
    _strip=lambda s:s if not isinstance(s,basestring)else s.strip()

    itemMap= {
        'source'      : resultItem.SourceSite,
        'title'       : _strip(resultItem.title),
        'price'       : resultItem.price,
        'referecePage': resultItem.RefPage,
        'imageRefUrl' : resultItem.image.hRef
    }
# 
#     itemMap= {
#         'title'       : 'yingpan',
#         'price'       :  '123',
#         'referecePage':  'app'
#     }   
    message.append(itemMap)
    return message

def JsonHelper_FromItems(resultItems =[] , message=JsonMessgePackage()):
    #i=0
    #log.debug("result num : %s" % len(message.data))
    for item in resultItems:
        #log.debug('id=%s' %(i))
        __helper_item2dic(item, message.data)
        #i = i+1
    return message

