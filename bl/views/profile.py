
from bl.views.common import *
from bl.views.file import SaveFile
from bl.models.models import User, Profile

def checkParam(email, gender, birthday):
    pass



def UpdateProfile(request):
    ret = {}

    try:
        uid = int(request.POST.get('uid'))
        user=User.objects.get(uid=uid)
        profile = Profile.objects.get(user=user)
        
        profile.nickname = request.POST.get('nickname', profile.nickname)
        profile.gender = request.POST.get('gender', profile.gender)
        profile.birthday = request.POST.get('birthday', profile.birthday)
        profile.address = request.POST.get('address', profile.address)
        profile.avatar = request.POST.get('avatar', profile.avatar) 
        file = request.FILES.get('file', None)       
        if file:
            (path, profile.avatar) = SaveFile(file, 'ProfileAvatar')
            ret['avatar'] = profile.avatar

        profile.save()
        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_PARAM)   

def GetProfile(request):
    ret = {}

    try:
        uid = int(request.POST.get('uid'))
        profile = Profile.objects.get(user=User.objects.get(uid=uid))
        ret['profile'] = profile.toJSON()
        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_PARAM)


