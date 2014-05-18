
from bl.views.common import *
from bl.models.models import User, Profile, Friend
from bl.views.auth import GetSelfUID
from bl.views.account import GetXmppAccountByUid
from bl.views.zmqsender import SendTextMsg
import json

def xmppNotify(fr, to, msg):
    msg['from'] = str(fr)
    msg['to'] = str(to)
    fr_xmpp = GetXmppAccountByUid(fr)
    to_xmpp = GetXmppAccountByUid(to)

    return SendTextMsg(fr_xmpp, to_xmpp, msg)

def InviteRequest(request):
    ret = {}

    try:
        uid = GetSelfUID(request)
        user = User.objects.get(uid=uid)
        fid = int(request.POST.get('fid'))
        info = request.POST.get('info', '')

        if User.objects.filter(uid=fid).count() == 0 or uid == int(fid):
            raise BLParamError( 'illegal fid: ' + str(fid))

        friend1,created = Friend.objects.get_or_create(user=User(uid=uid), fid=fid)
        friend1.status = 'sent_invite'
        friend1.info = info
        friend1.save()

        friend2,created = Friend.objects.get_or_create(user=User(uid=fid), fid=uid)
        friend2.status = 'recv_invite'
        friend2.info = info
        friend2.save()

        #send xmpp msg to notify otherside
        msg = {}
        msg['type'] = 'recv_friend_invite_request'
        msg['info'] = info
        res = xmppNotify(uid, fid, msg)

        return SuccessResponse(ret)
    except BLParamError, e:
        return ErrorResponse(E_PARAM, e.info)
    except IOError:
        return ErrorResponse(E_PARAM)


def InviteResponse(request):
    ret = {}

    try:
        uid = GetSelfUID(request)
        user = User.objects.get(uid=uid)
        fid = int(request.POST.get('fid'))
        type = request.POST.get('type', '')
        info = request.POST.get('info', '')

        if User.objects.filter(uid=fid).count() == 0 or uid == int(fid):
            raise BLParamError( 'illegal fid: ' + str(fid))

        friend1 = Friend.objects.get(user=User(uid=uid), fid=fid)
        friend2 = Friend.objects.get(user=User(uid=fid), fid=uid)
        status1 = status2 = ''
        assert friend1.status == 'recv_invite' and friend2.status == 'sent_invite'

        if type == 'confirm':
            status1 = status2 = 'bound'
        elif type == 'reject':
            status1 = 'sent_reject'
            status2 = 'recv_reject'
        else:
            raise BLParamError( 'illegal type: ' + type)

        friend1.status = status1
        friend1.save()
        friend2.status = status2
        friend2.save()

        #send xmpp msg to notify otherside
        msg = {}
        msg['type'] = 'recv_friend_invite_response'
        msg['info'] = type
        xmppNotify(uid, fid, msg)
        
        return SuccessResponse(ret)
    except BLParamError, e:
        return ErrorResponse(E_PARAM, e.info)
    except AssertionError:
        return ErrorResponse(E_PARAM, 'status inconsistent')
    except:
        return ErrorResponse(E_PARAM)


def DelFriend(request):
    ret = {}

    try:
        uid = GetSelfUID(request)
        fid = int(request.POST.get('fid'))

        Friend.objects.filter(user=User(uid=uid), fid=fid).delete()
        #Friend.objects.filter(user=User(uid=fid), fid=uid).delete()
        friend2 = Friend.objects.get(user=User(uid=fid), fid=uid)
        if friend2 and friend2.status == 'bound':
            friend2.status = 'removed'
            friend2.save()
        elif friend2:
            friend2.delete()

        #send xmpp msg to notify otherside
        msg = {}
        msg['type'] = 'recv_friend_remove'
        xmppNotify(uid, fid, msg)        
    except:
        pass

    return SuccessResponse(ret)

def ShowFriend(request):
    ret = {}
    try:
        uid = GetSelfUID(request)
        page = int(request.REQUEST.get('page', 0))
        pagesize = 10
        min = page * pagesize
        max = (page + 1) * pagesize
        friends_bound = Friend.objects.filter(user=User(uid=uid), status='bound').order_by('-id')[min:max]
        friends_sent_invite = Friend.objects.filter(user=User(uid=uid), status='sent_invite').order_by('-id')[min:max]
        friends_recv_invite = Friend.objects.filter(user=User(uid=uid), status='recv_invite').order_by('-id')[min:max]
        friends_sent_reject = Friend.objects.filter(user=User(uid=uid), status='sent_reject').order_by('-id')[min:max]
        friends_recv_reject = Friend.objects.filter(user=User(uid=uid), status='recv_reject').order_by('-id')[min:max]
        friends_removed = Friend.objects.filter(user=User(uid=uid), status='removed').order_by('-id')[min:max]

        res_friends = {}
        res_friends['bound'] = []
        res_friends['sent_invite'] = []
        res_friends['recv_invite'] = []
        res_friends['sent_reject'] = []
        res_friends['recv_reject'] = []
        res_friends['removed'] = []
        hasmore = 0

        for f in friends_bound:
            profile = Profile.objects.get(user=User(uid=f.fid))
            res_friends['bound'].append(profile.toJSON())

        for f in friends_sent_invite:
            profile = Profile.objects.get(user=User(uid=f.fid))
            res_friends['sent_invite'].append(profile.toJSON())

        for f in friends_recv_invite:
            profile = Profile.objects.get(user=User(uid=f.fid))
            res_friends['recv_invite'].append(profile.toJSON())

        for f in friends_sent_reject:
            profile = Profile.objects.get(user=User(uid=f.fid))
            res_friends['sent_reject'].append(profile.toJSON())

        for f in friends_recv_reject:
            profile = Profile.objects.get(user=User(uid=f.fid))
            res_friends['recv_reject'].append(profile.toJSON())

        for f in friends_removed:
            profile = Profile.objects.get(user=User(uid=f.fid))
            res_friends['removed'].append(profile.toJSON())

        ret['friends'] = res_friends

        if     len(friends_bound) >= pagesize \
            or len(friends_sent_invite) >= pagesize \
            or len(friends_recv_invite) >= pagesize \
            or len(friends_sent_reject) >= pagesize \
            or len(friends_recv_reject) >= pagesize \
            or len(friends_removed) >= pagesize:
            hasmore = 1

        ret['hasmore'] = hasmore

        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_PARAM)

