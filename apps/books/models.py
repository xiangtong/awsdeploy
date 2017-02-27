from __future__ import unicode_literals
from django.db import models
from ..login_register.models import User
from django.db.models import Count

class ReviewManager(models.Manager):
    def getrecent(self):
        reviews=Review.manager.all().order_by('-created_at')[:10]
        return reviews

    def create(self,data):
        validate=True
        errors=[]
        print data
        if len(data['post']['booktitle'])<1:
            validate=False
            errors.append({'error':'booktitle could not be empty','type':'book'})
        if len(data['post']['review'])<1:
            validate=False
            errors.append({'error':'review could not be empty','type':'review'})
        if not 'authorname' in data['post']:
            if int(data['post']['authorid'])==0:
                validate=False
                errors.append({'error':'you should input or select an author','type':'author'})
        elif len(data['post']['authorname'])<1 and int(data['post']['authorid'])==0:
                validate=False
                errors.append({'error':'you should input or select an author','type':'author'})            
        if not validate:
            return {'status':False,'errors':errors}

        if 'authorname' in data['post']:
            authorset=Author.objects.filter(name=data['post']['authorname'])
            print authorset
            if not authorset:
                author=Author(name=data['post']['authorname'])
                author.save()
            else:
                author=authorset[0]
        else:
            author=Author.objects.get(id=data['post']['authorid'])
        bookset=Book.manager.filter(title=data['post']['booktitle'],author=author)
        if not bookset:
            book=Book(title=data['post']['booktitle'],author=author)
            book.save()
        else:
            book=bookset[0]
        user=User.manager.get(id=data['userid'])
        ratingstr=''
        ratingemptystr=''
        for i in range(int(data['post']['rating'])):
            ratingstr=ratingstr+'1'
        for i in range(int(data['post']['rating']),5):
            ratingemptystr=ratingemptystr+'1'
        review=Review(content=data['post']['review'],book=book,rating=data['post']['rating'],post_by=user,ratingstr=ratingstr,ratingemptystr=ratingemptystr)
        review.save()
        return {'status':True,'bookid':book.id}

    def createforone(self,data):
        errors=[]
        if data['post']['review']=="":
            errors.append({'error':'review could not be empty','type':'review'})
            return {'status':False, 'errors':errors}
        else:
            bookobj=Book.manager.get(id=data['bookid'])
            userobj=User.manager.get(id=data['userid'])
            ratingstr=''
            ratingemptystr=''
            for i in range(int(data['post']['rating'])):
                ratingstr=ratingstr+'1'
            for i in range(int(data['post']['rating']),5):
                ratingemptystr=ratingemptystr+'1'
            review=Review(content=data['post']['review'],rating=data['post']['rating'],book=bookobj,post_by=userobj,ratingstr=ratingstr,ratingemptystr=ratingemptystr)
            review.save()
            return {'status':True}

    def delete(self,id):
        try:
            review=Review.manager.get(id=id)
            review.delete()
        except Exception as e:
            return False
        return True

    def temp(self):
        reviews=Review.manager.all()
        for review in reviews:
            if review.ratingstr=='':
                print '???'
                for i in range(review.rating):
                    review.ratingstr = "%s1" % review.ratingstr
            if review.ratingemptystr=='':
                for i in range(review.rating,5):
                    review.ratingemptystr = "%s1" % review.ratingemptystr
            review.save()

class BookManager(models.Manager):
    def getall(self):
        books=Book.manager.all()
        authors=Author.objects.distinct()
        return {'books':books,'authors':authors}

    def getlist(self):  #get all books which has at least one reviews and do not in recent list
        books=Book.manager.annotate(num_review=Count('reviews')).filter(num_review__gt=0)[:10]
        reviews=Review.manager.all().order_by('-created_at')[:10]
        booklist=[]
        for book in books:
            i=True
            for review in book.reviews.all():
                if review in reviews:
                    i=False
            if i==True:
                booklist.append(book)
        return booklist

    def getdetail(self,id):
        book=Book.manager.get(id=id)
        reviews=Review.manager.filter(book=book).order_by('-created_at')
        return {'book':book,'reviews':reviews}

    # def getuser(self,id):
    #     userobj=User.manager.get(id=id)
    #     books=Book.manager.filter(reviews__post_by=userobj)
    #     context={'user':profile,'books':books}
class Author(models.Model):
    name = models.CharField(max_length=50,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    title = models.CharField(max_length=50)
    author=models.ForeignKey(Author,related_name='books')
    # likeby=models.ManyToManyField(User,related_name='like')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    manager=BookManager()

class Review(models.Model):
    content=models.TextField(max_length=1000)
    rating=models.SmallIntegerField(default=3)
    ratingstr=models.CharField(max_length=10,default='')
    ratingemptystr=models.CharField(max_length=10,default='')
    book=models.ForeignKey(Book,related_name='reviews')
    post_by=models.ForeignKey(User,related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    manager=ReviewManager()
