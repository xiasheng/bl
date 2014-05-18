
from bl.views.common import *
from bl.views.auth import GenerateAccessToken, GetSelfUID
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

def generatePassword():
    return RandomStr(rlen=32)

def generateXmppAccount(uid):
    return 'x' + str(uid) + '@test.com'

def GetXmppAccountByUid(uid):
    return 'x' + str(uid) + '@test.com'

def checkEmail(email):
    try:
        if email is None:
            raise BLParamError('email field is required')
        validate_email(email)
        if User.objects.filter(email=email).count() > 0:
            raise BLParamError( email + ' is already registered')
    except ValidationError:
        raise BLParamError('illegal email address: ' + email)


def checkPassword(password):
    if password is None:
        raise BLParamError('password field is required')
    if len(password) < 6:
        raise BLParamError('password is too short')

def checkMagic1(email, password, magic):
    if magic is None:
        raise BLParamError('magic field is required')

    if magic.lower() != hashlib.md5(email + password + password).hexdigest().lower():
        raise BLParamError('magic illegal')
    
def checkMagic2(magic):
    if magic is None:
        raise BLParamError('magic field is required')

    if len(magic) < 24:
        raise BLParamError('magic illegal')
    
    mac = magic[12:24]
    mac_hash = magic[24:]
    
    if mac_hash.lower() != hashlib.md5(mac).hexdigest().lower():
        raise BLParamError('magic illegal')     


def Register(request):
    ret = {}

    try:
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        magic = request.POST.get('magic', None)
        checkEmail(email)
        checkPassword(password)
        checkMagic1(email, password, magic)
        
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

    try:
        magic = request.POST.get('magic', None)
        checkMagic2(magic)
        mac = magic[12:24]
        users =  User.objects.filter(mac=mac)
        if users.count() > 0:
            uid = users[0].uid
            password = users[0].password
            uid = users[0].uid
            xmpp_account = users[0].xmpp_account
        else:
            uid = generateUserId()
            password = generatePassword()
            xmpp_account = generateXmppAccount(uid)
            user = User.objects.create(uid=uid, password=hashlib.md5(MAGIC_SALT+password).hexdigest(), xmpp_account=xmpp_account, mac=mac)
            profile = Profile.objects.create(user=user)
        ret['uid'] = uid
        ret['access_token'] = GenerateAccessToken(uid)
        ret['xmpp_account'] = xmpp_account
        ret['password'] = password
        return SuccessResponse(ret)
    except BLParamError, e:
        return ErrorResponse(E_PARAM, e.info)
    except:
        return ErrorResponse(E_SYSTEM)


def BindEmail(request):
    ret = {}

    try:
        uid = GetSelfUID(request) 
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        checkEmail(email)
        checkPassword(password)
        
        user = User.objects.get(uid=uid)
        if user.email:
            raise BLParamError('this account already bind an email, sorry, you cannot change it')
  
        user.email = email
        user.password = hashlib.md5(MAGIC_SALT+password).hexdigest()
        user.save()
        return SuccessResponse(ret)
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
    ret = {}

    try:
        uid = GetSelfUID(request)
        user = User.objects.get(uid=uid)
        old = request.POST.get('old', None)
        new = request.POST.get('new', None)
        
        if not old or user.password != hashlib.md5(MAGIC_SALT+old).hexdigest():
            raise BLParamError('old password error')
        
        if not new or len(new) < 6:
            raise BLParamError('new password error')
            
        user.password = hashlib.md5(MAGIC_SALT+new).hexdigest()
        user.save()
            
        return SuccessResponse(ret)
    except BLParamError, e:
        return ErrorResponse(E_PARAM, e.info)
    except:
        return ErrorResponse(E_SYSTEM)


def ForgetPassword(request):
    return ErrorResponse(E_NOT_SUPPORT)

