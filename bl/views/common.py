
from django.http import HttpResponse
from random import Random
import json

MAGIC_SALT = 'mthxxqwertyuiop_op1131331231saldjdyueh'

#ERROR_CODE
E_SYSTEM = 10001
E_AUTH = 10002
E_PARAM = 10003
E_NOT_SUPPORT = 10004


def RandomStr(randomlength=64):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

def SuccessResponse(content):
    return HttpResponse(json.dumps(content),  content_type="application/json")

def ErrorResponse(err_code, info=''):
    content = {} 
    content['err_code'] = err_code
    if info:
        content['info'] = info 
    return HttpResponse(json.dumps(content),  content_type="application/json")
