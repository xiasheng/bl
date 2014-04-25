
from bl.views.common import *
from bl.views.auth import GetAccessToken
from bl.models.models import User
import random, hashlib


def generateAccountId():
    id = ''
    while True:
        id = str(random.randint(100000, 200000))
        if User.objects.filter(account_id=id).count() > 0:
            continue
        else:
            return id
    return id


def Register(request):
    ret = {}
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    nickname = request.POST.get('nickname', '')
    gender = request.POST.get('gender', '')
    birthday = request.POST.get('birthday', None)
    address = request.POST.get('address', '')
    avatar = request.POST.get('avatar', '')
    account_id = generateAccountId()

    try:
        user = User(account_id=account_id, email=email, password=hashlib.md5(MAGIC_SALT+password).hexdigest(),
                    nickname=nickname, gender=gender, birthday=birthday, address=address, avatar=avatar)
        user.save()
        ret['uid'] = account_id
        ret['at'] = GetAccessToken(account_id)
        return SuccessResponse(ret)
    except KeyError:
        return ErrorResponse(E_PARAM)


def QuickRegister(request):
    ret = {}
    account_id = generateAccountId()

    try:
        user = User(account_id=account_id)
        user.save()
        ret['uid'] = account_id
        ret['at'] = GetAccessToken(account_id)
        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_PARAM)
    
def ShowAllAccounts(request):
    ret = {}
    try:
        count = User.objects.all().count()
        users = User.objects.all()
        ret['count'] = count
        ret['ids'] = []
        for u in users:
            ret['ids'].append(u.account_id)
        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_PARAM)
    
def ResetPassword(request):
    return ErrorResponse(E_NOT_SUPPORT)

def ForgetPassword(request):
    return ErrorResponse(E_NOT_SUPPORT)

