
from django.http import HttpResponse
from django.core.cache import cache
from bl.views.common import *
from bl.models.models import User
import hashlib, time

AGING_TIME_ACCESS_TOKEN = 24 * 3600

def GenerateAccessToken(uid):
    access_token = RandomStr()
    cache.set(access_token, uid, AGING_TIME_ACCESS_TOKEN)

    userinfo = {}
    userinfo['token'] = access_token
    userinfo['time'] = int(time.time())
    cache.set(str(uid), userinfo, AGING_TIME_ACCESS_TOKEN)
    
    all = cache.get('allonlineuser')
    if all is None:
        all = []
    all.append(access_token)
    cache.set('allonlineuser', all, None)

    return access_token        
    
def IsOnline(uid):
    user = cache.get(str(uid))
    if user:
        return True
    else:
        return False

def GetSelfUID(request):
    return request.META['SELF_UID']

def RequireLogin(view):
    def new_view(request, *args, **kwargs):
        if request.method == 'GET':
            access_token = request.GET.get('access_token', '')
        elif request.method == 'POST':            
            access_token = request.POST.get('access_token', '')
        else:
            access_token = ''    
        
        self_uid = cache.get(access_token)
                
        if not self_uid:
            return ErrorResponse(E_AUTH)
        else:
            request.META['SELF_UID'] = int(self_uid)

        try:
            return view(request, *args, **kwargs)
        except AssertionError:
            return ErrorResponse(E_SYSTEM)

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
        ret['access_token'] = GenerateAccessToken(user.uid)
        return SuccessResponse(ret)

    except:
        pass

    return ErrorResponse(E_AUTH)



def Logout(request):
    ret = {}

    try:
        access_token = request.POST.get('access_token')

        if access_token == cache.get(access_token):
            cache.delete(access_token)

    except BLException:
        pass

    return SuccessResponse(ret)

def ExternalAuth(request):
    try:
        name = request.POST.get('name')
        password = request.POST.get('password')
        uid = cache.get(password)
        if uid and name.find(str(uid)) != -1:
            return HttpResponse("success", status=200)    
    except:
        pass

    return HttpResponse('failed', status=400)

def LoginTestUsers(request):
    ret = {}
    ret['count'] = 0
    ret['users'] = []

    try:
        test_users = User.objects.filter(is_test=True)

        for u in test_users:
            user = {}
            user['id'] = u.uid
            user['email'] = u.email
            user['access_token'] = GenerateAccessToken(u.uid)
            ret['users'].append(user)
            
        ret['count'] = len(test_users)
    except:
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
            user['id'] = cache.get(u)
            user['access_token'] = u
            ret['users'].append(user)

        ret['count'] = len(all)
    except:
        pass

    return SuccessResponse(ret)

