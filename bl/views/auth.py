
from django.core.cache import cache
from bl.views.common import *
from bl.models.models import User
import hashlib

def GetAccessToken(uid):
    access_token = RandomStr()
    cache.set(uid, access_token, 24 * 3600)
    return access_token

def RequireLogin(view):
    def new_view(request, *args, **kwargs):
        try:
            uid = request.POST.get('uid')
            at = request.POST.get('at')
            
            if at == cache.get(uid):
                cache.set(uid, at)  #update cache time
                return view(request, *args, **kwargs)
        except :
            pass
        return ErrorResponse(E_AUTH)
        
    return new_view

def Login(request):
    ret = {}

    try:
        uid = request.POST.get('uid', '')
        email = request.POST.get('email', '')
        password = hashlib.md5(MAGIC_SALT + request.POST.get('password')).hexdigest()
        
        found = 0
        if uid:
            user = User.objects.get(account_id=uid, password=password)
        elif email:
            user = User.objects.get(email=email, password=password)
                
        ret['uid'] = user.account_id
        ret['at'] = GetAccessToken(uid)
        return SuccessResponse(ret) 
            
    except:
        pass
        
    return ErrorResponse(E_AUTH)    
        


def Logout(request):
    ret = {}

    try:
        uid = request.POST.get('uid')
        at = request.POST.get('at')
        
        if at == cache.get(uid):
            cache.delete(uid)

    except :
        pass

    return SuccessResponse(ret) 

