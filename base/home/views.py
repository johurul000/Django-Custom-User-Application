import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import CustomUser
import random
import string

# Create your views here.

def generate_username(length=10, allowed_chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(allowed_chars) for _ in range(length))

def signUp(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        password01 = request.POST.get('password01')
        password02 = request.POST.get('password02')

        if password01 != password02:
            context = {
                'phone_number': phone_number,
                'email': email,
                'username': username,
                'message': "Passwords does not match"
            }
            return render(request, 'signup.html', context)
        
        default_image_path = 'profile/default_profile.jpg'

        username = generate_username()
        my_user = CustomUser.objects.create_user(phone_number = phone_number, password=password01, email=email, username=username, profile_image=default_image_path)
        my_user.save()
        return redirect('login')

    return render(request, 'signup.html')


def logIn(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        user = authenticate(request, phone_number=phone_number, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

@login_required(login_url='login')
def profileView(request):
    user = request.user

    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    name = first_name + " " + last_name
    if name == " ":
        name = username
    print(name)

    user_bio = user.user_bio
    if user_bio=="":
        user_bio = "None"
        

    context = {
        'user': user,
        'name': name,
        'user_bio': user_bio
    }
    
    return render(request, 'profile.html', context)
  

def editProfileView(request):
    if request.method == 'POST':
        new_profile_image = request.FILES.get('profile_image')
        new_first_name = request.POST.get('first_name')
        new_last_name = request.POST.get('last_name')
        new_email = request.POST.get('email')
        new_user_bio = request.POST.get('user_bio')


        update_user = request.user

        if new_profile_image:
            original_file_name = new_profile_image.name
            file_extension = os.path.splitext(original_file_name)[1]

            new_file_name = f'{update_user.username}{file_extension}'

            file_path = os.path.join(settings.MEDIA_ROOT, 'profile', new_file_name)

            with open(file_path, 'wb') as destination:
                for chunk in new_profile_image.chunks():
                    destination.write(chunk)

            update_user.profile_image = f'profile/{new_file_name}'



        
        update_user.first_name = new_first_name
        update_user.last_name = new_last_name
        update_user.email = new_email
        update_user.user_bio = new_user_bio
        update_user.save()

        return redirect('profile')




    user = request.user

    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    name = first_name + " " + last_name
    if name == " ":
        name = username

    profile_image_path = user.profile_image

    context = {
        'user': user,
        'name': name,
        'profile_image_path': profile_image_path
    }
    
    return render(request, 'editprofile.html', context)
