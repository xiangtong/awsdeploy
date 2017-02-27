from __future__ import unicode_literals
from django.db import models
from ..login_register.models import User

# Create your models here.

class WishlistManager(models.Manager):
    def add(self,data):
        errors=[]
        if len(data['post']['item'])<3:
            errors.append({'error':'item is at lease 3 letters long','type':'item'})
            return  {'status':False,'errors':errors}
        else:
            user=User.manager.get(id=data['userid'])
            itemset=Wishlist.manager.filter(name=data['post']['item'])
            if itemset:
                if itemset.filter(post_by=user):
                    errors.append({'error':'you have added and liked this item before','type':'item'})
                    return  {'status':True,'errors':errors}
                elif itemset.filter(like_by=user):
                    errors.append({'error':'you have liked this item before','type':'item'})
                    return  {'status':True,'errors':errors}
                else:
                    item=itemset[0]
            else:
                item=Wishlist(name=data['post']['item'],post_by=user)
                item.save()
            item.like_by.add(user)
            errors.append({'error':'add new item successfully','type':'item'})
            return {'status':True,'errors':errors}

    def delete(self,data):
        try:
            user=User.manager.get(id=data['userid'])
            item=Wishlist.manager.get(id=data['itemid'],post_by=user)
            print item.name
            print user.first_name
            item.like_by.clear()
            item.delete()
        except Exception as e:
            return False
        return True

    def addto(self, data):
        try:
            user=User.manager.get(id=data['userid'])
            item=Wishlist.manager.get(id=data['itemid'])
            item.like_by.add(user)
        except Exception as e:
            return False
        return True

    def remove(self, data):
        try:
            user=User.manager.get(id=data['userid'])
            item=Wishlist.manager.get(id=data['itemid'])
            item.like_by.remove(user)
        except Exception as e:
            return False
        return True

    def detail(self,id):
        try:
            item=Wishlist.manager.get(id=id)
        except Exception as e:
            return False
        return {'item':item}



class Wishlist(models.Model):
    name = models.CharField(max_length=100,unique=True)
    post_by=models.ForeignKey(User,related_name='post')
    like_by=models.ManyToManyField(User,related_name='like')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    manager=WishlistManager()
