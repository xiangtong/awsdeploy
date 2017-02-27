from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')


class UserManager(models.Manager):
    def regvalidate(self,postData):
        errors=[]
        valid=True
        print postData
        if len(postData['firstname'])<3:
            errors.append({'error':"First name can not less than 3 letters !",'type':'firstnamer'})
            valid=False
        if len(postData['username'])<3:
            errors.append({'error':"Username can not less than 3 letters!!" ,'type':'usernamer'})
            valid=False
        if len(postData['password']) < 1:
            errors.append({'error':"Password can not less than 1 letters!", 'type':'passwordr'})
            valid=False
        if len(postData['hired']) < 1:
            errors.append({'error':"Please select hired date!", 'type':'hiredr'})
            valid=False
        if postData['password']!=postData['cpassword']:
            errors.append({'error':"Password and confirmation are not identical", 'type':'cpasswordr'})
            valid=False
        # print errors
        if not valid:
            return {'status':False,'errors':errors}
        else:
            return {'status':True}
        # storage = get_messages(request)
        # for message in storage:
        #     print message

    def logvalidate(self,postData):
        valid=True
        errors=[]
        if  len(postData['username'])<3 :
            errors.append({'error':"Username cannot be blank or at least 3 letters long!" ,'type':'lusernamer'})
            valid=False
        if len(postData['password']) < 1:
            errors.append({'error':"Password is at least 1 letter long!", 'type':'lpasswordr'})
            valid=False
        if not valid:   # validate error
            return    {'status':False,'errors':errors}
        else:
            return {'status':True}

    def uregister(self,postData):
        hashed = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        try:
            newuser=User(first_name=postData['firstname'],username=postData['username'],password=hashed,hired=postData['hired'])
            newuser.save()
        except Exception as e:
            print e
            if str(e).find('not unique'):
                return 'dup'
            else:
                return 'error'
        return newuser.id

    def ulogin(self,postData):
        try:
            user=User.manager.get(username=postData['username'])
        except Exception as e:
            return 'usernameerror'
        postPass=postData['password'].encode()
        if not user.password==bcrypt.hashpw(postPass,user.password.encode()):
            return 'passworderror'
        else:
            return user.id

    def uprofile(self,id):
        try:
            user=User.manager.get(id=id)
        except:  # the session id is not a valid id
            return False
        myitems=user.like.all().order_by('-created_at')
        print user.first_name
        otherusers=User.manager.exclude(id=id)
        otheritems=[]
        for otheruser in otherusers:
            for item in otheruser.like.all():
                if item not in otheritems and item not in myitems:
                    otheritems.append(item)
        context={
        'user':user,
        'myitems':myitems,
        'otheritems':otheritems,
            }
        return context

class User(models.Model):
    first_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=255)
    hired = models.CharField(max_length=100,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    manager=UserManager()
