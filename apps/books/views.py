from django.shortcuts import render,redirect
from ..login_register.models import User
from .models import Book, Review, Author
from django.contrib import messages

# Create your views here.
def index(request):
    # display username,display recent reviews, display books which have reviews
    if 'id' not in request.session:
        return redirect('users:index')
    else:
        # Review.manager.temp()
        id=request.session['id']
        user=User.manager.get(id=id)
        reviews=Review.manager.getrecent()
        books=Book.manager.getlist()
        context={
            'user':user,
            'reviews':reviews,
            'books':books
        }
    return render(request,'books/index.html',context)

def add(request):
    if 'id' not in request.session:
        print 'not id in session'
        return redirect('users:index')
    #display form,auther droplist, rating drop list
    context=Book.manager.getall()
    return render(request,'books/add.html',context)

def create(request,id):
    if id=='':
        data={'userid':request.session['id'],'post':request.POST}
        print data
        result=Review.manager.create(data)
        if not result['status']:
            for error in result['errors']:
                messages.add_message(request, messages.ERROR,error['error'],extra_tags=error['type'])
            return redirect(request.META.get('HTTP_REFERER'))
        elif result['status']:
            messages.add_message(request, messages.INFO,'post new review successfully')
            return redirect('books:detail',id=result['bookid'])
    else:
        data={'bookid':id,'userid':request.session['id'],'post':request.POST}
        result=Review.manager.createforone(data)
        if not result['status']:
            for error in result['errors']:
                messages.add_message(request, messages.ERROR,error['error'],extra_tags=error['type'])
        elif result['status']:
            messages.add_message(request, messages.INFO,'post new review successfully')
        return redirect('books:detail',id=id)
    # created new review for book. if the input book-author pair has existed in db, then add review for that book. if not, then create a new book too.

def detail(request,id):
    if 'id' not in request.session:
        return redirect('users:index')
    #get book name, author and reviews for this book
    else:
        context=Book.manager.getdetail(id)
        return render(request,'books/detail.html',context)

def delete(request,id):
    #delete review
    result=Review.manager.delete(id)
    if result:
        messages.add_message(request, messages.INFO,'delete review successfully')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.add_message(request, messages.ERROR,'delete review error')
        return redirect(request.META.get('HTTP_REFERER'))
