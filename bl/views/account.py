
from bl.views.common import *
from bl.views.auth import GetAccessToken
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
        user = User.objects.create(uid=uid, email=email, password=hashlib.md5(MAGIC_SALT+password).hexdigest())
        profile = Profile.objects.create(user=user)
        ret['uid'] = uid
        ret['at'] = GetAccessToken(uid)
        return SuccessResponse(ret)
    except BLParamError, e:
        return ErrorResponse(E_PARAM, e.info)
    except:
        return ErrorResponse(E_SYSTEM)

def QuickRegister(request):
    ret = {}
    uid = generateUserId()

    try:
        user = User.objects.create(uid=uid)
        profile = Profile.objects.create(user=user)
        ret['uid'] = uid
        ret['at'] = GetAccessToken(uid)
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



def ShowAllAccounts(request):
    ret = {}
    try:
        count = User.objects.all().count()
        users = User.objects.all()
        ret['count'] = count
        ret['ids'] = []
        for u in users:
            ret['ids'].append(u.uid)
        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_PARAM)
    
def ResetPassword(request):
    return ErrorResponse(E_NOT_SUPPORT)

def ForgetPassword(request):
    return ErrorResponse(E_NOT_SUPPORT)

