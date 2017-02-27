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
        if len(postData['firstname'])<2 or not NAME_REGEX.match(postData['firstname']):
            errors.append({'error':"First name can not less than 2 letters and  could only contain letter!",'type':'firstnamer'})
            valid=False
        if len(postData['lastname'])<2 or not NAME_REGEX.match(postData['lastname']):
            errors.append({'error':"Last name can not less than 2 letters and  could only contain letter!!" ,'type':'lastnamer'})
            valid=False
        if len(postData['email'])<1 or not EMAIL_REGEX.match(postData['email']):
            errors.append({'error':"Email cannot be blank or invalid email address!" ,'type':'emailr'})
            valid=False
        if len(postData['password']) < 8:
            errors.append({'error':"Password can not less than 8 letters!", 'type':'passwordr'})
            valid=False
        if postData['password']!=postData['cpassword']:
            errors.append({'error':"Password and confirmation are not identical", 'type':'cpasswordr'})
            valid=False
        print errors
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
        if len(postData['email'])<1 or not EMAIL_REGEX.match(postData['email']):
            errors.append({'error':"Email cannot be blank or invalid email address!" ,'type':'lemailr'})
            valid=False
        if len(postData['password']) < 1:
            errors.append({'error':"Password can not be blank!", 'type':'lpasswordr'})
            valid=False
        if not valid:   # validate error
            return    {'status':False,'errors':errors}
        else:
            return {'status':True}

    def uregister(self,postData):
        hashed = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        try:
            newuser=User(email=postData['email'],first_name=postData['firstname'],last_name=postData['lastname'],password=hashed)
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
            user=User.manager.get(email=postData['email'])
        except Exception as e:
            return 'emailerror'
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
        reviews=user.reviews.all().order_by('-created_at')
        books=[]
        for review in reviews:
            if review.book not in books:
                books.append(review.book)
        print books
        context={'user':user,'books':books,'reviews':reviews}
        return context

class User(models.Model):
    email = models.CharField(max_length=100,unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    manager=UserManager()
