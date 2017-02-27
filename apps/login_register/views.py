from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import User
from django.contrib import messages
from django.contrib.messages import get_messages

# Create your views here.
def index(request):
    if 'id' not in request.session:
        print 'users:index no id'
        # response = HttpResponse("Here's the text of the Web page.")
        # return response
        return render(request,'index.html')
    else:
        id=request.session['id']
        print id
        try:
            context=User.manager.get(id=id)
        except:  # the session id is not a valid id
            del request.session['id']
            return  render(request,'index.html')
        print 'redirect to books:index'
        return redirect('books:index')

def register(request):
    if request.method=='POST':
        valid=User.manager.regvalidate(request.POST)
        if not valid['status']:   # validate error
            for error in valid['errors']:
                messages.add_message(request, messages.ERROR,error['error'],extra_tags=error['type'])
            return render(request,'index.html')
        else:
            result=User.manager.uregister(request.POST)
            print 'result:'+str(result)
            if result=='dup':
                messages.add_message(request, messages.ERROR,"Email existed!", extra_tags='emailr')
                return redirect('users:index')
            elif result=='error':
                messages.add_message(request, messages.ERROR,"database error!", extra_tags='backend')
                return redirect('users:index')
            else :
                request.session['id']=result
                messages.success(request,"successfully registered!", extra_tags='successlog')
                return redirect('books:index')

def profile(request,id):
    if 'id' not in request.session:
        return redirect('users:index')
    else:
        context= User.manager.uprofile(id)
        if context==False:
            return  redirect('books:index')
        else:
            return render(request,'profile.html',context)

def logout(request):
    request.session.pop('id')
    return redirect('users:index')

def login(request):
    if request.method=='POST':
        valid=User.manager.logvalidate(request.POST)
        if not valid['status']:   # validate error
            for error in valid['errors']:
                messages.add_message(request, messages.ERROR,error['error'],extra_tags=error['type'])
            return render(request,'index.html')
        else:
            result=User.manager.ulogin(request.POST)
            print result
            if result=='emailerror':
                messages.add_message(request, messages.ERROR,"Email does not exist!", extra_tags='lemailr')
                return redirect('users:index')
            elif result=='passworderror':
                messages.add_message(request, messages.ERROR,"Invalid password!", extra_tags='lpasswordr')
                return redirect('users:index')
            else:
                messages.success(request,"successfully login!", extra_tags='successlog')
                request.session['id']=result
                return redirect('books:index')
