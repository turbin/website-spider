'''
Created on Nov 10, 2015

@author: turbinyan
'''

import json
import re

jsonT= '''
getDataFromDsServer({\"status\":200,\
                     \"rs\":[{\"cmmdtyCode\":\"000000000124997068\",\
                            \"catentryId\":\"24374351\",\"price\":\"295.00\",\
                            \"priceType\":\"1\",\"bizCount\":\"1\",\
                            \"bizCode\":\"0070065388\",\
                            \"vendorName\":\"\xe4\xb9\x85\xe5\x88\x9b\xe4\xbc\x9f\xe4\xb8\x9a\xe7\x94\xb5\xe8\x84\x91DIY\xe4\xb8\x93\xe8\x90\xa5\xe5\xba\x97\",\
                            \"govPrice\":\"\",\"type\":\"1\",\"subCode\":\"\",\"invStatus\":\"1\",\
                            \"commondityTry\":\"\",\"reservationType\":\"\",\
                            \"reservationPrice\":\"\",\"subscribeType\":\"\",\
                            \"subscribePrice\":\"\",\"collection\":\"\",\
                            \"visited\":\"\",\"sellingPoint\":\"\",\
                            \"promoTypes\":[],\"imageUrl\":\"\",\"patternCss\":\"\",\"text\":\"\"}],\"message\":null});
'''
#,
# '''
# getDataFromDsServer({"status":200,\
#                             \"rs":[{"cmmdtyCode":"000000000120060162","catentryId":"20813562",\
#                             \"price":"295.00","priceType":"1","bizCount":"3",\
#                             \"bizCode":"0070066468","vendorName":"\xCE\xF7\xB2\xBF\xCA\xFD\xBE\xDD\xA3\xA8\x57\x44\x29\xB4\xE6\xB4\xA2\xC8\xD9\xB7\xA2\xD7\xA8\xD3\xAA\xB5\xEA",\
#                             \"govPrice":"","type":"1","subCode":"","invStatus":"1",\
#                             \"commondityTry":"","reservationType":"","reservationPrice":"",\
#                             \"subscribeType":"","subscribePrice":"","collection":"","visited":"",\
#                             \"sellingPoint":"","promoTypes":[],"imageUrl":"","patternCss":"","text":""}],"message":null});
# '''
# ]




pattern_0 = r'\([^()]*\)'      #depth 0 pattern
pat_left = r'\((?:[^()]|'    
pat_right = r')*\)'
def pattern_generate(pattern, depth=0):
    while(depth):
        pattern = pat_left + pattern + pat_right
        depth -= 1
    return pattern

def extractJsonFromResponse(stream=[], pat=[]):
    keyword_list = re.compile(pat)
    matchObj = keyword_list.search(stream)
    jsonObj = None if not matchObj else matchObj.group(0)
    
    if not jsonObj:
        print('json objct not exsit !')
        return None
    
    lastElementIndex = len(jsonObj) -1
    jsonObj = jsonObj[1:lastElementIndex]
    return jsonObj
    
    
def testForJson(jsonStream):
    print('jsonStream : %s' % jsonStream)
    last = len(jsonStream)-len(');')-1
    jsonObj = jsonStream[len('getDataFromDsServer(')+1:last]
    print('jsonObj =%s', jsonObj)
#     jsonObj = extractJsonFromResponse(jsonStream, pattern_generate(pattern_0, 2))
    respJson =  json.loads(jsonObj)
    print('json result : %s' % repr(respJson))
    price = respJson['rs'][0]['price']
    print('price =%s' % price)
    
if __name__ == '__main__':
    testForJson(jsonT)
    
    
    
    