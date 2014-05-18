
import os, shutil

# create file save directory 
ppath = '/var/www/bl/upload/'
cpath = [ 's/i', 's/a', 'm/i', 'm/a', 'p/a', 'p/p', 'o' ]

if os.path.exists(ppath):
    shutil.rmtree('ppath')
    
for p in cpath:
    os.makedirs(ppath + p, mode=0777)

# create log file
os.mkdir('/var/log/django')
os.mknod('/var/log/django/debug.log', mode=0777)

# init memcached
#os.system('killall memcached') 
#os.system('memcached -d')

