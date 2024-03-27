from django.shortcuts import render,HttpResponseRedirect,redirect
from .forms import SignUpForm,LoginForm,PostForm
from django.contrib import messages
from .models import post,Contact
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login,logout
import math
# Create your views here.
def home(request):
     posts=post.objects.all()[1:4]
     return render(request,'blog/home.html',{'posts':posts})


def about(request):
     return render(request,'blog/about.html')

def blog(request):
      no_of_post=3
      page=request.GET.get('page')
      if page is None:
            page=1
      else:
            page=int(page)      
      blogs=post.objects.all()
      length=len(blogs)
      blogs=blogs[(page-1)*no_of_post:page*no_of_post]
      if page>1:
         prev=page-1
      else:
           prev=None
      if page<math.ceil(length/no_of_post):        
        nxt=page+1
      else:
           nxt=None  
      context={
            'blogs':blogs,
            'prev':prev,
            'nxt':nxt
      }
      return render(request,'blog/bloghome.html',context)

def blogpost(request,id):
     posts=post.objects.get(pk=id)
     context={'posts':posts}
     return render(request,'blog/blogpost.html',context) 


def contact(request):
   try:  
     message=False
     data={}
     if request.method=="POST":
           name=request.POST.get("name")
           email=request.POST.get('email')
           phone=request.POST.get('phone')
           desc=request.POST.get('desc')
           instance=Contact(name=name,email=email,phone=phone,desc=desc)
           instance.save()
           data={
                'message':True 
           }
     return render(request,'blog/contact.html',data)
   except:
       return render(request,'blog/contact.html') 

    

# logout
def user_logout(request):
     logout(request)
     return HttpResponseRedirect('/')


def user_signup(request):
     if request.method=="POST":
          form=SignUpForm(request.POST)
          if form.is_valid():
               messages.success(request,'Congratulations! You have become an Author.')
               user=form.save()
               group=Group.objects.get(name="Author")
               user.groups.add(group)
     else:     
            form=SignUpForm()
     return render(request,'blog/signup.html',{'form':form})


  
# login
def user_login(request):
   try:  
     if not request.user.is_authenticated:
      if request.method=="POST":
          form=LoginForm(request,data=request.POST)
          if form.is_valid():
               uname=form.cleaned_data['username']
               upass=form.cleaned_data['password']
               user=authenticate(username=uname,password=upass)
               if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in Successfully !!')
                    return HttpResponseRedirect('/thanks/')
          # else:
          #          return HttpResponseRedirect('/signup/') 
      else:           
        form=LoginForm()
      return render(request,'blog/login.html',{'form':form})
     else:
          return HttpResponseRedirect('/thanks/')
   except:
        return HttpResponseRedirect('/thanks/')  

# add new post
def add_post(request):
     if request.user.is_authenticated:
          if request.method=="POST":
               form=PostForm(request.POST)
               if form.is_valid():
                   title=form.cleaned_data['title']
                   desc=form.cleaned_data['desc']
                   pst=post(title=title,desc=desc)
                   pst.save()
                   form=PostForm()
          else:
               form=PostForm()         
          return render(request, 'blog/addpost.html',{'form':form})
     else:
          return HttpResponseRedirect('/login/')  

       

def search(request):
      if request.method=="GET":
           st=request.GET.get('post_title')
           if st!=None:
                data=post.objects.filter(title__icontains=st)
      context={
           'data':data
      }          
      return render(request,'blog/search.html',context)

def thankyou(request):
     if request.user.is_authenticated:
        user=request.user
        full_name=user.get_full_name()
        data={
              'full_name':full_name,
              }
     return render(request,'blog/thanks.html',data)



# add new post
def add_post(request):
     if request.user.is_authenticated:
          if request.method=="POST":
               form=PostForm(request.POST)
               if form.is_valid():
                   title=form.cleaned_data['title']
                   desc=form.cleaned_data['desc']
                   pst=post(title=title,desc=desc)
                   pst.save()
                   form=PostForm()
          else:
               form=PostForm()         
          return render(request, 'blog/addpost.html',{'form':form})
     else:
          return HttpResponseRedirect('/login/')  

       
# update post
def update_post(request,id):
     message=False
     data={}
     if request.user.is_authenticated:
          if request.method=="POST":
                pi=post.objects.get(pk=id)
                form=PostForm(request.POST,instance=pi)
                if form.is_valid():
                     form.save()
                     message=True        
          else:
                pi=post.objects.get(pk=id) 
                form=PostForm(instance=pi)
          data={
           'form':form,
           'message':message
          }       
                     
          return render(request, 'blog/update.html',data)
     else:
          return HttpResponseRedirect('/login/')     

def delete_post(request,id):
     if request.user.is_authenticated:
          if  request.method=="POST":
                pi=post.objects.get(pk=id) 
                pi.delete()    
                return HttpResponseRedirect('/dashboard/')   
     else:
          return HttpResponseRedirect('/login/')    
     

def dashboard(request):
     if request.user.is_authenticated:
        posts=post.objects.all()
        user=request.user
        full_name=user.get_full_name()
        gps=user.groups.all()
        data={'posts':posts,
              'full_name':full_name,
              'groups':gps
              }
        return render(request,'blog/dashboard.html',data)
     else:
          return HttpResponseRedirect('/login')     