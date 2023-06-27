from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from Utilities.comUtilities import get_menu_list
from .forms import UserForm, UserCreationForm
from admin_palm.views import admin_veiw as adpalm
from user_mob.views import palm_view


# Create your views here.

def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return adpalm(request)
        else:
            return render(request, 'common/sMartpaLm_index.html')
    else:
        return redirect(request, 'common:login')

# views.py
def login_sys(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user=user)
            # redirect the user to the home page
            request.session['email'] = user.email
            request.session['id'] = user.id
            username = user.username
            if username is None or username == "":
                username = user.email
            request.session['username'] = username
            if user.is_superuser or user.is_staff:
                request.session['auth'] = 'A'
                user_format = {'user' : user}
                return redirect('admin_palm:admin_palm'.format(user_format))
            else:
                request.session['auth'] = 'U'
                return render(request, 'common/sMartpaLm_index.html', {'user': user})
            # redirect_to = reverse('login:welcome', kwargs={'name':user.username})
        else:
            # display an error message
            messages.error(request, '유효한 사용자가 아닙니다.')
            form = UserForm()
    else:
        form = UserForm()

    # render the login page
    return render(request, 'common/login.html', {'form': form})

def logout_sys(request):
    logout(request)
    if request.session.get('email'):
        del(request.session['email'])
        del(request.session['auth'])
        del(request.session['username'])
    return render(request, 'common/login.html')

def signup(request):
    if request.method == "POST":
        print(request.POST)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)

            login(request, user)
            return index(request)
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

def welcome(request):
    user = request.session.get('email')

    return render(request, 'common/sMartpaLm_index.html', {'user': user})