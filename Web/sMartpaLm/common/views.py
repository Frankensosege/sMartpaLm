from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from Utilities.comUtilities import get_menu_list
from .forms import UserForm, UserCreationForm

# Create your views here.

def index(request):
    return HttpResponse("내 손바닥 안에 똑똑한 농장입니다.")

def smartpalm_index(request):
    return render(request, 'common/sMartpaLm_index.html')

# views.py
def menu_list(request):
    auth = request.session.get('auth')
    if not request.user.is_authenticated:
        auth = 'X'

    menu_json = get_menu_list(auth)

    return HttpResponse(menu_json, content_type="application/json")

def login_sys(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        passwd = request.POST.get('passwd')

        user = authenticate(email=email, password=passwd)

        if user is not None:
            login(request, user=user)
            # redirect the user to the home page
            request.session['email'] = user.email
            request.session['id'] = user.id
            if user.is_superuser or user.is_staff:
                request.session['auth'] = 'A'
            else:
                request.session['auth'] = 'U'
            # redirect_to = reverse('login:welcome', kwargs={'name':user.user_name})
            user_name = user.user_name
            if user_name is None or user_name == "":
                user_name = user.email
            request.session['user_name'] = user_name

            return render(request, 'common/sMartpaLm_index.html', {'user': user})
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
        del(request.session['user_name'])
    return render(request, 'common/sMartpaLm_index.html')

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')

            form = UserForm()
            return render(request, 'common/login.html', {'form': form})
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

def welcome(request):
    user = request.session.get('email')

    return render(request, 'common_ui/stock_man_index.html', {'user': user})
