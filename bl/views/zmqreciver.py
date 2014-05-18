
import zmq,os,sys, subprocess, random, time, json
import logging

logger = logging.getLogger('django')
ADMIN = ('admin', 'test.com', '123456')
GROUP_DOMAIN = 'conference.test.com'

def RandomId():
    return str(random.randint(1, 1000000))

def RunEjabberdCmd(msg, user=ADMIN):

    try:
        ret = subprocess.call(["sudo", "/usr/sbin/ejabberdctl", "send_stanza_c2s", user[0], user[1], user[2], msg])
        if ret == 0:
            return True
    except:
        pass

    print 'RunEjabberdCmd failed: ' + msg
    return False

def CreateGroup(groupname, nickname):
    msg = "<presence id='%s' to='%s@%s/%s'>  <x xmlns='http://jabber.org/protocol/muc'/> </presence>" %(RandomId(), groupname, GROUP_DOMAIN, nickname)
    return RunEjabberdCmd(msg)


def DestroyGroup(groupname):
    msg = "<iq id='%s' to='%s@%s' type='set'> \
             <query xmlns='http://jabber.org/protocol/muc#owner'>  \
               <destroy> \
                 <reason>Destroy</reason> \
               </destroy> \
             </query> \
           </iq>" %(RandomId(), groupname, GROUP_DOMAIN)
    return RunEjabberdCmd(msg)


def JoinGroup(user, groupname, nickname):
    msg = "<presence id='%s' to='%s@%s/%s'>  <x xmlns='http://jabber.org/protocol/muc'/> </presence>" %(RandomId(), groupname, GROUP_DOMAIN, nickname)
    return RunEjabberdCmd(msg, user)


def LeaveGroup(user, groupname, nickname):
    msg = "<presence id='%s' to='%s@%s/%s type='unavailable'>  <x xmlns='http://jabber.org/protocol/muc'/> </presence>" %(RandomId(), groupname, GROUP_DOMAIN, nickname)
    return RunEjabberdCmd(msg, user)
    
 

def SendTextMsg(fr, to, body):
    try:
        ret = subprocess.call(["sudo", "/usr/sbin/ejabberdctl", "send_message_chat", fr, to, body])
        if ret == 0:
            return True
    except:
        pass

    return False


if __name__ == '__main__':
    context = zmq.Context()

    # Socket to receive messages on
    receiver = context.socket(zmq.REP)
    receiver.bind("tcp://*:5557")

    # Process tasks forever
    try:
        while True:
            msg = receiver.recv()
            print msg
            msg = json.loads(msg)
            cmd_type = msg['cmdtype']
        
            if cmd_type == 'SendTextMsg':
                SendTextMsg(msg['from'], msg['to'], json.dumps(msg['body']))
            elif cmd_type == 'CreateGroup':
                CreateGroup(msg['groupname'], msg['nickname'])
            elif cmd_type == 'DestroyGroup':
                DestroyGroup(msg['groupname'])
            elif cmd_type == 'JoinGroup':
                JoinGroup(msg['username'], msg['groupname'], msg['nickname'])
            elif cmd_type == 'SendTextMsg':
                LeaveGroup(msg['username'], msg['groupname'], msg['nickname'])
            elif cmd_type == 'SendTextMsg':
                SendTextMsg(msg['from'], msg['to'], json.dumps(msg['body']))
            else:
                pass  
                
            receiver.send("success")    
    except KeyboardInterrupt:
        exit(0)  

