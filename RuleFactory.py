'''
Created on Nov 3, 2015

@author: turbinyan
'''

from AbstractRule import BasicPageParser,BasicSiteRequest
from RuleForJD import JDParser,JDRequst
from RuleForSuning import SuningParser, SuningRequst
from RuleForYhd import YhdParser,YhdRequst
from RuleForTmall import TmallParser,TmallRequst
from RuleForFoodmall import FoodmallRequst, FoodmallParser
from Log import Logger


log = Logger(__name__)

class BasicRule(object):
    def __init__(self, forSite, keyword):
        self.forSite = forSite
        self.keyword = keyword
        self.parser = None
        self.request = None
        pass
    
    def getPaser(self):
        log.debug("call AbstracutRule class Method getPaser")
        return self.parser
    
    def getRequst(self):
        log.debug("call AbstracutRule class Method getRequst")
        self.request.setKeyword(self.keyword)
        return self.request
    
    @classmethod
    def create(cls, 
                parser=BasicPageParser(), 
                Reuest=BasicSiteRequest(),
                forSite='',
                keyword=''
                ):
        rule = BasicRule(forSite, keyword)
        
        rule.parser  = parser
        rule.request = Reuest
        assert isinstance(rule, BasicRule)
        return rule
        
class RuleFactory(object):
    
    def __init__(self):
        pass
    
    @staticmethod
    def create(theForSite, theKeyword):
        if(theForSite == 'JD'):
            return BasicRule.create(parser=JDParser(), 
                                     Reuest=JDRequst(), 
                                     forSite=theForSite, 
                                     keyword=theKeyword)
        elif(theForSite == 'SUNING'):
            return BasicRule.create(parser=SuningParser(),
                         Reuest=SuningRequst(),
                         forSite=theForSite,
                         keyword=theKeyword)
            
        elif(theForSite == 'Yhd'):
            return BasicRule.create(parser=YhdParser(),
                         Reuest=YhdRequst(),
                         forSite=theForSite,
                         keyword=theKeyword)
            
        elif(theForSite == 'Tmall'):
            return BasicRule.create(parser=TmallParser(),
                         Reuest=TmallRequst(),
                         forSite=theForSite,
                         keyword=theKeyword)
                         
        elif(theForSite == 'Foodmall'):
            return BasicRule.create(parser=FoodmallParser(),
                         Reuest=FoodmallRequst(),
                         forSite=theForSite,
                         keyword=theKeyword)
        else:
            return None
        
        