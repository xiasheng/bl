
from django.http import HttpResponse
from random import Random
import json

MAGIC_SALT = 'mthxxqwertyuiop_op1131331231saldjdyueh'

#ERROR_CODE
E_SYSTEM = 10001
E_AUTH = 10002
E_PARAM = 10003
E_NOT_SUPPORT = 10004

class BLException(Exception):
    def __init__(self, info):      
        Exception.__init__(self)  
        self.info = info

class BLParamError(BLException):
    pass

def RandomStr(rlen=64):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(rlen):
        str+=chars[random.randint(0, length)]
    return str

def SuccessResponse(content):
    content['rc'] = 0
    return HttpResponse(json.dumps(content),  content_type="application/json")

def ErrorResponse(err_code, info=''):
    content = {} 
    content['rc'] = err_code
    if info:
        content['info'] = info 
    return HttpResponse(json.dumps(content),  content_type="application/json")
