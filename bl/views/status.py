
from bl.views.common import *
from bl.views.file import SaveFile
from bl.models.models import User, Status, StatusFile
from bl.views.auth import GetSelfUID

def PostStatus(request):
    ret = {}

    try:
        uid = GetSelfUID(request)
        user = User.objects.get(uid=uid)
        text = request.POST.get('text')
        type = request.POST.get('type')
        (path, url) = ('', '')
        
        if type == 'text':
            pass
        elif type == 'image':
            file = request.FILES.get('file')
            (path, url) = SaveFile(file, 'StatusImage')
        elif type == 'audio':    
            file = request.FILES.get('file')
            (path, url) = SaveFile(file, 'StatusAudio')
        else:
            raise BLParamError( 'illegal type: ' + type)
        
        status = Status.objects.create(user=user, text=text, type=type) 
        ret['sid'] = status.id
        #ret['type'] = status.type
        
        if type in ['image', 'audio']:
            status_file = StatusFile.objects.create(status=status, url=url, path=path)
            ret['url'] = url

        return SuccessResponse(ret)
    except BLParamError, e:
        return ErrorResponse(E_PARAM, e.info)
    except:
        return ErrorResponse(E_PARAM)


def GetStatusByID(request):
    ret = {}

    try:
        #uid = GetSelfUID(request)
        uid = int(request.GET.get('uid'))
        sid = int(request.GET.get('sid'))
        status = Status.objects.get(user=User(uid=uid), id=sid)
        ret['status'] = status.toJSON()
        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_PARAM, 'status does not exist')

def GetStatusByUser(request):
    ret = {}
    try:
        uid = request.GET.get('uid')
        since_id = request.GET.get('since_id', 0)
        statuses = Status.objects.filter(pk__gt=since_id, user=User(uid=uid)).order_by('-id')[:10]
        
        res_statuses = []
        for s in statuses:
            res_statuses.append(s.toJSON())

        ret['count'] = len(res_statuses)
        ret['statuses'] = res_statuses
        if 10 > ret['count']:
            ret['hasmore'] = 0
        else:
            ret['hasmore'] = 1
            
        return SuccessResponse(ret)    
    except:
        return ErrorResponse(E_PARAM)
