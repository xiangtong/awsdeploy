from django.shortcuts import render,redirect
from .models import User
from django.contrib import messages
from django.contrib.messages import get_messages


# Create your views here.
def index(request):
    if 'id' not in request.session:
        return render(request,'index.html')
    else:
        id=request.session['id']
        try:
            context=User.manager.get(id=id)
        except:  # the session id is not a valid id
            del request.session['id']
            return  render(request,'index.html')
        return redirect('users:dashboard')

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
                messages.add_message(request, messages.ERROR,"Username existed!", extra_tags='usernamer')
                return redirect('users:index')
            elif result=='error':
                messages.add_message(request, messages.ERROR,"database error!", extra_tags='backend')
                return redirect('users:index')
            else :
                request.session['id']=result
                messages.success(request,"successfully registered!", extra_tags='successlog')
                return redirect('users:dashboard')

def profile(request):
    if 'id' not in request.session:
        return redirect('users:index')
    else:
        id=request.session['id']
        print id
        profile= User.manager.uprofile(id)
        if profile==False:
            del request.session['id']
            return  redirect('users:index')
        else:
            return render(request,'profile.html',profile)

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
            if result=='usernameerror':
                messages.add_message(request, messages.ERROR,"Username does not exist!", extra_tags='lusernamer')
                return redirect('users:index')
            elif result=='passworderror':
                messages.add_message(request, messages.ERROR,"Invalid password!", extra_tags='lpasswordr')
                return redirect('users:index')
            else:
                messages.success(request,"successfully login!", extra_tags='successlog')
                request.session['id']=result
                return redirect('users:dashboard')
