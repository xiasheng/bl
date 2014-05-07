
from bl.views.common import *
from bl.views.file import SaveFile, DeleteFile
from bl.models.models import User, Profile, Photo
from bl.views.auth import GetSelfUID
import os

def checkParam(email, gender, birthday):
    pass



def UpdateProfile(request):
    ret = {}

    try:
        uid = GetSelfUID(request)
        profile = Profile.objects.get(user=User(uid=uid))
        
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
        uid = request.GET.get('uid')
        profile = Profile.objects.get(user=User(uid=uid))
        ret['profile'] = profile.toJSON()
        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_PARAM)

def AddPhoto(request):
    ret = {}

    try:
        uid = GetSelfUID(request)
        file = request.FILES.get('file')
        (path, url) = SaveFile(file, 'ProfilePhoto')
        photo = Photo.objects.create(user=User(uid=uid), path=path, url=url)
        ret['url'] = url
        ret['pid'] = photo.id

        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_PARAM)
        
def DelPhoto(request):
    ret = {}

    try:
        uid = GetSelfUID(request)
        pid = request.POST.get('pid')
        photo = Photo.objects.get(user=User(uid=uid), id=pid)
        DeleteFile(photo.path)
        photo.delete()

        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_PARAM)        
        
def ListPhoto(request):
    ret = {}

    try:
        uid = request.GET.get('uid')
        photos = Photo.objects.filter(user=User(uid=uid))
        
        ret['count'] = len(photos)
        ret['photos'] = []
        for p in photos:
            ret['photos'].append(p.url)
            
        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_PARAM)   

