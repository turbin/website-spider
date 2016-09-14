'''
Created on Nov 3, 2015

@author: turbinyan
'''
#coding=utf-8
import logging
import sys


'''
utility for getting break point info,as line number, function name and so on.\
print sys._getframe().f_code.co_name
print sys._getframe().f_back.f_code.co_name
'''
def _get_breakpoint():
    funcName   = sys._getframe(1).f_back.f_code.co_name
    lineNumber = sys._getframe(1).f_back.f_lineno
    return (funcName,lineNumber)

class Logger(object):
    '''
    classdocs
    '''
    def __init__(self,theModuleName):
        '''
        Constructor
        '''
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s %(message)s',
            filename='/tmp/spider.log',
            filemode='w'
            )

        self.theModuleName = theModuleName
        self.logger = logging.getLogger(theModuleName)
        self.logger.setLevel(logging.FATAL)

    
    def __log(self,level,text,func, line):
        if level == 'warn':
            logging.warning('[@fn=%s,ln=%s]%s'%(func,line,text))
        elif level == 'Fatal':
            logging.fatal('[@fn=%s,ln=%s]%s'%(func,line,text))
        elif level == 'Error':
            logging.error('[@fn=%s,ln=%s]%s'%(func,line,text))
        elif level == 'Info':
            logging.info('[@fn=%s,ln=%s]%s'%(func,line,text))
        elif level == 'Debug':
            logging.debug('[@fn=%s,ln=%s]%s'%(func,line,text))
        
    def warn(self,text=''):
        func,line = _get_breakpoint()
        self.__log('warn', text,func,line)


    def fatal(self,text=''):
        func,line = _get_breakpoint()
        self.__log('Fatal', text,func,line)
    
    def error(self,text=''):
        func,line = _get_breakpoint()
        self.__log('Error', text, func,line)
        
    
    def info(self,text=''):
        func,line = _get_breakpoint()
        self.__log('Info', text, func,line)
        
    def debug(self,text=''):
        func,line = _get_breakpoint()
        self.__log('Debug', text, func,line)



