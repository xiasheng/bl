
from bl.views.common import *
from bl.views.auth import GenerateAccessToken
from bl.models.models import User, Profile
import random, hashlib
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def generateUserId():
    id = 0
    while True:
        id = random.randint(100000, 200000)
        if User.objects.filter(uid=id).count() > 0:
            continue
        else:
            return id
    return id

def generateXmppAccount(uid):
    return 'x' + str(uid) + '@test.com'

def checkParam(email, password):
    try:
        if email is None:
            raise BLParamError('email field is required')
        validate_email(email)
        if User.objects.filter(email=email).count() > 0:
            raise BLParamError( email + ' is already registered')

        if password is None:
            raise BLParamError('password field is required')
        if len(password) < 6:
            raise BLParamError('password is too short')

    except ValidationError:
        raise BLParamError('illegal email address: ' + email)


def Register(request):
    ret = {}

    try:
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        checkParam(email, password)
        uid = generateUserId()
        xmpp_account = generateXmppAccount(uid)
        user = User.objects.create(uid=uid, email=email, password=hashlib.md5(MAGIC_SALT+password).hexdigest(), xmpp_account=xmpp_account)
        profile = Profile.objects.create(user=user)
        ret['uid'] = uid
        ret['access_token'] = GenerateAccessToken(uid)
        ret['xmpp_account'] = xmpp_account
        return SuccessResponse(ret)
    except BLParamError, e:
        return ErrorResponse(E_PARAM, e.info)
    except:
        return ErrorResponse(E_SYSTEM)

def QuickRegister(request):
    ret = {}
    uid = generateUserId()
    xmpp_account = generateXmppAccount(uid)

    try:
        user = User.objects.create(uid=uid, xmpp_account=xmpp_account)
        profile = Profile.objects.create(user=user)
        ret['uid'] = uid
        ret['accsee_token'] = GenerateAccessToken(uid)
        ret['xmpp_account'] = xmpp_account
        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_SYSTEM)
    
def BindEmail(request):
    ret = {}

    try:
        uid = int(request.POST.get('uid', 0))
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        checkParam(email, password)
        user = User.objects.get(uid=uid)
        user.email = email
        user.password = hashlib.md5(MAGIC_SALT+password).hexdigest()
        user.save() 
    except BLParamError, e:
        return ErrorResponse(E_PARAM, e.info)
    except:
        return ErrorResponse(E_SYSTEM)

def CreateTestUsers(request):
    ret = {}
    ret['count'] = 0
    ret['users'] = []

    try:
        prefix = request.POST.get('prefix', 'test')
        password = request.POST.get('password', '123456')
        num = int(request.POST.get('num', 10))
        
        for i in range(num):
            email = prefix + str(i+1) + '@test.com'
            uid = generateUserId()
            xmpp_account = generateXmppAccount(uid)
            user = User.objects.create(uid=uid, email=email, password=hashlib.md5(MAGIC_SALT+password).hexdigest(), xmpp_account=xmpp_account, is_test=True)
            profile = Profile.objects.create(user=user)
            ret['users'].append(email)
            ret['count'] += 1
        
        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_SYSTEM)
        
def DeleteTestUsers(request):
    ret = {}

    try:
        users = User.objects.filter(is_test=True)
        
        for user in users:
            Profile.objects.filter(user=user).delete()
            #Photo.objects.filter(user=user).delete()
            #Status.objects.filter(user=user).delete()
            user.delete()
    except:
        pass
        
    return SuccessResponse(ret)        

def ShowAllAccounts(request):
    ret = {}
    try:
        count = User.objects.all().count()
        users = User.objects.all()
        ret['count'] = count
        ret['ids'] = []
        for u in users:
            ret['ids'].append(u.uid)
    except:
        pass

    return SuccessResponse(ret)

def ResetPassword(request):
    return ErrorResponse(E_NOT_SUPPORT)

def ForgetPassword(request):
    return ErrorResponse(E_NOT_SUPPORT)

