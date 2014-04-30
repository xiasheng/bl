
from django.core.cache import cache
from bl.views.common import *
from bl.models.models import User
import hashlib

def GenerateAccessToken(uid):
    access_token = RandomStr()
    cache.set(uid, access_token, 24 * 3600)
    
    all = cache.get('allonlineuser')
    if all is None:
        all = []
    all.append(uid)
    cache.set('allonlineuser', all)
    
    return access_token

def RequireLogin(view):
    def new_view(request, *args, **kwargs):
        try:
            uid = str(request.POST.get('uid'))
            at = request.POST.get('at')

            if at == cache.get(uid):
                cache.set(uid, at)  #update cache time
                return view(request, *args, **kwargs)
        except:
            pass
        return ErrorResponse(E_AUTH)

    return new_view

def Login(request):
    ret = {}

    try:
        uid = request.POST.get('uid', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password')

        user = None
        if uid:
            user = User.objects.get(uid=uid, password=hashlib.md5(MAGIC_SALT + password).hexdigest())
        elif email:
            user = User.objects.get(email=email, password=hashlib.md5(MAGIC_SALT + password).hexdigest())

        ret['uid'] = user.uid
        ret['at'] = GenerateAccessToken(str(user.uid))
        return SuccessResponse(ret)

    except:
        pass

    return ErrorResponse(E_AUTH)



def Logout(request):
    ret = {}

    try:
        uid = str(request.POST.get('uid'))
        at = request.POST.get('at')

        if at == cache.get(uid):
            cache.delete(uid)

    except BLException:
        pass

    return SuccessResponse(ret)

def ShowOnlineUsers(request):
    ret = {}
    ret['count'] = 0
    ret['users'] = []
    
    try:
        all = cache.get('allonlineuser')
    
        for u in all:
            user = {}
            user['id'] = u
            user['at'] = cache.get(u)
            ret['users'].append(user)
            
        ret['count'] = len(all)
    except:
        pass
        
    return SuccessResponse(ret)

