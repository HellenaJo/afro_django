from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import User_account
from django.contrib.auth.models import User
from .forms import ContactForm


# Create your views here.
def index(request):
    pr_title = 'Afro-Django'
    if request.user.is_authenticated:
        username = request.user.username
        return render(
            request,
            'index.html', 
            {'pr_title': pr_title, 'username':username}
        )
    else:
        author = 'Hellen'
        gender = 'Female'
        return render(
            request,
            'index.html', 
            {'pr_title': pr_title, 'author':author, 'gender':gender}
        ) 
        

def register(request):

    return render(request, 'register.html')

def registration(request):
    user_name = request.POST['username']
    email = request.POST['user_email']
    password = request.POST['password']
    gender = request.POST['gender']
    user_details=[ user_name,email,password,gender]
    print(user_details)
    if User.objects.filter(username=user_name).first():
        print('Username already exists.')
        return render(request, 'login.html')
    else:
        user=User.objects.create_user(user_name, email, password)
        return render(request, 'login.html')


def login_user(request):
    #here we handle data being posted from the login form
    user_name = request.POST['username']
    pwd = request.POST['password']
    #we check if the user already has an account in te database
    if User.objects.filter(username=user_name):
        print("This username exists.")
        #if the account exists we login using the username and password fields
        logged_user = authenticate(request, username=user_name, password=pwd)
        if logged_user is not None:
            #here we are logging in the user
            auth_login(request, logged_user)
            print(user_name+" "+"Logged in successfuly")
            return redirect('index')
        else: 
            #here we handle a scenario where the authentication has failed
            return render(request, 'login.html')
    else:
        print("User Credentials do not exist.")
        return render(request, 'login.html')
    
def login_page(request):
    return render(request, 'login.html')

@login_required
def logout_user(request):
    auth_logout(request)
    return redirect('login_page')

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            telephone = form.cleaned_data['telephone']
            return redirect('index', username=username, email=email, telephone=telephone)
    else:
        form = ContactForm()
    return render(request, 'contact_us.html', {'form': form})
