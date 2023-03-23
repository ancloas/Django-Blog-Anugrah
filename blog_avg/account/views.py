from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, Login_Auth_Form, ProfileUpdateForm
from blog.models import BlogPost
# Create your views here.

def registration_view(request):
    context = {}
    if request.POST:
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password= raw_password) 
            login(request, account)
            context['success_message']='User Added'
            return redirect('home')
        else: 
            context['registration_form']=form
    else:
        form=RegistrationForm()
        context['registration_form']=form
    return render(request, 'account/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    context= {}
    
    user= request.user

    if user.is_authenticated:
        return redirect("home")
    
    if request.POST:
        form= Login_Auth_Form(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user: 
                login(request, user)
                return redirect("home")
    else:
        form = Login_Auth_Form()
    
    context['login_form']= form
    return render(request, 'account/login.html', context)

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    
    context= {}

    if request.POST:
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial={
                "email": request.POST['email'],
                "username": request.POST['username'],
            }
            form.save()
            context['success_message']='Updated'
    else:
        form =ProfileUpdateForm(initial= {"email": request.user.email,
                                           "username": request.user.username
                                        } 
                                )
    context['profile_form']= form

    blog_posts= BlogPost.objects.filter(author=request.user) #filtering all blog_posts for current user
    context['blog_posts']=blog_posts


    return render(request, 'account/profile.html', context)

def must_authenticate_view(request):
    return render(request, 'account/must_authenticate.html', {})
