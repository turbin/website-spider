'''
Created on Nov 6, 2015

@author: turbinyan
'''
import  re
from Log import Logger

log = Logger(__name__)

#         self.page = htmlStream
def debugDumpTree(doc_tree):
    for element in doc_tree.iter():
        log.debug('element = %s attribute= %s text=%s' % (element.tag, element.attrib, repr(element.text)))

def debugDumpDiv(div_list):
    if len(div_list)==0:
        log.debug("empty div list %s" % div_list.__name__)
        return 
    for div in div_list:
        log.debug('div = %s attribute= %s' % (div.tag, div.attrib))
        debugDumpTree(div)

def debugDumpTree2File(doc_tree, file_name):
    with open(name =file_name, mode='w+') as fp:
        for element in doc_tree.iter():
            fp.write('element = %s attribute= %s text=%s' % (element.tag, element.attrib, repr(element.text)))
            
            
            
pattern_0 = r'\([^()]*\)'      #depth 0 pattern
pat_left = r'\((?:[^()]|'    
pat_right = r')*\)'

class Utility(object):

    @staticmethod
    def AddPrefixIfNotExsit(str_in='',prefix=None):
        # assert not prefix,rised ImportError
        if str_in == '' or not prefix:
            return str_in

        if not str_in.startswith(prefix):
            return prefix+str_in

        return str_in

    @staticmethod
    def ExtractJsonFromResponse(stream=[], pat=[]):
        keyword_list = re.compile(pat)
        matchObj = keyword_list.search(stream)
        jsonObj = None if not matchObj else matchObj.group(0)

        if not jsonObj:
            log.warn('json objct not exsit !')
            return None

        lastElementIndex = len(jsonObj) -1
        jsonObj = jsonObj[1:lastElementIndex]
        log.debug('jsonObj:%s' % repr(jsonObj))
        return jsonObj

    @staticmethod
    def PatternGenerater(pattern=pattern_0, depth=0):
        while(depth):
            pattern = pat_left + pattern + pat_right
            depth -= 1
        return pattern


