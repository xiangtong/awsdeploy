from django.shortcuts import render,redirect
from ..login_register.models import User
from .models import Wishlist
from django.contrib import messages
# Create your views here.
def detail(request,id):
    if 'id' not in request.session:
        return redirect('users:index')
    else:
        result=Wishlist.manager.detail(id)
        if not result:
            messages.add_message(request, messages.ERROR,'backend error')
            return redirect('users:dashboard')
        else:
            return render(request,'wishlist/detail.html', result)

def create(request):
    if 'id' not in request.session:
        return redirect('users:index')
    else:
        return render(request,'wishlist/add.html')

def add(request):
    if 'id' not in request.session:
        return redirect('users:index')
    else:
        if request.method=='POST':
            data={'userid':request.session['id'],'post':request.POST}
            result=Wishlist.manager.add(data)
            if not result['status']:
                for error in result['errors']:
                    messages.add_message(request, messages.ERROR,error['error'])
                return redirect(request.META.get('HTTP_REFERER'))
            elif result['status']:
                for error in result['errors']:
                    messages.add_message(request, messages.INFO,error['error'])
                return redirect('users:dashboard')
        else:
            return redirect('users:index')

def delete(request,id):
    if 'id' not in request.session:
        return redirect('users:index')
    else:
        data={'userid':request.session['id'],'itemid':id}
        print data
        result=Wishlist.manager.delete(data)
        if not result:
            messages.add_message(request, messages.ERROR,'delete item failed')
        elif result:
            messages.add_message(request, messages.INFO,'delete item successfully')
        return redirect('users:dashboard')

def addto(request,id):
    if 'id' not in request.session:
        return redirect('users:index')
    else:
        data={'userid':request.session['id'],'itemid':id}
        result=Wishlist.manager.addto(data)
        if not result:
            messages.add_message(request, messages.ERROR,'add item to your wishlist failed')
        elif result:
            messages.add_message(request, messages.INFO,'add item to your wishlist successfully')
        return redirect('users:dashboard')

def remove(request,id):
    if 'id' not in request.session:
        return redirect('users:index')
    else:
        data={'userid':request.session['id'],'itemid':id}
        result=Wishlist.manager.remove(data)
        if not result:
            messages.add_message(request, messages.ERROR,'remove item from your wishlist failed')
        elif result:
            messages.add_message(request, messages.INFO,'remove item from your wishlist successfully')
        return redirect('users:dashboard')
