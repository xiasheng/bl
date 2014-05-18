
import os,sys, subprocess, random, time, json
import logging

logger = logging.getLogger('django') 

ADMIN = ('admin', 'test.com', '123456')
GROUP_DOMAIN = 'conference.test.com'

def RandomId():
    return str(random.randint(1, 1000000))

def RunEjabberdCmd(msg, user=ADMIN):

    try:
        ret = subprocess.call(["sudo", "/usr/sbin/ejabberdctl", "send_stanza_c2s", user[0], user[1], user[2], msg])
        print 'ret ' + str(ret)
        if ret == 0:
            return True
    except:
        pass

    print 'RunEjabberdCmd failed: ' + msg
    return False


def SendTextMsg(fr, to, body):
    try:
        ret = subprocess.check_output(["sudo", "/usr/sbin/ejabberdctl", "send_message_chat", fr, to, body])
        print 'ret ' + str(ret)
        logger.info('SendTextMsg :' + str(ret)) 
        if ret == 0:
            return True
    except IOError:
        pass

    print 'SendTextMsg failed: ' + body
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



if __name__ == '__main__':
    CreateGroup('g1', '111')
    CreateGroup('g2', '111')
    CreateGroup('g3', '111')
    #time.sleep(1)

    user1 = ('test1', 'test.com', 'Gajim')
    user2 = ('test2', 'test.com', 'Gajim')
    user3 = ('test3', 'test.com', 'Gajim')

    JoinGroup(user1, 'g1', 'u1')
    JoinGroup(user1, 'g2', 'u2')
    JoinGroup(user1, 'g3', 'u3')

    LeaveGroup(user1, 'g1', 'u1')
    LeaveGroup(user1, 'g2', 'u2')
    LeaveGroup(user1, 'g3', 'u3')

    DestroyGroup('g1')
    DestroyGroup('g2')
    DestroyGroup('g3')


    body = {}
    body['type'] = 'recv_friend invite request'
    body['from'] = 12345678
    body['info'] = 'someinfo'

    SendTextMsg('admin@test.com', 'x110701@test.com', json.dumps(body))

