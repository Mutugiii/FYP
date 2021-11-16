import requests

from django.shortcuts import render, loader, redirect, HttpResponse
from django.contrib import messages

from .forms import UserSignUpForm, UserLoginForm, QuoteForm, OrderForm, InvoiceForm

from decouple import config

API_URL = config('API_URL')

def handle_refresh(function):
    def wrapper(request, *args, **kwargs):
        if request.session["access_token"] and request.session['refresh_token']:
            payload = {
                'refresh': request.session["refresh_token"]
            }
            response = requests.post(f'{API_URL}token/refresh', payload)
            request.session["access_token"] = response.json()["access"]
            return function(request, *args, **kwargs)
        return redirect('signin')
    return wrapper

# def index(request):
#     '''
#     Create and View all the Posts
#     '''
#     template = loader.get_template('index.html')
#     data = requests.get(f'{API_URL}post').json
#     context = {
#         'posts': data,
#     }
#     return HttpResponse(template.render(context, request))

def index(request):
    '''
    Create and View all the Posts
    '''
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))


def signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            payload = {
                'username': form.cleaned_data['username'],
                'first_name':  form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password'],
                'bio': form.cleaned_data['bio'],
                'location': form.cleaned_data['location']
            }
            response = requests.post(f'{API_URL}register', data=payload)
            if response.status_code == 201:
                messages.add_message(request, messages.SUCCESS, 'User successfully registered, Login!')
                return redirect('signin')
            else:
                messages.add_message(request, messages.INFO, 'Username is already taken!')
    else:
        form = UserSignUpForm()            
    template = loader.get_template('forms/signup.html')
    context = {
        'form': form
    }
    return HttpResponse(template.render(context, request))

def signin(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            payload = {
                'username': form.cleaned_data['username'],
                'password': form.cleaned_data['password'],
            }
            response = requests.post(f'{API_URL}login', data=payload)
            if response.status_code == 200:
                response_data = response.json()
                request.session["access_token"] = response_data['authentication']['access_token']
                request.session["refresh_token"] = response_data['authentication']['refresh_token']
                request.session['id'] = response_data['user']['id']
                request.session.set_expiry(86400)
                # redirect to dashboard based on the status of is_staff
                return redirect('index')
            else:
                messages.add_message(request, messages.INFO, 'Username or Password is invalid!')
    else:
        form = UserLoginForm()    
    template = loader.get_template('forms/login.html')
    context = {
        'form': form
    }
    return HttpResponse(template.render(context, request))


def logout(request):
    try:
        del request.session['access_token']
        del request.session['refresh_token']
        del request.session['id']
    except KeyError:
        pass
    return redirect('index')


@handle_refresh
def dashboard(request):
    template = loader.get_template('dashboard.html')
    return HttpResponse(template.render({}, request))

# @handle_refresh
# def create_quote(request):
#     if request.method == 'POST':
#         form = QuoteForm(request.POST)
#         if form.is_valid():
#             payload = {
#                 'title': form.cleaned_data['title'],
#                 'about': form.cleaned_data['about']
#             }
#             headers = {
#                 "Authorization": f'Bearer {request.session["access_token"]}'
#             }
#             response = requests.post(f'{API_URL}post', data=payload, headers=headers)
#             if response.status_code == 201:
#                 return redirect('index')
#             else:
#                 messages.add_message(request, messages.INFO, 'Unable to Add post at this moment!')
#     else:
#         form = PostForm()
#     template = loader.get_template('forms/post.html')
#     context = {
#         'form': form
#     }
#     return HttpResponse(template.render(context, request))

# @handle_refresh
# def post(request, id):
#     headers = {
#         "Authorization": f'Bearer {request.session["access_token"]}'
#     }
#     response = requests.delete(f'{API_URL}post/{id}', headers=headers)
#     return redirect('index')