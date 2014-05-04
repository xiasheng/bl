
from django.db import models
import time

class User(models.Model):
    uid = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128, null=True)
    email = models.EmailField(null=True)
    is_test = models.BooleanField(default=False) 
    time_created = models.IntegerField(default=int(time.time()))
 
class Profile(models.Model):
    user = models.ForeignKey('User')
    nickname = models.CharField(max_length=64, null=True)
    gender = models.CharField(max_length=10, null=True)
    birthday = models.DateField(null=True)
    address = models.CharField(max_length=64, null=True)
    avatar = models.URLField(null=True)
    time_modified = models.IntegerField(default=int(time.time()))
    
    def toJSON(self):
        r = {}
        r['uid'] = self.user.uid
        r['nickname'] = self.nickname
        r['gender'] = self.gender
        r['birthday'] = self.birthday
        r['address'] = self.address
        r['avatar'] = self.avatar
        return r

class Photo(models.Model):
    user = models.ForeignKey('User')
    url = models.URLField(null=True)
    path = models.CharField(max_length=128, null=True)
    time_created = models.IntegerField(default=int(time.time()))
     
class Status(models.Model):
    user = models.ForeignKey('User')
    text = models.CharField(max_length=1024)
    lat = models.DecimalField(max_digits=10, decimal_places=5, null=True)
    lng = models.DecimalField(max_digits=10, decimal_places=5, null=True)
    type = models.CharField(max_length=64, default='text')
    time_created = models.IntegerField(default=int(time.time()))

    def toJSON(self):
        r = {}
        r['uid'] = self.user.uid
        r['sid'] = self.id
        r['type'] = self.type
        r['text'] = self.text
        r['time_created'] = self.time_created
       
        if self.type != 'text':
            r['files'] = []
            files = StatusFile.objects.filter(status=self)
            for f in files:
                r['files'].append(f.url)
            
        return r
        
class StatusFile(models.Model):
    status = models.ForeignKey('Status')
    type = models.CharField(max_length=64, null=True)
    url = models.URLField(null=True)
    path = models.CharField(max_length=128, null=True)
    time_created = models.IntegerField(default=int(time.time()))
