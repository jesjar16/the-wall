from django.shortcuts import render, redirect
from django.urls import reverse
from wall.models import User
from django.contrib import messages
import bcrypt
from django.db import IntegrityError
from wall.decorators import login_required

# Create your views here.
def index(request):
    return render(request, "index.html")

def register(request):
    print (request.POST)
    
    # getting form variables
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    birthday = request.POST['birthday']
    password = request.POST['password']
    password2 = request.POST['password2']
    
    # errors dict is received
    errors = User.objects.basic_validator(request.POST)
    
    # if there are errors
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        
        form_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'birthday': birthday
        }
        
        request.session['form_data'] = form_data
        
        #return render(request, "messages.html")
        return redirect(reverse("my_index"))
    else:
        try:
            # hashing password
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            
            # creating the user
            this_user = User.objects.create(first_name=first_name, last_name=last_name, email=email, birthday=birthday, password=hashed_password) 

            user_data = {
                    'user_id': this_user.id,
                    'first_name': this_user.first_name.capitalize(),
                    'last_name': this_user.last_name.capitalize(),
                    'email': this_user.email,
                    'action': 'register'
            }
            
            request.session['user_data'] = user_data
                
            messages.success(request, "User successfully created and logged in")
        
            return redirect(reverse("my_success"))
        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e.args):
                messages.error(request, 'Email is already registered, try logging in')
                
                form_data = {
                    'first_name': first_name.capitalize(),
                    'last_name': last_name.capitalize(),
                    'email': email,
                    'birthday': birthday
                }
                
                request.session['form_data'] = form_data

            #return render(request, "messages.html")
            return redirect(reverse("my_index"))

def login(request):
    # form variables are received
    email_login = request.POST['email_login']
    password_login = request.POST['password_login']
    
    # errors dict is received
    errors = User.objects.basic_validator2(request.POST)
    
    # if there are errors
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        
        form_data = {
            'email_login': email_login
        }
        
        request.session['form_data'] = form_data
        
        #print(request.session['form_data']['email_login'])
        
        return redirect(reverse("my_index"))
        #return render(request, "messages.html")
    else:
        user = User.objects.filter(email=email_login)
        if user:
            logged_user = user[0] 
            if bcrypt.checkpw(password_login.encode(), logged_user.password.encode()):
                # creating session variables for logged in user
                user_data = {
                    'user_id': logged_user.id,
                    'first_name': logged_user.first_name.capitalize(),
                    'last_name': logged_user.last_name.capitalize(),
                    'email': logged_user.email,
                    'action': 'login'
                }
                
                request.session['user_data'] = user_data
                
                messages.success(request, "You have successfully login")
                
                return redirect(reverse("my_success"))
            else:
                messages.error(request, "Wrong email or password")
                
                return redirect(reverse("my_index"))
                #return render(request, "messages.html")
        else:
            messages.error(request, "Wrong email or password")
                
            return redirect(reverse("my_index"))
            #return render(request, "messages.html")

@login_required
def success(request):
    return redirect(reverse("my_homepage"))
    
@login_required    
def homepage(request):
    return render(request, "homepage.html")

@login_required
def about(request):
    return render(request, "about.html")

def logout(request):
    # deleting session variables
    if 'form_data' in request.session:
        del request.session['form_data']
        
    if 'user_data' in request.session:
        del request.session['user_data']
        messages.success(request, "You have successfully logout")
    
    return redirect(reverse("my_index")) 