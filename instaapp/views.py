from django.template import loader
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import *
from .forms import *

def index(request):	

	template = loader.get_template('instaapp/main.html')

	context = {	}

	return HttpResponse(template.render(context, request))


def signup(request):
    	if request.method == 'POST':
         form = SignupForm(request.POST)
         if form.is_valid():
             username = form.cleaned_data.get('username')
             email = form.cleaned_data.get('email')
             password = form.cleaned_data.get('password')
             User.objects.create_user(username=username, email=email, password=password)
             return redirect('index')
         else:
             form = SignupForm()
             context = {'form':form,}
             
             return render(request, 'signup.html', context)