
import zmq, json


class ZMQSender():
    instance = None
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5557")
    

    @staticmethod
    def SendMsg(msg):
        ZMQSender.socket.send(json.dumps(msg))
        res = ZMQSender.socket.recv()
        return res

def SendTextMsg(fr, to, body):
    msg = {}
    msg['cmdtype'] = "SendTextMsg"
    msg['from'] = fr
    msg['to'] = to
    msg['body'] = body
    ZMQSender.SendMsg(msg)          
    
    
def CreateGroup(groupname, nickname):
    msg = {}
    msg['cmdtype'] = "CreateGroup"
    msg['groupname'] = groupname
    msg['nickname'] = nickname
    ZMQSender.SendMsg(msg)


def DestroyGroup(groupname):
    msg = {}
    msg['cmdtype'] = "DestroyGroup"
    msg['groupname'] = groupname
    ZMQSender.SendMsg(msg)


def JoinGroup(username, groupname, nickname):
    msg = {}
    msg['cmdtype'] = "JoinGroup"
    msg['username'] = username
    msg['groupname'] = groupname
    msg['nickname'] = nickname
    ZMQSender.SendMsg(msg)


def LeaveGroup(user, groupname, nickname):
    msg = {}
    msg['cmdtype'] = "JoinGroup"
    msg['username'] = username
    msg['groupname'] = groupname
    msg['nickname'] = nickname
    ZMQSender.SendMsg(msg)  

