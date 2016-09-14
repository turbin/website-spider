'''
Created on Nov 2, 2015

@author: turbinyan
'''

# from RuleForJD import  JDRule
from Log import Logger

log = Logger(__name__)

class BasicPageParser(object):
    '''
        abstract class for parser
    '''
    def __init__(self):
        pass
    
    def getItems(self, page=None):
        log.debug("call BasicPageParser class Method getItems")
        raise NotImplementedError

class BasicSiteRequest(object):
    '''
    abstarct class for request
    '''
    def __init__(self):
        pass
    
    def setKeyword(self,keyword):
        log.debug("call BasicSiteRequest class Method setKeyword")
        raise NotImplementedError
    
    def Url(self):
        log.debug("call BasicSiteRequest class Method Url")
        raise NotImplementedError
        
    def getData(self):
        return None
